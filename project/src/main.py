import sys
import os
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv

from src.utils.serial_reader import start_reading

def run_migrations():
    print("Checking for database updates...")
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Success: Database is at the latest version.")
    except Exception as e:
        print(f"Error: Migration failed: {e}")
        sys.exit(1)

def main():
    load_dotenv()
    run_migrations()
    start_reading(os.getenv("SERIAL_PORT"), os.getenv("BAUDRATE"))

if __name__ == "__main__":
    main()
