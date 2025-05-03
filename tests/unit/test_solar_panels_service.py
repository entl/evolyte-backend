from datetime import datetime

import pytest
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from src.core.exceptions.solar_panels import SolarPanelNotFoundException
from src.solar_panels.models import PanelStatus, SolarPanel
from src.solar_panels.schemas import SolarPanelCreate
from src.solar_panels.service import SolarPanelService


@pytest.fixture
def solar_panels_service(mock_uow):
    return SolarPanelService(mock_uow)


@pytest.fixture
def sample_solar_panels():
    return [
        SolarPanel(
            id=1,
            serial_number="SP-UK-001",
            name="Cambridge Roof Panel",
            manufacturer="SunPower",
            model="X21-345",
            installation_date=datetime(2023, 4, 1),
            capacity_kw=5.0,
            efficiency=20.5,
            voltage_rating=48.0,
            current_rating=10.2,
            width=1.0,
            length=1.6,
            height=0.04,
            weight=18.5,
            orientation=180.0,
            tilt=35.0,
            status=PanelStatus.OPERATIONAL,
            location=from_shape(Point(-0.1218, 52.2053), srid=4326),
            user_id=1,
            created_at=datetime(2023, 4, 1, 10, 0),
            updated_at=datetime(2023, 4, 1, 10, 0),
        ),
        SolarPanel(
            id=2,
            serial_number="SP-UK-002",
            name="London Garden Panel",
            manufacturer="LG Solar",
            model="LG370N1C-V5",
            installation_date=datetime(2022, 7, 15),
            capacity_kw=3.7,
            efficiency=19.8,
            voltage_rating=42.0,
            current_rating=8.9,
            width=0.98,
            length=1.65,
            height=0.05,
            weight=17.8,
            orientation=150.0,
            tilt=30.0,
            status=PanelStatus.MAINTENANCE,
            location=from_shape(Point(-0.1276, 51.5074), srid=4326),
            user_id=2,
            created_at=datetime(2022, 7, 15, 12, 0),
            updated_at=datetime(2022, 7, 15, 12, 0),
        ),
    ]


def test_get_all_solar_panels_success(solar_panels_service, sample_solar_panels, mock_uow):
    mock_uow.solar_panels.get_all.return_value = sample_solar_panels
    solar_panels = solar_panels_service.get_all_solar_panels()
    assert len(solar_panels) == 2
    assert solar_panels[0].id == 1
    assert solar_panels[0].name == "Cambridge Roof Panel"
    assert solar_panels[1].id == 2
    assert solar_panels[1].name == "London Garden Panel"


def test_get_solar_panel_by_id_success(solar_panels_service, sample_solar_panels, mock_uow):
    mock_uow.solar_panels.get_by.return_value = sample_solar_panels[0]
    solar_panel = solar_panels_service.get_solar_panel_by_id(1)

    assert solar_panel is not None
    assert solar_panel.id == 1
    assert solar_panel.name == "Cambridge Roof Panel"


def test_get_solar_panel_by_id_not_found(solar_panels_service, mock_uow):
    mock_uow.solar_panels.get_by.return_value = None

    with pytest.raises(SolarPanelNotFoundException):
        solar_panels_service.get_solar_panel_by_id(1)


def test_create_solar_panel_success(solar_panels_service, mock_uow):
    solar_panel = SolarPanelCreate(
        serial_number="SP-UK-001",
        name="Cambridge Roof Panel",
        manufacturer="SunPower",
        capacity_kw=5.0,
        location=(51, -0.1),
        user_id=1,
    )

    mock_uow.solar_panels.create.return_value = SolarPanel(
        id=1,
        serial_number="SP-UK-001",
        name="Cambridge Roof Panel",
        manufacturer="SunPower",
        capacity_kw=5.0,
        location=from_shape(Point(-0.1, 51), srid=4326),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user_id=1,
    )

    result = solar_panels_service.create_solar_panel(solar_panel)

    assert result is not None
    assert result.id == 1
    assert result.name == "Cambridge Roof Panel"
    assert result.manufacturer == "SunPower"
    assert result.capacity_kw == 5.0
    assert result.location == (-0.1, 51.0)
    assert result.user_id == 1
    assert result.created_at is not None
