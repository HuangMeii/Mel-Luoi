import customtkinter as ctk
from typing import Optional, Callable

class BaseUI:
    def __init__(self, parent: Optional[ctk.CTk] = None):
        self.parent = parent or ctk.CTk()
        self.setup_theme()

    def setup_theme(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def show_error(self, message: str, callback: Optional[Callable] = None):
        error_window = ctk.CTkToplevel(self.parent)
        error_window.title("Error")
        error_window.geometry("300x100")
        
        ctk.CTkLabel(error_window, text=message).pack(pady=20)
        ctk.CTkButton(
            error_window,
            text="OK",
            command=lambda: [error_window.destroy(), callback() if callback else None]
        ).pack()

    def show_success(self, message: str, callback: Optional[Callable] = None):
        success_window = ctk.CTkToplevel(self.parent)
        success_window.title("Success")
        success_window.geometry("300x100")
        
        ctk.CTkLabel(success_window, text=message).pack(pady=20)
        ctk.CTkButton(
            success_window,
            text="OK",
            command=lambda: [success_window.destroy(), callback() if callback else None]
        ).pack()

    def clear_container(self, container: ctk.CTkFrame):
        for widget in container.winfo_children():
            widget.destroy() 