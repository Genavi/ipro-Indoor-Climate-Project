import sys
import logging

from alembic.config import Config
from alembic import command
from datetime import datetime, timezone

from src.database.connection import SessionLocal
from src.database.models import SensorReading

logger = logging.getLogger(__name__)

def run_migrations():
    logger.info("Checking for database updates...")
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Success: Database is at the latest version.")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)

def save_to_database(sensor_0_name, sensor_0_value, sensor_1_name=None, sensor_1_value=None,
                     sensor_2_name=None, sensor_2_value=None, sensor_3_name=None,
                     sensor_3_value=None, sensor_4_name=None, sensor_4_value=None):
    db = SessionLocal()
    try:
        reading = SensorReading(
            timestamp=datetime.now(timezone.utc),
            reader=1,
            location=1,
            sensor_0_name=sensor_0_name,
            sensor_0_value=sensor_0_value,
            sensor_1_name=sensor_1_name,
            sensor_1_value=sensor_1_value,
            sensor_2_name=sensor_2_name,
            sensor_2_value=sensor_2_value,
            sensor_3_name=sensor_3_name,
            sensor_3_value=sensor_3_value,
            sensor_4_name=sensor_4_name,
            sensor_4_value=sensor_4_value
        )
        db.add(reading)
        db.commit()
        print(f"[{reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Inserted: co2={sensor_0_value}, humidity={sensor_1_value if sensor_1_value is not None else 'N/A'}, temperature={sensor_2_value if sensor_2_value is not None else 'N/A'}, celcius={sensor_3_value if sensor_3_value is not None else 'N/A'}, fahrenheit={sensor_4_value if sensor_4_value is not None else 'N/A'}")
    except Exception as e:
        db.rollback()
        print(f"Error inserting data into the database: {e}")
    finally:
        db.close()
