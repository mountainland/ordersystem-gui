import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback


class OrderApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{1100}x{580}")
        self.title("Order")
        self.focus()
        self.label = customtkinter.CTkLabel(self, text="Order")
        self.label.pack(padx=20, pady=20)
        self.products = []
        self.build_main()
        # self.grab_set()
        self.attributes('-topmost', True)  # for focus on toplevel

    def build_main(self):
        self.products = []
        products_url = f"https://api.ordersystem.luova.club/products/"
        product_response = requests.get(products_url)
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
            self, text="Submit", command=self.send_order)
        self.send_button.pack(pady=10)
            
        self.exit_button = customtkinter.CTkButton(
            self, text="Exit", command=self.destroy)
        self.exit_button.pack(pady=10)

    def send_order(self):
        data = {"order": []}
        order = data["order"]
        for product in self.products:
            value = product[2].get()
            order.append(
                {"name": product[0], "price": int(product[1]), "count": int(value)})

        data["customer"] = int(self.customer_entry.get()) # type: ignore

        orders_url = f"https://api.ordersystem.luova.club/orders/"
        try:
            order_response = requests.post(orders_url, json=data)
            #order_response.raise_for_status()
            
            

        except requests.exceptions.RequestException as e:
            # Show error message and technical details in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Error")
            popup_window.geometry("300x200")

            error_label = customtkinter.CTkLabel(
                popup_window, text=f"Error: {e}")
            error_label.pack(pady=10)

            show_details_button = customtkinter.CTkButton(
                popup_window, text="Show Technical Details", command=lambda: self.show_technical_details(traceback.format_exc()))
            show_details_button.pack(pady=10)

            close_button = customtkinter.CTkButton(
                popup_window, text="Close", command=popup_window.destroy)
            close_button.pack(pady=10)
            
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