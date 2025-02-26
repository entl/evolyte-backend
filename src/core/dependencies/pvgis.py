from typing import Annotated

from fastapi import Depends

from src.pvgis.client import PVGISAPIClient
from src.pvgis.service import PVGISService


def pvgis_service():
    return PVGISService(PVGISAPIClient())


PVGISServiceDep = Annotated[PVGISService, Depends(pvgis_service)]

