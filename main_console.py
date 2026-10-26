from cls import Warehouse, NotFindDataInJson, MinValue, WarehouseJournal


def run_console():
    warehouse = Warehouse()

    while True:
        print("\n==== Управление складом ====")
        print("""
Товары 1:
Склад 2:

Выход: 0
""")
        choice = input("Выберите пункт: ").strip()
        if choice == '1':
            products_logic(warehouse)
        elif choice == '2':
            warehouse_logic(warehouse)
        elif choice == '0':
            print("До встречи")
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def products_logic(warehouse):

    while True:
        print("\n==== Меню товаров ====")
        print("""
Создание товара: 1
Редактирование товара: 2
ID товара: 3

Выход: 0
""")
        choice = input("Выберите пункт: ").strip()
        if choice == '1':
            create_product(warehouse)
        elif choice == '2':
            update_product(warehouse)
        elif choice == '3':
            get_id_product(warehouse)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def warehouse_logic(warehouse):

    while True:
        print("\n==== Меню склада ====")
        print("""
Принять товар: 1
Списать товар: 2
Наличие товара: 3
Сортировка: 4
Отчетность: 5

Выход: 0
""")
        choice = input("Выберите пункт: ").strip()

        if choice == '1':
            reasons = input("Причина добавления товара: ")
            accept_product(warehouse, reasons)
        elif choice == '2':
            reasons = input("Причина списания товара: ")
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
            print("Выбран не верный пункт попробуйте снова")


def create_product(warehouse):

    while True:
        print("\n==== Создание товара ====")
        try:
            title = input('Название: ').rstrip()
            category = input('Категория: ').rstrip()
            amount = input('Количество: ').strip()
            price = input('Цена: ').strip()
            warehouse.create_product(
                title=title, category=category, amount=amount, price=price)
            record_transaction(id=warehouse.get_id(
                title), amount=amount, reasons='create')
            break
        except (ValueError, TypeError, KeyError, NotFindDataInJson) as e:
            print(e)


def update_product(warehouse):

    while True:
        print("\n==== Редактирование товара ====")
        try:
            try:
                print("Выход: 0")
                id = input('ID изменяемого товара: ').rstrip()
                if id == '0':
                    break
                warehouse.get_data(id)
                warehouse.update_product(id=id,
                                         title=input(
                                             'Новое название: ').rstrip(),
                                         category=input(
                                             'Новая категория: ').rstrip(),
                                         price=input('Новая цена: ').strip())
                break
            except (KeyError, NotFindDataInJson) as e:
                print("Нет товара с таким ID")
        except (ValueError, TypeError) as e:
            print(e)


def get_id_product(warehouse):
    while True:
        print("\n==== Получение ID ====")
        try:
            print("Выход: 0")
            name = input("Название товара: ").rstrip()
            if name == '0':
                break
            id = warehouse.get_id(name)
            print(f"ID товара {name}: \n{id}")
            break
        except (NotFindDataInJson, KeyError) as e:
            print(e)


def accept_product(warehouse, reasons):
    while True:
        print("\n==== Принятие товара ====")
        print("\nВведите название товара для принятия на вклад \nВыход: 0\n")

        title = input("Название: ").rstrip()
        if title == '0':
            break
        try:
            id = warehouse.get_id(title)
            try:
                amount = input("Количество: ").strip()
                warehouse.set_amount_product(id, amount, plus=True)
                record_transaction(id=id, amount=amount, reasons=reasons)

            except ValueError as e:
                print(e)
        except (KeyError, NotFindDataInJson):
            print("""
Нет зарегестрированого товара с таким названием
Зарегестрировать товар: 1
Пропустить: 0
""")

            choice = input("Выберите пункт: ").strip()
            if choice == '1':
                create_product(warehouse)
            elif choice == '0':
                continue
            else:
                print("Выбран не верный пункт попробуйте снова")


def write_off_product(warehouse, reasons):
    while True:
        print("\n==== Списание товара ====")
        print("Введите название товара для списания со склада \nВыход: 0\n")
        title = input("Название: ").rstrip()
        if title == '0':
            break
        try:
            id = warehouse.get_id(title)
            try:
                amount = input("Количество: ").strip()
                warehouse.set_amount_product(id, amount, plus=False)
                record_transaction(id=id, amount=amount,
                                   reasons=reasons, operation='outgoing')

            except (MinValue, ValueError, TypeError) as e:
                print(e)
        except (KeyError, NotFindDataInJson) as e:
            print(e)


def availability_product(warehouse):
    while True:
        print("\n==== Наличие товара ====")
        warehouse.get_remains(info=True)

        print("""
Найти товар по: 
Названию: 1
ID: 2
Категории: 3

Выход: 0
""")
        choice = input("Выберите пункт: ").strip()
        if choice == '1' or choice == '2':
            if choice == '1':
                try:
                    title = input("Название товара: ").rstrip()
                    id = warehouse.get_id(title)
                except (KeyError, NotFindDataInJson):
                    print("Нет товара с таким названием")
                    id = None
            else:
                id = input("ID товара: ").rstrip()

            if id:
                try:
                    warehouse.product_info(id)
                except (KeyError, NotFindDataInJson) as e:
                    print(e)
        elif choice == '3':
            try:
                category = input("Название категории: ").rstrip()
                warehouse.product_from_category(category)
            except (KeyError, NotFindDataInJson) as e:
                print(e)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def sorted_product(warehouse):
    while True:
        print("\n==== Сортировка товара ====")
        print("""
Сортировать по:
Цене: 1
Названию: 2
Количеству: 3

Выход: 0
""")
        choice = input("Выберите пункт: ").strip()
        if choice in ['1', '2', '3']:
            try:
                warehouse.sort_product(choice)
            except NotFindDataInJson as e:
                print(e)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def report_poduct(warehouse):
    while True:
        print("\n==== Отчет наличия ====")
        print("""
Общий отчет: 1
Остаток ниже заданого количества: 2

Выход: 0
""")
        choice = input("Выберите пункт: ").strip()
        if choice == '1':
            try:
                warehouse.get_remains()
            except NotFindDataInJson as e:
                print(e)
        elif choice == '2':
            num = input("Ниже какого количества искать: ")
            try:
                warehouse.get_remains(num)
            except (NotFindDataInJson, TypeError, MinValue) as e:
                print(e)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def record_transaction(id, amount, reasons, operation='incoming'):
    journal = WarehouseJournal()
    journal.record_transaction(
        operation=operation, id=id, amount=amount, reasons=reasons)


if __name__ == "__main__":
    run_console()
