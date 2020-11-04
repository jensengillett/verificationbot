from sqlalchemy import Table

from util.data.value_helper import ValueHelper


class TableHelper:

    def __init__(self, table: Table, conn):
        self.table = table
        self.conn = conn

    def delete(self, name: str):
        val = self.fetch_by_name(name)
        if val is not None:
            rep = self.table.delete().where(self.table.columns.name == name)
            self.conn.execute(rep)
            return True
        else:
            return False

    def delete_all(self):
        rep = self.table.delete()
        self.conn.execute(rep)

    def fetch_all(self):
        sel = self.table.select()
        return list(self.conn.execute(sel))

    def fetch_all_by_name(self, name: str):
        sel = self.table.select().where(self.table.columns.name == name)
        return list(self.conn.execute(sel))

    def fetch_by_name(self, name: str, val_pos=2):
        return ValueHelper.list_tuple_value(self.fetch_all_by_name(name), val_pos)

    def insert_(self, items: list):
        self.conn.execute(self.table.insert(), items)

    def set(self, name: str, value):
        val = self.fetch_by_name(name)
        if val is not None:
            rep = self.table.update().where(self.table.columns.name == name).values(value=value)
            self.conn.execute(rep)
            return value
        else:
            self.insert_([{'name': name, 'value': value}])
            return value

    def toggle_boolean(self, name: str, default_val=True):
        val = self.fetch_by_name(name)
        if val is not None:
            new_val = not val
            rep = self.table.update().where(self.table.columns.name == name).values(value=new_val)
            self.conn.execute(rep)
            return new_val
        else:
            self.insert_([{'name': name, 'value': default_val}])
            return True
