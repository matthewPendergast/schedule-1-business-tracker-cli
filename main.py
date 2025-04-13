# MIT License
# Copyright (c) 2025 Matthew Pendergast

### Imports ###

# Standard Library Imports
import os
import time

# Local Application Imports
import modules.config as config
import modules.data_io as io

### Interface ###

APP_NAME = "Schedule 1 Business Tracker"

MAIN_MENU_OPTIONS = [
    "Add Sales Data",
    "Manage Products",
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

def show_menu_options(options):
    print("Menu Options:")
    for i, option in enumerate(options, start=1):
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
                if get_yes_no(f"Asking price of ${ask_rate} is unusual. Proceed? (y/n): ") == "n":
                    continue
            return ask_rate
        except ValueError:
            handle_error("Please enter a valid integer for the asking price.")

### Menu Options ###

# Add Sales Data Menu
def add_sales_data_menu():
    display_menu_title(MAIN_MENU_OPTIONS[0])

    # Ensure user has setup at least one product
    if not product_names:
        add_new_product()

    current_day = get_current_day()
    products = []

    while True:
        display_menu_title(MAIN_MENU_OPTIONS[0])
        print(f"Current Day: {current_day}")

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

        # Products sold
        while True:
            selected_product = select_product()
            if selected_product is None:
                return

            # Units
            while True:
                try:
                    units_sold = int(input("Units sold: "))
                    if units_sold < 0 or units_sold > 10:
                        if get_yes_no(f"{units_sold} is an unusual amount. Proceed? (y/n): ") == "n":
                            continue
                    break
                except ValueError:
                    handle_error("Please enter a valid integer for units sold.")
            
            # Pull selected product's sell price
            product_price = None
            for row in product_data:
                if row[0] == selected_product:
                    product_price = int(row[4])
                    break
            if product_price is None:
                handle_error(f"Could not find price for {selected_product}.")
                return
            products.append([selected_product, units_sold, product_price])
            if get_yes_no("Add another product? (y/n): ") == "n":
                break

        # Total sales
        while True:
            try:
                total_sales = int(input("Total sales: $"))
                if total_sales < 30 or total_sales > 1000:
                    if get_yes_no(f"${total_sales} is an unusual amount. Proceed? (y/n): ") == "n":
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
        print("Time of day:")
        for i, option in enumerate(config.TIME_OF_DAY_OPTIONS, start=1):
            print(f"- {i}: {option}")
        while True:
            try:
                choice = int(input("Choice: "))
                if 1 <= choice <= 4:
                    time_of_day = config.TIME_OF_DAY_OPTIONS[choice - 1]
                    break
                else:
                    handle_error("Invalid input.")
            except ValueError:
                handle_error("Invalid input.")

        # Relationship
        print("Relationship level:")
        for i, option in enumerate(config.RELATIONSHIP_OPTIONS, start=0):
            print(f"- {i}: {option}")
        while True:
            try:
                choice = int(input("Choice: "))
                if 0 <= choice <= 5:
                    relationship_level = config.RELATIONSHIP_OPTIONS[choice]
                    break
                else:
                    handle_error("Invalid input.")
            except ValueError:
                handle_error("Invalid input.")

        # Calculate real (actual) rate
        total_units = sum(units for _, units, _ in products)
        real_rate = round((total_sales / total_units), 2)

        # Calculate ask (expected) rate
        total_ask_value = sum(units * price for _, units, price in products)
        ask_rate = round(total_ask_value / total_units, 2)

        # Serialize product information
        products_string = "|".join(
            f"{name}:{units}:{price}" for name, units, price in products
        )

        # Export user inputs
        export_data = [
            current_day,
            customer_name,
            total_units,
            total_sales,
            real_rate,
            ask_rate,
            products_string,
            location,
            time_of_day,
            relationship_level
        ]
        io.append_csv(config.SALES_DATA_CSV, export_data)
        sales_data.append(export_data)

        products.clear()

        if get_yes_no("Add another sale? (y/n): ") == "n":
            break

# Manage Product Menu
def manage_product_menu():
    MENU_OPTIONS = [
        "Add New Product",
        "Edit Product",
        "Delete Product",
        "Return to Main Menu"
    ]
    while True:
        display_menu_title(MAIN_MENU_OPTIONS[1])
        show_menu_options(MENU_OPTIONS)
        choice = input("Choice: ")

        if choice == "1":
            add_new_product()
        elif choice == "2":
            selected_product = select_product()
            if selected_product:
                edit_product(selected_product)
        elif choice == "3":
            selected_product = select_product()
            if selected_product:
                delete_product(selected_product)
        elif choice == "4":
            return
        else:
            handle_error("Invalid input.")

def add_new_product():
    clear_screen()
    materials = []
    
    while True:
        # Product name
        while True:
            product_name = input("Product Name: ")
            if product_name in product_names:
                handle_error("Product already exists.")
                return
            else:
                io.append_csv(config.PRODUCT_NAMES_CSV, [product_name])
                product_names.add(product_name)
                break
        
        # Required materials
        while True:
            material_name = input("Enter a required material/ingredient: ").replace(":", "").replace("|", "")
            # Material price
            while True:
                try:
                    material_price = int(input(f"Enter price of 1 unit of {material_name}: $"))
                    break
                except ValueError:
                    handle_error("Please enter a valid integer for material price.")
            # Material amount
            while True:
                try:
                    material_amount = int(input(f"Enter required amount of {material_name}: "))
                    if material_amount > 10:
                        if get_yes_no(f"{material_amount} is an unusual amount. Proceed? (y/n): ") == "n":
                            continue
                    elif material_amount < 1:
                        handle_error("Please enter a valid integer for required amount.")
                        continue
                    break
                except ValueError:
                    handle_error("Please enter a valid integer for required amount.")
            materials.append([material_name, material_amount, material_price])
            if get_yes_no("Add another material/ingredient? (y/n): ") == "n":
                break
        
        # Production timeframe
        while True:
            try:
                timeframe = int(input("Enter total time (hours) to produce yield: "))
                if timeframe < 1:
                    handle_error("Please enter a valid integer for total time.")
                    continue
                elif timeframe > 24:
                    if get_yes_no(f"{timeframe} hours is an unusual amount. Proceed? (y/n): ") == "n":
                        continue
                break
            except ValueError:
                handle_error("Please enter a valid integer for total time.")
        
        # Yield amount
        while True:
            try:
                yield_amount = int(input("Enter yield amount per batch: "))
                if yield_amount < 1:
                    handle_error("Please enter a valid integer for yield amount.")
                    continue
                elif yield_amount > 12:
                    if get_yes_no(f"{yield_amount} units is an unusual amount. Proceed? (y/n): ") == "n":
                        continue
                break
            except ValueError:
                handle_error("Please enter a valid integer for yield amount.")

        # Sell price
        while True:
            try:
                sell_price = int(input("Enter sell price per unit: $"))
                if sell_price < 30 or sell_price > 500:
                    if get_yes_no(f"${sell_price} is an unusual amount. Proceed? (y/n): ") == "n":
                        continue
                break
            except ValueError:
                handle_error("Please enter a valid integer for sell price.")

        # Serialize material information
        materials_string = "|".join(
            f"{name}:{amount}:{price}" for name, amount, price in materials
        )

        # Store and save product information
        export_data = [
            product_name,
            materials_string,
            timeframe,
            yield_amount,
            sell_price
        ]
        io.append_csv(config.PRODUCT_DATA_CSV, export_data)
        product_data.append(export_data)

        if get_yes_no("Add another product? (y/n): ") == "n":
            break

def select_product():
    clear_screen()

    if not product_names:
        handle_error("No products available.")
        return
    
    product_list = sorted(product_names)
    print("Select a product: ")
    for i, name in enumerate(product_list, start=1):
        print(f"- {i}: {name}")
    print("- 0: Cancel")

    while True:
        try:
            choice = int(input("Choice: "))
            if 1 <= choice <= len(product_list):
                selected_product = product_list[choice - 1]
                break
            elif choice == 0:
                return
            else:
                handle_error("Invalid input.")
        except ValueError:
            handle_error("Please enter a valid integer.")

    return selected_product

def edit_product(selected_product):
    clear_screen()

    MENU_OPTIONS = [
        "Edit Price",
        "Cancel"
    ]
    while True:
        print(f"Selected Product: {selected_product}")
        choice = input("Choice: ")

        if choice == "1":
            edit_product_price(selected_product)
        elif choice == "2":
            return
        else:
            handle_error("Invalid input.")

def edit_product_price(selected_product):
    clear_screen()
    print(f"Selected Product: {selected_product}")

    for row in product_data:
        if row[0] == selected_product:
            current_price = int(row[4])
            print(f"- Current Price: ${current_price}")
            break
    
    while True:
        try:
            new_price = int(input("- New Price: $"))
            if new_price < 30 or new_price > 500:
                if get_yes_no(f"{new_price} is an unusual amount. Proceed? (y/n): ") == "n":
                    continue
            break
        except ValueError:
            handle_error("Please enter a valid integer for the new price.")
    
    # Update in-memory list
    for row in product_data:
        if row[0] == selected_product:
            row[4] = new_price
            break
    
    io.write_csv(config.PRODUCT_DATA_CSV, product_data, headers=config.PRODUCT_DATA_HEADERS)

    print(f"{selected_product} price updated.")
    time.sleep(1)
    clear_screen()

def delete_product(selected_product):
    clear_screen()

    if get_yes_no(f"Delete {selected_product}? (y/n): ") == "n":
        return
    
    product_names.remove(selected_product)

    # Modify product_names.csv
    updated_names = [[name] for name in product_names]
    io.write_csv(config.PRODUCT_NAMES_CSV, updated_names, headers=["PRODUCT"])

    # Modify product_data.csv
    updated_product_data = [
        row for row in product_data if row[0] != selected_product
    ]
    io.write_csv(config.PRODUCT_DATA_CSV, updated_product_data, headers=config.PRODUCT_DATA_HEADERS)

    # Update in-memory list
    product_data.clear()
    product_data.extend(updated_product_data)

    print(f"{selected_product} deleted successfully.")
    time.sleep(1)
    clear_screen()

### Initialization ###

def initialize():
    global sales_data, product_data, customer_names, location_names, product_names
    sales_data = io.load_or_create_list_csv(config.SALES_DATA_CSV, config.RAW_DATA_REPORT_HEADERS)
    product_data = io.load_or_create_list_csv(config.PRODUCT_DATA_CSV, config.PRODUCT_DATA_HEADERS)
    customer_names = io.load_or_create_set_csv(config.CUSTOMER_NAMES_CSV, ["CUSTOMER NAME"])
    location_names = io.load_or_create_set_csv(config.LOCATION_NAMES_CSV, ["LOCATION"])
    product_names = io.load_or_create_set_csv(config.PRODUCT_NAMES_CSV, ["PRODUCT"])

### Main Loop ###

def main_menu_loop():
    while True:
        display_menu_title(APP_NAME)
        show_menu_options(MAIN_MENU_OPTIONS)
        choice = input("Choice: ")
        
        if choice == "1":
            add_sales_data_menu()
        elif choice == "2":
            manage_product_menu()
        elif choice == "3":
            clear_screen()
            io.export_spreadsheet()
            io.export_figures()
            print("Closing program.")
            break
        else:
            handle_error("Invalid input.")

if __name__ == "__main__":
    try:
        initialize()
        main_menu_loop()
    except KeyboardInterrupt:
        print("\nClosing program.")
