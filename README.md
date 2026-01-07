# Sales Analytics System

A Python-based sales data analytics tool that processes transaction data, performs comprehensive analysis, enriches data with external APIs, and generates detailed reports.

## Features

- **Robust Data Ingestion**: Handles multiple file encodings
- **Data Validation**: Ensures data quality before analysis
- **Comprehensive Analytics**: 
  - Total revenue calculation
  - Region-wise sales analysis
  - Date-based trend analysis
  - Product performance tracking
- **API Integration**: Enriches data with product details from DummyJSON
- **Interactive Filtering**: User-driven data exploration
- **Professional Reporting**: Generates formatted text reports

## Installation

1. Clone this repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Place your sales data file in `data/sales_data.txt`

## Usage

Make sure you're in the project root, then run:

Windows
```bash
python main.py
```

Mac/Linux
```bash
python3 main.py
```

What to expect:
1. System reads your data
2. Asks if you want to filter (type `n` for now to test everything)
3. Shows analysis
4. Fetches from API
5. Generates reports

If it works, you'll see:
```text
============================================================
             SALES ANALYTICS SYSTEM
============================================================

Step 1: Reading sales data...
Successfully read file with utf-8 encoding
Read 10 lines

Step 2: Parsing transactions...
Parsed 10 transactions

Step 3: Validating data...
Validation complete: 10 valid, 0 invalid

------------------------------------------------------------
FILTERING OPTIONS
------------------------------------------------------------
Available regions: East, North, South, West
Transaction amount range: $280.00 - $3,747.00

Apply filters? (y/n): n

------------------------------------------------------------
QUICK ANALYSIS
------------------------------------------------------------
Total Revenue: $17,163.00
Top Region: East ($7,343.00)
Peak Sales Day: 2024-01-19

------------------------------------------------------------
API ENRICHMENT
------------------------------------------------------------
Fetching product data from API...
Fetched 100 products from API
Enriched 10 transactions (0 matched with API)
Enriched data saved to output/enriched_sales_data.txt

------------------------------------------------------------
REPORT GENERATION
------------------------------------------------------------
Report generated: output/sales_report.txt

============================================================
               ANALYSIS COMPLETE!
============================================================

Generated files:
  output/enriched_sales_data.txt
  output/sales_report.txt
```

## File Structure

- `main.py` - Main workflow and user interaction
- `utils/file_handler.py` - Data reading, parsing, validation
- `utils/data_processor.py` - Analysis functions
- `utils/api_handler.py` - External API integration
- `data/` - Input data folder
- `output/` - Generated reports and enriched data

## Data Format

Input file should be pipe-delimited (|) with these columns:
```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
```

## Output

The system generates:
1. `output/enriched_sales_data.txt` - JSON file with API-enriched data
2. `output/sales_report.txt` - Formatted analysis report

## Requirements

- Python 3.7+
- requests library

## Author

Priti Saldanha

## License

MIT
nul not found
