import os
from dotenv import load_dotenv

load_dotenv()

STATION_NAME = os.getenv("STATION_NAME", "Buchs / Aarau")

FORECAST_HISTORY_HOURS = int(os.getenv("FORECAST_HISTORY_HOURS", "48"))
FORECAST_LOOKAHEAD_HOURS = int(os.getenv("FORECAST_LOOKAHEAD_HOURS", "24"))
INDOOR_HISTORY_HOURS = int(os.getenv("INDOOR_HISTORY_HOURS", "24"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODELS = os.getenv("GEMINI_MODELS", "gemini-2.5-flash,gemini-2.0-flash").split(",")
