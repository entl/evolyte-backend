import datetime
import math
from functools import reduce

import pandas as pd
import pvlib.solarposition

from src.predict.client import PredictionClient
from src.predict.schemas import (
    BatchPredictionClientRequest,
    BatchPredictionRequest,
    BatchPredictionResponse,
    FeatureInput,
    PredictionClientRequest,
    PredictionRequest,
    PredictionResponse,
    TimeSeriesPredictionRequest,
)
from src.weather.schemas import HourlyWeatherData, WeatherRequest
from src.weather.service import WeatherService


class PredictionService:
    def __init__(self, weather_service: WeatherService, prediction_client: PredictionClient):
        self.weather_service = weather_service
        self.prediction_client = prediction_client

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        weather_schema = WeatherRequest(
            latitude=request.latitude,
            longitude=request.longitude,
            start_date=request.datetime.date(),
            end_date=request.datetime.date(),
            azimuth=request.azimuth,
            tilt=request.tilt,
        )

        weather_data = self.weather_service.get_weather(weather_schema)
        request_datetime = request.datetime.strftime("%Y-%m-%dT%H:%M")

        # weather api returns data for every hour, so we can reduce the list to get the data for the requested datetime
        weather_data_hourly = reduce(lambda x, y: x if x.time == request_datetime else y, weather_data.hourly)

        # calculate derived features
        solar_position = self.__calculate_solar_position(
            latitude=request.latitude,
            longitude=request.longitude,
            time=request.datetime,
        )
        poa = self.__calculate_poa(
            weather_data_hourly=weather_data_hourly,
            tilt=request.tilt,
            azimuth=request.azimuth,
            solar_zenith=solar_position["solar_zenith"],
            solar_azimuth=solar_position["solar_azimuth"],
        )
        cell_temp = self.__calcualte_cell_temperature(weather_data_hourly=weather_data_hourly, poa=poa)
        physical_model_prediction = self.__calculate_physical_model(poa=poa, cell_temp=cell_temp, kwp=request.kwp)
        hour_encoding = self.__calculate_cycling_encoding(value=request.datetime.hour, period=24)
        day_of_year_encoding = self.__calculate_cycling_encoding(value=request.datetime.timetuple().tm_yday, period=365)
        month_encoding = self.__calculate_cycling_encoding(value=request.datetime.month, period=12)
        clear_sky_index = self.__calculate_clear_sky_index(
            weather_data_hourly=weather_data_hourly,
            latitude=request.latitude,
            longitude=request.longitude,
        )

        # populate the features with initially available data
        features = FeatureInput(
            kwp=request.kwp,
            relative_humidity_2m=weather_data_hourly.relative_humidity_2m,
            dew_point_2m=weather_data_hourly.dew_point_2m,
            pressure_msl=weather_data_hourly.pressure_msl,
            precipitation=weather_data_hourly.precipitation,
            wind_speed_10m=weather_data_hourly.wind_speed_10m,
            wind_direction_10m=weather_data_hourly.wind_direction_10m,
            day_of_year=request.datetime.timetuple().tm_yday,
            solar_zenith=solar_position["solar_zenith"],
            solar_azimuth=solar_position["solar_azimuth"],
            poa=poa,
            clearsky_index=clear_sky_index,
            cloud_cover_3_moving_average=weather_data_hourly.cloud_cover,
            hour_sin=hour_encoding["sin"],
            hour_cos=hour_encoding["cos"],
            day_of_year_sin=day_of_year_encoding["sin"],
            month_cos=month_encoding["cos"],
            cell_temp=cell_temp,
            physical_model_prediction=physical_model_prediction,
        )

        # make a prediction
        prediction_request_schema = PredictionClientRequest(datetime=request.datetime, features=features)
        prediction_response = self.prediction_client.predict(prediction_request_schema)

        money_saved = None
        if request.kwh_price:
            money_saved = self.__calculate_money_saved(prediction_response.prediction["prediction"], request.kwh_price)

        return PredictionResponse(
            datetime=prediction_response.datetime,
            prediction=prediction_response.prediction,
            co2_saved=self.__calculate_co2_saved(prediction_response.prediction),
            money_saved=money_saved,
        )

    def predict_batch(self, request: BatchPredictionRequest) -> BatchPredictionResponse:
        predictions = []
        for entry in request.entries:
            prediction = self.predict(entry)
            predictions.append(prediction)

        return BatchPredictionResponse(predictions=predictions)

    def predict_time_series(self, request: TimeSeriesPredictionRequest) -> BatchPredictionResponse:
        batch_predictions_requests = []

        start_time = request.start  # Assuming request.start is a datetime object
        end_time = request.end  # Assuming request.end is a datetime object

        weather_schema = WeatherRequest(
            latitude=request.latitude,
            longitude=request.longitude,
            start_date=start_time.date(),
            end_date=end_time.date(),
            azimuth=request.azimuth,
            tilt=request.tilt,
        )

        weather_data = self.weather_service.get_weather(weather_schema)

        for entry in self.__generate_hourly_records(start_time, end_time):
            # calculate derived features
            weather_data_hourly = reduce(
                lambda x, y: x if x.time == entry.strftime("%Y-%m-%dT%H:%M") else y,
                weather_data.hourly,
            )
            solar_position = self.__calculate_solar_position(
                latitude=request.latitude, longitude=request.longitude, time=entry
            )

            poa = self.__calculate_poa(
                weather_data_hourly=weather_data_hourly,
                tilt=request.tilt,
                azimuth=request.azimuth,
                solar_zenith=solar_position["solar_zenith"],
                solar_azimuth=solar_position["solar_azimuth"],
            )
            cell_temp = self.__calcualte_cell_temperature(weather_data_hourly=weather_data_hourly, poa=poa)
            physical_model_prediction = self.__calculate_physical_model(poa=poa, cell_temp=cell_temp, kwp=request.kwp)
            hour_encoding = self.__calculate_cycling_encoding(value=entry.hour, period=24)
            day_of_year_encoding = self.__calculate_cycling_encoding(value=entry.timetuple().tm_yday, period=365)
            month_encoding = self.__calculate_cycling_encoding(value=entry.month, period=12)
            clear_sky_index = self.__calculate_clear_sky_index(
                weather_data_hourly=weather_data_hourly,
                latitude=request.latitude,
                longitude=request.longitude,
            )

            features = FeatureInput(
                kwp=request.kwp,
                relative_humidity_2m=weather_data_hourly.relative_humidity_2m,
                dew_point_2m=weather_data_hourly.dew_point_2m,
                pressure_msl=weather_data_hourly.pressure_msl,
                precipitation=weather_data_hourly.precipitation,
                wind_speed_10m=weather_data_hourly.wind_speed_10m,
                wind_direction_10m=weather_data_hourly.wind_direction_10m,
                day_of_year=entry.timetuple().tm_yday,
                solar_zenith=solar_position["solar_zenith"],
                solar_azimuth=solar_position["solar_azimuth"],
                poa=poa,
                clearsky_index=clear_sky_index,
                cloud_cover_3_moving_average=weather_data_hourly.cloud_cover,
                hour_sin=hour_encoding["sin"],
                hour_cos=hour_encoding["cos"],
                day_of_year_sin=day_of_year_encoding["sin"],
                month_cos=month_encoding["cos"],
                cell_temp=cell_temp,
                physical_model_prediction=physical_model_prediction,
            )

            prediction_request_schema = PredictionClientRequest(datetime=entry, features=features)
            batch_predictions_requests.append(prediction_request_schema)

        predictions = self.prediction_client.batch_predict(
            BatchPredictionClientRequest(entries=batch_predictions_requests)
        )
        predictions = predictions.dict()["predictions"]
        for prediction in predictions:
            prediction["co2_saved"] = self.__calculate_co2_saved(prediction["prediction"])
            if request.kwh_price:
                prediction["money_saved"] = self.__calculate_money_saved(prediction["prediction"], request.kwh_price)

        return BatchPredictionResponse(predictions=predictions)

    def __generate_hourly_records(self, start_time, end_time):
        current = start_time
        while current <= end_time:
            yield current
            current += datetime.timedelta(hours=1)

    def __calculate_solar_position(self, latitude: float, longitude: float, time: datetime) -> dict:
        solar_position = pvlib.solarposition.get_solarposition(time=time, latitude=latitude, longitude=longitude)

        return {
            "solar_zenith": solar_position["apparent_zenith"].round(2),
            "solar_azimuth": solar_position["azimuth"].round(2),
            "solar_elevation": solar_position["elevation"].round(2),
        }

    def __calculate_poa(
        self,
        weather_data_hourly: HourlyWeatherData,
        tilt,
        azimuth,
        solar_zenith,
        solar_azimuth,
    ):
        # Calculate POA
        poa_irradiance = pvlib.irradiance.get_total_irradiance(
            surface_tilt=tilt,
            surface_azimuth=azimuth,
            dni=weather_data_hourly.direct_normal_irradiance,
            ghi=weather_data_hourly.shortwave_radiation,
            dhi=weather_data_hourly.diffuse_radiation,
            solar_zenith=solar_zenith,
            solar_azimuth=solar_azimuth,
        )

        return poa_irradiance["poa_global"].round(2)

    def __calculate_physical_model(self, poa, cell_temp, kwp, inverter_efficiency=0.96):
        # Calculate physical model
        physical_model_prediction = pvlib.pvsystem.pvwatts_dc(
            g_poa_effective=poa,
            temp_cell=cell_temp,
            pdc0=kwp,
            gamma_pdc=-0.004,
        )

        return physical_model_prediction * inverter_efficiency

    def __calculate_clear_sky_index(self, weather_data_hourly: HourlyWeatherData, latitude, longitude) -> float:
        location = pvlib.location.Location(latitude=latitude, longitude=longitude)
        pd_request_datetime = pd.Timestamp(weather_data_hourly.time).tz_localize("UTC")
        pd_request_datetime = pd.DatetimeIndex([pd_request_datetime])
        cs = location.get_clearsky(pd_request_datetime, model="ineichen")

        clear_sky_index = pvlib.irradiance.clearsky_index(weather_data_hourly.shortwave_radiation, cs["ghi"])

        return clear_sky_index[0].round(2)

    def __calcualte_cell_temperature(self, weather_data_hourly: HourlyWeatherData, poa: float):
        temperature_model_params = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_polymer"]
        cell_temperature = pvlib.temperature.sapm_cell(
            poa_global=poa,
            temp_air=weather_data_hourly.temperature_2m,
            wind_speed=weather_data_hourly.wind_speed_10m,
            a=temperature_model_params["a"],
            b=temperature_model_params["b"],
            deltaT=temperature_model_params["deltaT"],
        )

        return cell_temperature.round(2)

    def __calculate_cycling_encoding(self, value, period):
        return {
            "sin": round(math.sin(2 * math.pi * value / period), 5),
            "cos": round(math.cos(2 * math.pi * value / period), 5),
        }

    def __calculate_co2_saved(self, produced_energy) -> float:
        return produced_energy * 0.225

    def __calculate_money_saved(self, produced_energy, kwh_price) -> float:
        return produced_energy * kwh_price
