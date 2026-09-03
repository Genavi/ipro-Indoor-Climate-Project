import json
import logging

import requests

from .config import GEMINI_API_KEY, GEMINI_MODELS

logger = logging.getLogger(__name__)

GEMINI_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
)

PROMPT_TEMPLATE = (
    "You are an indoor climate advisor. Analyze the following MeteoSwiss "
    "forecast history/lookahead and indoor sensor readings for station "
    "'{station}' on {date}.\n\n"
    "Data:\n{payload}\n\n"
    "Task:\n"
    "1. Summarize the short-term prediction per parameter (temperature, "
    "wind_speed, wind_direction, precipitation, sunshine, radiation) as a "
    "list of entries, one per parameter: trend, min/max and when they occur.\n"
    "2. Identify any notable weather events today based on the data alone "
    "(e.g. heavy rain >2.5 mm/h, wind gusts >50 km/h, frost <0°C, strong "
    "sunshine). Do not invent events that aren't supported by the data.\n"
    "3. Give 2-5 short, actionable indoor climate tips (ventilation, window "
    "closing, sun protection) tied to specific times/values from the data. "
    "If indoor_readings is empty, give general outdoor-based tips only."
)

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "predictions": {
            "type": "ARRAY",
            "description": "One entry per forecast parameter (e.g. temperature, wind_speed).",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "parameter": {"type": "STRING"},
                    "trend": {"type": "STRING"},
                    "min": {"type": "NUMBER"},
                    "max": {"type": "NUMBER"},
                    "notable": {"type": "STRING"},
                },
                "required": ["parameter", "trend", "min", "max", "notable"],
            },
        },
        "weather_events": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "type": {"type": "STRING"},
                    "severity": {"type": "STRING"},
                    "description": {"type": "STRING"},
                },
                "required": ["type", "severity", "description"],
            },
        },
        "tips": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
    },
    "required": ["predictions", "weather_events", "tips"],
}


class AgentClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY must be set")

    def ask(self, payload: dict) -> dict:
        prompt = PROMPT_TEMPLATE.format(
            station=payload.get("station"),
            date=payload.get("date"),
            payload=json.dumps(payload),
        )
        request_body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": RESPONSE_SCHEMA,
            },
        }
        headers = {"Content-Type": "application/json"}

        for model in GEMINI_MODELS:
            model = model.strip()
            url = GEMINI_URL_TEMPLATE.format(model=model, key=GEMINI_API_KEY)
            logger.info(f"Calling Gemini ({model})...")
            try:
                response = requests.post(url, json=request_body, headers=headers, timeout=30)
            except requests.RequestException as e:
                logger.warning(f"Connection error calling Gemini ({model}): {e}")
                continue

            if response.status_code == 200:
                return self._parse_response(response.json())
            elif response.status_code in (429, 503):
                logger.warning(
                    f"Gemini ({model}) temporarily unavailable "
                    f"(status {response.status_code}), trying next model"
                )
                continue
            else:
                logger.error(f"Gemini ({model}) HTTP error {response.status_code}: {response.text}")

        raise RuntimeError("All Gemini models failed or hit rate limits")

    @staticmethod
    def _parse_response(response_json: dict) -> dict:
        raw_text = response_json["candidates"][0]["content"]["parts"][0]["text"]

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            logger.warning("Gemini response was not valid JSON, storing raw text only")
            return {
                "predictions": None,
                "weather_events": None,
                "tips": None,
                "raw": raw_text,
            }
