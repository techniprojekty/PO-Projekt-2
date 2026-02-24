import pytest

from services.user_service import UserService, VALID_GROUPS
from persistence.user_repository import UserRepository


@pytest.fixture

def service():
    return UserService(UserRepository())


def valid_user():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "birthYear": 1990,
        "group": "user",
    }


def test_create_and_get(service):
    user = service.create_user(valid_user())
    assert user["id"] == 1
    assert user["firstName"] == "John"
    assert user["age"] == ( __import__('datetime').date.today().year - 1990 )

    retrieved = service.get_user(1)
    assert retrieved == user


def test_list_empty_then_one(service):
    assert service.list_users() == []
    service.create_user(valid_user())
    assert len(service.list_users()) == 1


def test_update(service):
    user = service.create_user(valid_user())
    updated = service.update_user(user["id"], {"firstName": "Jane"})
    assert updated["firstName"] == "Jane"
    assert service.get_user(user["id"])["firstName"] == "Jane"


def test_update_missing(service):
    assert service.update_user(999, {"firstName": "x"}) is None
    assert service.get_user(-1) is None
    assert service.update_user(0, {"firstName": "y"}) is None
    assert not service.delete_user(-5)


def test_delete(service):
    user = service.create_user(valid_user())
    assert service.delete_user(user["id"])
    assert service.get_user(user["id"]) is None
    assert not service.delete_user(999)


def test_validation(service):
    bad = valid_user().copy()
    bad["birthYear"] = "not int"
    with pytest.raises(ValueError):
        service.create_user(bad)
    bad = valid_user().copy()
    bad["group"] = "invalid"
    with pytest.raises(ValueError):
        service.create_user(bad)

