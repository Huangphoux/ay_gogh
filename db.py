from apswutils import Database
import os


class DatabaseDict:
    def __init__(self, db_dir: str = "data"):
        self._db_dir = db_dir
        os.makedirs(self._db_dir, exist_ok=True)
        self._dbs: dict[str, Database] = {
            "app": Database(
                os.path.join(self._db_dir, "app.db"),
                strict=True,
            )
        }

        self._dbs["app"].execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    pwd TEXT NOT NULL
                )
            """)

        # https://sqlite.org/autoinc.html

    def get(self, name: str = "app") -> Database:
        if name not in self._dbs:
            self._dbs[name] = Database(
                os.path.join(self._db_dir, f"{name}.db"),
                strict=True,
            )

        return self._dbs[name]

    def close(self, name: str = "app") -> None:
        self._dbs[name].close()
