import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta
import time

# 1. Obtener token de acceso
def obtener_token():
    print("Obteniendo token...")
    login_url = "https://api-mconn.maxisistemas.com.ar/login"
    login_payload = {
        "email": "your_email@example.com",
        "pass": "your_password",
        "cod_cli": "your_client_code"
    }

    response = requests.post(login_url, json=login_payload)

    if response.status_code == 200:
        login_data = response.json()
        token = login_data['content']['tokenAccess']
        print("Token de acceso obtenido con éxito.")
        return token
    else:
        print(f"Error en la autenticación: {response.status_code} - {response.text}")
        return None

# 2. Solicitar datos de facturación de la API
def obtener_datos_facturacion(token, fecha_inicio, fecha_fin):
    print(f"Obteniendo datos de facturación para el periodo {fecha_inicio} a {fecha_fin}...")
    invoice_url = "https://api-mconn.maxisistemas.com.ar/estadisticas/invoicebydate"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "from": fecha_inicio,  # Fecha de inicio
        "to": fecha_fin  # Fecha de fin
    }

    response = requests.get(invoice_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Datos de facturación obtenidos con éxito.")
        return data
    else:
        print(f"Error en la consulta de facturación: {response.status_code} - {response.text}")
        return None

# 3. Procesar datos a DataFrame (Items)
def procesar_datos_a_dataframe_items(data):
    if data and 'content' in data and 'content' in data['content']:
        print("Procesando los datos de Items...")
        
        filas = []

        for order in data['content']['content']:
            if 'order' in order and 'orderData' in order['order']:
                order_data = order['order']['orderData']
                order_id = order_data.get('orderId', 'Desconocido')
                fecha = order_data.get('orderDate', 'Desconocido')
                order_type = order_data.get('orderType', 'Desconocido')

                if 'orderItems' in order['order']:
                    for item in order['order']['orderItems']:
                        item_data = item['orderItem']
                        titulo_item = item_data.get('title', 'Desconocido')
                        categoria_producto = item_data.get('productCategory', 'Desconocido')
                        cantidad = item_data.get('quantity', 0)
                        precio_producto = item_data.get('productPrice', 0)
                        total_item = item_data.get('totalPrice', 0)

                        fila = [fecha, order_id, order_type, titulo_item, categoria_producto, cantidad, precio_producto, total_item]
                        filas.append(fila)

        df_items = pd.DataFrame(filas, columns=['Fecha', 'OrderID', 'OrderType', 'Título de Ítem', 'Categoría del Producto', 'Cantidad', 'Precio del Ítem', 'Total del Ítem'])
        return df_items
    else:
        print("No se encontraron datos de Items.")
        return pd.DataFrame()

# 4. Procesar datos a DataFrame (Tiempos)
def procesar_datos_a_dataframe_tiempos(data):
    if data and 'content' in data and 'content' in data['content']:
        print("Procesando los datos de Tiempos...")
        
        filas = []

        for order in data['content']['content']:
            if 'order' in order and 'orderData' in order['order']:
                order_data = order['order']['orderData']
                order_id = order_data.get('orderId', 'Desconocido')
                fecha = order_data.get('orderDate', 'Desconocido')
                time_open = order_data.get('timeOpen', 'Desconocido')
                time_close = order_data.get('timeClose', 'Desconocido')
                total_sales = order_data.get('totalSales', 0)
                order_type = order_data.get('orderType', 'Desconocido')

                fila = [fecha, order_id, order_type, time_open, time_close, total_sales]
                filas.append(fila)

        df_tiempos = pd.DataFrame(filas, columns=['Fecha', 'OrderID', 'OrderType', 'Time Open', 'Time Close', 'Total Sales'])
        return df_tiempos
    else:
        print("No se encontraron datos de Tiempos.")
        return pd.DataFrame()

# 5. Escribir DataFrames en Google Sheets
def escribir_dataframe_en_google_sheets(df_items, df_tiempos):
    print("Conectando con Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json')
    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open('ETL APIs')
        print(f"Accediendo a la hoja de cálculo: {spreadsheet.title}")

        # Especificamos la pestaña de Items
        sheet_items = spreadsheet.worksheet('Items')
        print(f"Conectado a la pestaña: {sheet_items.title}")

        # Especificamos la pestaña de Tiempos
        sheet_tiempos = spreadsheet.worksheet('Tiempos')
        print(f"Conectado a la pestaña: {sheet_tiempos.title}")

        # Limpiar datos previos (si es necesario)
        sheet_items.clear()
        sheet_tiempos.clear()

        # Escribir los encabezados y los datos del DataFrame de Items
        sheet_items.update([df_items.columns.values.tolist()] + df_items.values.tolist())
        print("Datos de Items escritos en Google Sheets exitosamente.")

        # Escribir los encabezados y los datos del DataFrame de Tiempos
        sheet_tiempos.update([df_tiempos.columns.values.tolist()] + df_tiempos.values.tolist())
        print("Datos de Tiempos escritos en Google Sheets exitosamente.")
        
    except Exception as e:
        print(f"Error al conectar con Google Sheets: {e}")
        return

# 6. Flujo principal para descargar datos históricos
def descargar_datos_historicos():
    token = obtener_token()

    if token:
        # Definir fecha de inicio y fin
        fecha_inicio = datetime.strptime("2023-12-01", "%Y-%m-%d")  # Definir como variable
        fecha_actual = datetime.now()

        df_items_total = pd.DataFrame()  # DataFrame vacío para acumular todos los Items
        df_tiempos_total = pd.DataFrame()  # DataFrame vacío para acumular todos los Tiempos

        while fecha_inicio < fecha_actual:
            fecha_fin = fecha_inicio + timedelta(days=6)  # Avanzar en periodos de 7 días

            # Obtener datos de facturación
            data = obtener_datos_facturacion(token, fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d"))

            if data:
                # Procesar datos de Items y Tiempos
                df_items = procesar_datos_a_dataframe_items(data)
                df_tiempos = procesar_datos_a_dataframe_tiempos(data)

                # Acumular los datos en los DataFrames totales
                df_items_total = pd.concat([df_items_total, df_items], ignore_index=True)
                df_tiempos_total = pd.concat([df_tiempos_total, df_tiempos], ignore_index=True)

            # Aumentar la fecha de inicio para la siguiente iteración
            fecha_inicio += timedelta(days=7)

            # Espera de 2 segundos entre consultas para no sobrecargar el servidor
            time.sleep(1)

        # Escribir los DataFrames completos en Google Sheets
        escribir_dataframe_en_google_sheets(df_items_total, df_tiempos_total)

# Ejecutar el flujo principal
if __name__ == "__main__":
    descargar_datos_historicos()
