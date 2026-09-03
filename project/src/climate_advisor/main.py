import sys
import logging
from datetime import datetime, timezone

from utils.config import STATION_NAME, GEMINI_MODELS
from utils.agent_client import AgentClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info(
        "\n" + "=" * 70 + "\n" +
        " " * 25 + "Climate Advisor" + "\n" +
        "-" * 70 + "\n" +
        f"Station: {STATION_NAME}\n" +
        f"Gemini models: {', '.join(GEMINI_MODELS)}\n" +
        "=" * 70 + "\n")

    try:
        agent_client = AgentClient()

        logger.info("Collecting forecast history and indoor readings...")
        now = datetime.now(timezone.utc)
        payload = {
            "date": now.date().isoformat(),
            "station": STATION_NAME,
            "forecast_history": [],
            "indoor_readings": [],
        }

        logger.info(f"Forecast rows: {len(payload['forecast_history'])}")
        logger.info(f"Indoor readings: {len(payload['indoor_readings'])}")

        logger.info("Asking Gemini for predictions/events/tips...")
        response = agent_client.ask(payload)

        logger.info("Agent response:")
        logger.info("-" * 50)
        logger.info(f"Predictions: {response.get('predictions')}")
        logger.info(f"Weather events: {response.get('weather_events')}")
        logger.info(f"Tips: {response.get('tips')}")

    except Exception as e:
        logger.error(f"Error generating climate advice: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
