import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from src.predict.schemas import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    TimeSeriesPredictionRequest,
    FeatureInput,
    PredictionClientRequest,
    PredictionClientResponse,
    BatchPredictionClientRequest,
    BatchPredictionClientResponse,
)


def test_prediction_request_valid_minimal():
    payload = {
        "datetime": "2025-01-01T12:00:00",
        "kwp": 5.0,
        "latitude": 51.5,
        "longitude": -0.12,
        "azimuth": 180.0,
        "tilt": 30.0,
    }
    req = PredictionRequest(**payload)
    assert req.kwp == 5.0
    assert isinstance(req.datetime, datetime)


def test_prediction_request_with_optional_price():
    payload = {
        "datetime": "2025-01-02T08:30:00",
        "kwp": 3.3,
        "latitude": 40.0,
        "longitude": -75.0,
        "azimuth": 90.0,
        "tilt": 15.0,
        "kwh_price": 0.20,
    }
    req = PredictionRequest(**payload)
    assert req.kwh_price == 0.20


def test_prediction_request_invalid_types_and_missing():
    bad = {
        "datetime": "not-a-date",
        "kwp": "five",
        "latitude": None,
        # missing longitude, azimuth, tilt
    }
    with pytest.raises(ValidationError) as exc:
        PredictionRequest(**bad)
    errs = {e["loc"][0] for e in exc.value.errors()}
    assert "datetime" in errs
    assert "kwp" in errs
    assert "latitude" in errs
    assert "longitude" in errs
    assert "azimuth" in errs
    assert "tilt" in errs


def test_prediction_response_valid():
    payload = {
        "datetime": "2025-01-01T12:00:00",
        "prediction": 4.7,
        "co2_saved": 0.8,
        "money_saved": 1.2,
    }
    resp = PredictionResponse(**payload)
    assert resp.prediction == 4.7
    assert resp.co2_saved == 0.8
    assert resp.money_saved == 1.2


def test_batch_prediction_request_and_response():
    entry = {
        "datetime": "2025-01-01T12:00:00",
        "kwp": 1.0,
        "latitude": 0.0,
        "longitude": 0.0,
        "azimuth": 0.0,
        "tilt": 0.0,
    }
    batch_req = BatchPredictionRequest(entries=[entry, entry])
    assert len(batch_req.entries) == 2

    # fake responses
    resp_list = [
        {"datetime": "2025-01-01T12:00:00", "prediction": 2.2},
        {"datetime": "2025-01-01T13:00:00", "prediction": 2.5, "co2_saved": 0.1},
    ]
    batch_resp = BatchPredictionResponse(predictions=resp_list)
    assert len(batch_resp.predictions) == 2
    assert batch_resp.predictions[1].co2_saved == 0.1


def test_time_series_prediction_request_valid_within_limits():
    now = datetime.utcnow()
    start = now + timedelta(days=1)
    end = start + timedelta(days=5)
    payload = {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "kwp": 5.0,
        "latitude": 10.0,
        "longitude": 20.0,
    }
    req = TimeSeriesPredictionRequest(**payload)
    assert req.start == start
    assert req.end == end


def test_time_series_prediction_request_range_exceeds_30_days():
    now = datetime.utcnow()
    start = now
    end = now + timedelta(days=31)
    payload = {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "kwp": 2.0,
        "latitude": 0.0,
        "longitude": 0.0,
    }
    with pytest.raises(ValidationError) as exc:
        TimeSeriesPredictionRequest(**payload)
    messages = [e["msg"] for e in exc.value.errors()]
    assert any("Date range must be within 30 days" in m for m in messages)


def test_time_series_prediction_request_dates_too_far_ahead():
    now = datetime.utcnow()

    # start after  16 days
    start = now + timedelta(days=17)
    end = start + timedelta(days=1)
    payload = {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "kwp": 1.0,
        "latitude": 0.0,
        "longitude": 0.0,
    }
    with pytest.raises(ValidationError) as exc:
        TimeSeriesPredictionRequest(**payload)
    messages = [e["msg"] for e in exc.value.errors()]
    assert any(
        "Forecast dates must not be more than 16 days in advance" in m for m in messages
    )


def test_feature_input_valid_and_missing_fields():
    good = {
        "kwp": 5.0,
        "relative_humidity_2m": 60.0,
        "dew_point_2m": 10.0,
        "pressure_msl": 1015.0,
        "precipitation": 0.0,
        "wind_speed_10m": 3.0,
        "wind_direction_10m": 180.0,
        "day_of_year": 150,
        "solar_zenith": 45.0,
        "solar_azimuth": 150.0,
        "poa": 800.0,
        "clearsky_index": 0.9,
        "cloud_cover_3_moving_average": 10.0,
        "hour_sin": 0.5,
        "hour_cos": 0.87,
        "day_of_year_sin": 0.2,
        "month_cos": 0.3,
        "cell_temp": 25.0,
        "physical_model_prediction": 4.0,
    }
    feat = FeatureInput(**good)
    assert feat.poa == 800.0  # spot‐check one
    # missing one required
    bad = {**good}
    bad.pop("kwp")
    with pytest.raises(ValidationError) as exc:
        FeatureInput(**bad)
    assert any(e["loc"][0] == "kwp" for e in exc.value.errors())


def test_prediction_client_models_and_batches():
    # client request
    feat = FeatureInput(
        kwp=1,
        relative_humidity_2m=50,
        dew_point_2m=5,
        pressure_msl=1000,
        precipitation=0,
        wind_speed_10m=2,
        wind_direction_10m=90,
        day_of_year=100,
        solar_zenith=30,
        solar_azimuth=140,
        poa=700,
        clearsky_index=0.8,
        cloud_cover_3_moving_average=20,
        hour_sin=0.1,
        hour_cos=0.99,
        day_of_year_sin=0.5,
        month_cos=0.4,
        cell_temp=30,
        physical_model_prediction=3.5,
    )
    cli_req = PredictionClientRequest(
        features=feat,
        datetime="2025-01-01T10:00:00",
    )
    assert cli_req.features.physical_model_prediction == 3.5

    # client response
    cli_resp = PredictionClientResponse(prediction=2.2, datetime="2025-01-01T10:00:00")
    assert cli_resp.prediction == 2.2

    batch_cli_req = BatchPredictionClientRequest(entries=[cli_req, cli_req])
    assert len(batch_cli_req.entries) == 2

    batch_cli_resp = BatchPredictionClientResponse(
        predictions=[{"prediction": 1.1, "datetime": "2025-01-01T11:00:00"}]
    )
    assert len(batch_cli_resp.predictions) == 1
