import logging
from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from database.models import ClimateAdvice

logger = logging.getLogger(__name__)


class DatabaseWriter:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def save_advice(self, station: str, agent_response: dict, raw_response: str = None):
        session = self.Session()
        try:
            entry = {
                "time": datetime.now(timezone.utc),
                "station": station,
                "predictions": agent_response.get("predictions"),
                "weather_events": agent_response.get("weather_events"),
                "tips": agent_response.get("tips"),
                "raw_response": raw_response,
            }
            stmt = insert(ClimateAdvice).values(**entry)
            stmt = stmt.on_conflict_do_update(
                index_elements=['time', 'station'],
                set_={
                    'predictions': stmt.excluded.predictions,
                    'weather_events': stmt.excluded.weather_events,
                    'tips': stmt.excluded.tips,
                    'raw_response': stmt.excluded.raw_response,
                }
            )
            session.execute(stmt)
            session.commit()
            logger.info(f"Saved climate advice for station '{station}'")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save climate advice: {e}")
            raise
        finally:
            session.close()
