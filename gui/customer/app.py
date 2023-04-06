import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback
import json

from .create import CustomerCreateApp # pylint: disable=relative-beyond-top-level

from .fetch import CustomerFetchApp # pylint: disable=relative-beyond-top-level

class CustomerApp(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.user = self.parent.user
    
        self.geometry(f"{1100}x{580}")
        self.title("Customer")
        self.label = customtkinter.CTkLabel(self, text="Customer")
        self.label.pack(padx=20, pady=20)
        self.attributes('-topmost', True)  # for focus on toplevel
        self.build_menu()
        
        self.fetch = None

    def build_menu(self):
        # Create customer ID label and entry
        # Create button to fetch customer info
        self.fetch_button = customtkinter.CTkButton(
            self, text="Hae", command=self.open_search)
        self.fetch_button.pack(pady=10)

        self.create_button = customtkinter.CTkButton(
            self, text="Luo", command=self.open_create)
        
        self.create_button.pack(pady=10)
        # Create exit button
        self.exit_button = customtkinter.CTkButton(
            self, text="Poistu", command=self.destroy)
        self.exit_button.pack(pady=10)

    def shut(self, window):
        window.destroy()
        self.attributes('-topmost', True)  # for focus on topleve

    def open_search(self):
        open_window = CustomerFetchApp(self)
        open_window.focus()
        
    def open_create(self):
        open_window = CustomerCreateApp(self)
        open_window.focus()
