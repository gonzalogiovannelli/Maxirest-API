## API Data Extractor  
A Python script to extract billing data from the Oceanside API and export it to Google Sheets.  

## Features  
- Connects to the API using secure authentication  
- Processes and structures billing data (Items and Times)  
- Saves data into Google Sheets  

## 📌 Product Backlog  

### 🔹 Epic 1: Automate Data Retrieval  
- **User Story 1**  
  - As a data analyst, I want to extract billing data from the API, so I can analyze it without manual input.  
  - **Acceptance Criteria:**  
    - API credentials are securely stored.  
    - The script retrieves the latest billing data without errors.  
    - API response time is logged for monitoring.  

- **User Story 2**  
  - As a developer, I want to schedule automated data extractions, so I can ensure up-to-date insights.  
  - **Acceptance Criteria:**  
    - Extraction runs automatically at a predefined time.  
    - API request failures trigger a retry mechanism.  

### 🔹 Epic 2: Validate & Clean Data  
- **User Story 3**  
  - As a BI consultant, I want to validate the extracted data, so I can ensure it matches real transactions.  
  - **Acceptance Criteria:**  
    - The script checks for missing or duplicate records.  
    - Transactions with incorrect formats are flagged for review.  

- **User Story 4**  
  - As a data engineer, I want to standardize date formats, so I can ensure consistency across reports.  
  - **Acceptance Criteria:**  
    - All date values follow a single standard format.  
    - Time zone adjustments are handled correctly.  

### 🔹 Epic 3: Store & Structure Data  
- **User Story 5**  
  - As a Power BI user, I want the extracted data to be formatted correctly, so I can create accurate reports.  
  - **Acceptance Criteria:**  
    - The script saves structured data in a clean format.  
    - Field names match the expected schema for Power BI.  

- **User Story 6**  
  - As a business analyst, I want the data stored in a Google Sheet, so I can access it without technical expertise.  
  - **Acceptance Criteria:**  
    - The script uploads extracted data to a predefined Google Sheet.  
    - Data is updated without overwriting historical records.  

### 🔹 Epic 4: Monitor & Maintain the Process  
- **User Story 7**  
  - As a system admin, I want error logs to be generated, so I can troubleshoot issues easily.  
  - **Acceptance Criteria:**  
    - API request errors are logged with timestamps.  
    - A summary of extracted records is stored for debugging.  

- **User Story 8**  
  - As a project manager, I want documentation on how the API is used, so onboarding new team members is easier.  
  - **Acceptance Criteria:**  
    - README includes clear setup instructions.  
    - API parameters and authentication methods are documented.  

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
