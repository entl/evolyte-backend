from unittest.mock import MagicMock, PropertyMock

import pytest


@pytest.fixture(scope="function")
def mock_uow(mock_user_repository, mock_solar_panel_repository):
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.__exit__.return_value = None
    uow.commit.return_value = None
    uow.rollback.return_value = None
    type(uow).users = PropertyMock(return_value=mock_user_repository)
    type(uow).solar_panels = PropertyMock(return_value=mock_solar_panel_repository)
    return uow


@pytest.fixture
def mock_user_repository():
    mock_user_repository = MagicMock()
    mock_user_repository.get_all.return_value = []
    mock_user_repository.get_by.return_value = None
    mock_user_repository.create.return_value = None
    mock_user_repository.update.return_value = None
    mock_user_repository.delete.return_value = None

    return mock_user_repository


@pytest.fixture
def mock_solar_panel_repository():
    mock_solar_panel_repository = MagicMock()
    mock_solar_panel_repository.get_all.return_value = []
    mock_solar_panel_repository.get_by.return_value = None
    mock_solar_panel_repository.create.return_value = None
    mock_solar_panel_repository.update.return_value = None
    mock_solar_panel_repository.delete.return_value = None

    mock_solar_panel_repository.get_clustered_panels.return_value = []
    mock_solar_panel_repository.get_panels_in_bounds.return_value = []
    mock_solar_panel_repository.get_nearby_panels.return_value = []

    return mock_solar_panel_repository
