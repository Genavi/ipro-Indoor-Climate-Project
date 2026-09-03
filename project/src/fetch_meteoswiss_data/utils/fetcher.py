import httpx
import pandas as pd
import logging
from datetime import datetime
from io import StringIO
from typing import Dict, Optional
from zoneinfo import ZoneInfo

from .config import STAC_BASE_URL, COLLECTION_ID, LOCAL_TZ

logger = logging.getLogger(__name__)

def fetch_today_stac_item() -> Dict:
    today_id = f"{datetime.now(LOCAL_TZ).strftime('%Y%m%d')}-ch"
    item_url = f"{STAC_BASE_URL}/collections/{COLLECTION_ID}/items/{today_id}"
    
    response = httpx.get(item_url, follow_redirects=True, timeout=30)
    response.raise_for_status()
    
    return response.json()


def get_latest_run_time(stac_item: Optional[Dict] = None) -> str:
    if stac_item is None:
        stac_item = fetch_today_stac_item()
    
    assets = stac_item["assets"]
    
    all_runs = sorted({key.split(".")[2] for key in assets})
    
    if not all_runs:
        raise ValueError("No forecast runs found in STAC item")
    
    return all_runs[-1]


def get_parameter_urls( params: Dict[str, str], latest_run: str, stac_item: Optional[Dict] = None) -> Dict[str, str]:
    if stac_item is None:
        stac_item = fetch_today_stac_item()
    
    assets = stac_item["assets"]
    param_urls = {}
    
    for name, param_id in params.items():
        for key, asset in assets.items():
            if latest_run in key and param_id in key:
                param_urls[name] = asset["href"]
                break
    
    return param_urls


def parse_parameter_csv(csv_content: bytes, param_id: str, poi_id: str, poi_type_id: str) -> pd.DataFrame:
    
    df = pd.read_csv(StringIO(csv_content.decode("latin-1")), sep=";")
    df_poi = df[
        (df["point_id"].astype(str) == poi_id) &
        (df["point_type_id"].astype(str) == poi_type_id)
    ]
    
    if df_poi.empty:
        raise ValueError(f"No data found for POI {poi_id}/{poi_type_id}")
    
    time_col = next(c for c in df_poi.columns if c.lower() in ("date", "time"))
    df_poi = df_poi.copy()
    df_poi[time_col] = (
        pd.to_datetime(df_poi[time_col].astype(int).astype(str), format="%Y%m%d%H%M", utc=True)
        .dt.tz_convert(LOCAL_TZ)
    )
    
    df_poi = df_poi.set_index(time_col)
    df_poi[param_id] = pd.to_numeric(df_poi[param_id], errors="coerce")
    
    return df_poi


def get_latest_forecast_values(params: Dict[str, str], poi_id: str, poi_type_id: str, return_full_series: bool = False) -> Dict:
    stac_item = fetch_today_stac_item()
    latest_run = get_latest_run_time(stac_item)
    
    run_datetime = (
        datetime.strptime(latest_run, "%Y%m%d%H%M")
        .replace(tzinfo=ZoneInfo("UTC"))
        .astimezone(LOCAL_TZ)
    )
    
    param_urls = get_parameter_urls(params, latest_run, stac_item)
    
    result = {
        "run_time": latest_run,
        "run_datetime": run_datetime,
        "values": {}
    }
    
    with httpx.Client(timeout=30.0) as client:
        for name, url in param_urls.items():
            param_id = params[name]
            
            resp = client.get(url)
            resp.raise_for_status()
            
            df = parse_parameter_csv(resp.content, param_id, poi_id, poi_type_id)
            
            now = datetime.now(LOCAL_TZ)
            time_diffs = abs(df.index - now)
            closest_idx = time_diffs.argmin()
            
            result["values"][name] = {
                "latest_value": df.iloc[closest_idx][param_id],
                "latest_time": df.index[closest_idx],
                "param_id": param_id
            }
            
            if return_full_series:
                result["values"][name]["series"] = df
    
    return result
