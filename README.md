# Documentation

Creating a class

```py
import simple_pydb

db = simple_pydb.Database("database.pydb")
```

Getting all items
`<db>.get_all()`

# Database

Creating a database object
`<db>.db(database_name)`

Creating a database
`<db>.create_db(database_name)`

Deleting a database
`<db>.delete_db(database_name)`

# Table

Creating a table object
`<db>.db(database_name).table(table_name)`

Creating a table
`<db>.db(database_name).create_table(table_name)`

Deleting a table
`<db>.db(database_name).delete_table(table_name)`

# Columns and values

Getting all items from column
`<db>.db(database_name).table(table_name).get_items_from_column(column_name)`

Getting row by value
`<db>.db(database_name).table(table_name).get_row_by_value(value)`

Getting items
`<db>.db(database_name).table(table_name).get_items()`

Pushing items
`<db>.db(database_name).table(table_name).push({column_name: value})`

Updating item
`<db>.db(database_name).table(table_name).update(column_name, value, new_value)`

Deleting row
`<db>.db(database_name).table(table_name).delete(column_name, value)`

Deleting column
`<db>.db(database_name).table(table_name).delete_column(column_name)`
