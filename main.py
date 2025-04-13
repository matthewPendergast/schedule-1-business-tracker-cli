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

def show_menu_options(options, title=None):
    if title is not None:
        print(f"{title}:")
    for i, option in enumerate(options, start=1):
        print(f"- {i}: {option}")

### Utility ###

def get_yes_no(prompt=""):
    while True:
        try:
            choice = int(input(prompt + " (1 = Yes, 0 = No): "))
            if choice == 1:
                return True
            elif choice == 0:
                return False
            else:
                handle_error("Please enter 1 for 'yes' or 0 for 'no.")
        except ValueError:
            handle_error("Please enter 1 for 'yes' or 0 for 'no.")

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
                if not get_yes_no(f"Asking price of ${ask_rate} is unusual. Proceed?"):
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
        clear_screen()

    current_day = get_current_day()
    products = []

    while True:
        display_menu_title(MAIN_MENU_OPTIONS[0])
        print(f"Current Day: {current_day}")

        # Customer region
        while True:
            show_menu_options(config.CUSTOMER_REGIONS, "Select a region")
            try:
                choice = int(input("Customer region: "))
                if 1 <= choice <= len(config.CUSTOMER_REGIONS):
                    customer_region = config.CUSTOMER_REGIONS[choice - 1]
                else:
                    handle_error("Invalid input.")
            except ValueError:
                handle_error("Please enter a valid integer to select a region.")

            customers = [
                name for name, data in customer_data.items()
                if data["REGION"].strip().lower() == customer_region.lower()
            ]

            clear_screen()
            customers.sort()
            print(f"Customers in {customer_region}:")
            for i, name in enumerate(customers, start=1):
                print(f"- {i}: {name}")
            print("- 0: Add new customer")

            while True:
                try:
                    customer_choice = int(input("Select a customer: "))
                    if customer_choice == 0:
                        customer_name = input("Customer name: ")
                        if customer_name in customer_data:
                            handle_error("Customer already exists.")
                            continue
                        if not get_yes_no(f"Add '{customer_name}' to {customer_region}?"):
                            continue

                        io.append_csv(config.CUSTOMER_DATA_CSV, [customer_name, customer_region, "", ""])
                        customer_data[customer_name] = {
                            "REGION": customer_region,
                            "LOCATIONS": set(),
                            "RELATIONSHIP": ""
                        }
                        break
                    elif 1 <= customer_choice <= len(customers):
                        customer_name = customers[customer_choice - 1]
                        break
                    else:
                        handle_error("Invalid selection.")
                except ValueError:
                    handle_error("Please enter a valid number.")
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
                        if not get_yes_no(f"{units_sold} is an unusual amount. Proceed?"):
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
            if not get_yes_no("Add another product?"):
                break

        # Total sales
        while True:
            try:
                total_sales = int(input("Total sales: $"))
                if total_sales < 30 or total_sales > 1000:
                    if not get_yes_no(f"${total_sales} is an unusual amount. Proceed?"):
                        continue
                break
            except ValueError:
                handle_error("Please enter a valid integer for total sales.")

        # Location
        customer_locations = customer_data[customer_name].get("LOCATIONS", set())
        while True:
            clear_screen()
            sorted_locations = sorted(customer_locations)

            if customer_locations:
                show_menu_options(sorted_locations)
            
            print("- 0: Add new location")

            try:
                choice = int(input("Selection location: "))
                if choice == 0:
                    new_location = input("Enter location name: ")
                    customer_locations.add(new_location)
                    location = new_location
                    break
                elif 1 <= choice <= len(sorted_locations):
                    location = sorted_locations[choice - 1]
                    break
                else:
                    handle_error("Invalid input.")
            except ValueError:
                handle_error("Please enter a valid number.")
        customer_data[customer_name]["LOCATIONS"] = customer_locations

        # Time of day
        clear_screen()
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
        clear_screen()
        last_relationship_value = customer_data[customer_name].get("RELATIONSHIP", None)
        print("Relationship level:")
        for i, option in enumerate(config.RELATIONSHIP_OPTIONS, start=0):
            if option == last_relationship_value:
                print(f"- {i}: {option} (previous)")
            else:
                print(f"- {i}: {option}")
        while True:
            try:
                choice = int(input("Choice: "))
                if 0 <= choice <= 5:
                    relationship_level = config.RELATIONSHIP_OPTIONS[choice]
                    customer_data[customer_name]["RELATIONSHIP"] = relationship_level
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

        # Export sales data
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

        # Export customer data
        rows = []
        for name, data in customer_data.items():
            locations_str = "|".join(sorted(data.get("LOCATIONS", [])))
            relationship = data.get("RELATIONSHIP", "")
            rows.append([name, data["REGION"], locations_str, relationship])

        io.write_csv(config.CUSTOMER_DATA_CSV, rows, headers=config.CUSTOMER_DATA_HEADERS)

        products.clear()
        
        clear_screen()
        if not get_yes_no("Add another sale?"):
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
                        if not get_yes_no(f"{material_amount} is an unusual amount. Proceed?"):
                            continue
                    elif material_amount < 1:
                        handle_error("Please enter a valid integer for required amount.")
                        continue
                    break
                except ValueError:
                    handle_error("Please enter a valid integer for required amount.")
            materials.append([material_name, material_amount, material_price])
            if not get_yes_no("Add another material/ingredient?"):
                break
        
        # Production timeframe
        while True:
            try:
                timeframe = int(input("Enter total time (hours) to produce yield: "))
                if timeframe < 1:
                    handle_error("Please enter a valid integer for total time.")
                    continue
                elif timeframe > 24:
                    if not get_yes_no(f"{timeframe} hours is an unusual amount. Proceed?"):
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
                    if not get_yes_no(f"{yield_amount} units is an unusual amount. Proceed?"):
                        continue
                break
            except ValueError:
                handle_error("Please enter a valid integer for yield amount.")

        # Sell price
        while True:
            try:
                sell_price = int(input("Enter sell price per unit: $"))
                if sell_price < 30 or sell_price > 500:
                    if not get_yes_no(f"${sell_price} is an unusual amount. Proceed?"):
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

        if not get_yes_no("Add another product?"):
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
    MENU_OPTIONS = [
        "Edit Price"
    ]
    clear_screen()
    while True:
        print(f"Selected Product: {selected_product}")
        show_menu_options(MENU_OPTIONS)
        print("- 0: Cancel")

        choice = input("Choice: ")
        if choice == "1":
            edit_product_price(selected_product)
        elif choice == "0":
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
                if not get_yes_no(f"{new_price} is an unusual amount. Proceed?"):
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

    if not get_yes_no(f"Delete {selected_product}?"):
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
    global sales_data, product_data, customer_data, location_names, product_names
    sales_data = io.load_or_create_list_csv(config.SALES_DATA_CSV, config.RAW_DATA_REPORT_HEADERS)
    product_data = io.load_or_create_list_csv(config.PRODUCT_DATA_CSV, config.PRODUCT_DATA_HEADERS)
    customer_data = io.load_or_create_dict_csv(
        file_name=config.CUSTOMER_DATA_CSV,
        headers=config.CUSTOMER_DATA_HEADERS,
        key_field="CUSTOMER"
    )
    location_names = io.load_or_create_set_csv(config.LOCATION_NAMES_CSV, ["LOCATION"])
    product_names = io.load_or_create_set_csv(config.PRODUCT_NAMES_CSV, ["PRODUCT"])

    # Convert locations string to set for in-memory use
    for customer, data in customer_data.items():
        loc_string = data.get("LOCATIONS", "")
        data["LOCATIONS"] = set(loc_string.split("|")) if loc_string else set()


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
