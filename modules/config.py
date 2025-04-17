# CSV File names

SALES_DATA_CSV = "csv/sales_data.csv"
DISTRIBUTOR_SALES_DATA_CSV = "csv/distributor_sales_data.csv"
PRODUCT_DATA_CSV = "csv/product_data.csv"
CUSTOMER_DATA_CSV = "csv/customer_data.csv"
PRODUCT_NAMES_CSV = "csv/product_names.csv"
DISTRIBUTOR_NAMES_CSV = "csv/distributor_names.csv"

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
DISTRIBUTOR_SUMMARY_REPORT_NAME = "Distributor Summary"
CUSTOMER_SUMMARY_REPORT_NAME = "Customer Summary"
PRODUCT_SUMMARY_REPORT_NAME = "Product Summary"
RAW_DATA_REPORT_NAME = "Raw Data"

# Table Headers

DAILY_SUMMARY_HEADERS = [
    "DAY",
    "TOTAL SALES",
    "MY SALES",
    "DISTR SALES",
    "TOTAL UNITS",
    "MY UNITS",
    "DISTR UNITS",
    "DEALS",
    "PRODUCTS SOLD",
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

PRODUCT_SUMMARY_REPORT_HEADERS = [
    "PRODUCT",
    "MATERIAL COST",
    "SELL PRICE",
    "YIELD",
    "PRODUCTION TIME",
    "MARGIN",
    "PROFIT PER BATCH",
    "PROFIT PER HOUR",
    "TOTAL SALES",
    "UNITS SOLD",
    "REAL RATE"
]

RAW_DATA_REPORT_HEADERS = [
    "DAY",
    "CUSTOMER",
    "UNITS SOLD",
    "TOTAL SALES",
    "REAL RATE",
    "ASK RATE",
    "PRODUCTS",
    "LOCATION",
    "TIME OF DAY",
    "RELATIONSHIP"
]

RAW_DISTRIBUTOR_DATA_REPORT_HEADERS = [
    "DAY",
    "DISTRIBUTOR",
    "UNITS SOLD",
    "GROSS SALES",
    "NET SALES",
    "REAL RATE",
    "ASK RATE",
    "PRODUCTS"
]

CUSTOMER_DATA_HEADERS = [
    "CUSTOMER",
    "REGION",
    "LOCATIONS",
    "RELATIONSHIP"
]

PRODUCT_DATA_HEADERS = [
    "PRODUCT",
    "MATERIALS",
    "TIMEFRAME",
    "YIELD",
    "SELL PRICE"
]

# Game Values

CUSTOMER_REGIONS = [
    "Northtown",
    "Westville",
    "Downtown",
    "Docks",
    "Suburbia",
    "Uptown"
]

TIME_OF_DAY_OPTIONS = [
    "6AM-12PM",
    "12PM-6PM",
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