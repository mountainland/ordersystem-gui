import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

from torch import e
import customtkinter
import requests
import traceback

from .functions import send_order  # pylint: disable=relative-beyond-top-level


class OrderCreateApp(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(f"{1100}x{580}")
        self.user = parent.user

        self.title("Order")
        self.focus()
        self.label = customtkinter.CTkLabel(self, text="Tilauksen luominen")
        self.label.pack(padx=20, pady=20)
        self.products = []
        self.build_main()
        # self.grab_set()
        self.attributes('-topmost', True)  # for focus on toplevel

    def build_main(self):
        self.products = []
        products_url = f"https://api.ordersystem.luova.club/products/"
        headers = {"Content-Type": "application/json",
                   "user": self.user["username"], "password": self.user["password"]}

        product_response = requests.get(products_url, headers=headers)
        product_response.raise_for_status()
        products_data = product_response.json()
        products = products_data["products"]

        label = customtkinter.CTkLabel(master=self, text=f'Customer id:')
        label.pack()
        self.customer_entry = customtkinter.CTkEntry(
            master=self, placeholder_text=f"1")
        self.customer_entry.pack(padx=20, pady=10)

        for product in products:

            label = customtkinter.CTkLabel(
                master=self, text=f'{product["Name"]} {product["Price"]}€')
            label.pack()
            entry = customtkinter.CTkEntry(master=self, placeholder_text=f"1")
            entry.pack(padx=20, pady=10)
            self.products.append((product["Name"], product["Price"], entry))

        self.send_button = customtkinter.CTkButton(
            self, text="Submit", command=lambda: send_order(self))
        self.send_button.pack(pady=10)

        self.exit_button = customtkinter.CTkButton(
            self, text="Poistu", command=self.destroy)
        self.exit_button.pack(pady=10)
