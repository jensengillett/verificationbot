from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, Boolean

from util.data.table_helper import TableHelper
from util.data.value_helper import ValueHelper


class GuildData:
    def __init__(self, guild_id):
        self.guild_id = guild_id

        engine = create_engine(f'sqlite:///data/guild_{self.guild_id}.db', echo=False)
        meta = MetaData()
        self.conn = engine.connect()

        self.booleans = self.Booleans(meta, self.conn)
        self.disabled_commands = self.DisabledCommands(meta, self.conn)
        self.reactors = self.Reactors(meta, self.conn)
        self.strings = self.Strings(meta, self.conn)
        self.tags = self.Tags(meta, self.conn)

        meta.create_all(engine)

    class Booleans(TableHelper):
        def __init__(self, meta, conn):
            self.conn = conn

            self.booleans = Table(
                'booleans', meta,
                Column('id', Integer, primary_key=True),
                Column('name', String, unique=True),
                Column('value', Boolean)
            )

            super().__init__(self.booleans, self.conn)

        def insert(self, name: str, value: bool):
            self.insert_([{'name': name, 'value': value}])

    class DisabledCommands(TableHelper):
        def __init__(self, meta, conn):
            self.conn = conn

            self.disabled_commands = Table(
                'disabled_commands', meta,
                Column('id', Integer, primary_key=True),
                Column('name', String, unique=True)
            )

            super().__init__(self.disabled_commands, self.conn)

        def delete(self, name: str):
            val = self.fetch_by_name(name, 1)
            if val is not None:
                rep = self.table.delete().where(self.table.columns.name == name)
                self.conn.execute(rep)
                return True
            else:
                return False

        def insert(self, name: str):
            self.insert_([{'name': name}])

    class Reactors(TableHelper):
        def __init__(self, meta, conn):
            self.conn = conn

            self.reactors = Table(
                'reactors', meta,
                Column('id', Integer, primary_key=True),
                Column('message_id', Integer),
                Column('role_id', Integer),
                Column('emoji', String)
            )

            super().__init__(self.reactors, self.conn)

        def delete(self, message_id: int):
            val = self.fetch_by_message_id(message_id)
            if val is not None:
                rep = self.table.delete().where(self.table.columns.message_id == message_id)
                self.conn.execute(rep)
                return True
            else:
                return False

        def fetch_all_by_message_id(self, m_id: int):
            sel = self.table.select().where(self.table.columns.message_id == m_id)
            return list(self.conn.execute(sel))

        def fetch_by_message_id(self, m_id: int, val_pos=2):
            return ValueHelper.list_tuple_value(self.fetch_all_by_message_id(m_id), val_pos)

        def insert(self, message_id: int, role_id: int, emoji: str):
            self.insert_([{'message_id': message_id, 'role_id': role_id, 'emoji': emoji}])

    class Strings(TableHelper):
        def __init__(self, meta, conn):
            self.conn = conn

            self.strings = Table(
                'strings', meta,
                Column('id', Integer, primary_key=True),
                Column('name', String, unique=True),
                Column('value', String)
            )

            super().__init__(self.strings, self.conn)

        def insert(self, name: str, value: str):
            self.insert_([{'name': name, 'value': value}])

    class Tags(TableHelper):
        def __init__(self, meta, conn):
            self.conn = conn

            self.tags = Table(
                'tags', meta,
                Column('id', Integer, primary_key=True),
                Column('name', String, unique=True),
                Column('value', String)
            )

            super().__init__(self.tags, self.conn)

        def insert(self, name: str, value: str):
            self.insert_([{'name': name, 'value': value}])
