from src.pvgis.client import PVGISAPIClient
from src.pvgis.schemas import PVGISGridConnectedTrackingPVSystemsRequest, PVGISOffGridRequest, \
    PVGISMonthlyRadiationRequest, PVGISDailyRadiationRequest, PVGISHourlyRadiationRequest, PVGISTMYRequest


class PVGISService:
    def __init__(self, client: PVGISAPIClient):
        self.client = client

    def get_pv_performance(self, data: PVGISGridConnectedTrackingPVSystemsRequest):
        params = {**data.model_dump(exclude_none=True, exclude_unset=True)}

        return self.client.fetch_data("PVcalc", params)

    def get_offgrid_pv(self, data: PVGISOffGridRequest):
        params = {**data.model_dump(exclude_none=True, exclude_unset=True)}

        return self.client.fetch_data("SHScalc", params)

    def get_monthly_radiation(self, data: PVGISMonthlyRadiationRequest):
        params = {**data.model_dump(exclude_none=True, exclude_unset=True)}
        return self.client.fetch_data("MRcalc", params)

    def get_daily_radiation(self, data: PVGISDailyRadiationRequest):
        params = {**data.model_dump(exclude_none=True, exclude_unset=True)}
        return self.client.fetch_data("DRcalc", params)

    def get_hourly_radiation(self, data: PVGISHourlyRadiationRequest):
        params = {**data.model_dump(exclude_none=True, exclude_unset=True)}
        return self.client.fetch_data("seriescalc", params)

    def get_tmy_data(self, data: PVGISTMYRequest):
        params = {**data.model_dump(exclude_none=True, exclude_unset=True)}
        return self.client.fetch_data("tmy", params)

