from apswutils import Database
from passlib.context import CryptContext
import csv
import frontmatter
import os
from math import ceil
from load_env import is_debug, whose_test

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class DatabaseDict:
    def __init__(self):
        self.user: dict[str, Database] = {}  # store connections
        # python wouldn't know where to find and reuse connections

        os.makedirs("db", exist_ok=True)
        self.app: Database = Database(f"db/app.db", strict=True)
        # Tables for storing user login infos
        self.app.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    pwd TEXT NOT NULL
                )
        """)

        self.insert_forms()
        self.insert_chapters()
        self.insert_ngsl_words()

        self.seed_app() if is_debug else None

    def insert_forms(self):  # Tables for storing NGSLT form a, b, c

        for form in "abc":
            self.app.execute(f"""
                    CREATE TABLE IF NOT EXISTS form_{form} (
                        number INTEGER PRIMARY KEY,
                        lemma TEXT,
                        question TEXT,
                        \"1\" TEXT,
                        \"2\" TEXT,
                        \"3\" TEXT,
                        \"4\" TEXT,
                        answer INTEGER
                    )
            """)

            with open(f"test/ngslt_{form}.csv", "r") as f:
                dict_reader = csv.DictReader(f, delimiter="\t")
                to_db = [
                    (
                        int(row["number"]),
                        row["lemma"],
                        row["question"],
                        *(row[i] for i in "1234"),
                        row["answer"],
                    )
                    for row in dict_reader
                ]

            for row in to_db:
                self.app.execute(
                    f"""
                        INSERT OR IGNORE INTO form_{form}
                        (number, lemma, question, \"1\", \"2\", \"3\", \"4\", answer)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row,
                )

    def insert_chapters(self):  # Table for storing chapters
        self.app.execute(f"""
                CREATE TABLE IF NOT EXISTS chapter (
                    number INTEGER PRIMARY KEY,
                    number_word TEXT,
                    cardinal TEXT,
                    cardinal_word TEXT,
                    title TEXT,
                    content TEXT,
                    ngsl REAL
                )
        """)

        for i in range(1, 60 + 1):
            with open(f"read/chapter/{i}.md", "r") as f:
                meta, content = frontmatter.parse(f.read())

                self.app.execute(
                    f"""
                        INSERT OR IGNORE INTO chapter
                        (number, number_word, cardinal, cardinal_word, title, content, ngsl)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        meta["number"],
                        meta["number_word"],
                        meta["cardinal_number"],
                        meta["cardinal_word"],
                        meta["title"],
                        content,
                        meta["ngsl"],
                    ),
                )

    def insert_ngsl_words(self):  # Table for storing ngsl word level
        self.app.execute(
            f"""
                    CREATE TABLE IF NOT EXISTS ngsl (
                        number INTEGER PRIMARY KEY,
                        lemma TEXT UNIQUE,
                        level INTEGER
                    )
            """
        )

        with open(f"read/ngsl/NGSL_1.2_stats.csv", "r") as f:
            dict_reader = csv.DictReader(f, delimiter=",")
            for row in dict_reader:
                self.app.execute(
                    f"""
                        INSERT OR IGNORE INTO ngsl (lemma, level) VALUES (?, ?)
                    """,
                    (
                        row["Lemma"],
                        ceil(int(row["SFI Rank"]) / 562),
                    ),
                )

    def seed_app(self):
        self.app.execute(
            "INSERT OR IGNORE INTO user (name, pwd) VALUES (?, ?)",
            ("DEBUG", pwd_context.hash("DEBUG_DEBUG_DEBUG")),
        )

    def get(self, name: str = "app") -> Database:
        if name not in self.user:
            self.user[name] = Database(f"db/{name}.db", strict=True)
            # test
            self.user[name].execute(""" 
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
            # wordle
            self.user[name].execute(""" 
                    CREATE TABLE IF NOT EXISTS wordle (
                        number INTEGER PRIMARY KEY,
                        guess TEXT NOT NULL,
                        is_submitted INTEGER NOT NULL
                    )
            """)
            # chapter
            self.user[name].execute(""" 
                    CREATE TABLE IF NOT EXISTS chapter (
                        number INTEGER PRIMARY KEY,
                        progress INTEGER NOT NULL,
                        done TEXT
                    )
            """)
            for i in range(1, 60 + 1):
                self.user[name].execute(
                    "INSERT OR IGNORE INTO chapter (number, progress) VALUES (?, ?)",
                    (i, 1),
                )
            # deck
            self.user[name].execute(""" 
                    CREATE TABLE IF NOT EXISTS deck (
                        id INTEGER PRIMARY KEY,
                        front TEXT NOT NULL UNIQUE,
                        back TEXT NOT NULL,
                        state INTEGER NOT NULL,
                        step INTEGER,
                        stability REAL,
                        difficulty REAL,
                        due TEXT NOT NULL, -- new cards due upon creation
                        last_review TEXT,
                        is_retired INTEGER NOT NULL CHECK (is_retired = 1 OR is_retired = 0)
                    )
            """)
            # review_log
            self.user[name].execute("""
                    CREATE TABLE IF NOT EXISTS review_log (
                        id INTEGER PRIMARY KEY,
                        card_id INTEGER NOT NULL REFERENCES deck(id) ON DELETE CASCADE,
                        rating INTEGER NOT NULL,
                        review_datetime TEXT NOT NULL,
                        review_duration INTEGER
                    )
            """)
            # settings
            self.user[name].execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY,
                        setting TEXT UNIQUE NOT NULL,
                        value TEXT NOT NULL
                    )
            """)
            # desired_retention
            self.user[name].execute(
                "INSERT OR IGNORE INTO settings (setting, value) VALUES (?, ?)",
                ("desired_retention", 0.8),
            )
            # parameters
            self.user[name].execute(
                "INSERT OR IGNORE INTO settings (setting, value) VALUES (?, ?)",
                (
                    "parameters",  # defaults from https://github.com/open-spaced-repetition/py-fsrs#usage
                    "0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, \
                     0.001, 1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, \
                     1.6483, 0.6014, 1.8729, 0.5425, 0.0912, 0.0658, 0.1542",
                ),
            )
            # default settings
            self.user[name].execute(
                "INSERT OR IGNORE INTO settings (setting, value) VALUES (?, ?)",
                ("show_mark", "1"),
            )
            self.user[name].execute(
                "INSERT OR IGNORE INTO settings (setting, value) VALUES (?, ?)",
                ("show_aside", "1"),
            )

            self.seed_user(name) if is_debug else None

        return self.user[name] if name else self.app

    def seed_user(self, name: str):
        self.user[name].execute(
            """
                INSERT INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?)
            """,  # Trương Hoàng Phúc, (UTC) 2026-05-06 07:57:12
            ("c", 100, 20, 19, 20, 20, 20),
        ) if whose_test == "Phuc" else None

        self.user[name].execute(
            """
            INSERT INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
            VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?)
        """,  # Lê Minh Phát, (UTC) 2026-05-08 01:48:52
            ("c", 100, 18, 18, 20, 17, 16),
        ) if whose_test == "Phat" else None

        self.user[name].execute(
            """
                INSERT INTO test (day, form, progress, lv1, lv2, lv3, lv4, lv5)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?)
            """,  # Lý Hoàng Em, (UTC) 2026-06-04 11:27:17
            ("c", 100, 15, 13, 16, 12, 13),
        ) if whose_test == "HoangEm" else None

    def close(self, name: str = "app"):
        try:
            self.user[name].close()
            del self.user[name]
        except KeyError:
            # Newly created then sign out immediately means no DB made yet
            # but bypassing that is okay tho
            pass

    def close_all(self):
        self.app.close()

        for name in self.user:
            self.user[name].close()
            del self.user[name]
