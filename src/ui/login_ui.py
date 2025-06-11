import customtkinter as ctk
from typing import Callable
from src.model.user import User
from src.service.user_service import UserService
from src.ui.base_ui import BaseUI

class LoginUI(BaseUI):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        user_service: UserService,
        on_login_success: Callable[[User], None]
    ):
        super().__init__()
        self.parent = parent
        self.user_service = user_service
        self.on_login_success = on_login_success
        
        self.setup_ui()

    def setup_ui(self):
        # Create login form
        form_frame = ctk.CTkFrame(self.parent)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            form_frame,
            text="Login",
            font=("Arial", 24)
        ).pack(pady=20)
        
        # Username
        ctk.CTkLabel(form_frame, text="Username:").pack(pady=5)
        self.username_entry = ctk.CTkEntry(form_frame)
        self.username_entry.pack(pady=5)
        
        # Password
        ctk.CTkLabel(form_frame, text="Password:").pack(pady=5)
        self.password_entry = ctk.CTkEntry(form_frame, show="*")
        self.password_entry.pack(pady=5)
        
        # Login button
        ctk.CTkButton(
            form_frame,
            text="Login",
            command=self.login
        ).pack(pady=10)
        
        # Register button
        ctk.CTkButton(
            form_frame,
            text="Register",
            command=self.show_register
        ).pack(pady=10)
        
        # Guest login button
        ctk.CTkButton(
            form_frame,
            text="Continue as Guest",
            command=self.guest_login
        ).pack(pady=10)
        
        # Error message
        self.error_label = ctk.CTkLabel(
            form_frame,
            text="",
            text_color="red"
        )
        self.error_label.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            user = self.user_service.authenticate_user(username, password)
            if user:
                self.on_login_success(user)
            else:
                self.error_label.configure(text="Invalid username or password")
        except Exception as e:
            self.error_label.configure(text=str(e))

    def show_register(self):
        # Create register dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Register")
        dialog.geometry("400x300")
        
        # Create form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            form_frame,
            text="Create Account",
            font=("Arial", 24)
        ).pack(pady=20)
        
        # Username
        ctk.CTkLabel(form_frame, text="Username:").pack(pady=5)
        username_entry = ctk.CTkEntry(form_frame)
        username_entry.pack(pady=5)
        
        # Password
        ctk.CTkLabel(form_frame, text="Password:").pack(pady=5)
        password_entry = ctk.CTkEntry(form_frame, show="*")
        password_entry.pack(pady=5)
        
        # Confirm Password
        ctk.CTkLabel(form_frame, text="Confirm Password:").pack(pady=5)
        confirm_password_entry = ctk.CTkEntry(form_frame, show="*")
        confirm_password_entry.pack(pady=5)
        
        # Error message
        error_label = ctk.CTkLabel(
            form_frame,
            text="",
            text_color="red"
        )
        error_label.pack(pady=5)
        
        def register():
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if not username or not password:
                error_label.configure(text="Username and password are required")
                return
                
            if password != confirm_password:
                error_label.configure(text="Passwords do not match")
                return
            
            try:
                user = self.user_service.register_user(username, password)
                if user:
                    dialog.destroy()
                    self.error_label.configure(text="Registration successful! Please login.")
                else:
                    error_label.configure(text="Username already exists")
            except Exception as e:
                error_label.configure(text=str(e))
        
        # Register button
        ctk.CTkButton(
            form_frame,
            text="Register",
            command=register
        ).pack(pady=20)

    def guest_login(self):
        guest = User(
            username="guest",
            password="",
            role="guest",
            assigned_events=[]
        )
        self.on_login_success(guest) 