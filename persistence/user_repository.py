from typing import Dict, List, Optional


class UserRepository:
    def __init__(self) -> None:
        self._data: Dict[int, Dict] = {}
        self._next_id = 1

    def list(self) -> List[Dict]:
        return list(self._data.values())

    def get(self, user_id: int) -> Optional[Dict]:
        return self._data.get(user_id)

    def create(self, user_data: Dict) -> Dict:
        user = user_data.copy()
        user["id"] = self._next_id
        self._data[self._next_id] = user
        self._next_id += 1
        return user

    def update(self, user_id: int, fields: Dict) -> Optional[Dict]:
        if user_id not in self._data:
            return None
        self._data[user_id].update(fields)
        return self._data[user_id]

    def delete(self, user_id: int) -> bool:
        if user_id in self._data:
            del self._data[user_id]
            return True
        return False
