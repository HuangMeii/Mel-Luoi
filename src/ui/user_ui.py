import customtkinter as ctk
from typing import Callable
from ..model.user import User
from ..service.user_service import UserService
from .base_ui import BaseUI

class UserUI(BaseUI):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        user_service: UserService,
        current_user: User,
        on_back: Callable
    ):
        super().__init__(parent)
        self.user_service = user_service
        self.current_user = current_user
        self.on_back = on_back
        
        self.setup_ui()

    def setup_ui(self):
        self.clear_container(self.parent)
        
        ctk.CTkLabel(self.parent, text="User Management", font=("Arial", 20)).pack(pady=20)
        
        # Create user list
        user_frame = ctk.CTkFrame(self.parent)
        user_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Add user button
        ctk.CTkButton(
            user_frame,
            text="Add New User",
            command=self.show_add_user
        ).pack(pady=10)
        
        # User list
        for username, user_data in self.user_service.get_all_users().items():
            if username != self.current_user.username:  # Don't show current user
                self.create_user_card(user_frame, username, user_data)
        
        # Back button
        ctk.CTkButton(self.parent, text="Back", command=self.on_back).pack(pady=10)

    def create_user_card(self, parent: ctk.CTkFrame, username: str, user: User):
        user_card = ctk.CTkFrame(parent)
        user_card.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(user_card, text=f"Username: {username}").pack(side="left", padx=10)
        ctk.CTkLabel(user_card, text=f"Role: {user.role}").pack(side="left", padx=10)
        
        ctk.CTkButton(
            user_card,
            text="Edit",
            command=lambda: self.show_edit_user(username, user)
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            user_card,
            text="Delete",
            command=lambda: self.delete_user(username)
        ).pack(side="right", padx=5)

    def show_add_user(self):
        window = ctk.CTkToplevel(self.parent)
        window.title("Add User")
        window.geometry("400x400")
        
        ctk.CTkLabel(window, text="Add New User", font=("Arial", 20)).pack(pady=20)
        
        username_entry = ctk.CTkEntry(window, placeholder_text="Username")
        username_entry.pack(pady=10, padx=20)
        
        password_entry = ctk.CTkEntry(window, placeholder_text="Password", show="*")
        password_entry.pack(pady=10, padx=20)
        
        role_var = ctk.StringVar(value="user")
        ctk.CTkLabel(window, text="Role:").pack(pady=5)
        ctk.CTkRadioButton(window, text="User", variable=role_var, value="user").pack()
        ctk.CTkRadioButton(window, text="Admin", variable=role_var, value="admin").pack()
        
        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            
            if username and password:
                user = self.user_service.register_user(username, password, role)
                if user:
                    window.destroy()
                    self.show_success("User added successfully!", self.setup_ui)
                else:
                    self.show_error("Username already exists")
            else:
                self.show_error("Please fill all fields")
        
        ctk.CTkButton(window, text="Save User", command=save_user).pack(pady=20)

    def show_edit_user(self, username: str, user: User):
        window = ctk.CTkToplevel(self.parent)
        window.title("Edit User")
        window.geometry("400x400")
        
        ctk.CTkLabel(window, text="Edit User", font=("Arial", 20)).pack(pady=20)
        
        password_entry = ctk.CTkEntry(window, placeholder_text="New Password", show="*")
        password_entry.pack(pady=10, padx=20)
        
        role_var = ctk.StringVar(value=user.role)
        ctk.CTkLabel(window, text="Role:").pack(pady=5)
        ctk.CTkRadioButton(window, text="User", variable=role_var, value="user").pack()
        ctk.CTkRadioButton(window, text="Admin", variable=role_var, value="admin").pack()
        
        def save_changes():
            password = password_entry.get()
            role = role_var.get()
            
            if password:
                updated_user = self.user_service.update_user(username, password, role)
                if updated_user:
                    window.destroy()
                    self.show_success("User updated successfully!", self.setup_ui)
                else:
                    self.show_error("Failed to update user")
            else:
                self.show_error("Please enter a new password")
        
        ctk.CTkButton(window, text="Save Changes", command=save_changes).pack(pady=20)

    def delete_user(self, username: str):
        if self.user_service.delete_user(username):
            self.show_success("User deleted successfully!", self.setup_ui)
        else:
            self.show_error("Failed to delete user") 