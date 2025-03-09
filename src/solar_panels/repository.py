from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select
from geoalchemy2.functions import ST_X, ST_Y, ST_Within, ST_MakeEnvelope, ST_DWithin, ST_GeomFromText, ST_ClusterDBSCAN

from src.solar_panels.models import SolarPanel
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

    def get_clustered_panels(self, min_lat, max_lat, min_lon, max_lon, eps: float = 0.1, min_points: int = 50):
        clustered_panels = (
            select(
                ST_ClusterDBSCAN(SolarPanel.location, eps, min_points).over().label("cluster_id"),
                SolarPanel.id.label("panel_id"),
                ST_X(SolarPanel.location).label("lon"),
                ST_Y(SolarPanel.location).label("lat")
            )
            .where(
                SolarPanel.location.op("&&")(ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326))
            )
        ).subquery()

        query = (
            select(
                func.count(clustered_panels.c.panel_id).label("count"),
                func.avg(clustered_panels.c.lon).label("lon"),
                func.avg(clustered_panels.c.lat).label("lat"),
                func.min(clustered_panels.c.lon).label("min_lon"),
                func.max(clustered_panels.c.lon).label("max_lon"),
                func.min(clustered_panels.c.lat).label("min_lat"),
                func.max(clustered_panels.c.lat).label("max_lat"),
            )
            .group_by(clustered_panels.c.cluster_id)
            .order_by(func.count(clustered_panels.c.panel_id).desc())
        )

        res = self.session.execute(query).fetchall()
        return res

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
