from typing import List

from fastapi import APIRouter

from src.core.dependencies.solar_panels import SolarPanelServiceDep
from src.solar_panels.schemas import (
    ClusteredSolarPanelsResponse,
    PanelStatusEnum,
    SolarPanelCreate,
    SolarPanelResponse,
    SolarPanelUpdate,
)

solar_panels_router = APIRouter(prefix="/solar-panels", tags=["Solar Panels"])


@solar_panels_router.post("/", response_model=SolarPanelResponse)
def create_solar_panel(solar_panel: SolarPanelCreate, solar_panel_service: SolarPanelServiceDep):
    new_panel = solar_panel_service.create_solar_panel(solar_panel)
    return new_panel


@solar_panels_router.post("/bulk", response_model=List[SolarPanelResponse])
def create_solar_panels_bulk(solar_panels: List[SolarPanelCreate], solar_panel_service: SolarPanelServiceDep):
    new_panels = solar_panel_service.create_bulk_solar_panels(solar_panels)
    return new_panels


@solar_panels_router.get("/", response_model=List[SolarPanelResponse])
def list_solar_panels(solar_panel_service: SolarPanelServiceDep):
    return solar_panel_service.get_all_solar_panels()


@solar_panels_router.put("/{panel_id}", response_model=SolarPanelResponse)
def update_solar_panel(
    solar_panel_id: int,
    solar_panel: SolarPanelUpdate,
    solar_panel_service: SolarPanelServiceDep,
):
    panel = solar_panel_service.update_solar_panel(solar_panel_id, solar_panel)
    return panel


@solar_panels_router.get("/user/{user_id}", response_model=List[SolarPanelResponse])
def get_user_solar_panels(user_id: int, solar_panel_service: SolarPanelServiceDep):
    return solar_panel_service.get_solar_panels_by_user(user_id)


@solar_panels_router.get("/status/{status}", response_model=List[SolarPanelResponse])
def get_solar_panels_by_status(status: PanelStatusEnum, solar_panel_service: SolarPanelServiceDep):
    return solar_panel_service.get_solar_panels_by_status(status)


@solar_panels_router.get("/nearby", response_model=List[SolarPanelResponse])
def get_nearby_solar_panels(lat: float, lon: float, radius: float, solar_panel_service: SolarPanelServiceDep):
    return solar_panel_service.get_nearby_solar_panels(lat, lon, radius)


@solar_panels_router.get("/clustered", response_model=ClusteredSolarPanelsResponse)
def get_clustered_solar_panels(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    zoom_level: int,
    solar_panel_service: SolarPanelServiceDep,
):
    panels = solar_panel_service.get_clustered_panels(min_lat, max_lat, min_lon, max_lon, zoom_level)
    return panels


@solar_panels_router.get("/bounds", response_model=List[SolarPanelResponse])
def get_panels_in_bounds(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    solar_panel_service: SolarPanelServiceDep,
):
    return solar_panel_service.get_solar_panel_in_bounds(min_lat, max_lat, min_lon, max_lon)


@solar_panels_router.delete("/{panel_id}", status_code=204)
def delete_solar_panel(solar_panel_id: int, solar_panel_service: SolarPanelServiceDep):
    solar_panel_service.delete_solar_panel(solar_panel_id)


@solar_panels_router.get("/{panel_id}", response_model=SolarPanelResponse)
def get_solar_panel(solar_panel_id: int, solar_panel_service: SolarPanelServiceDep):
    panel = solar_panel_service.get_solar_panel_by_id(solar_panel_id)

    return panel
