import os


save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chapter")


def fix_spelling(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        content = f.read()

    dict = {
        "to-day": "today",
        "To-day": "Today",
        "to-morrow": "tomorrow",
        "To-morrow": "Tomorrow",
        "to-night": "tonight",
        "To-night": "Tonight",
    }

    for k, v in dict.items():
        content = content.replace(k, v)
        content = content.replace(k.title(), v.title())

    with open(fname, mode="w", encoding="utf-8") as f:
        f.write(content)
