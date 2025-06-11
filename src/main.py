import customtkinter as ctk
from src.repository.user_repository import UserRepository
from src.repository.event_repository import EventRepository
from src.service.user_service import UserService
from src.service.event_service import EventService
from src.ui.main_ui import MainUI

def main():
    # Initialize repositories
    user_repository = UserRepository()
    event_repository = EventRepository()
    
    # Initialize services
    user_service = UserService(user_repository)
    event_service = EventService(event_repository, user_repository)
    
    # Create default admin user if no users exist
    if not user_repository.get_all_users():
        user_service.register_user('admin', 'admin123', 'admin')
    
    # Initialize and run UI
    root = ctk.CTk()
    app = MainUI(user_service, event_service)
    app.run()

if __name__ == "__main__":
    main() 