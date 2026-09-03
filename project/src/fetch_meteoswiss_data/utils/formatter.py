from typing import Dict, List
from datetime import datetime

def get_unit_for_param(param: str) -> str:
    units = {
        "temperature": "°C",
        "wind_speed": "km/h",
        "wind_direction": "°",
        "precipitation": "mm",
        "sunshine": "min",
        "radiation": "W/m²"
    }
    return units.get(param, "")

def format_for_timescaledb(data: Dict[str, Dict[str, any]], station: Dict[str, any], runtime: str) -> List[Dict[str, any]]:
    if isinstance(runtime, str):
        runtime = datetime.fromisoformat(runtime)
    
    formatted_data = []
    
    for param, details in data.items():
        value = details.get("latest_value", None)
        if value is not None:
            value = float(value)
        
        formatted_entry = {
            "time": details.get("latest_time"),
            "parameter": param,
            "station": station.get("name"),
            "abbreviation": station.get("abbreviation"),
            "point_id": int(station.get("point_id")),
            "point_type_id": int(station.get("point_type_id")),
            "value": value,
            "unit": get_unit_for_param(param),
            "fetch_runtime": runtime
        }
        formatted_data.append(formatted_entry)
    
    return formatted_data
