from pathlib import Path
from apswutils import Database
import os


class DatabaseDict:
    def __init__(self, db_dir: Path = Path("db")):
        self._db_dir = db_dir
        os.makedirs(self._db_dir, exist_ok=True)

        self._dbs: dict[str, Database] = {
            "app": Database(
                os.path.join(self._db_dir, "app.db"),
                strict=True,
            )
        }

        self._dbs["app"].execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    pwd TEXT NOT NULL
                )
            """)

        # https://sqlite.org/autoinc.html

    def get(self, name: str = "app") -> Database:
        if name not in self._dbs:
            self.init_user_db(name)

        return self._dbs[name]

    def close(self, name: str = "app") -> None:
        self._dbs[name].close()

    def init_user_db(self, name: str = "app"):
        self._dbs[name] = Database(
            os.path.join(self._db_dir, f"{name}.db"),
            strict=True,
        )

        self._dbs[name].execute("""
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
        import random

        self._dbs[name].execute(
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
