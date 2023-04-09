
import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback
import json

from .functions import create_error_window, add_products_to_popup, setup_popup_defaults, create_popup  # pylint: disable=relative-beyond-top-level


class OrderSearchApp(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(f"{1100}x{580}") # TODO: #1 figure out, why this is f string

        self.user = parent.user

        self.title("Tilaus")
        self.focus()
        self.label = customtkinter.CTkLabel(self, text="Tilauksen hakeminen")
        self.label.pack(padx=20, pady=20)
        self.build_menu()
        self.products = []
        # self.grab_set()
        self.attributes('-topmost', True)  # for focus on toplevel

    def build_menu(self):
        # Create customer ID label and entry
        self.order_id_label = customtkinter.CTkLabel(
            self, text="Tilaus ID:")
        self.order_id_label.pack(pady=10)

        self.order_id_entry = customtkinter.CTkEntry(self)
        self.order_id_entry.pack(pady=5)

        # Create button to fetch customer info
        self.fetch_button = customtkinter.CTkButton(
            self, text="Hae tiedot", command=self.fetch_order_info)
        self.fetch_button.pack(pady=10)

        # Create exit button
        self.exit_button = customtkinter.CTkButton(
            self, text="Poistu", command=self.destroy)
        self.exit_button.pack(pady=10)

    def fetch_order_info(self):
        order_url = f"https://api.ordersystem.luova.club/order/{self.order_id_entry.get()}"
        headers = {"Content-Type": "application/json",
                   "user": self.user["username"], "password": self.user["password"]}

        try:
            order_info = self.get_order(order_url, headers)
            self.order_info = order_info

            self.attributes('-topmost', False)  # for focus on topleve

            # Create popup window with customer info and editing fields
            popup_window = create_popup()  # Create popup window

            setup_popup_defaults(order_info, popup_window)             # put order info things to popup window


            # Add products in order to popup window
            add_products_to_popup(self, order_info, popup_window)

            order_is_ready_label = customtkinter.CTkLabel(
                popup_window, text="Valmiina:")
            order_is_ready_label.pack(pady=5)

            entry = customtkinter.CTkEntry(
                master=popup_window, placeholder_text="1")
            entry.pack(padx=20, pady=10)
            isready = "Ei"
            if order_info["is_ready"] is True:
                isready = "Kyllä"
            entry.insert(0, isready)
            entry.configure(state="disabled")

            label = customtkinter.CTkLabel(
                master=popup_window, text='Kokonaishinta:')
            label.pack()
            entry = customtkinter.CTkEntry(
                master=popup_window, placeholder_text="1")
            entry.pack(padx=20, pady=10)
            entry.insert(0, order_info["price"])
            entry.configure(state="disabled")

            close_button = customtkinter.CTkButton(
                popup_window, text="Poistu", command=popup_window.destroy)  # Define close button
            close_button.pack(pady=10)
            
            ready_button = customtkinter.CTkButton(
                popup_window, text="Tilaus valmis", command=self.mark_ready
            )
            ready_button.pack(pady=10)

        except requests.exceptions.RequestException as e:
            create_error_window()

    def mark_ready(self):
        orders_url = f"https://api.ordersystem.luova.club/order/{self.order_id_entry.get()}"
        headers = {"Content-Type": "application/json",
                "user": self.user["username"], "password": self.user["password"]}

        data = {"is_ready": True}
        
        order_response = requests.post(
            orders_url, json=data, headers=headers, timeout=20)
        order_response.raise_for_status()
            
    def get_order(self, order_url, headers):
        order_response = requests.get(order_url, headers=headers)
        order_response.raise_for_status()
        text = order_response.text.replace("'", '"').replace("False", "false").replace("True", "true")
        print(text)

        order_info = json.loads(text)
        return order_info

    def show_technical_details(self, technical_details):
        # Show technical details in popup window
        popup_window = tk.Toplevel()
        popup_window.title("Technical Details")
        popup_window.geometry("500x300")

        technical_details_label = customtkinter.CTkLabel(
            popup_window, text=technical_details)
        technical_details_label.pack(pady=10)

        close_button = customtkinter.CTkButton(
            popup_window, text="Close", command=popup_window.destroy)
        close_button.pack(pady=10)
