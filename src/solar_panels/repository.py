from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from geoalchemy2.functions import ST_X, ST_Y, ST_Within, ST_MakeEnvelope, ST_DWithin, ST_GeomFromText

from .models import SolarPanel
from src.repository import BaseRepository, T


class SolarPanelRepository(BaseRepository[SolarPanel]):
    def __init__(self, session: Session):
        super().__init__(SolarPanel, session)

    # Override the create method to convert the lat, lon to a PostGIS POINT
    def create(self, obj_data: T) -> T:
        lat, lon = obj_data.location
        location = ST_GeomFromText(f"POINT({lon} {lat})", 4326)
        obj_data.location = location

        return super().create(obj_data)

    def get_clustered_panels(self, min_lat, max_lat, min_lon, max_lon, grid_size):
        query = (
            self.session.query(
                (func.round(ST_X(SolarPanel.location) / grid_size) * grid_size).label("lon"),
                (func.round(ST_Y(SolarPanel.location) / grid_size) * grid_size).label("lat"),
                func.count(SolarPanel.id).label("panel_count")
            )
            .filter(
                ST_Within(
                    SolarPanel.location,
                    ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
                )
            )
            .group_by("lon", "lat")
        )

        return query.all()

    def get_panels_in_bounds(self, min_lat, max_lat, min_lon, max_lon):
        return (
            self.session.query(SolarPanel)
            .filter(
                ST_Within(
                    SolarPanel.location,
                    ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
                )
            )
            .all()
        )

    def get_nearby_panels(self, lat: float, lon: float, radius_km: float):
        radius_meters = radius_km * 1000  # convert km to meters
        point = func.ST_GeomFromText(f'POINT({lon} {lat})', 4326)

        query = (
            self.session.query(SolarPanel)
            .filter(ST_DWithin(SolarPanel.location, point, radius_meters))
        )

        return query.all()
