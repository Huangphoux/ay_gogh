from apswutils import Database
from passlib.context import CryptContext
import csv
import frontmatter
from random import choice

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class DatabaseDict:
    def __init__(self):
        self._user: dict[str, Database] = {}  # store connections
        # python wouldn't know where to find and reuse connections

        import os

        os.makedirs("db", exist_ok=True)
        self.app: Database = Database(f"db/app.db", strict=True)

        self.app.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    pwd TEXT NOT NULL
                )
        """)  # NOT NULL, UNIQUE, CHECK

        ### DEBUG
        self.app.execute(
            "INSERT OR IGNORE INTO user (name, pwd) VALUES (?, ?)",
            ("DEBUG", pwd_context.hash("DEBUG")),
        )
        ### DEBUG

        # Tables for storing NGSLT form a, b, c
        for form in "abc":
            self.app.execute(f"""
                    CREATE TABLE IF NOT EXISTS form_{form} (
                        number INTEGER PRIMARY KEY,
                        lemma TEXT,
                        question TEXT,
                        a TEXT,
                        b TEXT,
                        c TEXT,
                        d TEXT,
                        answer TEXT
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
                        INSERT OR IGNORE INTO form_{form} (number, lemma, question, a, b, c, d, answer)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row,
                )

            # Table for storing chapters
            self.app.execute(f"""
                    CREATE TABLE IF NOT EXISTS chapter (
                        number INTEGER PRIMARY KEY,
                        number_word TEXT,
                        cardinal TEXT,
                        cardinal_word TEXT,
                        title TEXT,
                        content TEXT
                    )
            """)

            for i in range(1, 60 + 1):
                with open(f"read/chapter/{i}.md", "r") as f:
                    meta, content = frontmatter.parse(f.read())

                    self.app.execute(
                        f"""
                            INSERT OR IGNORE INTO chapter
                            (number, number_word, cardinal, cardinal_word, title, content)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            meta["number"],
                            meta["number_word"],
                            meta["cardinal_number"],
                            meta["cardinal_word"],
                            meta["title"],
                            content,
                        ),
                    )

    def get(self, name: str = "app") -> Database:
        if name not in self._user:
            self._user[name] = Database(f"db/{name}.db", strict=True)

            self._user[name].execute("""
                    CREATE TABLE IF NOT EXISTS test (
                        number INTEGER PRIMARY KEY,
                        day TEXT NOT NULL,
                        form TEXT NOT NULL,
                        progress INTEGER NOT NULL,
                        lv1 INTEGER NOT NULL,
                        lv2 INTEGER NOT NULL,
                        lv3 INTEGER NOT NULL,
                        lv4 INTEGER NOT NULL,
                        lv5 INTEGER NOT NULL
                    )
            """)

            self._user[name].execute("""
                    CREATE TABLE IF NOT EXISTS chapter (
                        number INTEGER PRIMARY KEY,
                        done INTEGER CHECK (done = 1)
                    )
            """)

            self._user[name].execute("""
                    CREATE TABLE IF NOT EXISTS deck (
                        id INTEGER PRIMARY KEY,
                        front TEXT NOT NULL UNIQUE,
                        back TEXT NOT NULL,
                        state INTEGER NOT NULL,
                        step INTEGER,
                        stability REAL,
                        difficulty REAL,
                        due TEXT NOT NULL, -- new cards due upon creation
                        last_review TEXT
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

    def close_all(self):
        self.app.close()

        for name in self._user:
            self._user[name].close()
            del self._user[name]
