from dataclasses import dataclass
from typing import List

@dataclass
class User:
    username: str
    password: str
    role: str
    assigned_events: List[str]

    @classmethod
    def from_dict(cls, username: str, data: dict) -> 'User':
        return cls(
            username=username,
            password=data['password'],
            role=data['role'],
            assigned_events=data.get('assigned_events', [])
        )

    def to_dict(self) -> dict:
        return {
            'password': self.password,
            'role': self.role,
            'assigned_events': self.assigned_events
        } 