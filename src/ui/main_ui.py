import customtkinter as ctk
from typing import Optional
from src.model.user import User
from src.service.user_service import UserService
from src.service.event_service import EventService
from src.ui.base_ui import BaseUI
from src.ui.login_ui import LoginUI
from src.ui.event_ui import EventUI
from src.ui.user_ui import UserUI

class MainUI(BaseUI):
    def __init__(self, user_service: UserService, event_service: EventService):
        super().__init__()
        self.user_service = user_service
        self.event_service = event_service
        self.current_user: Optional[User] = None
        
        self.setup_window()
        self.show_login()

    def setup_window(self):
        self.parent.title("Event Management System")
        self.parent.geometry("800x600")
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.parent)
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)

    def show_login(self):
        self.clear_container(self.main_container)
        login_ui = LoginUI(
            self.main_container,
            self.user_service,
            on_login_success=self.on_login_success
        )

    def on_login_success(self, user: User):
        self.current_user = user
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_container(self.main_container)
        
        # Add navigation buttons based on user role
        if self.current_user.role == 'admin':
            ctk.CTkButton(
                self.main_container,
                text="Manage Events",
                command=self.show_event_management
            ).pack(pady=10)
            
            ctk.CTkButton(
                self.main_container,
                text="Manage Users",
                command=self.show_user_management
            ).pack(pady=10)
            
            ctk.CTkButton(
                self.main_container,
                text="View Events",
                command=self.show_events
            ).pack(pady=10)
        
        elif self.current_user.role == 'user':
            ctk.CTkButton(
                self.main_container,
                text="View Events",
                command=self.show_events
            ).pack(pady=10)
        
        # Web events and logout buttons for all users
        ctk.CTkButton(
            self.main_container,
            text="View Web Events",
            command=self.show_web_events
        ).pack(pady=10)
        
        ctk.CTkButton(
            self.main_container,
            text="Logout",
            command=self.logout
        ).pack(pady=10)

    def show_event_management(self):
        self.clear_container(self.main_container)
        EventUI(
            self.main_container,
            self.event_service,
            self.user_service,
            self.current_user,
            on_back=self.show_main_menu
        )

    def show_user_management(self):
        self.clear_container(self.main_container)
        user_ui = UserUI(
            self.main_container,
            self.user_service,
            self.current_user,
            on_back=self.show_main_menu
        )

    def show_events(self):
        self.clear_container(self.main_container)
        EventUI(
            self.main_container,
            self.event_service,
            self.user_service,
            self.current_user,
            view_only=True,
            on_back=self.show_main_menu
        )

    def show_web_events(self):
        self.clear_container(self.main_container)
        EventUI(
            self.main_container,
            self.event_service,
            self.user_service,
            self.current_user,
            web_only=True,
            on_back=self.show_main_menu
        )

    def logout(self):
        self.current_user = None
        self.show_login()

    def run(self):
        self.parent.mainloop() 