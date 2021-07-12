from .parser import Parser
from .types import Empty
from typing import List, Dict, Any

class Db:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
    def __repr__(self):
        return "Db"
    def __str__(self):
        return "Db"

class Table:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
    def __repr__(self):
        return "Table"
    def __str__(self):
        return "Table"

class Database:
    def __init__(self, database):
        self.database = database
        self.content = open(self.database, "r").read()
        self.parser = Parser(self.content)

        self.items = {
            "database": "",
            "table": ""
        }

    def save(self):
        open(self.database, "w").write(self.parser.content)

    def get_all(self) -> Dict[Any, Dict[Any, list]]:
        self.parser.generate_items()

        return self.parser.parse_items()

    def db(self, name) -> Db:
        self.items["database"] = name

        return Db(
            table = self.table,
            create_table = self.create_table,
            delete_table = self.delete_table
        )

    def create_db(self, name):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if name in items:
            return False

        items[name] = {}
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True

    def delete_db(self, name):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if not name in items:
            return False

        del items[name]
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True

    def table(self, name) -> Table:
        self.items["table"] = name

        return Table(
            create_column = self.create_column,
            get_items_from_column = self.get_items_from_column,
            get = self.get,
            get_items = self.get_items,
            push = self.push,
            update = self.update,
            delete = self.delete,
            delete_row = self.delete_row,
            delete_column = self.delete_column
        )

    def create_table(self, name):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if name in items[self.items["database"]]:
            return False

        items[self.items["database"]][name] = {}
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()
        
        return True

    def delete_table(self, name):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if not name in items[self.items["database"]]:
            return False

        del items[self.items["database"]][name]
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()
        
        return True

    def create_column(self, name):
        self.parser.generate_items()

        values = []
        items = self.parser.parse_items()

        if name in items[self.items["database"]][self.items["table"]]:
            return False

        if items[self.items["database"]][self.items["table"]]:
            for _ in list(items[self.items["database"]][self.items["table"]].values())[0]:
                values.append(Empty())
            
        items[self.items["database"]][self.items["table"]][name] = values
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True

    def get_items_from_column(self, name) -> list:
        self.parser.generate_items()

        items = self.parser.parse_items()[self.items["database"]][self.items["table"]]

        if not name in items:
            return False

        return items[name]

    def get(self, column, value) -> List[dict]:
        self.parser.generate_items()

        data = []
        index = None
        items = self.parser.parse_items()[self.items["database"]][self.items["table"]]

        if not column in items:
            return False

        for _column in items:
            if _column == column:
                for _value in items[column]:
                    if _value == value:
                        index = items[column].index(value)
                        break
                break

        if index == None:
            return False

        for _column in items:
            data.append({_column: items[_column][index]})

        return data

    def get_items(self) -> Dict[Any, list]:
        self.parser.generate_items()

        return self.parser.parse_items()[self.items["database"]][self.items["table"]]

    def push(self, values: dict):
        self.parser.generate_items()

        items = self.parser.parse_items()

        for item in items[self.items["database"]][self.items["table"]].keys():
            if not item in values:
                values[item] = Empty()

        for column, value in values.items():
            if not column in items[self.items["database"]][self.items["table"]]:
                return False

            items[self.items["database"]][self.items["table"]][column].append(value)

        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True

    def update(self, column, value, in_column, new_value):
        self.parser.generate_items()

        index = None
        items = self.parser.parse_items()

        if not (column in items[self.items["database"]][self.items["table"]] or in_column in items[self.items["database"]][self.items["table"]]):
            return False

        for _column in items[self.items["database"]][self.items["table"]]:
            if _column == column:
                for _value in items[self.items["database"]][self.items["table"]][column]:
                    if _value == value:
                        index = items[self.items["database"]][self.items["table"]][column].index(value)
                        break
                break

        if index == None:
            return False

        items[self.items["database"]][self.items["table"]][in_column][index] = new_value
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True

    def delete(self, column, value, in_column):
        self.parser.generate_items()

        index = None
        items = self.parser.parse_items()

        if not (column in items[self.items["database"]][self.items["table"]] or in_column in items[self.items["database"]][self.items["table"]]):
            return False

        for _column in items[self.items["database"]][self.items["table"]]:
            if _column == column:
                for _value in items[self.items["database"]][self.items["table"]][column]:
                    if _value == value:
                        index = items[self.items["database"]][self.items["table"]][column].index(value)
                        break
                break

        if index == None:
            return False

        items[self.items["database"]][self.items["table"]][in_column][index] = Empty()
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True

    def delete_row(self, column, value):
        self.parser.generate_items()

        index = None
        items = self.parser.parse_items()

        if not column in items[self.items["database"]][self.items["table"]]:
            return False

        for _column in items[self.items["database"]][self.items["table"]]:
            if _column == column:
                for _value in items[self.items["database"]][self.items["table"]][column]:
                    if _value == value:
                        index = items[self.items["database"]][self.items["table"]][column].index(value)
                        break
                break

        if index == None:
            return False

        for _column in items[self.items["database"]][self.items["table"]]:
            del items[self.items["database"]][self.items["table"]][_column][index]

        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True

    def delete_column(self, name):
        self.parser.generate_items()

        items = self.parser.parse_items()

        if not name in items[self.items["database"]][self.items["table"]]:
            return False

        del items[self.items["database"]][self.items["table"]][name]
        self.parser.content = self.parser.parse_from_dict(items)
        self.save()

        return True