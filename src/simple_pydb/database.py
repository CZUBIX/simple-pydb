from .parser import Parser

class Object:
    def __init__(self, json):
        self.__dict__ = json

class Database:
    def __init__(self, database):
        self.database = database
        self.content = open(database, "r").read()
        self.parser = Parser(self.content)

        self.items = {
            "database": "",
            "table": ""
        }

    def get_all(self):
        self.parser.generate_items()

        return self.parser.parse_items()

    def db(self, db):
        self.items["database"] = db
        
        return Object({
            "table": self.table,
            "create_table": self.create_table,
            "delete_table": self.delete_table
        })

    def create_db(self, db):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if db in items:
            return False

        items[db] = {}

        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True

    def delete_db(self, db):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if db in items:
            del items[db]

        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True

    def table(self, table):
        self.items["table"] = table

        return Object({
            "get_items_from_column": self.get_items_from_column,
            "get_row_by_value": self.get_row_by_value,
            "get_items": self.get_items,
            "push": self.push,
            "update": self.update,
            "delete": self.delete,
            "delete_column": self.delete_column
        })

    def create_table(self, table):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if table in items:
            return False

        items[self.items["database"]][table] = []

        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True

    def delete_table(self, table):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if table in items[self.items["database"]]:
            del items[self.items["database"]][table]

        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True

    def get_items_from_column(self, column):
        self.parser.generate_items()

        data = []

        for item in self.parser.parse_items()[self.items["database"]][self.items["table"]]:
            if list(item.keys())[0] == column:
                data.append(item)

        return data

    def get_row_by_value(self, value):
        self.parser.generate_items()

        items = {}
        current_row = 0
        data = {}

        for item in self.parser.parse_items()[self.items["database"]][self.items["table"]]:
            column = list(item.keys())[0]

            if not column in items:
                items[column] = []
                current_row = 0

            items[column].append([list(item.values())[0], current_row])

            current_row += 1

        current_row = None

        for item in items:
            for x in items[item]:
                if x[0] == value:
                    current_row = x[1]
                    break

        for item in items:
            for x in items[item]:
                if x[1] == current_row:
                    data[item] = x[0]

        return data

    def get_items(self):
        self.parser.generate_items()

        return self.parser.parse_items()[self.items["database"]][self.items["table"]]

    def push(self, json):
        self.parser.generate_items()

        items = self.parser.parse_items()
        columns = {}
        data = []

        for item in items[self.items["database"]][self.items["table"]]:
            column = list(item.keys())[0]

            if not column in columns:
                columns[column] = []

            columns[column].append(list(item.values())[0])

        if not len(columns) == len(json):
            return False

        for item in json:
            columns[item].append(json[item])

        for item in columns:
            for x in columns[item]:
                data.append({item: x})
    
        items[self.items["database"]][self.items["table"]] = data   

        print(items[self.items["database"]][self.items["table"]])
        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True

    def update(self, column, value, new_value):
        self.parser.generate_items()
 
        data = []
        items = self.parser.parse_items()

        for item in items[self.items["database"]][self.items["table"]]:
            current_column = list(item.keys())[0]

            if current_column == column and item[current_column] == value:
                item[current_column] = new_value

            data.append(item)

        items[self.items["database"]][self.items["table"]] = data

        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True

    def delete(self, column, value):
        self.parser.generate_items()

        data = []
        items = self.parser.parse_items()

        for item in items[self.items["database"]][self.items["table"]]:
            if list(item.keys())[0] == column and list(item.values())[0] == value:
                item[list(item.keys())[0]] = None

        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True

    def delete_column(self, column):
        self.parser.generate_items()

        data = []
        items = self.parser.parse_items()

        for item in items[self.items["database"]][self.items["table"]]:
            if list(item.keys())[0] == column:
                items[self.items["database"]][self.items["table"]].remove(item)

        self.parser.content = self.parser.parse_from_dict(items)
        open(self.database, "w").write(self.parser.content)

        return True