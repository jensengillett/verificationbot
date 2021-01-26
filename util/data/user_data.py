from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, Boolean

from EmailVerify.util.data.table_helper import TableHelper


class UserData:
    def __init__(self, user_id):
        self.user_id = user_id

        engine = create_engine(f'sqlite://./data/user_{self.user_id}.db', echo=False)
        meta = MetaData()
        self.conn = engine.connect()

        self.booleans = self.Booleans(meta, self.conn)

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
