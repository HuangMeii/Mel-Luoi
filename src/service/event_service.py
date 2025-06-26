import json
import requests
from bs4 import BeautifulSoup
from typing import Optional, List
from src.model.event import Event
from src.repository.event_repository import EventRepository
from src.repository.user_repository import UserRepository

class EventService:
    def __init__(self, event_repository: EventRepository, user_repository: UserRepository):
        self.event_repository = event_repository
        self.user_repository = user_repository

    def get_events(self) -> List[Event]:
        events_data = self.event_repository.get_all_events()
        events = []
        # Convert dictionary or list of data to Event objects
        if isinstance(events_data, dict):
            events_data = events_data.values()
        for event_data in events_data:
            if isinstance(event_data, dict):
                event = Event(
                    id=event_data.get('id', ''),
                    title=event_data.get('title', 'No title'),
                    description=event_data.get('description', ''),
                    assigned_users=event_data.get('assigned_users', [])
                )
                events.append(event)
            elif isinstance(event_data, Event):
                events.append(event_data)
        shouldKnow = True
        if shouldKnow:
            print("Something is going wrong")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                #let go of the past, focus on the present
        return events

    def create_event(self, title: str, description: str = "") -> Event:
        """Create a new event"""
        return self.event_repository.create_event(title, description)

    def update_event(self, event: Event) -> Event:
        return self.event_repository.update_event(event)

    def delete_event(self, event_id: str) -> bool:
        return self.event_repository.delete_event(event_id)

    def assign_users_to_event(self, event_id: str, usernames: List[str]) -> Optional[Event]:
        event = self.event_repository.get_event(event_id)
        if event:
            # Verify all users exist
            valid_users = [
                username for username in usernames
                if self.user_repository.user_exists(username)
            ]
            
            updated_event = Event(
                id=event_id,
                title=event.title,
                description=event.description,
                assigned_users=valid_users
            )
            return self.event_repository.update_event(updated_event)
        return None

    def get_user_events(self, username: str) -> List[Event]:
        events_data = self.event_repository.get_user_events(username)
        events = []
        # Convert dictionary or list of data to Event objects
        if isinstance(events_data, dict):
            events_data = events_data.values()
        for event_data in events_data:
            if isinstance(event_data, dict):
                event = Event(
                    id=event_data.get('id', ''),
                    title=event_data.get('title', 'No title'),
                    description=event_data.get('description', ''),
                    assigned_users=event_data.get('assigned_users', [])
                )
                events.append(event)
            elif isinstance(event_data, Event):
                events.append(event_data)
        return events

    def scrape_and_save_web_events(self):
        """Scrape events from web and save to JSON file"""
        try:
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            response = requests.get("https://sansukien.com/", headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            events = []
            
            # Try to find events in different sections
            event_sections = [
                soup.find_all('div', class_='event-item'),
                soup.find_all('div', class_='event-card'),
                soup.find_all('article'),
                soup.find_all('div', class_='event'),
                soup.find_all('div', class_='event-list-item'),
                soup.find_all('div', class_='event-section')
            ]
            
            for section in event_sections:
                if section:
                    for event in section:
                        # Extract event information
                        title = None
                        date = None
                        location = None
                        description = None
                        
                        # Try to find title - more comprehensive approach
                        title_elem = None
                        # First try common title classes
                        for class_name in ['title', 'event-title', 'event-name', 'event-heading']:
                            title_elem = event.find(class_=class_name)
                            if title_elem:
                                break
                        
                        # If not found, try heading tags
                        if not title_elem:
                            for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                                title_elem = event.find(tag)
                                if title_elem:
                                    break
                        
                        # If still not found, try finding any text that looks like a title
                        if not title_elem:
                            # Look for text that's not too long and not too short
                            for elem in event.find_all(['div', 'span', 'p']):
                                text = elem.get_text(strip=True)
                                if 5 < len(text) < 100 and not any(keyword in text.lower() for keyword in ['địa điểm', 'location', 'date', 'time']):
                                    title_elem = elem
                                    break
                        
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                        
                        # Try to find date
                        date_elem = (
                            event.find('time') or
                            event.find(['span', 'div'], class_=['date', 'event-date', 'time', 'event-time']) or
                            event.find('div', string=lambda text: text and any(keyword in text.lower() for keyword in ['ngày', 'date', 'thời gian', 'time']))
                        )
                        if date_elem:
                            date = date_elem.get_text(strip=True)
                        
                        # Try to find location
                        location_elem = (
                            event.find(['span', 'div'], class_=['location', 'event-location', 'venue', 'event-venue']) or
                            event.find('div', string=lambda text: text and any(keyword in text.lower() for keyword in ['địa điểm', 'location', 'venue']))
                        )
                        if location_elem:
                            location = location_elem.get_text(strip=True)
                        
                        # Try to find description
                        desc_elem = (
                            event.find(['div', 'p'], class_=['description', 'event-description', 'content', 'event-content']) or
                            event.find('p')
                        )
                        if desc_elem:
                            description = desc_elem.get_text(strip=True)
                        
                        # If we found any information, create an event
                        if any([title, date, location, description]):
                            # Combine location into description if available
                            full_description = []
                            if location:
                                full_description.append(f"Location: {location}")
                            if description:
                                full_description.append(description)
                            
                            events.append({
                                "id": f"web_{len(events) + 1}",
                                "title": title or "No title",
                                "description": "\n".join(full_description) if full_description else "",
                                "date": date or ""
                            })
                    break  # Stop after finding the first valid section
            
            # If no events found with specific classes, try finding by content
            if not events:
                for div in soup.find_all('div'):
                    text = div.get_text(strip=True)
                    if any(keyword in text.lower() for keyword in ['sự kiện', 'event', 'hội thảo', 'seminar']):
                        if len(text) > 5:  # Only add if text seems valid
                            events.append({
                                "id": f"web_{len(events) + 1}",
                                "title": text,
                                "description": "",
                            })
            
            # Save events to JSON file
            with open('web_events.json', 'w', encoding='utf-8') as f:
                json.dump({"events": events}, f, ensure_ascii=False, indent=4)
                
            return True
        except Exception as e:
            print(f"Error scraping web events: {str(e)}")
            return False

    def get_web_events(self) -> List[Event]:
        """Get events from JSON file"""
        try:
            # First try to scrape and save new events
            self.scrape_and_save_web_events()
            
            # Then read from the JSON file
            with open('web_events.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                events = []
                for event_data in data['events']:
                    # Add date to description if available
                    description = event_data.get('description', '')
                    date = event_data.get('date', '')
                    if date:
                        description = f"Date: {date}\n{description}"
                    
                    event = Event(
                        id=event_data.get('id', ''),
                        title=event_data.get('title', 'No title'),
                        description=description,
                        assigned_users=[]  # Web events don't have assigned users
                    )
                    events.append(event)
                return events
        except Exception as e:
            print(f"Error reading web events: {str(e)}")
            return []