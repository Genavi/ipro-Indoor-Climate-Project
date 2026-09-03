import os
import sys
import logging
import signal
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from utils.config import STATION_NAME, STATION_ABBR, STATION_POI_ID, STATION_POI_TYPE_ID, DEFAULT_PARAMS
from utils.fetcher import get_latest_forecast_values
from utils.formatter import format_for_timescaledb
from utils.database_writer import DatabaseWriter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST', 'postgres')}:5432/{os.getenv('DATABASE_NAME')}"

db_writer = DatabaseWriter(DATABASE_URL)

station = {
    "name": STATION_NAME,
    "abbreviation": STATION_ABBR,
    "point_id": STATION_POI_ID,
    "point_type_id": STATION_POI_TYPE_ID
}

params = {
    "temperature": DEFAULT_PARAMS["temperature_2m_hourly_mean"],
    "wind_speed": DEFAULT_PARAMS["wind_speed_scalar_hourly_mean_kmh"],
    "wind_direction": DEFAULT_PARAMS["wind_direction_hourly_mean"],
    "precipitation": DEFAULT_PARAMS["precipitation_hourly_total"],
    "sunshine": DEFAULT_PARAMS["sunshine_duration_hourly_total"],
    "radiation": DEFAULT_PARAMS["global_radiation_hourly_mean"],
}


def fetch_and_store():
    try:
        logger.info("=" * 70)
        logger.info(f"Starting MeteoSwiss data fetch at {datetime.now()}")
        logger.info(f"Station: {STATION_NAME} ({STATION_ABBR})")
        logger.info("=" * 70)
        
        results = get_latest_forecast_values(
            params,
            poi_id=STATION_POI_ID,
            poi_type_id=STATION_POI_TYPE_ID,
            return_full_series=False
        )
        
        logger.info(f"Data fetched from run: {results['run_time']}")
        logger.info(f"Run timestamp: {results['run_datetime'].strftime('%Y-%m-%d %H:%M %Z')}")
        
        timescaledb_data = format_for_timescaledb(
            results["values"], 
            station, 
            results['run_datetime'].isoformat()
        )
        
        db_writer.insert_forecast_data(timescaledb_data, check_newer=True)
        
        logger.info("Fetch cycle completed successfully\n")
        
    except Exception as e:
        logger.error(f"Fetch cycle failed: {e}", exc_info=True)


def main():
    logger.info("=" * 70)
    logger.info("MeteoSwiss Data Fetcher - Scheduler Starting")
    logger.info("=" * 70)
    logger.info(f"Database: {os.getenv('DATABASE_HOST', 'postgres')}:{os.getenv('DATABASE_NAME')}")
    logger.info(f"Station: {STATION_NAME} ({STATION_ABBR})")
    logger.info(f"Schedule: Every hour at minute 15")
    logger.info("=" * 70 + "\n")
    
    logger.info("Running initial fetch...")
    fetch_and_store()
    
    scheduler = BlockingScheduler()
    scheduler.add_job(
        fetch_and_store,
        CronTrigger(minute=15),
        id='meteoswiss_fetcher',
        name='Fetch MeteoSwiss forecast data',
        replace_existing=True
    )
    
    def shutdown_handler(signum, frame):
        logger.info("Shutdown signal received, stopping scheduler...")
        scheduler.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    logger.info("Scheduler started. Waiting for next scheduled run...\n")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    main()
