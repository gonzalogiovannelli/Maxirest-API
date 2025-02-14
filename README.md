## API Data Extractor  
A Python script to extract billing data from the Oceanside API and export it to Google Sheets.  

## Features  
- Connects to the API using secure authentication  
- Processes and structures billing data (Items and Times)  
- Saves data into Google Sheets  

## Requirements  
- Python 3.10+  
- `requests`, `pandas`, `gspread`, `oauth2client`  

## Installation  
```bash  
pip install -r requirements.txt  
```  

## Usage  
```bash  
python maxirest_API_connection.py  
```  

## Extracted Tables  
The script retrieves two main datasets from the API and exports them to Google Sheets:  

### 1. Items Table (`Items` Sheet)  
Details of each item in billing orders.  

| **Column**            | **Description**                                |
|-----------------------|------------------------------------------------|
| Fecha                | Order date (`orderDate`)                       |
| OrderID             | Unique identifier for the order (`orderId`)    |
| OrderType           | Type of order (`orderType`)                    |
| Título de Ítem      | Name of the item (`title`)                    |
| Categoría del Producto | Product category (`productCategory`)        |
| Cantidad            | Quantity ordered (`quantity`)                  |
| Precio del Ítem     | Price per item (`productPrice`)               |
| Total del Ítem      | Total cost for the item (`totalPrice`)         |

### 2. Times Table (`Tiempos` Sheet)  
Records the opening, closing, and sales times for each order.  

| **Column**           | **Description**                                |
|----------------------|------------------------------------------------|
| Fecha                | Order date (`orderDate`)                      |
| OrderID             | Unique identifier for the order (`orderId`)   |
| OrderType           | Type of order (`orderType`)                   |
| Time Open           | Opening time of the order (`timeOpen`)       |
| Time Close          | Closing time of the order (`timeClose`)      |
| Total Sales         | Total sales amount (`totalSales`)            |

## Author  
[Gonzalo Giovannelli](https://github.com/gonzalogiovannelli)
