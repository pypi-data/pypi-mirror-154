# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['light_sql3']
setup_kwargs = {
    'name': 'light-sql3',
    'version': '1.0.0',
    'description': 'Light cover for sqlite3',
    'long_description': '# Light db\nLight db this is easy cover for database sqlite3\n## How to use\n```py\nfrom light_db import database\n\nexample = DataBase(\n    name="light_db"\n)\n\n# Method insert (return type bool)\nexample.insert(id="some_id", value="some_value")\n\n\n# Method get (return value by id)\nprint(example.get(id="some_id"))\n\n\n# Method add (return type bool)\nexample.add(id="some_id", num=100)\n\n\n# Method remove (return type bool)\nexample.remove(id="some_id", num=100)\n\n\n# Method all (return all values from table)\nprint(example.all())\n\n\n# Method update (return type bool)\nexample.update(id="some_id", value=1000)\n\n\n# Method has (return type bool)\nprint(example.has(id="some_id"))\n\n\n# Method delete (return type bool)\nexample.delete(id="some_id")\n\n# I think the command names make it clear what exactly they do\n```',
    'author': 'Forzy',
    'author_email': 'nikita11tzby@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
