import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_password = None
if os.path.exists('/run/secrets/database_password'):
    with open('/run/secrets/database_password', 'r') as f:
        db_password = f.read().strip()
else:
    db_password = os.getenv('DATABASE_PASSWORD')

DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{db_password}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
