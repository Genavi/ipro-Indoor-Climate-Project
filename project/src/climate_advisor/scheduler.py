import os
import sys
import logging
import signal

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from utils.config import STATION_NAME
from utils.data_collector import DataCollector
from utils.agent_client import AgentClient
from utils.database_writer import DatabaseWriter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST', 'postgres')}:5432/{os.getenv('DATABASE_NAME')}"

collector = DataCollector(DATABASE_URL)
agent_client = AgentClient()
db_writer = DatabaseWriter(DATABASE_URL)


def generate_advice():
    try:
        logger.info("=" * 70)
        logger.info("Generating climate advice")
        logger.info("=" * 70)

        payload = collector.build_payload(STATION_NAME)
        response = agent_client.ask(payload)
        db_writer.save_advice(STATION_NAME, response, raw_response=str(response))

        logger.info("Climate advice generation complete")
    except Exception as e:
        logger.error(f"Climate advice generation failed: {e}", exc_info=True)


def main():
    scheduler = BlockingScheduler()

    scheduler.add_job(generate_advice, CronTrigger(hour="6,18", minute=15))

    def shutdown(signum, frame):
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("Climate advisor scheduler started")
    generate_advice()
    scheduler.start()


if __name__ == "__main__":
    main()
