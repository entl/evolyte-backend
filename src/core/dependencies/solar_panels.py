from typing import Annotated

from fastapi import Depends

from src.solar_panels.repository import SolarPanelRepository
from src.solar_panels.service import SolarPanelService
from src.core.db.session import SessionFactory
from .db import UowDep


def solar_panel_repository():
    return SolarPanelRepository(SessionFactory())


SolarPanelRepositoryDep = Annotated[SolarPanelRepository, Depends(solar_panel_repository)]


def solar_panel_service(uow: UowDep):
    return SolarPanelService(uow)


SolarPanelServiceDep = Annotated[SolarPanelService, Depends(solar_panel_service)]
