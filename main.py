# MIT License
# Copyright (c) 2025 Matthew Pendergast

### Imports ###

# Standard Library Imports
import os
import time

# Third-Party Library Imports

# Local Application Imports
import config
import data_io as io

### Interface ###

APP_NAME = "Schedule 1 Business Tracker"

MENU_OPTIONS = [
    "Add Sales Data",
    "Export & Exit"
]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def handle_error(message):
    print(f"⚠️  {message}")
    time.sleep(1)

def display_menu_title(title):
    buffer = 10
    width = len(title) + buffer
    clear_screen()
    print("╔" + "═" * width + "╗")
    print(f"║{title.center(width)}║")
    print("╚" + "═" * width + "╝")

def show_menu_options():
    print("Menu Options:")
    for i, option in enumerate(MENU_OPTIONS, start=1):
        print(f"- {i}: {option}")

### Utility ###

def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "n"):
            return choice
        else:
            handle_error("Please enter 'y' for yes or 'n' for no.")

def get_current_day():
    while True:
        try:
            current_day = int(input("Enter the day number: "))
            break
        except ValueError:
            handle_error("Please enter a valid integer for the day.")
    return current_day

def get_ask_rate():
    while True:
        try:
            ask_rate = int(input("Enter the product asking price: "))
            if ask_rate < 30 or ask_rate > 100:
                if get_yes_no(f"Asking price of {ask_rate} is unusual. Proceed? (y/n): ") == "n":
                    continue
            return ask_rate
        except ValueError:
            handle_error("Please enter a valid integer for the asking price.")

### Menu Options ###

def add_sales_data_menu():
    current_day = 0
    ask_rate = 0

    display_menu_title(MENU_OPTIONS[0])
    current_day = get_current_day()
    ask_rate = get_ask_rate()

    while True:
        display_menu_title(MENU_OPTIONS[0])
        print(f"Current Day: {current_day}")
        print(f"Asking Price: {ask_rate}")

        # Customer name
        while True:
            customer_name = input("Customer: ")
            if customer_name not in customer_names:
                if get_yes_no(f"{customer_name} is not in the known customer list. Add new customer? (y/n): ") == "n":
                    continue
                else:
                    io.append_csv(config.CUSTOMER_NAMES_CSV, [customer_name])
                    customer_names.add(customer_name)
            break

        # Units
        while True:
            try:
                units_sold = int(input("Units sold: "))
                if units_sold < 1 or units_sold > 10:
                    if get_yes_no(f"{units_sold} is an unusual amount. Proceed? (y/n): ") == "n":
                        continue
                break
            except ValueError:
                handle_error("Please enter a valid integer for units sold.")

        # Total sales
        while True:
            try:
                total_sales = int(input("Total sales: "))
                if total_sales < 35 or total_sales > 1000:
                    if get_yes_no(f"{total_sales} is an unusual amount. Proceed? (y/n): ") == "n":
                        continue
                break
            except ValueError:
                handle_error("Please enter a valid integer for total sales.")

        # Location
        while True:
            location = input("Location of sale: ")
            if location not in location_names:
                if get_yes_no(f"{location} is not in the known location list. Add new location? (y/n): ") == "n":
                    continue
                else:
                    io.append_csv(config.LOCATION_NAMES_CSV, [location])
                    location_names.add(location)
            break

        # Time of day
        print("Time of day options:")
        for i, option in enumerate(config.TIME_OF_DAY_OPTIONS, start=1):
            print(f"- {i}: {option}")
        while True:
            try:
                choice = int(input("Choice: "))
                if 1 <= choice <= 4:
                    time_of_day = config.TIME_OF_DAY_OPTIONS[choice-1]
                    break
                else:
                    handle_error("Invalid input.")
            except ValueError:
                handle_error("Invalid input.")

        # Rate
        real_rate = round((total_sales / units_sold), 2)

        # Export user inputs
        export_data = [
            current_day,
            customer_name,
            units_sold,
            total_sales,
            real_rate,
            ask_rate,
            location,
            time_of_day,
        ]
        io.append_csv(config.SALES_DATA_CSV, export_data)
        sales_data.append(export_data)

        if get_yes_no("Add another sale? (y/n): ") == "n":
            break

### Initialization ###

# Load or create CSV files
sales_data = io.load_or_create_list_csv(config.SALES_DATA_CSV, config.CUSTOMER_SUMMARY_HEADERS)
customer_names = io.load_or_create_set_csv(config.CUSTOMER_NAMES_CSV, ["CUSTOMER NAME"])
location_names = io.load_or_create_set_csv(config.LOCATION_NAMES_CSV, ["LOCATION"])

### Main Loop ###
while True:
    display_menu_title(APP_NAME)
    show_menu_options()
    choice = input("Choice: ")
    
    if choice == "1":
        add_sales_data_menu()
    elif choice == "2":
        clear_screen()
        io.export_spreadsheet()
        io.export_figures()
        print("Closing program.")
        break
    else:
        handle_error("Invalid input.")
