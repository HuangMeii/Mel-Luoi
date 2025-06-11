from dataclasses import dataclass
from typing import List

@dataclass
class Event:
    id: str
    title: str
    description: str
    assigned_users: List[str]

    @classmethod
    def from_dict(cls, event_id: str, data: dict) -> 'Event':
        return cls(
            id=event_id,
            title=data['title'],
            description=data['description'],
            assigned_users=data.get('assigned_users', [])
        )

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'description': self.description,
            'assigned_users': self.assigned_users
        }