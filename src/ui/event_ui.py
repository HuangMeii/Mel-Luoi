import customtkinter as ctk
from typing import Callable, Optional
from src.model.user import User
from src.model.event import Event
from src.service.event_service import EventService
from src.service.user_service import UserService
from src.ui.base_ui import BaseUI

class EventUI(BaseUI):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        event_service: EventService,
        user_service: UserService,
        current_user: User,
        view_only: bool = False,
        web_only: bool = False,
        on_back: Optional[Callable[[], None]] = None
    ):
        super().__init__()
        self.parent = parent
        self.event_service = event_service
        self.user_service = user_service
        self.current_user = current_user
        self.view_only = view_only
        self.web_only = web_only
        self.on_back = on_back
        
        self.setup_ui()
        self.load_events()

    def setup_ui(self):
        # Create main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title = "View Events" if self.view_only else "Manage Events"
        if self.web_only:
            title = "Web Events"
        ctk.CTkLabel(
            self.main_frame,
            text=title,
            font=("Arial", 24)
        ).pack(pady=20)

        # Add search box only if not viewing web events
        if not self.web_only:
            search_frame = ctk.CTkFrame(self.main_frame)
            search_frame.pack(pady=10, padx=20, fill="x")
            
            ctk.CTkLabel(search_frame, text="Search by title:").pack(side="left", padx=5)
            self.search_entry = ctk.CTkEntry(search_frame)
            self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
            
            ctk.CTkButton(
                search_frame,
                text="Search",
                command=self.search_events
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                search_frame,
                text="Delete",
                command=self.clear_search
            ).pack(side="left", padx=5)
        
        # Create event form if not view only
        if not self.view_only and not self.web_only:
            self.create_event_form()
        
        # Create event list
        self.create_event_list()
        
        # Back button
        if self.on_back:
            ctk.CTkButton(
                self.main_frame,
                text="Back",
                command=self.on_back
            ).pack(pady=20)

    def create_event_form(self):
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Title
        ctk.CTkLabel(form_frame, text="Title:").pack(pady=5)
        self.title_entry = ctk.CTkEntry(form_frame)
        self.title_entry.pack(pady=5)
        
        # Description
        ctk.CTkLabel(form_frame, text="Description:").pack(pady=5)
        self.description_entry = ctk.CTkEntry(form_frame)
        self.description_entry.pack(pady=5)
        
        # Add button
        ctk.CTkButton(
            form_frame,
            text="Add Event",
            command=self.add_event
        ).pack(pady=20)

    def create_event_list(self):
        # Create scrollable frame for events
        self.events_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.events_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)

    def load_events(self):
        try:
            # Clear existing events
            for widget in self.events_frame.winfo_children():
                widget.destroy()
            
            # Get events based on mode
            if self.web_only:
                events = self.event_service.get_web_events()
            else:
                # For regular users, only show assigned events
                if self.current_user.role == "user":
                    events = self.event_service.get_user_events(self.current_user.username)
                else:
                    events = self.event_service.get_events()
            
            if not events:
                no_events_label = ctk.CTkLabel(
                    self.events_frame,
                    text="No events yet",
                    font=("Arial", 14)
                )
                no_events_label.pack(pady=20)
                return
            
            # Add events to the container
            for event in events:
                self.create_event_widget(event)
                
        except Exception as e:
            self.show_error(f"Error loading event list: {str(e)}")

    def create_event_widget(self, event: Event):
        frame = ctk.CTkFrame(self.events_frame)
        frame.pack(fill="x", padx=10, pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            frame,
            text=event.title,
            font=("Arial", 14, "bold")
        )
        title_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Description
        if event.description:
            desc_label = ctk.CTkLabel(
                frame,
                text=event.description,
                font=("Arial", 12)
            )
            desc_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Buttons frame
        if not self.view_only and not self.web_only:
            btn_frame = ctk.CTkFrame(frame)
            btn_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            # Edit button
            edit_btn = ctk.CTkButton(
                btn_frame,
                text="Edit",
                command=lambda: self.edit_event(event),
                width=60
            )
            edit_btn.pack(side="left", padx=5)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                btn_frame,
                text="Delete",
                command=lambda: self.delete_event(event),
                width=60,
                fg_color="red",
                hover_color="darkred"
            )
            delete_btn.pack(side="left", padx=5)

            # Assign Users button (only for admin)
            if self.current_user.role == "admin":
                assign_btn = ctk.CTkButton(
                    btn_frame,
                    text="Assignment",
                    command=lambda: self.show_assign_users(event),
                    width=80
                )
                assign_btn.pack(side="left", padx=5)

    def add_event(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        
        if not title:
            self.show_error("Please enter event title")
            return
            
        try:
            event = self.event_service.create_event(title, description)
            if event:
                # Clear input fields
                self.title_entry.delete(0, "end")
                self.description_entry.delete(0, "end")
                
                # Reload events
                self.load_events()
                
                # Show success message
                self.show_success("Add event successfully!")
        except Exception as e:
            self.show_error(f"Error adding event: {str(e)}")

    def edit_event(self, event: Event):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Edit Event")
        dialog.geometry("400x300")
        
        # Title
        ctk.CTkLabel(dialog, text="Title:").pack(pady=5)
        title_entry = ctk.CTkEntry(dialog)
        title_entry.insert(0, event.title)
        title_entry.pack(pady=5)
        
        # Description
        ctk.CTkLabel(dialog, text="Description:").pack(pady=5)
        description_entry = ctk.CTkEntry(dialog)
        description_entry.insert(0, event.description or "")
        description_entry.pack(pady=5)
        
        def save():
            try:
                event.title = title_entry.get()
                event.description = description_entry.get()
                self.event_service.update_event(event)
                dialog.destroy()
                self.load_events()
                self.show_success("Event update successful!")
            except Exception as e:
                self.show_error(str(e))
        
        ctk.CTkButton(
            dialog,
            text="Save",
            command=save
        ).pack(pady=20)

    def delete_event(self, event: Event):
        try:
            self.event_service.delete_event(event.id)
            self.load_events()
            self.show_success("Event deleted successfully!")
        except Exception as e:
            self.show_error(str(e))

    def show_assign_users(self, event: Event):
        # Create assign users dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("User assignment")
        dialog.geometry("400x500")
        
        # Title
        ctk.CTkLabel(
            dialog,
            text=f"Assign users to event: {event.title}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Create scrollable frame for user list
        scroll_frame = ctk.CTkScrollableFrame(dialog)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Get all users
        users = self.user_service.get_all_users()
        user_vars = {}
        
        # Create checkboxes for each user
        for username, user in users.items():
            if user.role == "user":  # Only show regular users
                var = ctk.BooleanVar(value=username in event.assigned_users)
                user_vars[username] = var
                
                user_frame = ctk.CTkFrame(scroll_frame)
                user_frame.pack(fill="x", pady=5)
                
                ctk.CTkCheckBox(
                    user_frame,
                    text=username,
                    variable=var
                ).pack(side="left", padx=10)
        
        def save_assignments():
            # Get selected users
            selected_users = [
                username for username, var in user_vars.items()
                if var.get()
            ]
            
            # Update event assignments
            self.event_service.assign_users_to_event(event.id, selected_users)
            
            # Show success message
            self.show_success("Successful user assignment!")
            
            # Close dialog and refresh event list
            dialog.destroy()
            self.load_events()
        
        # Save button
        ctk.CTkButton(
            dialog,
            text="Save",
            command=save_assignments
        ).pack(pady=10)

    def search_events(self):
        search_text = self.search_entry.get().lower()
        try:
            # Clear existing events
            for widget in self.events_frame.winfo_children():
                widget.destroy()
            
            # Get events based on mode
            if self.web_only:
                events = self.event_service.get_web_events()
            else:
                # For regular users, only show assigned events
                if self.current_user.role == "user":
                    events = self.event_service.get_user_events(self.current_user.username)
                else:
                    events = self.event_service.get_events()
            
            # Filter events by title
            if search_text:
                events = [event for event in events if search_text in event.title.lower()]
            
            if not events:
                no_events_label = ctk.CTkLabel(
                    self.events_frame,
                    text="No events found",
                    font=("Arial", 14)
                )
                no_events_label.pack(pady=20)
                return
            
            # Add events to the container
            for event in events:
                self.create_event_widget(event)
                
        except Exception as e:
            self.show_error(f"Error while searching for event: {str(e)}")

    def clear_search(self):
        # Clear the search entry
        self.search_entry.delete(0, "end")
        # Reload all events
        self.load_events()

    def show_error(self, message: str):
        error_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            text_color="red"
        )
        error_label.pack(pady=5)
        self.parent.after(3000, error_label.destroy)

    def show_success(self, message: str):
        success_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            text_color="green"
        )
        success_label.pack(pady=5)
        self.parent.after(3000, success_label.destroy) 