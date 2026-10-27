from cls import Warehouse, NotFindDataInJson, MinValue, WarehouseJournal


def run_console():
    warehouse = Warehouse()

    while True:
        print("\n==== Warehouse Management ====")
        print("""
Products 1:
Warehouse 2:

Exit: 0
""")
        choice = input("Select an option: ").strip()
        if choice == '1':
            products_logic(warehouse)
        elif choice == '2':
            warehouse_logic(warehouse)
        elif choice == '0':
            print("See you later")
            break
        else:
            print("Invalid option, please try again")


def products_logic(warehouse):

    while True:
        print("\n==== Products Menu ====")
        print("""
Create product: 1
Edit product: 2
Product ID: 3

Exit: 0
""")
        choice = input("Select an option: ").strip()
        if choice == '1':
            create_product(warehouse)
        elif choice == '2':
            update_product(warehouse)
        elif choice == '3':
            get_id_product(warehouse)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again")


def warehouse_logic(warehouse):

    while True:
        print("\n==== Warehouse Menu ====")
        print("""
Receive product: 1
Write-off product: 2
Product availability: 3
Sort: 4
Reporting: 5

Exit: 0
""")
        choice = input("Select an option: ").strip()

        if choice == '1':
            reasons = input("Reason for adding product: ")
            accept_product(warehouse, reasons)
        elif choice == '2':
            reasons = input("Reason for writing off product: ")
            write_off_product(warehouse, reasons)
        elif choice == '3':
            availability_product(warehouse)
        elif choice == '4':
            sorted_product(warehouse)
        elif choice == '5':
            report_poduct(warehouse)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again")


def create_product(warehouse):

    while True:
        print("\n==== Create Product ====")
        try:
            title = input('Title: ').rstrip()
            category = input('Category: ').rstrip()
            amount = input('Amount: ').strip()
            price = input('Price: ').strip()
            warehouse.create_product(
                title=title, category=category, amount=amount, price=price)
            record_transaction(id=warehouse.get_id(
                title), amount=amount, reasons='Сreate')
            break
        except (ValueError, TypeError, KeyError, NotFindDataInJson) as e:
            print(e)


def update_product(warehouse):

    while True:
        print("\n==== Edit Product ====")
        try:
            try:
                print("Exit: 0")
                id = input('ID of the product to edit: ').rstrip()
                if id == '0':
                    break
                warehouse.get_data(id)
                warehouse.update_product(id=id,
                                         title=input(
                                             'New title: ').rstrip(),
                                         category=input(
                                             'New category: ').rstrip(),
                                         price=input('New price: ').strip())
                break
            except (KeyError, NotFindDataInJson) as e:
                print("No product with this ID")
        except (ValueError, TypeError) as e:
            print(e)


def get_id_product(warehouse):
    while True:
        print("\n==== Get ID ====")
        try:
            print("Exit: 0")
            name = input("Product title: ").rstrip()
            if name == '0':
                break
            id = warehouse.get_id(name)
            print(f"Product ID {name}: \n{id}")
            break
        except (NotFindDataInJson, KeyError) as e:
            print(e)


def accept_product(warehouse, reasons):
    while True:
        print("\n==== Receive Product ====")
        print("\nEnter product title to receive into stock \nExit: 0\n")

        title = input("Title: ").rstrip()
        if title == '0':
            break
        try:
            id = warehouse.get_id(title)
            try:
                amount = input("Amount: ").strip()
                warehouse.set_amount_product(id, amount, plus=True)
                record_transaction(id=id, amount=amount, reasons=reasons)

            except ValueError as e:
                print(e)
        except (KeyError, NotFindDataInJson):
            print("""
No registered product with this title
Register product: 1
Skip: 0
""")

            choice = input("Select an option: ").strip()
            if choice == '1':
                create_product(warehouse)
            elif choice == '0':
                continue
            else:
                print("Invalid option, please try again")


def write_off_product(warehouse, reasons):
    while True:
        print("\n==== Write-off Product ====")
        print("Enter product title to write off from warehouse \nExit: 0\n")
        title = input("Title: ").rstrip()
        if title == '0':
            break
        try:
            id = warehouse.get_id(title)
            try:
                amount = input("Amount: ").strip()
                warehouse.set_amount_product(id, amount, plus=False)
                record_transaction(id=id, amount=amount,
                                   reasons=reasons, operation='outgoing')

            except (MinValue, ValueError, TypeError) as e:
                print(e)
        except (KeyError, NotFindDataInJson) as e:
            print(e)


def availability_product(warehouse):
    while True:
        print("\n==== Product Availability ====")
        warehouse.get_remains(info=True)

        print("""
Find product by: 
Title: 1
ID: 2
Category: 3

Exit: 0
""")
        choice = input("Select an option: ").strip()
        if choice == '1' or choice == '2':
            if choice == '1':
                try:
                    title = input("Product title: ").rstrip()
                    id = warehouse.get_id(title)
                except (KeyError, NotFindDataInJson):
                    print("No product with this title")
                    id = None
            else:
                id = input("Product ID: ").rstrip()

            if id:
                try:
                    warehouse.product_info(id)
                except (KeyError, NotFindDataInJson) as e:
                    print(e)
        elif choice == '3':
            try:
                category = input("Category name: ").rstrip()
                warehouse.product_from_category(category)
            except (KeyError, NotFindDataInJson) as e:
                print(e)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again")


def sorted_product(warehouse):
    while True:
        print("\n==== Sort Products ====")
        print("""
Sort by:
Price: 1
Title: 2
Amount: 3

Exit: 0
""")
        choice = input("Select an option: ").strip()
        if choice in ['1', '2', '3']:
            try:
                warehouse.sort_product(choice)
            except NotFindDataInJson as e:
                print(e)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again")


def report_poduct(warehouse):
    while True:
        print("\n==== Stock Report ====")
        print("""
General report: 1
Stock below specified amount: 2

Exit: 0
""")
        choice = input("Select an option: ").strip()
        if choice == '1':
            try:
                warehouse.get_remains()
            except NotFindDataInJson as e:
                print(e)
        elif choice == '2':
            num = input("Search below what amount: ")
            try:
                warehouse.get_remains(num)
            except (NotFindDataInJson, TypeError, MinValue) as e:
                print(e)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again")


def record_transaction(id, amount, reasons, operation='incoming'):
    journal = WarehouseJournal()
    journal.record_transaction(
        operation=operation, id=id, amount=amount, reasons=reasons)


if __name__ == "__main__":
    run_console()
