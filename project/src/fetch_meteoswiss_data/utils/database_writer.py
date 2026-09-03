import logging
from datetime import datetime
from typing import List, Dict
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from database.models import MeteoSwissForecast

logger = logging.getLogger(__name__)


class DatabaseWriter:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
    
    def insert_forecast_data(self, forecast_data: List[Dict], check_newer: bool = True):
        session = self.Session()
        inserted_count = 0
        skipped_count = 0
        
        try:
            for entry in forecast_data:
                if isinstance(entry['time'], str):
                    entry['time'] = datetime.fromisoformat(entry['time'])
                
                if check_newer:
                    stmt = select(func.max(MeteoSwissForecast.time)).where(
                        MeteoSwissForecast.parameter == entry['parameter'],
                        MeteoSwissForecast.station == entry['station']
                    )
                    latest_time = session.execute(stmt).scalar()
                    
                    if latest_time and entry['time'] <= latest_time:
                        logger.debug(f"Skipping {entry['parameter']}: existing data is newer or equal")
                        skipped_count += 1
                        continue
                
                stmt = insert(MeteoSwissForecast).values(**entry)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['time', 'parameter', 'station'],
                    set_={
                        'value': stmt.excluded.value,
                        'fetch_runtime': stmt.excluded.fetch_runtime,
                        'abbreviation': stmt.excluded.abbreviation,
                        'point_id': stmt.excluded.point_id,
                        'point_type_id': stmt.excluded.point_type_id,
                        'unit': stmt.excluded.unit,
                    }
                )
                session.execute(stmt)
                inserted_count += 1
            
            session.commit()
            logger.info(f"Database write complete: {inserted_count} inserted/updated, {skipped_count} skipped")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Database write failed: {e}")
            raise
        finally:
            session.close()
