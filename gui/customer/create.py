import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback
import json

class CustomerCreateApp(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.username = parent.username
        self.password = parent.password
        self.geometry(f"{1100}x{580}")
        self.title("Asiakas")
        self.label = customtkinter.CTkLabel(self, text="Asiakkaan luonti")
        self.label.pack(padx=20, pady=20)
        self.attributes('-topmost', True)  # for focus on toplevel
        self.build_menu()

    def build_menu(self):
            
        self.first_name_label = customtkinter.CTkLabel(
            self, text="Etunimi:")
        self.first_name_label.pack(pady=10)

        self.first_name_entry = customtkinter.CTkEntry(self)
        self.first_name_entry.pack(pady=5)
        
        self.last_name_label = customtkinter.CTkLabel(
            self, text="Sukunimi:")
        self.last_name_label.pack(pady=10)

        self.last_name_entry = customtkinter.CTkEntry(self)
        self.last_name_entry.pack(pady=5)
        
        # Create button to fetch customer info
        self.create_button = customtkinter.CTkButton(
            self, text="Luo asiakas", command=self.create_customer)
        self.create_button.pack(pady=10)

        # Create exit button
        self.exit_button = customtkinter.CTkButton(
            self, text="Poistu", command=self.destroy)
        self.exit_button.pack(pady=10)

    def shut(self, window):
        window.destroy()
        self.attributes('-topmost', True)  # for focus on topleve

    def create_customer(self):
        # Get customer ID from entry widget
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        try:
            # Make API request to get customer info
            customer_url = f"http://api.ordersystem.luova.club:8081/customers/"
            headers = {"Content-Type": "application/json", "user": self.username, "password": self.password}
            customer_response = requests.post(customer_url, data=json.dumps({"FirstName": first_name, "LastName": last_name}), headers=headers)
            customer_response.raise_for_status()
            customer_data = json.loads(customer_response.text.replace("'", '"'))
            
            customer_id = customer_data["id"]

            self.attributes('-topmost', False)  # for focus on topleve
            # Create popup window with customer info and editing fields
            popup_window = customtkinter.CTkToplevel()
            popup_window.title("Customer Info")
            popup_window.geometry("300x500")
            popup_window.attributes('-topmost', True)  # for focus on toplevel
            id_label = customtkinter.CTkLabel(
                popup_window, text=f"Asiakas id: {customer_id}")
            id_label.pack(pady=5)
                        
            close_button = customtkinter.CTkButton(
                popup_window, text="Close", command=lambda: self.shut(popup_window))
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

    def save_customer_info(self, customer_id, first_name, last_name, balance):
        # Create payload data
        payload = {
            "FirstName": first_name,
            "LastName": last_name,
            "Balance": int(balance)
        }

        try:
            # Make API request to update customer info
            customer_url = f"http://api.ordersystem.luova.club:8081/customer/{customer_id}"
            customer_response = requests.post(customer_url, json=payload)
            customer_response.raise_for_status()

            # Show success message in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Success")
            popup_window.geometry("300x200")

            success_label = customtkinter.CTkLabel(
                popup_window, text="Customer info saved successfully.")
            success_label.pack(pady=10)

            close_button = customtkinter.CTkButton(
                popup_window, text="Close", command=popup_window.destroy)
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
