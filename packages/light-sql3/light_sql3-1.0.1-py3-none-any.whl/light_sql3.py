# MIT License

# Copyright (c) 2022 @Forzy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sqlite3 as SQL
import os
import os.path
from typing import Any


class DataBase:
    def __init__(
            self,
            directory: str=os.getcwd(),
            name: str="database",
            ext: str="db"    
        ) -> None:
        if ext in ("db", "sqlite3") and os.path.exists(path=directory):
            self.name = "{}.{}".format(name, ext)
            self.dir = directory
            self.path = os.path.join(self.dir, self.name)
            # Sql 
            self.connection = SQL.connect(database=self.path)
            self.cursor = self.connection.cursor()

            self.cursor.execute("CREATE TABLE IF NOT EXISTS js (id TEXT, value TEXT)")
            self.connection.commit()
    def __str__(self) -> str:
        return self.path
    def __repr__(self) -> str:
        return self.path
        
    # Methods

    def get(self, id: str=None) -> SQL.Cursor:
        '''It is necessary to display the `value` from the table by id'''
        if id is None: 
            raise TypeError("You must enter id")
        elif self.cursor.execute("SELECT value FROM js WHERE id='{id}'".format(id=id)).fetchone() == None:
            return None

        self.cursor.execute("SELECT value FROM js WHERE id='{id}'".format(id=id))
        return self.cursor.fetchone()[0]

    def insert(self, id: str=None, value: str | Any=None) -> SQL.Cursor:
        '''It is necessary to insert the `value` in the table'''
        if None in (id, value): 
            raise TypeError("You must enter args")

        try:
            if self.cursor.execute("SELECT value FROM js WHERE id='{id}'".format(id=id)).fetchone() is None:
                self.cursor.execute("INSERT INTO js VALUES ('{id}', '{value}')".format(id=id, value=value))
            else:
                self.cursor.execute("UPDATE js SET value='{value}' WHERE id='{id}'".format(value=value, id=id))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return True    

    def add(self, id: str=None, num: int | Any=None) -> SQL.Cursor:
        if None in (id, num):
            raise TypeError("You must enter args")
        elif not isinstance(num, int):
            if not num.isdigit():
                raise TypeError("Bad Type")
        elif self.cursor.execute("SELECT value FROM js WHERE id = '{id}'".format(id=id)).fetchone() is None:
            return None

        s = int(self.cursor.execute("SELECT value FROM js WHERE id = '{id}'".format(id=id)).fetchone()[0])
        try:
            self.cursor.execute("UPDATE js SET value={value} WHERE id='{id}'".format(value=int(num)+s, id=id))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return True

    def remove(self, id: str=None, num: int | Any=None) -> SQL.Cursor:
        if None in (id, num):
            raise TypeError("You must enter args")
        elif not isinstance(num, int):
            if not num.isdigit():
                raise TypeError("Bad Type")
        elif self.cursor.execute("SELECT value FROM js WHERE id = '{id}'".format(id=id)).fetchone() is None:
            return None


        s = int(self.cursor.execute("SELECT value FROM js WHERE id = '{id}'".format(id=id)).fetchone()[0])
        try:
            self.cursor.execute("UPDATE js SET value={value} WHERE id='{id}'".format(value=s-int(num), id=id))
            self.connection.commit()
        except:
            return False
        else:
            return True

    def all(self) -> Any:
        self.cursor.execute("SELECT * from js")
        for iter in self.cursor.fetchall(): 
            yield iter

    def update(self, id: str=None, value: str | Any=None) -> SQL.Cursor:
        if None in (id, value):
            raise TypeError("You must enter args")
        elif self.cursor.execute("SELECT value FROM js WHERE id = '{id}'".format(id=id)).fetchone() is None:
            return None
        value = "{value}".format(value=value) if type(value) == int else "'{value}'".format(value=value)
        
        try:
            self.cursor.execute("UPDATE js SET value="+value+" WHERE id='{id}'".format(id=id))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return True
    

    def has(self, id: str=None) -> SQL.Cursor:
        if id is None:
            raise TypeError("You must enter args")


        self.cursor.execute("SELECT value FROM js WHERE id='{id}'".format(id=id))
        return True if self.cursor.fetchone() is not None else False
    
    def delete(self, id: str=None) -> SQL.Cursor:
        if id is None:
            raise TypeError("You must enter args")
        elif self.cursor.execute("SELECT value FROM js WHERE id = '{id}'".format(id=id)).fetchone() is None:
            return None

        try:
            self.cursor.execute("DELETE FROM js WHERE id='{id}'".format(id=id))
        except Exception as e:
            return e
        else:
            return True
