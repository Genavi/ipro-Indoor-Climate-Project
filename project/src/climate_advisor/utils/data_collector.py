import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from database.models import MeteoSwissForecast, SensorReading
from .config import (
    FORECAST_HISTORY_HOURS,
    FORECAST_LOOKAHEAD_HOURS,
    INDOOR_HISTORY_HOURS,
)

logger = logging.getLogger(__name__)

INDOOR_BUCKET_MINUTES = 15


class DataCollector:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def get_forecast_history(self, station: str) -> list[dict]:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(hours=FORECAST_HISTORY_HOURS)
        window_end = now + timedelta(hours=FORECAST_LOOKAHEAD_HOURS)

        session = self.Session()
        try:
            stmt = (
                select(MeteoSwissForecast)
                .where(
                    MeteoSwissForecast.station == station,
                    MeteoSwissForecast.time >= window_start,
                    MeteoSwissForecast.time <= window_end,
                )
                .order_by(MeteoSwissForecast.time)
            )
            rows = session.execute(stmt).scalars().all()
            return [
                {
                    "time": row.time.isoformat(),
                    "parameter": row.parameter,
                    "value": row.value,
                    "unit": row.unit,
                }
                for row in rows
            ]
        finally:
            session.close()

    def get_indoor_readings(self) -> list[dict]:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(hours=INDOOR_HISTORY_HOURS)

        session = self.Session()
        try:
            stmt = (
                select(SensorReading)
                .where(SensorReading.time >= window_start)
                .order_by(SensorReading.time)
            )
            rows = session.execute(stmt).scalars().all()

            buckets: dict[tuple, dict] = {}
            bucket_seconds = INDOOR_BUCKET_MINUTES * 60
            for row in rows:
                bucket_epoch = int(row.time.timestamp() // bucket_seconds) * bucket_seconds
                bucket_time = datetime.fromtimestamp(bucket_epoch, tz=timezone.utc)
                key = (bucket_time, row.sensor_type, row.location, row.unit)
                agg = buckets.setdefault(
                    key,
                    {"sum": 0.0, "count": 0, "min": row.value, "max": row.value},
                )
                agg["sum"] += row.value
                agg["count"] += 1
                agg["min"] = min(agg["min"], row.value)
                agg["max"] = max(agg["max"], row.value)

            result = [
                {
                    "time": bucket_time.isoformat(),
                    "sensor_type": sensor_type,
                    "location": location,
                    "unit": unit,
                    "avg": round(agg["sum"] / agg["count"], 2),
                    "min": agg["min"],
                    "max": agg["max"],
                    "samples": agg["count"],
                }
                for (bucket_time, sensor_type, location, unit), agg in sorted(buckets.items())
            ]
            logger.info(
                f"Aggregated {len(rows)} raw indoor readings into "
                f"{len(result)} {INDOOR_BUCKET_MINUTES}-min buckets"
            )
            return result
        finally:
            session.close()

    def build_payload(self, station: str) -> dict:
        now = datetime.now(timezone.utc)
        forecast_history = self.get_forecast_history(station)
        indoor_readings = self.get_indoor_readings()

        logger.info(
            f"Collected {len(forecast_history)} forecast rows, "
            f"{len(indoor_readings)} indoor readings for station '{station}'"
        )

        return {
            "date": now.date().isoformat(),
            "station": station,
            "forecast_history": forecast_history,
            "indoor_readings": indoor_readings,
        }
