from pydantic import BaseModel, Field, model_validator, ValidationInfo
from typing import List, Optional, Annotated

from datetime import datetime, timedelta


class PredictionRequest(BaseModel):
    datetime: Annotated[datetime, Field(..., example="2024-01-01T12:00:00", description="Prediction datetime")]
    kwp: float = Field(..., example=5.0, description="Installed capacity in kW")
    latitude: float = Field(..., example=51.5074, description="Latitude")
    longitude: float = Field(..., example=-0.1278, description="Longitude")
    azimuth: float = Field(..., example=180.0, description="Azimuth angle in degrees")
    tilt: float = Field(..., example=30.0, description="Tilt angle in degrees")
    kwh_price: Optional[float] = Field(None, example=0.15, description="Price per kWh in selected currency")


class PredictionResponse(BaseModel):
    datetime: Annotated[datetime, Field(..., example="2024-01-01T12:00:00", description="Prediction datetime")]
    prediction: float = Field(..., example=4.7, description="Predicted output in kW")
    co2_saved: Optional[float] = Field(None, example=0.5, description="CO2 saved in kg")
    money_saved: Optional[float] = Field(None, example=0.5, description="Money saved in selected currency")


class BatchPredictionRequest(BaseModel):
    entries: List[PredictionRequest]


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]


class TimeSeriesPredictionRequest(BaseModel):
    start: Annotated[datetime, Field(..., example="2024-01-01T12:00:00", description="Start datetime")]
    end: Annotated[datetime, Field(..., example="2024-01-01T12:00:00", description="End datetime")]
    kwp: float = Field(..., example=5.0, description="Installed capacity in kW")
    latitude: float = Field(..., example=51.5074, description="Latitude")
    longitude: float = Field(..., example=-0.1278, description="Longitude")
    tilt: Optional[float] = Field(None, example=30.0, description="Tilt angle in degrees")
    azimuth: Optional[float] = Field(None, example=180.0, description="Azimuth angle in degrees")
    kwh_price: Optional[float] = Field(None, example=0.15, description="Price per kWh in selected currency")
    
    @model_validator(mode="after")
    def check_date_constraints(cls, m):
        # ensure end >= start
        if m.end < m.start:
            raise ValueError("`end` must be the same or after `start`")

        span = m.end - m.start

        # no more than 30 days
        if span > timedelta(days=30):
            raise ValueError("Date range must be within 30 days")

        # date cant be more than 16 days in advance
        max_ahead = datetime.now() + timedelta(days=16)
        if m.start > max_ahead or m.end > max_ahead:
            raise ValueError("Forecast dates must not be more than 16 days in advance")

        return m


class FeatureInput(BaseModel):
    kwp: float = Field(..., example=5.0, description="Installed capacity in kW")
    relative_humidity_2m: float = Field(..., example=65.3, description="%")
    dew_point_2m: float = Field(..., example=12.5, description="°C")
    pressure_msl: float = Field(..., example=1012.3, description="hPa")
    precipitation: float = Field(..., example=0.4, description="mm")
    wind_speed_10m: float = Field(..., example=3.2, description="km/h")
    wind_direction_10m: float = Field(..., example=180.0, description="degrees")
    day_of_year: float = Field(..., example=120, description="Day number in the year")
    solar_zenith: float = Field(..., example=45.7, description="degrees")
    solar_azimuth: float = Field(..., example=150.4, description="degrees")
    poa: float = Field(..., example=800.5, description="W/m² (Plane of Array irradiance)")
    clearsky_index: float = Field(..., example=0.8, description="0-2 range")
    cloud_cover_3_moving_average: float = Field(..., example=0.5, description="0-100 range")
    hour_sin: float = Field(..., example=0.866, description="Encoded hour cyclically")
    hour_cos: float = Field(..., example=0.5, description="Encoded hour cyclically")
    day_of_year_sin: float = Field(..., example=0.75, description="Encoded day of year cyclically")
    month_cos: float = Field(..., example=0.4, description="Encoded month cyclically")
    cell_temp: float = Field(..., example=35.0, description="Cell temperature in °C")
    physical_model_prediction: float = Field(..., example=4.7, description="Physical model prediction in kW")


class PredictionClientRequest(BaseModel):
    features: FeatureInput
    datetime: Annotated[datetime, Field(..., example="2024-01-01T12:00:00", description="Prediction datetime")]


class PredictionClientResponse(BaseModel):
    prediction: float
    datetime: Annotated[datetime, Field(..., example="2024-01-01T12:00:00", description="Prediction datetime")]


class BatchPredictionClientRequest(BaseModel):
    entries: List[PredictionClientRequest]


class BatchPredictionClientResponse(BaseModel):
    predictions: List[PredictionClientResponse]
