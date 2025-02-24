from geoalchemy2.shape import to_shape

from src.core.db.uow import UnitOfWork
from src.core.exceptions.solar_panels import SolarPanelNotFoundException
from src.solar_panels.models import SolarPanel
from src.solar_panels.schemas import SolarPanelCreate, SolarPanelUpdate, SolarPanelResponse, PanelStatusEnum


class SolarPanelService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_all_solar_panels(self) -> list[SolarPanelResponse]:
        panels = self.uow.solar_panels.get_all()
        return [SolarPanelResponse.model_validate(panel) for panel in panels]

    def get_solar_panel_by_id(self, solar_panel_id: int) -> SolarPanelResponse:
        panel = self.uow.solar_panels.get_by(id=solar_panel_id)
        panel.location = self.__wkbelement_to_lat_lon(panel.location)
        return SolarPanelResponse.model_validate(panel) if panel else None

    def get_solar_panels_by_user_id(self, user_id: int) -> list[SolarPanelResponse]:
        panels = self.uow.solar_panels.get_by(user_id=user_id)
        return [SolarPanelResponse.model_validate(panel) for panel in panels]

    def get_solar_panels_by_status(self, status: PanelStatusEnum) -> list[SolarPanelResponse]:
        panels = self.uow.solar_panels.get_by(status=status)
        return [SolarPanelResponse.model_validate(panel) for panel in panels]

    def get_solar_panels_based_on_zoom(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float, zoom_level: int):
        if zoom_level > 12:
            return self.uow.solar_panels.get_panels_in_bounds(min_lat, max_lat, min_lon, max_lon)

        grid_size = 0.1 if zoom_level < 5 else 0.01 if zoom_level < 10 else 0.001
        return self.uow.solar_panels.get_clustered_panels(min_lat, max_lat, min_lon, max_lon, grid_size)

    def get_nearby_solar_panels(self, lat: float, lon: float, radius: float) -> list[SolarPanelResponse]:
        panels = self.uow.solar_panels.get_nearby_panels(lat, lon, radius)
        return [SolarPanelResponse.model_validate(panel) for panel in panels]

    def get_clustered_panels(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float, zoom_level: int) -> list[SolarPanelResponse]:
        panels = self.uow.solar_panels.get_clustered_panels(min_lat, max_lat, min_lon, max_lon, zoom_level)
        return [SolarPanelResponse.model_validate(panel) for panel in panels]

    def get_solar_panel_in_bounds(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> list[SolarPanelResponse]:
        panels = self.uow.solar_panels.get_panels_in_bounds(min_lat, max_lat, min_lon, max_lon)
        return [SolarPanelResponse.model_validate(panel) for panel in panels]

    def create_solar_panel(self, solar_panel_data: SolarPanelCreate) -> SolarPanelResponse:
        print(solar_panel_data)
        with self.uow as uow:
            solar_panel = SolarPanel(**solar_panel_data.dict())
            print(solar_panel)

            created_solar_panel = uow.solar_panels.create(solar_panel)
            uow.flush()  # ensure the ID and location
            uow.refresh(created_solar_panel)

            # convert postgis POINT to lat, lon
            uow.expunge(created_solar_panel)  # remove from session to avoid auto-update in database
            created_solar_panel.location = self.__wkbelement_to_lat_lon(created_solar_panel.location)

            return SolarPanelResponse.model_validate(created_solar_panel)

    def create_bulk_solar_panels(self, solar_panels: list[SolarPanelCreate]) -> list[SolarPanelResponse]:
        with self.uow:
            print("Hui")
            print(solar_panels[0])
            solar_panels = [SolarPanel(**panel.model_dump()) for panel in solar_panels]
            created_solar_panels = []

            for solar_panel in solar_panels:
                created_solar_panel = self.uow.solar_panels.create(solar_panel)
                self.uow.flush()
                self.uow.refresh(created_solar_panel)
                self.uow.expunge(created_solar_panel)

                created_solar_panel.location = self.__wkbelement_to_lat_lon(created_solar_panel.location)
                created_solar_panels.append(created_solar_panel)

            return [SolarPanelResponse.model_validate(panel) for panel in created_solar_panels]

    def update_solar_panel(self, solar_panel_data: SolarPanelUpdate) -> SolarPanelResponse:
        with self.uow:
            solar_panel = self.uow.solar_panels.get_by(id=solar_panel_data.id)
            if not solar_panel:
                raise SolarPanelNotFoundException()

            update_data = solar_panel_data.model_dump(exclude_unset=True, exclude_none=True)
            for key, value in update_data.items():
                setattr(solar_panel, key, value)

            return SolarPanelResponse.model_validate(solar_panel)

    def delete_solar_panel(self, solar_panel_id: int) -> None:
        with self.uow:
            solar_panel = self.uow.solar_panels.get_by(id=solar_panel_id)
            if not solar_panel:
                raise SolarPanelNotFoundException()

            self.uow.solar_panels.delete(solar_panel)
            return None

    def __wkbelement_to_lat_lon(self, wkbelement) -> tuple[float, float]:
        # convert postgis POINT to lat, lon
        point = to_shape(wkbelement)
        return (point.x, point.y)
