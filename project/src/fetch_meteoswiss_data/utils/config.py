from zoneinfo import ZoneInfo

STAC_BASE_URL = "https://data.geo.admin.ch/api/stac/v1"
COLLECTION_ID = "ch.meteoschweiz.ogd-local-forecasting"
LOCAL_TZ = ZoneInfo("Europe/Zurich")
STATION_POI_ID = "67"
STATION_POI_TYPE_ID = "1"
STATION_NAME = "Buchs / Aarau"
STATION_ABBR = "BUS"
DEFAULT_PARAMS = {
    "wind_direction_hourly_mean": "dkl010h0",
    "wind_speed_scalar_hourly_mean_kmh": "fu3010h0",
    "wind_gust_peak_hourly_maximum_kmh": "fu3010h1",
    "wind_speed_hourly_mean_10%_quantile_kmh": "fu3q10h0",
    "wind_speed_gust_peak_hourly_maximum_10%_quantile_kmh": "fu3q10h1",
    "wind_speed_hourly_mean_90%_quantile_kmh": "fu3q90h0",
    "wind_speed_gust_peak_hourly_maximum_90%_quantile_kmh": "fu3q90h1",
    "global_radiation_hourly_mean": "gre000h0",
    "diffuse_radiation_hourly_mean": "ods000h0",
    "graphics_meteoswiss_icon": "jww003i0",
    "clouds_high_cloud_cover": "nprohihs",
    "clouds_low_cloud_cover": "nprolohs",
    "clouds_medium_cloud_cover": "npromths",
    "precipitation_probability_3h": "rp0003i0",
    "precipitation_total_3h": "rre003i0",
    "precipitation_hourly_total": "rre150h0",
    "precipitation_hourly_total_10%_quantile": "rreq10h0",
    "precipitation_hourly_total_90%_quantile": "rreq90h0",
    "sunshine_duration_hourly_total": "sre000h0",
    "temperature_2m_hourly_mean": "tre200h0",
    "temperature_2m_hourly_mean_10%_quantile": "treq10h0",
    "temperature_2m_hourly_mean_90%_quantile": "treq90h0",
    "zero_degree_level_hourly_forecast": "zprfr0hs",
}
