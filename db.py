from apswutils import Database
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class DatabaseDict:
    def __init__(self):
        self._user: dict[str, Database] = {}  # store connections
        # python wouldn't know where to find and reuse connections

        import os

        os.makedirs("db", exist_ok=True)
        self.app: Database = Database("db/app.db", strict=True)
        self.app.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    name TEXT NOT NULL PRIMARY KEY,
                    pwd TEXT NOT NULL
                )
        """)

        ### DEBUG
        self.app.execute(
            "INSERT OR REPLACE INTO user (name, pwd) VALUES (?, ?)",
            ("asd", pwd_context.hash("asd")),
        )
        ### DEBUG

    def get(self, name: str = "app") -> Database:  # db.app, db.name
        if name not in self._user:
            self._user[name] = Database(f"db/{name}.db", strict=True)

            if not self._user[name].table_names():
                self._user[name].execute("""
                        CREATE TABLE IF NOT EXISTS test (
                            day DATE PRIMARY KEY,
                            form TEXT NOT NULL,
                            progress INTEGER NOT NULL,
                            lv1 INTEGER NOT NULL,
                            lv2 INTEGER NOT NULL,
                            lv3 INTEGER NOT NULL,
                            lv4 INTEGER NOT NULL,
                            lv5 INTEGER NOT NULL
                        )
                """)

                ### DEBUG
                import random

                self._user[name].execute(
                    """
                        INSERT OR REPLACE INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
                        VALUES (CURRENT_DATE, ?, ?, ?, ?, ?, ?, ?)
                        """,
                    (
                        random.choice(("abc")),  # form
                        random.randint(0, 100),  # progress
                        random.randint(0, 20),  # lv1
                        random.randint(0, 20),  # lv2
                        random.randint(0, 20),  # lv3
                        random.randint(0, 20),  # lv4
                        random.randint(0, 20),  # lv5
                    ),
                )
                ### DEBUG

        return self._user[name]


# no need to manually close connections
# rely on Python's garbage collector
