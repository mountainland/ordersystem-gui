import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback
import json


class CustomerFetchApp(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.user = parent.user
        self.geometry(f"{1100}x{580}")
        self.title("Customer")
        self.label = customtkinter.CTkLabel(self, text="Asiakashaku")
        self.label.pack(padx=20, pady=20)
        self.attributes('-topmost', True)  # for focus on toplevel
        self.build_menu()

    def build_menu(self):
        # Create customer ID label and entry
        self.customer_id_label = customtkinter.CTkLabel(
            self, text="Asiakas ID:")
        self.customer_id_label.pack(pady=10)

        self.customer_id_entry = customtkinter.CTkEntry(self)
        self.customer_id_entry.pack(pady=5)

        # Create button to fetch customer info
        self.fetch_button = customtkinter.CTkButton(
            self, text="Hae tiedot", command=self.fetch_customer_info)
        self.fetch_button.pack(pady=10)

        # Create exit button
        self.exit_button = customtkinter.CTkButton(
            self, text="Poistu", command=self.destroy)
        self.exit_button.pack(pady=10)

    def shut(self, window):
        window.destroy()
        self.attributes('-topmost', True)  # for focus on topleve

    def fetch_customer_info(self):
        # Get customer ID from entry widget
        customer_id = self.customer_id_entry.get()

        try:
            # Make API request to get customer info
            customer_url = f"https://api.ordersystem.luova.club/customer/{customer_id}"
            headers = {"Content-Type": "application/json",
                       "user": self.user["username"], "password": self.user["password"]}

            customer_response = requests.get(customer_url, headers=headers)
            # customer_response.raise_for_status()
            customer_data = json.loads(
                customer_response.text.replace("'", '"'))
            # customer_data = customer_response.json()
            self.attributes('-topmost', False)  # for focus on topleve
            # Create popup window with customer info and editing fields
            popup_window = customtkinter.CTkToplevel()
            popup_window.title("Asiakastiedot")
            popup_window.geometry("300x500")
            popup_window.attributes('-topmost', True)  # for focus on toplevel
            first_name_label = customtkinter.CTkLabel(
                popup_window, text="Etunimi:")
            first_name_label.pack(pady=5)
            first_name_entry = customtkinter.CTkEntry(popup_window)
            first_name_entry.pack(pady=5)
            first_name_entry.insert(0, customer_data.get('firstname'))

            last_name_label = customtkinter.CTkLabel(
                popup_window, text="Sukunimi:")
            last_name_label.pack(pady=5)
            last_name_entry = customtkinter.CTkEntry(popup_window)
            last_name_entry.pack(pady=5)
            last_name_entry.insert(0, customer_data.get('lastname'))
            
            phonenumber_label = customtkinter.CTkLabel(
                popup_window, text="Puhelinnumero:")
            phonenumber_label.pack(pady=5)
            phonenumber_entry = customtkinter.CTkEntry(popup_window)
            phonenumber_entry.pack(pady=5)
            phonenumber_entry.insert(0, customer_data.get('phonenumber'))
            
            email_label = customtkinter.CTkLabel(
                popup_window, text="Sähköposti:")
            email_label.pack(pady=5)
            email_entry = customtkinter.CTkEntry(popup_window)
            email_entry.pack(pady=5)
            email_entry.insert(0, customer_data.get('email'))

            balance_label = customtkinter.CTkLabel(
                popup_window, text="Saldo:")
            balance_label.pack(pady=5)
            
            balance_entry = customtkinter.CTkEntry(popup_window)
            balance_entry.pack(pady=5)
            balance_entry.insert(0, customer_data.get('balance'))            
        
            if not self.user["is_admin"]:
                balance_entry.configure(state="disabled")                

            save_button = customtkinter.CTkButton(popup_window, text="Tallenna muutokset", command=lambda: self.save_customer_info(
                customer_id, first_name_entry.get(), last_name_entry.get(), balance_entry.get(), phonenumber_entry.get(), email_entry.get()))
            save_button.pack(pady=10)

            close_button = customtkinter.CTkButton(
                popup_window, text="Poistu", command=lambda: self.shut(popup_window))
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

    def save_customer_info(self, customer_id, first_name, last_name, balance, phonenumber, email):
        # Create payload data
        payload = {
            "firstname": first_name,
            "lastname": last_name,
            "phonenumber": phonenumber,
            "email": email}
        
        payload["balance"] = balance
            
        try:
            # Make API request to update customer info
            customer_url = f"https://api.ordersystem.luova.club/customer/{customer_id}"
            headers = {"Content-Type": "application/json",
                       "user": self.user["username"], "password": self.user["password"]}

            customer_response = requests.post(
                customer_url, json=payload, headers=headers)
            customer_response.raise_for_status()

            # Show success message in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Onnistuneesti tallennettu")
            popup_window.geometry("300x200")

            success_label = customtkinter.CTkLabel(
                popup_window, text="Asiakastiedot tallennettu onnistuneesti.")
            success_label.pack(pady=10)

            close_button = customtkinter.CTkButton(
                popup_window, text="Poistu", command=popup_window.destroy)
            close_button.pack(pady=10)

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
