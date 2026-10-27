from datetime import datetime
import uuid
import json


class NotFindDataInJson(Exception):
    pass


class MinValue(Exception):
    pass


class WarehouseJournal:

    def record_transaction(self, operation, id, amount, reasons):
        with open('info_log.jsonl', 'a', encoding='utf-8') as file:
            data = {'operation': operation,
                    'id': id,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'amount': int(amount),
                    'reasons': reasons}
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write('\n')


class Warehouse:

    @staticmethod
    def get_data(id=None):
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                if id:
                    if data.get(id):
                        return data
                    else:
                        raise KeyError("Product with this ID does not exist")
                if data:
                    return data
                else:
                    raise json.JSONDecodeError
        except json.JSONDecodeError:
            raise NotFindDataInJson("Product database is empty")

    @staticmethod
    def dump_data(data):
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write('\n')

    def get_id(self, title):

        try:
            data = self.get_data()
        except NotFindDataInJson:
            raise

        for k in data.keys():
            if data[k]['title'] == title:
                return k
        raise KeyError("Product with this title does not exist")

    def create_product(self, **kwargs):
        product = Product(**kwargs)
        id = product.id

        with open('data.json', 'r') as file_r:
            try:
                data = json.load(file_r)
            except json.JSONDecodeError:
                data = {}

            if data.get(id) is None:
                data[id] = product.in_json()
                self.dump_data(data)

            else:
                raise KeyError("Product with this ID already exists")
        return print("Product registered successfully")

    def update_product(self, id, **kwargs):

        try:
            data = self.get_data(id)
        except (KeyError, NotFindDataInJson):
            raise

        try:
            product = Product(id=id, amount=data[id]['amount'], **kwargs)
            data[id] = product.in_json()
            self.dump_data(data)
        except (ValueError, TypeError):
            raise
        return print("Product updated successfully")

    def set_amount_product(self, id, amount, plus):
        try:
            data = self.get_data(id)
        except (KeyError, NotFindDataInJson):
            raise

        product = Product(id=id, **data[id])
        product.set_amount(amount, plus=plus)
        data[id] = product.in_json()

        self.dump_data(data)
        if plus:
            return print(f"Product {data[id]['title']} received")
        return print(f"Product {data[id]['title']} dispatched in quantity of {amount} pcs.")

    def product_info(self, id):
        try:
            data = self.get_data(id)
        except (KeyError, NotFindDataInJson):
            raise

        if id in data:
            product = Product(id=id, **data[id])
            return print(product)
        raise KeyError("Product with this ID does not exist")

    def product_from_category(self, category):
        try:
            data = self.get_data()
        except NotFindDataInJson:
            raise
        res = []
        for k, v in data.items():
            if v['category'] == category:
                res.append(Product(id=k, **v))

        if not res:
            raise KeyError("No products found in this category")
        for el in res:
            print(el, '\n')

    def sort_product(self, key):
        dict_key = {'1': 'price', '2': 'title', '3': 'amount'}
        try:
            data = self.get_data()
        except NotFindDataInJson:
            raise
        for id, el in sorted(data.items(), key=lambda x: x[1][dict_key[key]], reverse=False if key == '2' else True):
            print(Product(**el, id=id))

    def get_remains(self, n=None, info=None):
        try:
            data = self.get_data()
        except NotFindDataInJson:
            raise

        count = 0
        full_price = 0
        all_product = []
        if n:
            try:
                n = int(n)
                if n < 1:
                    raise MinValue("Number cannot be less than 1")
            except (TypeError, ValueError):
                raise TypeError("Please enter a number")
            except MinValue:
                raise

            for el in data.values():
                if el['amount'] <= n:
                    count += 1
                    full_price += el['price'] * el['amount']
                    all_product.append(el['title'])
        else:
            for el in data.values():
                count += 1
                full_price += el['price'] * el['amount']
                all_product.append(el['title'])

        if info is True:
            return print(f"There are {count} items in stock")
        print(f"{count} item(s) for a total cost of {full_price}$")
        print(f"Product(s): {', '.join(all_product)}")


class Product:

    def __init__(self, title, category, amount, price, id=None):
        self.id = [id, str(uuid.uuid4())][id is None]

        self.title = title
        self.category = category

        self.amount = amount
        self.price = price

    def __setattr__(self, name, value):
        if name in {'title', 'category'}:
            if not isinstance(value, str):
                print(type(value))
                print(value)
                raise TypeError(f"{name} must be a string")
            if len(value) < 3:
                raise ValueError(f"Name is too short for: {name}")

        if name in {'amount', 'price'}:
            if not isinstance(value, (int, float)):
                try:
                    value = str(value.replace(',', '.'))
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except (TypeError, ValueError):
                    raise TypeError(f"{name} must be a number")
            if value < 0:
                raise ValueError(
                    f"Number for {name} cannot be negative")
        super().__setattr__(name, value)

    def __str__(self):
        return f"{self.title} Category: {self.category}, Stock: {self.amount} pcs, Price: {self.price}$, Total cost: {self.amount * self.price}$"

    def __repr__(self):
        return f"{self.id}: {self.amount}"

    def in_json(self):
        product = self.__dict__
        data = {'title': product['title'],
                'amount': product['amount'],
                'price': product['price'],
                'category': product['category']}
        return data

    def set_amount(self, value, plus=True):
        try:
            value = (int(value), float(value))['.' in value]
        except ValueError:
            raise ValueError("Value must be a number")
        if value < 0:
            raise ValueError(f"Number cannot be negative")

        if not plus:
            if (self.amount - value) < 0:
                raise MinValue("Not enough products in stock")
            self.amount -= value
        else:
            self.amount += value
