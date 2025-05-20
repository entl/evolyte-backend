from datetime import datetime

import pytest

from src.core.exceptions.user import DuplicateEmailOrUsernameException
from src.user.models import User
from src.user.schemas import UserCreate, UserUpdate
from src.user.service import UserService


@pytest.fixture
def sample_users():
    now = datetime.utcnow()
    return [
        User(
            id=1,
            email="john@example.com",
            password="hashed_pass",
            role="user",
            full_name="John Doe",
            created_at=now,
            updated_at=now,
        ),
        User(
            id=2,
            email="admin@example.com",
            password="hashed_admin",
            role="admin",
            full_name="Admin User",
            created_at=now,
            updated_at=now,
        ),
    ]


def test_get_all_users_returns_all_users(mock_uow, sample_users):
    mock_uow.users.get_all.return_value = [*sample_users]
    service = UserService(mock_uow)

    result = service.get_all_users()

    assert len(result) == 2
    assert result[0].id == sample_users[0].id
    assert result[1].id == sample_users[1].id


def test_get_user_by_id_returns_correct_user(mock_uow, sample_users):
    test_user = sample_users[0]
    mock_uow.users.get_by.return_value = test_user
    service = UserService(mock_uow)

    result = service.get_user_by_id(test_user.id)

    assert result is not None
    assert result.id == test_user.id
    assert result.email == test_user.email

    mock_uow.users.get_by.assert_called_once_with(id=test_user.id)


def test_create_user_raises_exception_on_duplicate_email(mock_uow):
    service = UserService(mock_uow)

    test = User(
        id=3,
        email="test@example.com",
        password="hashedpass123",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    mock_uow.users.get_by.side_effect = [test]

    user = UserCreate(
        email="test@example.com",
        password="12345678",
        password_confirmation="12345678",
        full_name="test user",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    with pytest.raises(DuplicateEmailOrUsernameException):
        service.create_user(user)


def test_create_user_raises_success(mock_uow):
    service = UserService(mock_uow)

    # mock that no existing user is found with same email oe username
    mock_uow.users.get_by.side_effect = None

    test_user = User(
        id=3,
        email="test@example.com",
        password="hashedpass123",
        full_name="test user",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_uow.users.create.return_value = test_user

    user_create = UserCreate(
        email="test@example.com",
        password="12345678",
        password_confirmation="12345678",
        full_name="test user",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    result = service.create_user(user_create)

    assert result is not None
    assert result.email == "test@example.com"

    mock_uow.users.create.assert_called_once()


def test_update_user_success(mock_uow):
    service = UserService(mock_uow)

    test_user = User(
        id=1,
        email="old@example.com",
        password="oldpass123",
        full_name="Old Name",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # Mock get existing user
    mock_uow.users.get_by.return_value = test_user

    new_data = UserUpdate(id=1, email="newname@test.com", full_name="New Name")

    # Mock update
    updated_user = User(
        id=1,
        email="new@example.com",
        password="oldpass123",
        full_name="New Name",
        created_at=test_user.created_at,
        updated_at=datetime.now(),
    )
    mock_uow.users.update.return_value = updated_user

    result = service.update_user(new_data)

    assert result is not None
    assert result.id == 1
    assert result.email == "new@example.com"
    assert result.full_name == "New Name"

    mock_uow.users.get_by.assert_called_once_with(id=1)
    mock_uow.users.update.assert_called_once()
