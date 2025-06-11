import json
from typing import Dict, List, Optional
from src.model.event import Event

class EventRepository:
    def __init__(self):
        self.events_file = "events.json"
        self.load_events()

    def load_events(self):
        try:
            with open(self.events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.events = {}
                # Handle both old and new format
                if isinstance(data, dict):
                    if 'events' in data:  # New format
                        for event_data in data['events']:
                            event = Event(
                                id=event_data.get('id', ''),
                                title=event_data.get('title', ''),
                                description=event_data.get('description', ''),
                                assigned_users=event_data.get('assigned_users', [])
                            )
                            self.events[event.id] = event
                    else:  # Old format (direct event mapping)
                        for event_id, event_data in data.items():
                            event = Event(
                                id=event_id,
                                title=event_data.get('title', ''),
                                description=event_data.get('description', ''),
                                assigned_users=event_data.get('assigned_users', [])
                            )
                            self.events[event_id] = event
        except FileNotFoundError:
            self.events = {}
            self.save_events()

    def save_events(self):
        data = {
            'events': [
                {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'assigned_users': event.assigned_users
                }
                for event in self.events.values()
            ]
        }
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def create_event(self, title: str, description: str = "") -> Event:
        # Generate a new ID based on existing IDs
        existing_ids = [int(id) for id in self.events.keys() if id.isdigit()]
        next_id = str(max(existing_ids) + 1) if existing_ids else "1"
        
        event = Event(
            id=next_id,
            title=title,
            description=description,
            assigned_users=[]
        )
        self.events[next_id] = event
        self.save_events()
        return event

    def get_event(self, event_id: str) -> Optional[Event]:
        return self.events.get(event_id)

    def get_all_events(self) -> Dict[str, Event]:
        return self.events

    def update_event(self, event: Event) -> Event:
        self.events[event.id] = event
        self.save_events()
        return event

    def delete_event(self, event_id: str) -> bool:
        if event_id in self.events:
            del self.events[event_id]
            self.save_events()
            return True
        return False

    def assign_users_to_event(self, event_id: str, usernames: List[str]) -> bool:
        event = self.get_event(event_id)
        if event:
            event.assigned_users = usernames
            self.update_event(event)
            return True
        return False

    def get_user_events(self, username: str) -> Dict[str, Event]:
        return {
            event_id: event
            for event_id, event in self.events.items()
            if username in event.assigned_users
        } 