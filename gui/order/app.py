import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback

from .fetch import OrderSearchApp  # pylint: disable=relative-beyond-top-level

from .create import OrderCreateApp  # pylint: disable=relative-beyond-top-level


class OrderApp(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.user = parent.user

        self.geometry(f"{1100}x{580}")
        self.title("Customer")
        self.label = customtkinter.CTkLabel(self, text="Customer")
        self.label.pack(padx=20, pady=20)
        self.attributes('-topmost', True)  # for focus on toplevel
        self.build_menu()

        self.fetch = None

    def build_menu(self):
        self.fetch_button = customtkinter.CTkButton(
            self, text="Hae", command=self.open_search)
        self.fetch_button.pack(pady=10)

        self.create_button = customtkinter.CTkButton(
            self, text="Luo", command=self.open_create)
        self.create_button.pack(pady=10)

        self.exit_button = customtkinter.CTkButton(
            self, text="Poistu", command=self.destroy)
        self.exit_button.pack(pady=10)

    def shut(self, window):
        window.destroy()
        self.attributes('-topmost', True)  # for focus on topleve

    def open_search(self):
        open_window = OrderSearchApp(self)
        open_window.focus()

    def open_create(self):
        open_window = OrderCreateApp(self)
        open_window.focus()
