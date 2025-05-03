from typing import Annotated

from fastapi import APIRouter, Query

from src.core.dependencies.pvgis import PVGISServiceDep
from src.pvgis.schemas import (
    PVGISDailyRadiationRequest,
    PVGISGridConnectedTrackingPVSystemsRequest,
    PVGISHourlyRadiationRequest,
    PVGISMonthlyRadiationRequest,
    PVGISOffGridRequest,
    PVGISTMYRequest,
)

pvgis_router = APIRouter(prefix="/pvgis", tags=["PVGIS"])


@pvgis_router.get("/performance")
def get_pv_performance(
    data: Annotated[PVGISGridConnectedTrackingPVSystemsRequest, Query()],
    pvgis_service: PVGISServiceDep,
):
    """Fetches grid-connected PV system performance data."""
    return pvgis_service.get_pv_performance(data)


@pvgis_router.get("/offgrid")
def get_offgrid_pv(data: Annotated[PVGISOffGridRequest, Query()], pvgis_service: PVGISServiceDep):
    """Fetches off-grid PV system data."""
    return pvgis_service.get_offgrid_pv(data)


@pvgis_router.get("/radiation/monthly")
def get_monthly_radiation(
    data: Annotated[PVGISMonthlyRadiationRequest, Query()],
    pvgis_service: PVGISServiceDep,
):
    """Fetches monthly radiation data."""
    return pvgis_service.get_monthly_radiation(data)


@pvgis_router.get("/radiation/daily")
def get_daily_radiation(data: Annotated[PVGISDailyRadiationRequest, Query()], pvgis_service: PVGISServiceDep):
    """Fetches daily radiation data for a specific month."""
    return pvgis_service.get_daily_radiation(data)


@pvgis_router.get("/radiation/hourly")
def get_hourly_radiation(
    data: Annotated[PVGISHourlyRadiationRequest, Query()],
    pvgis_service: PVGISServiceDep,
):
    """Fetches hourly radiation data."""
    return pvgis_service.get_hourly_radiation(data)


@pvgis_router.get("/radiation/tmy")
def get_tmy_data(data: Annotated[PVGISTMYRequest, Query()], pvgis_service: PVGISServiceDep):
    """Fetches Typical Meteorological Year (TMY) data."""
    return pvgis_service.get_tmy_data(data)
