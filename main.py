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
    "Add Individual Sales Data",
    "Add Distributor Sales Data",
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

def get_yes_no(prompt=""):
    while True:
        try:
            choice = int(input(prompt + " (1 = Yes, 0 = No): "))
            match choice:
                case 1:
                    return True
                case 0:
                    return False
                case _:
                    handle_error("Please enter 1 for 'yes' or 0 for 'no.")
        except ValueError:
            handle_error("Please enter 1 for 'yes' or 0 for 'no.")

### Add Individual Sales Data Menu ###

def display_sales_data_menu_title(menu_index=None, current_day=None, person_name=None):
    clear_screen()
    character_type = "Customer" if menu_index == 0 else "Distributor"
    if menu_index:
        display_menu_title(MAIN_MENU_OPTIONS[menu_index])
    if current_day:
        print(f"= Current Day: {current_day} =")
    if person_name:
        print(f"= Current {character_type}: {person_name} =")

def add_sales_data_menu():
    # Ensure user has setup at least one product
    if not product_names:
        display_sales_data_menu_title(0)
        print("No products registered. Please add a product to begin.")
        add_new_product()

    display_sales_data_menu_title(0)
    current_day = get_current_day()
    products = []

    while True:
        # Customer region
        while True:
            display_sales_data_menu_title(0, current_day)
            show_menu_options(config.CUSTOMER_REGIONS, "Select a region")
            try:
                choice = int(input("Choice: "))
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

            display_sales_data_menu_title(0, current_day)
            customers.sort()
            print(f"Customers in {customer_region}:")
            for i, name in enumerate(customers, start=1):
                print(f"- {i}: {name}")
            print("- 0: Add new customer")

            while True:
                try:
                    customer_choice = int(input("Choice: "))
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
        display_sales_data_menu_title(0, current_day, customer_name)
        products = get_products_sold([])

        # Total sales
        total_sales = get_total_sales()

        # Location
        customer_locations = customer_data[customer_name].get("LOCATIONS", set())
        while True:
            display_sales_data_menu_title(0, current_day, customer_name)
            sorted_locations = sorted(customer_locations)

            if customer_locations:
                show_menu_options(sorted_locations, "Select a location")
            
            print("- 0: Add new location")

            try:
                choice = int(input("Choice: "))
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
        display_sales_data_menu_title(0, current_day, customer_name)
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
        display_sales_data_menu_title(0, current_day, customer_name)
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
        
        display_sales_data_menu_title(0, current_day, customer_name)
        print("Sale complete!\n")
        if not get_yes_no("Add another sale?"):
            break

def get_current_day():
    while True:
        try:
            current_day = int(input("Enter the day number: "))
            break
        except ValueError:
            handle_error("Please enter a valid integer for the day.")
    return current_day

def get_products_sold(products):
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
                elif units_sold <= 0:
                    handle_error("Please enter a valid amount for units sold.")
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

    return products

def get_total_sales():
    while True:
        try:
            total_sales = int(input("Total sales: $"))
            if total_sales < 30 or total_sales > 1000:
                if not get_yes_no(f"${total_sales} is an unusual amount. Proceed?"):
                    continue
            break
        except ValueError:
            handle_error("Please enter a valid integer for total sales.")
    return total_sales

### Distributor Sales Data Menu ###

def add_distributor_sales_data_menu():
    clear_screen()
    display_menu_title(MAIN_MENU_OPTIONS[1])

    current_day = get_current_day()

    while True:
        display_sales_data_menu_title(1, current_day)
        distributors = sorted(distributor_names)
        show_menu_options(distributors, "Select a distributor")
        print("- 0: Add new distributor")

        # Distributor name
        while True:
            try:
                choice = int(input("Choice: "))
                if 1 <= choice <= len(distributors):
                    selected_distributor = distributors[choice - 1]
                    break
                elif choice == 0:
                    selected_distributor = input("Distributor name: ")
                    if selected_distributor in distributor_names:
                        handle_error("Distributor already exists.")
                        continue
                    elif not get_yes_no(f"Add {selected_distributor} to distributor list?"):
                        continue
                    else:
                        io.append_csv(config.DISTRIBUTOR_NAMES_CSV, [selected_distributor])
                        distributor_names.add(selected_distributor)
                        break
                else:
                    handle_error("Invalid input.")
            except ValueError:
                handle_error("Please enter a valid integer.")

        # Products
        display_sales_data_menu_title(1, current_day, selected_distributor)
        products = get_products_sold([])

        # Sales
        total_sales = get_total_sales()

        if get_yes_no(f"Is {selected_distributor}'s cut already included?"):
            gross_sales = int(total_sales / 0.8)
            net_sales = total_sales
        else:
            gross_sales = total_sales
            net_sales = int(total_sales * 0.8)

        # Calculate real (actual) rate
        total_units = sum(units for _, units, _ in products)
        real_rate = round((gross_sales / total_units), 2)

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
            selected_distributor,
            total_units,
            gross_sales,
            net_sales,
            real_rate,
            ask_rate,
            products_string
        ]

        io.append_csv(config.DISTRIBUTOR_SALES_DATA_CSV, export_data)
        distributor_sales_data.append(export_data)

        products.clear()
        
        display_sales_data_menu_title(1, current_day, selected_distributor)
        print("Distributor sales complete!\n")
        if not get_yes_no("Add another distributor's sales?"):
             break

