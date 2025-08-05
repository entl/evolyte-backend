from typing import List

from fastapi import APIRouter

from src.core.dependencies.solar_panels import SolarPanelServiceDep
from src.logger import get_logger
from src.solar_panels.schemas import (
    ClusteredSolarPanelsResponse,
    PanelStatusEnum,
    SolarPanelCreate,
    SolarPanelResponse,
    SolarPanelUpdate,
)

solar_panels_router = APIRouter(prefix="/solar-panels", tags=["Solar Panels"])

# Configure logger for this module
solar_logger = get_logger(__name__)


@solar_panels_router.post("/", response_model=SolarPanelResponse)
def create_solar_panel(solar_panel: SolarPanelCreate, solar_panel_service: SolarPanelServiceDep):
    solar_logger.info(f"Creating solar panel: {solar_panel}")
    new_panel = solar_panel_service.create_solar_panel(solar_panel)
    solar_logger.info(f"Created solar panel with ID: {getattr(new_panel, 'id', None)}")
    return new_panel


@solar_panels_router.post("/bulk", response_model=List[SolarPanelResponse])
def create_solar_panels_bulk(solar_panels: List[SolarPanelCreate], solar_panel_service: SolarPanelServiceDep):
    solar_logger.info(f"Bulk creating solar panels: {solar_panels}")
    new_panels = solar_panel_service.create_bulk_solar_panels(solar_panels)
    solar_logger.info(f"Created {len(new_panels)} solar panels")
    return new_panels


@solar_panels_router.get("/", response_model=List[SolarPanelResponse])
def list_solar_panels(solar_panel_service: SolarPanelServiceDep):
    solar_logger.info("Listing all solar panels")
    panels = solar_panel_service.get_all_solar_panels()
    solar_logger.info(f"Found {len(panels)} solar panels")
    return panels


@solar_panels_router.put("/{panel_id}", response_model=SolarPanelResponse)
def update_solar_panel(
    solar_panel_id: int,
    solar_panel: SolarPanelUpdate,
    solar_panel_service: SolarPanelServiceDep,
):
    solar_logger.info(f"Updating solar panel {solar_panel_id} with data: {solar_panel}")
    panel = solar_panel_service.update_solar_panel(solar_panel)
    solar_logger.info(f"Updated solar panel {solar_panel_id}")
    return panel





@solar_panels_router.get("/status/{status}", response_model=List[SolarPanelResponse])
def get_solar_panels_by_status(status: PanelStatusEnum, solar_panel_service: SolarPanelServiceDep):
    solar_logger.info(f"Getting solar panels by status: {status}")
    panels = solar_panel_service.get_solar_panels_by_status(status)
    solar_logger.info(f"Found {len(panels)} panels with status {status}")
    return panels


@solar_panels_router.get("/nearby", response_model=List[SolarPanelResponse])
def get_nearby_solar_panels(lat: float, lon: float, radius: float, solar_panel_service: SolarPanelServiceDep):
    solar_logger.info(f"Getting nearby solar panels at lat={lat}, lon={lon}, radius={radius}")
    panels = solar_panel_service.get_nearby_solar_panels(lat, lon, radius)
    solar_logger.info(f"Found {len(panels)} nearby panels")
    return panels


@solar_panels_router.get("/clustered", response_model=ClusteredSolarPanelsResponse)
def get_clustered_solar_panels(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    zoom_level: int,
    solar_panel_service: SolarPanelServiceDep,
):
    solar_logger.info(
        f"Getting clustered solar panels for bounds lat=({min_lat},{max_lat}), lon=({min_lon},{max_lon}), zoom={zoom_level}"
    )
    panels = solar_panel_service.get_clustered_panels(min_lat, max_lat, min_lon, max_lon, zoom_level)
    solar_logger.info("Clustered solar panels fetched")
    return panels


@solar_panels_router.get("/bounds", response_model=List[SolarPanelResponse])
def get_panels_in_bounds(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    solar_panel_service: SolarPanelServiceDep,
):
    solar_logger.info(f"Getting panels in bounds lat=({min_lat},{max_lat}), lon=({min_lon},{max_lon})")
    panels = solar_panel_service.get_solar_panel_in_bounds(min_lat, max_lat, min_lon, max_lon)
    solar_logger.info(f"Found {len(panels)} panels in bounds")
    return panels


@solar_panels_router.delete("/{panel_id}", status_code=204)
def delete_solar_panel(solar_panel_id: int, solar_panel_service: SolarPanelServiceDep):
    solar_logger.info(f"Deleting solar panel {solar_panel_id}")
    solar_panel_service.delete_solar_panel(solar_panel_id)
    solar_logger.info(f"Deleted solar panel {solar_panel_id}")


@solar_panels_router.get("/{panel_id}", response_model=SolarPanelResponse)
def get_solar_panel(solar_panel_id: int, solar_panel_service: SolarPanelServiceDep):
    solar_logger.info(f"Getting solar panel {solar_panel_id}")
    panel = solar_panel_service.get_solar_panel_by_id(solar_panel_id)
    solar_logger.info(f"Fetched solar panel {solar_panel_id}")
    return panel
