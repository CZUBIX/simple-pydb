import json
from .types import Empty

class Parser:
    def __init__(self, content: str):
        self.content = content.splitlines()
        self.generated = []
        self.parsed = {}

        self.items = {
            "database": "",
            "table": "",
            "column": "",
            "type": "",
            "value": "",
            "values": {}
        }

        self.types = {
            "str": self.injection_fix,
            "int": int,
            "float": float,
            "bool": self.bool_checker,
            "list": self.list_parser,
            "dict": json.loads,
            "Empty": Empty
        }

        self.types2 = {
            "str": self.str_replace,
            "int": str,
            "float": str,
            "bool": str,
            "list": self.list_dumper,
            "dict": json.dumps,
            "Empty": Empty
        }

    def injection_fix(self, item):
        item = item.replace("\n", "\\n")
        item = item.replace("->", "-\\>")

        return item

    def bool_checker(self, item):
        items = {
            "True": True,
            "False": False
        }
        
        return items[item]

    def list_parser(self, items):
        data = []
        items = items.split(";")

        for item in items:
            item = item.split("->")
            item = self.types[item[1]](item[0])
            
            data.append(item)

        return data

    def str_replace(self, item):
        item = item.replace("\\n", "\n")
        item = item.replace("-\\>", "->")

        return item

    def list_dumper(self, items):
        data = []

        for item in items:
            _type = type(item).__name__
            item = self.types2[_type](item)

            data.append((item, _type))

        return ";".join([f"{x[0]}->{x[1]}" for x in data])

    def clear_items(self, item: str = None):
        to_clear = {
            "table": "",
            "column": "",
            "type": "",
            "value": "",
            "values": {}
        }

        if item: to_clear[item] = ""

        for x in to_clear:
            self.items[x] = to_clear[x]

    def generate_items(self):
        for line in self.content:
            tokens = line.split(":", 1)

            try:
                while tokens[0][0] == " ":
                    tokens[0] = tokens[0][1:]
            except:
                continue
                
            self.generated.append(tokens)

        return self.generated

    def parse_items(self):
        for item in self.generated:
            if item[0] == "DB":
                self.clear_items("database")
                self.items["database"] = item[1]

            elif item[0] == "TABLE":
                self.clear_items()
                self.items["table"] = item[1]

            elif item[0] == "COLUMN":
                self.items["column"] = item[1]

            elif item[0] == "TYPE":
                self.items["type"] = self.types[item[1]]

            elif item[0] == "VALUE":
                self.items["value"] = self.items["type"](item[1])

            if self.items["column"]:
                if not self.items["column"] in self.items["values"]:
                    self.items["values"][self.items["column"]] = []

                if self.items["value"]:
                    self.items["values"][self.items["column"]].append(self.items["value"])

            if self.items["database"] and not self.items["database"] in self.parsed:
                self.parsed[self.items["database"]] = {}
            
            if self.items["table"] and not self.items["table"] in self.parsed[self.items["database"]]:
                self.parsed[self.items["database"]][self.items["table"]] = self.items["values"]

            self.items["value"] = ""

        return self.parsed

    def parse_from_dict(self, parsed: dict):
        text = ""

        for db in parsed:
            text += f"DB:{db}\n"

            for table in parsed[db]:
                text += f"    TABLE:{table}\n"
                
                for column in parsed[db][table]:
                    text += f"        COLUMN:{column}\n"

                    for value in parsed[db][table][column]:
                        text += f"            TYPE:{type(value).__name__}\n"
                        text += f"            VALUE:{self.types2[type(value).__name__](value)}\n"

        return text