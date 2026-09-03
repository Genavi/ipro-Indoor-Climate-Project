import sys
import logging

from utils.config import STAC_BASE_URL, COLLECTION_ID, DEFAULT_PARAMS, STATION_NAME, STATION_ABBR, STATION_POI_ID, STATION_POI_TYPE_ID
from utils.fetcher import get_latest_forecast_values

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

def main():
    logger.info("=" * 70)
    logger.info(" " * 25 +"MeteoSwiss Data Fetcher")
    logger.info("-" * 70)
    logger.info("URL: {}/{}".format(STAC_BASE_URL, COLLECTION_ID))
    logger.info("Station: {} ({})".format(STATION_NAME, STATION_ABBR))
    logger.info("Point ID: {} (Type {})".format(STATION_POI_ID, STATION_POI_TYPE_ID))
    logger.info("=" * 70)

    try:
        logger.info("Fetching latest forecast values for today from MeteoSwiss...")
        logger.info("Parameters: {}".format(params).replace("{", "{\n ").replace(",", ",\n").replace("}", "\n}"))

        results = get_latest_forecast_values(
            params,
            poi_id=STATION_POI_ID,
            poi_type_id=STATION_POI_TYPE_ID,
            return_full_series=False
        )

        logger.info("Current outdoor conditions:")
        logger.info("-" * 50)

        for param, details in results["values"].items():
            logger.info(f"{param}: {details.get('latest_value')} at {details.get('latest_time')}")

    except Exception as e:
        logger.error(f"Error fetching forecast values: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


        