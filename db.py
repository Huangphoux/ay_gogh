from apswutils import Database
from passlib.context import CryptContext
import csv

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
            ("DEBUG", pwd_context.hash("DEBUG")),
        )
        ### DEBUG

        # Tables for storing NGSLT form a, b, c
        for form in "abc":
            self.app.execute(f"""
                    CREATE TABLE IF NOT EXISTS form_{form} (
                        number INT NOT NULL PRIMARY KEY,
                        lemma TEXT NOT NULL,
                        question TEXT NOT NULL,
                        a TEXT NOT NULL,
                        b TEXT NOT NULL,
                        c TEXT NOT NULL,
                        d TEXT NOT NULL,
                        answer TEXT NOT NULL
                    )
            """)

            with open(f"test/ngslt_{form}.csv", "r") as f:
                dr = csv.DictReader(f, delimiter="\t")
                to_db = [
                    (
                        int(i["number"]),
                        i["lemma"],
                        i["question"],
                        i["a"],
                        i["b"],
                        i["c"],
                        i["d"],
                        i["answer"],
                    )
                    for i in dr
                ]

            for row in to_db:
                self.app.execute(
                    f"""
                        INSERT OR REPLACE INTO form_{form} (number, lemma, question, a, b, c, d, answer)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row,
                )

    def get(self, name: str = "app") -> Database:  # db.app, db.name
        if name not in self._user:
            self._user[name] = Database(f"db/{name}.db", strict=True)

            self._user[name].execute("""
                    CREATE TABLE IF NOT EXISTS test (
                        day DATE PRIMARY KEY NOT NULL DEFAULT CURRENT_DATE,
                        form TEXT NOT NULL DEFAULT "a",
                        progress INTEGER NOT NULL DEFAULT 0,
                        lv1 INTEGER NOT NULL DEFAULT 0,
                        lv2 INTEGER NOT NULL DEFAULT 0,
                        lv3 INTEGER NOT NULL DEFAULT 0,
                        lv4 INTEGER NOT NULL DEFAULT 0,
                        lv5 INTEGER NOT NULL DEFAULT 0
                    )
            """)

        return self._user[name]

    def close(self, name: str = "app"):
        try:
            self._user[name].close()
            del self._user[name]
        except KeyError: 
            # Newly created then sign out immediately means no DB made yet
            # but bypassing that is okay tho
            pass
