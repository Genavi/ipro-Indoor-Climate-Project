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

def save_to_database(sensor_type, value, unit, reader=1, location=1, topic=None):
    db = SessionLocal()
    try:
        reading = SensorReading(
            time=datetime.now(timezone.utc),
            reader=reader,
            location=location,
            sensor_type=sensor_type,
            value=value,
            unit=unit,
            topic=topic
        )
        db.add(reading)
        db.commit()
        logger.info(f"Inserted sensor data: {sensor_type}={value}{unit}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting data into the database: {e}")
    finally:
        db.close()

def save_multiple_readings(readings):
    db = SessionLocal()
    try:
        timestamp = datetime.now(timezone.utc)
        for data in readings:
            reading = SensorReading(
                time=timestamp,
                reader=data.get('reader', 1),
                location=data.get('location', 1),
                sensor_type=data['sensor_type'],
                value=data['value'],
                unit=data['unit'],
                topic=data.get('topic')
            )
            db.add(reading)
        db.commit()
        logger.info(f"Inserted {len(readings)} sensor readings at {timestamp}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting batch data into the database: {e}")
    finally:
        db.close()
