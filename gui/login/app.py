import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback


class LoginWindow(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Login")
        self.geometry("300x500")
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.bind("<Alt-F4>", lambda event: None)
        self.bind("<Control-w>", lambda event: None)
        self.bind("<Control-W>", lambda event: None)

        # Create login form
        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_label.pack(pady=10)

        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.pack(pady=5)

        self.password_label = customtkinter.CTkLabel(self, text="Password:")
        self.password_label.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = customtkinter.CTkButton(
            self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.error_label = customtkinter.CTkLabel(self)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        
        url = "http://api.ordersystem.luova.club:8081/login/"

        payload={}
        headers = {
        'user': username,
        'password': password
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if not response.status_code == 401:
            self.destroy()
            self.parent.logged_in = True
            self.parent.username = username
            self.parent.password = password
        else:
            self.error_label.config(text="Invalid username or password")
            self.error_label.pack(pady=10)
