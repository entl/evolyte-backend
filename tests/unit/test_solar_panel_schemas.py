from datetime import datetime

import pytest
from pydantic import ValidationError

from src.solar_panels.schemas import (
    ClusteredSolarPanelsResponse,
    PanelStatusEnum,
    SolarPanelBase,
    SolarPanelCreate,
    SolarPanelResponse,
    SolarPanelsCluster,
    SolarPanelUpdate,
)


def test_panel_status_enum_valid():
    #  accept only valid enum strings
    assert PanelStatusEnum("OPERATIONAL") == PanelStatusEnum.OPERATIONAL
    assert PanelStatusEnum.MAINTENANCE.value == "MAINTENANCE"


def test_panel_status_enum_invalid():
    with pytest.raises(ValueError):
        PanelStatusEnum("NOT_A_STATUS")


def test_solar_panel_base_valid_minimum():
    payload = {
        "serial_number": "SP-001",
        "name": "Roof Panel",
        "capacity_kw": 3.2,
        "location": (51.5, -0.12),
    }
    panel = SolarPanelBase(**payload)
    assert panel.serial_number == payload["serial_number"]
    assert panel.capacity_kw == payload["capacity_kw"]
    assert panel.location == payload["location"]

    # Optional fields default to None
    assert panel.manufacturer is None
    assert panel.status is None


def test_solar_panel_base_all_fields():
    now = datetime.utcnow()
    payload = {
        "serial_number": "SP-002",
        "name": "East Panel",
        "manufacturer": "SolarCo",
        "model": "X100",
        "installation_date": now,
        "capacity_kw": 5.5,
        "efficiency": 20.1,
        "voltage_rating": 48.0,
        "current_rating": 11.0,
        "width": 1.0,
        "length": 2.0,
        "height": 0.04,
        "weight": 22.0,
        "orientation": 90.0,
        "tilt": 25.0,
        "status": "OFFLINE",
        "location": (34.0, -118.2),
    }
    panel = SolarPanelBase(**payload)
    assert panel.status == PanelStatusEnum.OFFLINE
    assert panel.installation_date == now


def test_solar_panel_base_invalid_types():
    bad = {
        "serial_number": 123,
        "name": None,
        "capacity_kw": "five",
        "location": [0, 0, 0],
    }
    with pytest.raises(ValidationError) as exc:
        SolarPanelBase(**bad)
    errors = exc.value.errors()

    # expect errors for serial_number, name, capacity_kw, location length
    fields = {e["loc"][0] for e in errors}
    assert "serial_number" in fields
    assert "name" in fields
    assert "capacity_kw" in fields
    assert "location" in fields


def test_solar_panel_create_inherits_base():
    base = {
        "serial_number": "SP-003",
        "name": "South Panel",
        "capacity_kw": 4.0,
        "location": (40.0, -74.0),
        "user_id": 42,
    }
    panel = SolarPanelCreate(**base)
    for k, v in base.items():
        assert getattr(panel, k) == v


def test_solar_panel_update_same_as_base():
    payload = {
        "serial_number": "SP-004",
        "name": "West Panel",
        "capacity_kw": 2.5,
        "location": (48.8, 2.3),
    }
    panel = SolarPanelUpdate(**payload)
    assert panel.serial_number == "SP-004"


def test_solar_panel_response_from_attributes():
    class Dummy:
        def __init__(self):
            self.id = 10
            self.serial_number = "SP-010"
            self.name = "Dummy Panel"
            self.manufacturer = "DumCo"
            self.model = "D10"
            self.installation_date = datetime(2025, 1, 1, 12, 0, 0)
            self.capacity_kw = 6.0
            self.efficiency = 19.5
            self.voltage_rating = 50.0
            self.current_rating = 12.0
            self.width = 1.1
            self.length = 2.2
            self.height = 0.05
            self.weight = 24.0
            self.orientation = 180.0
            self.tilt = 35.0
            self.status = PanelStatusEnum.OPERATIONAL
            self.location = (35.0, 139.0)
            self.user_id = 7
            self.created_at = datetime(2025, 1, 2, 8, 0, 0)
            self.updated_at = datetime(2025, 1, 3, 9, 30, 0)

    dummy = Dummy()
    resp = SolarPanelResponse.from_orm(dummy)
    assert resp.id == dummy.id
    assert resp.created_at == dummy.created_at
    assert resp.updated_at == dummy.updated_at
    assert resp.status == dummy.status


def test_solar_panels_cluster_valid():
    cluster_payload = {
        "latitude": 10.0,
        "longitude": 20.0,
        "count": 5,
        "min_longitude": 19.0,
        "max_longitude": 21.0,
        "min_latitude": 9.5,
        "max_latitude": 10.5,
    }
    cluster = SolarPanelsCluster(**cluster_payload)
    for k, v in cluster_payload.items():
        assert getattr(cluster, k) == v


def test_solar_panels_cluster_invalid():
    with pytest.raises(ValidationError):
        SolarPanelsCluster(latitude=0, longitude=0, count=1)  # missing bounds


def test_clustered_solar_panels_response():
    clusters = [
        {
            "latitude": 1.0,
            "longitude": 2.0,
            "count": 3,
            "min_longitude": 1.5,
            "max_longitude": 2.5,
            "min_latitude": 0.5,
            "max_latitude": 2.1,
        },
    ]
    resp = ClusteredSolarPanelsResponse(clusters=clusters)
    assert isinstance(resp.clusters, list)
    assert resp.clusters[0].count == 3
