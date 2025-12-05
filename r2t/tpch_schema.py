from .db import execute
from pathlib import Path

def main():
    ddl = Path("db/schema.sql").read_text(encoding="utf-8")
    execute(ddl)

if __name__ == "__main__":
    main()