### Manage Product Menu ###

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

        choice = int(input("Choice: "))
        match choice:
            case 1:
                clear_screen()
                add_new_product()
            case 2:
                clear_screen()
                selected_product = select_product()
                if selected_product:
                    edit_product(selected_product)
            case 3:
                clear_screen()
                selected_product = select_product()
                if selected_product:
                    delete_product(selected_product)
            case 4:
                return
            case _:
                handle_error("Invalid input.")

def add_new_product():
    materials = []
    
    while True:
        # Set product information
        product_name = set_product_name()
        materials = set_product_materials(materials)
        timeframe = set_product_timeframe()
        yield_amount = set_product_yield_amount()
        sell_price = set_product_price()

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

def set_product_name(current_name=None):
    prompt = "Product Name: "
    if current_name is not None:
        prompt = "- New product name: "

    while True:
            product_name = input(prompt)
            if product_name in product_names:
                handle_error("Product already exists.")
                return
            else:
                io.append_csv(config.PRODUCT_NAMES_CSV, [product_name])
                product_names.add(product_name)
                break

    return product_name

def set_product_materials(materials):
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

    return materials

def set_product_timeframe(current_timeframe=None):
    prompt = "Enter total time (hours) to produce yield: "
    if current_timeframe is not None:
        print(f"- Current Timeframe (hours): {current_timeframe}")
        prompt = "- New Timeframe (hours): "

    while True:
        try:
            timeframe = int(input(prompt))
            if timeframe < 1:
                handle_error("Please enter a valid integer for total time.")
                continue
            elif timeframe > 24:
                if not get_yes_no(f"{timeframe} hours is an unusual amount. Proceed?"):
                    continue
            break
        except ValueError:
            handle_error("Please enter a valid integer for total time.")

    return timeframe

def set_product_yield_amount(current_yield=None):
    prompt = "Enter yield amount per batch: "
    if current_yield is not None:
        print(f"- Current Yield: {current_yield}")
        prompt = "- New Yield: "
    
    while True:
        try:
            yield_amount = int(input(prompt))
            if yield_amount < 1:
                handle_error("Please enter a valid integer for yield amount.")
                continue
            elif yield_amount > 12:
                if not get_yes_no(f"{yield_amount} units is an unusual amount. Proceed?"):
                    continue
            break
        except ValueError:
            handle_error("Please enter a valid integer for yield amount.")
        
    return yield_amount

def set_product_price(current_price=None):
    prompt = "Enter sell price per unit: $"
    if current_price is not None:
        print(f"- Current Price: ${current_price}")
        prompt = "- New Price: $"

    while True:
        try:
            product_price = int(input(prompt))
            if product_price < 30 or product_price > 500:
                if not get_yes_no(f"{product_price} is an unusual amount. Proceed?"):
                    continue
            break
        except ValueError:
            handle_error("Please enter a valid integer for the sell price.")

    return product_price    

def select_product():
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
        "Edit Name",
        "Edit Price",
        "Edit Materials",
        "Edit Timeframe",
        "Edit Yield"
    ]
    clear_screen()
    while True:
        print(f"Selected Product: {selected_product}")
        show_menu_options(MENU_OPTIONS)
        print("- 0: Cancel")

        choice = int(input("Choice: "))
        match choice:
            case 1:
                edit_product_name(selected_product)
                return
            case 2:
                edit_product_price(selected_product)
            case 3:
                edit_product_materials(selected_product)
            case 4:
                edit_product_timeframe(selected_product)
            case 5:
                edit_product_yield_amount(selected_product)
            case 0:
                return
            case _:
                handle_error("Invalid input.")

