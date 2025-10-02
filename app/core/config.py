import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database path; default to ./data/app.db inside project root
DB_PATH_ENV = os.getenv("DB_PATH", "./data/app.db")

# Resolve to absolute path and ensure parent directory exists
DB_PATH = Path(DB_PATH_ENV).expanduser().resolve()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Build SQLite URL
SQLITE_URL = f"sqlite:///{DB_PATH}"


