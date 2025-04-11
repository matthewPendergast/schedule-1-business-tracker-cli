# CSV File names

SALES_DATA_CSV = "csv/sales_data.csv"
CUSTOMER_NAMES_CSV = "csv/customer_names.csv"
LOCATION_NAMES_CSV = "csv/location_names.csv"

# Excel File names

BUSINESS_REPORT = "business_report.xlsx"

# Matplotlib File names

SALES_TOTALS_PER_DAY = "figures/daily_sales_totals.png"
UNITS_SOLD_PER_DAY = "figures/daily_units_sold.png"
DEALS_PER_DAY = "figures/daily_deals.png"

# Spreadsheet Personalization

FONT_COLOR = "FFFFFF"
CELL_COLOR = "000000"

# Table Names

DAILY_SUMMARY_REPORT_NAME = "Daily Summary"
CUSTOMER_SUMMARY_REPORT_NAME = "Customer Summary"
RAW_DATA_REPORT_NAME = "Raw Data"

# Table Headers

DAILY_SUMMARY_HEADERS = [
    "DAY",
    "TOTAL SALES",
    "UNITS SOLD",
    "REAL RATE",
    "ASK RATE",
    "DEALS",
    "CUSTOMERS"
]

CUSTOMER_SUMMARY_REPORT_HEADERS = [
    "CUSTOMER",
    "TOTAL SALES",
    "UNITS SOLD",
    "DEALS",
    "AVG SALE",
    "AVG UNITS",
    "AVG RATE",
    "RELATIONSHIP",
    "TIME OF DAY (DEALS)",
    "LOCATIONS (DEALS)"
]

RAW_DATA_REPORT_HEADERS = [
    "DAY",
    "CUSTOMER",
    "UNITS SOLD",
    "TOTAL SALES",
    "REAL RATE",
    "ASK RATE",
    "LOCATION",
    "TIME OF DAY",
    "RELATIONSHIP"
]

# Game Values

TIME_OF_DAY_OPTIONS = [
    "6AM-12PM",
    "12AM-6PM",
    "6PM-12AM",
    "12AM-6AM"
]

RELATIONSHIP_OPTIONS = [
    "Hostile",
    "Unfriendly",
    "Neutral",
    "Friendly",
    "Loyal"
]