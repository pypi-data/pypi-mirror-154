# Light db
Light db this is easy cover for database sqlite3
## How to use
```py
from light_db import database

example = DataBase(
    name="light_db"
)

# Method insert (return type bool)
example.insert(id="some_id", value="some_value")


# Method get (return value by id)
print(example.get(id="some_id"))


# Method add (return type bool)
example.add(id="some_id", num=100)


# Method remove (return type bool)
example.remove(id="some_id", num=100)


# Method all (return all values from table)
print(example.all())


# Method update (return type bool)
example.update(id="some_id", value=1000)


# Method has (return type bool)
print(example.has(id="some_id"))


# Method delete (return type bool)
example.delete(id="some_id")

# I think the command names make it clear what exactly they do
```