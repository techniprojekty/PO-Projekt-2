from datetime import date
from typing import Dict, List, Optional


VALID_GROUPS = {"user", "premium", "admin"}


class UserService:
    def __init__(self, repository):
        self._repo = repository

    def list_users(self) -> List[Dict]:
        return [self._transform_output(u) for u in self._repo.list()]

    def get_user(self, user_id: int) -> Optional[Dict]:
        if user_id <= 0:
            return None
        user = self._repo.get(user_id)
        if user is None:
            return None
        return self._transform_output(user)

    def create_user(self, data: Dict) -> Dict:
        self._validate_input(data, creating=True)
        stored = self._repo.create(data)
        return self._transform_output(stored)

    def update_user(self, user_id: int, data: Dict) -> Optional[Dict]:
        if user_id <= 0:
            return None
        if not data:
            raise ValueError("No fields to update")
        self._validate_input(data, creating=False)
        updated = self._repo.update(user_id, data)
        if updated is None:
            return None
        return self._transform_output(updated)

    def delete_user(self, user_id: int) -> bool:
        if user_id <= 0:
            return False
        return self._repo.delete(user_id)

    def _validate_input(self, data: Dict, creating: bool):
        if creating:
            for key in ("firstName", "lastName", "birthYear", "group"):
                if key not in data:
                    raise ValueError(f"Missing field {key}")
        if "firstName" in data and not isinstance(data["firstName"], str):
            raise ValueError("firstName must be string")
        if "lastName" in data and not isinstance(data["lastName"], str):
            raise ValueError("lastName must be string")
        if "birthYear" in data:
            if not isinstance(data["birthYear"], int):
                raise ValueError("birthYear must be integer")
            if data["birthYear"] < 1900 or data["birthYear"] > date.today().year:
                raise ValueError("birthYear invalid")
        if "group" in data and data["group"] not in VALID_GROUPS:
            raise ValueError("group must be one of user/premium/admin")

    def _transform_output(self, stored: Dict) -> Dict:
        age = date.today().year - stored.get("birthYear", 0)
        return {
            "id": stored["id"],
            "firstName": stored.get("firstName"),
            "lastName": stored.get("lastName"),
            "age": age,
            "group": stored.get("group"),
        }
