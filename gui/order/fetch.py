
import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback
import json

class OrderSearchApp(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(f"{1100}x{580}")
        self.username = parent.username
        self.password = parent.password
        self.title("Order")
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
        headers = {"Content-Type": "application/json", "user": self.username, "password": self.password}

        try:
            order_response = requests.get(order_url, headers=headers)
            order_response.raise_for_status()    
            print(order_response.text)
            text = order_response.text.replace("'", '"').replace("False", "false")
            print(text)
            order_info = json.loads(text)
            self.order_info = order_info

            #order_info = customer_response.json()
            self.attributes('-topmost', False)  # for focus on topleve
            # Create popup window with customer info and editing fields
            popup_window = customtkinter.CTkToplevel()
            popup_window.title("Tilauksen tiedot")
            popup_window.geometry("300x500")
            popup_window.attributes('-topmost', True)  # for focus on toplevel
            
            label = customtkinter.CTkLabel(
                    master=popup_window, text=f'Asiakas ID:')
            label.pack()
            entry = customtkinter.CTkEntry(master=popup_window, placeholder_text=f"1")
            entry.pack(padx=20, pady=10)
            entry.insert(0, order_info["Customer"])
            entry.configure(state="disabled")
            
            
            for product in order_info["Order"]:

                label = customtkinter.CTkLabel(
                    master=popup_window, text=f'{product["name"]} {product["price"]}€')
                label.pack()
                entry = customtkinter.CTkEntry(master=popup_window, placeholder_text=f"1")
                entry.pack(padx=20, pady=10)
                entry.insert(0, product["count"])
                entry.configure(state="disabled")
                self.products.append((product["name"], product["price"], entry))
            
            order_is_ready_label = customtkinter.CTkLabel(
                popup_window, text="Valmiina:")
            order_is_ready_label.pack(pady=5)
            
            entry = customtkinter.CTkEntry(master=popup_window, placeholder_text=f"1")
            entry.pack(padx=20, pady=10)
            isready = "Ei"
            if order_info["IsReady"] == True:
                isready = "Kyllä"
            entry.insert(0, isready)
            entry.configure(state="disabled")
                
            label = customtkinter.CTkLabel(
                    master=popup_window, text=f'Kokonaishinta:')
            label.pack()
            entry = customtkinter.CTkEntry(master=popup_window, placeholder_text=f"1")
            entry.pack(padx=20, pady=10)
            entry.insert(0, order_info["Price"])
            entry.configure(state="disabled")
            
            close_button = customtkinter.CTkButton(
                popup_window, text="Poistu", command=lambda: popup_window.destroy())
            close_button.pack(pady=10)
            
        except requests.exceptions.RequestException as e:
            # Show error message and technical details in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Virhe")
            popup_window.geometry("300x200")

            error_label = customtkinter.CTkLabel(
                popup_window, text=f"Virhe: {e}")
            error_label.pack(pady=10)

            show_details_button = customtkinter.CTkButton(
                popup_window, text="Näytä lisätietoa (asiantuntijatila)", command=lambda: self.show_technical_details(traceback.format_exc()))
            show_details_button.pack(pady=10)

            close_button = customtkinter.CTkButton(
                popup_window, text="Poistu", command=popup_window.destroy)
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