def edit_product_name(selected_product):
    clear_screen()
    print(f"Selected Product: {selected_product}")
    new_name = set_product_name(selected_product)

    # Update the product names list
    if selected_product in product_names:
        product_names.remove(selected_product)
    product_names.add(new_name)

    # Update the relevant CSV files
    updated_names = [[name] for name in sorted(product_names)]
    io.write_csv(config.PRODUCT_NAMES_CSV, updated_names, headers=["PRODUCT"])
    save_product_edit_changes(selected_product, 0, new_name)

def edit_product_price(selected_product):
    clear_screen()
    print(f"Selected Product: {selected_product}")

    for row in product_data:
        if row[0] == selected_product:
            current_price = int(row[4])
            break

    new_price = set_product_price(current_price)
    save_product_edit_changes(selected_product, 4, new_price)

def edit_product_materials(selected_product):
    clear_screen()
    print(f"Selected Product: {selected_product}")
    
    new_materials = set_product_materials([])

    # Serialize materials list
    materials_string = "|".join(
        f"{name}:{amount}:{price}" for name, amount, price in new_materials
    )

    save_product_edit_changes(selected_product, 1, materials_string)

def edit_product_timeframe(selected_product):
    clear_screen()
    print(f"Selected Product: {selected_product}")

    for row in product_data:
        if row[0] == selected_product:
            current_timeframe = int(row[2])
            break
    
    new_timeframe = set_product_timeframe(current_timeframe)
    save_product_edit_changes(selected_product, 2, new_timeframe)

def edit_product_yield_amount(selected_product):
    clear_screen()
    print(f"Selected Product: {selected_product}")

    for row in product_data:
        if row[0] == selected_product:
            current_yield = int(row[3])
            break
    
    new_yield = set_product_yield_amount(current_yield)
    save_product_edit_changes(selected_product, 3, new_yield)

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
        row for row in product_data[1:] if row[0] != selected_product
    ]
    io.write_csv(config.PRODUCT_DATA_CSV, updated_product_data, headers=config.PRODUCT_DATA_HEADERS)

    # Update in-memory list
    product_data.clear()
    product_data.extend(updated_product_data)

    print(f"{selected_product} deleted successfully.")
    time.sleep(1)
    clear_screen()

def save_product_edit_changes(selected_product, row_number, new_value):
    # Update in-memory list
    for row in product_data:
        if row[0] == selected_product:
            row[row_number] = new_value
            # Update name if changed
            if row_number == 0:
                selected_product = new_value
            break
    
    io.write_csv(config.PRODUCT_DATA_CSV, product_data[1:], headers=config.PRODUCT_DATA_HEADERS)
    
    print(f"{selected_product} updated.")
    time.sleep(1)
    clear_screen()

### Initialization ###

def initialize():
    global sales_data, distributor_sales_data, product_data, customer_data, product_names, distributor_names
    sales_data = io.load_or_create_list_csv(config.SALES_DATA_CSV, config.RAW_DATA_REPORT_HEADERS)
    distributor_sales_data = io.load_or_create_list_csv(config.DISTRIBUTOR_SALES_DATA_CSV, config.RAW_DISTRIBUTOR_DATA_REPORT_HEADERS)
    product_data = io.load_or_create_list_csv(config.PRODUCT_DATA_CSV, config.PRODUCT_DATA_HEADERS)
    customer_data = io.load_or_create_dict_csv(
        file_name=config.CUSTOMER_DATA_CSV,
        headers=config.CUSTOMER_DATA_HEADERS,
        key_field="CUSTOMER"
    )
    product_names = io.load_or_create_set_csv(config.PRODUCT_NAMES_CSV, ["PRODUCT"])
    distributor_names = io.load_or_create_set_csv(config.DISTRIBUTOR_NAMES_CSV, ["DISTRIBUTOR"])

    # Convert locations string to set for in-memory use
    for customer, data in customer_data.items():
        loc_string = data.get("LOCATIONS", "")
        data["LOCATIONS"] = set(loc_string.split("|")) if loc_string else set()


### Main Loop ###

def main_menu_loop():
    while True:
        display_menu_title(APP_NAME)
        show_menu_options(MAIN_MENU_OPTIONS)

        choice = int(input("Choice: "))
        match choice:
            case 1:
                add_sales_data_menu()
            case 2:
                add_distributor_sales_data_menu()
            case 3:
                manage_product_menu()
            case 4:
                clear_screen()
                io.export_spreadsheet()
                io.export_figures()
                print("Closing program.")
                break
            case _:
                handle_error("Invalid input.")

if __name__ == "__main__":
    try:
        initialize()
        main_menu_loop()
    except KeyboardInterrupt:
        print("\nClosing program.")
