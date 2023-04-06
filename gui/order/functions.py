import requests
import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

from torch import e
import customtkinter
import requests
import traceback


def show_technical_details(technical_details):
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


def create_error_window():
    popup_window = tk.Toplevel()
    popup_window.title("Error")
    popup_window.geometry("300x200")

    error_label = customtkinter.CTkLabel(
        popup_window, text=f"Error: {e}")
    error_label.pack(pady=10)

    show_details_button = customtkinter.CTkButton(
        popup_window, text="Show Technical Details", command=lambda: show_technical_details(traceback.format_exc()))
    show_details_button.pack(pady=10)

    close_button = customtkinter.CTkButton(
        popup_window, text="Close", command=popup_window.destroy)
    close_button.pack(pady=10)


def send_order(self):
    data = {"order": []}
    order = data["order"]
    for product in self.products:
        value = product[2].get()
        order.append(
            {"name": product[0], "price": int(product[1]), "count": int(value)})

    data["customer"] = int(self.customer_entry.get())  # type: ignore

    orders_url = f"https://api.ordersystem.luova.club/orders/"
    headers = {"Content-Type": "application/json",
               "user": self.user["username"], "password": self.user["password"]}

    try:
        order_response = requests.post(
            orders_url, json=data, headers=headers, timeout=20)
        order_response.raise_for_status()

    except requests.exceptions.RequestException as e:
        create_error_window()


def add_products_to_popup(self, order_info, popup_window):
    for product in order_info["Order"]:
        label = customtkinter.CTkLabel(
            master=popup_window, text=f'{product["name"]} {product["price"]}€')
        label.pack()
        entry = customtkinter.CTkEntry(
            master=popup_window, placeholder_text="1")
        entry.pack(padx=20, pady=10)
        entry.insert(0, product["count"])
        entry.configure(state="disabled")
        self.products.append(
            (product["name"], product["price"], entry))


def setup_popup_defaults(order_info, popup_window):
    label = customtkinter.CTkLabel(
        master=popup_window, text='Asiakas ID:')
    label.pack()
    entry = customtkinter.CTkEntry(
        master=popup_window, placeholder_text="1")
    entry.pack(padx=20, pady=10)
    entry.insert(0, order_info["Customer"])
    entry.configure(state="disabled")


def create_popup():
    popup_window = customtkinter.CTkToplevel()
    popup_window.title("Tilauksen tiedot")
    popup_window.geometry("300x500")
    popup_window.attributes('-topmost', True)
    return popup_window
