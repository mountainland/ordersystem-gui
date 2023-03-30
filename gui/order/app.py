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
        #self.grab_set()
        self.attributes('-topmost',True)  #for focus on toplevel
    
    def build_main(self):
        self.products = []
        products_url = f"https://api.ordersystem.luova.club/products/"
        product_response = requests.get(products_url)
        product_response.raise_for_status()
        products_data = product_response.json()
        products = products_data["products"]
        
        label = customtkinter.CTkLabel(master=self, text=f'Customer id:')
        label.pack()
        self.customer_entry = customtkinter.CTkEntry(master=self, placeholder_text=f"1")
        self.customer_entry.pack(padx=20, pady=10)

        for product in products:
            
            label = customtkinter.CTkLabel(master=self, text=f'{product["Name"]} {product["Price"]}€')
            label.pack()
            entry = customtkinter.CTkEntry(master=self, placeholder_text=f"1")
            entry.pack(padx=20, pady=10)
            self.products.append((product["Name"], product["Price"], entry))

        self.exit_button = customtkinter.CTkButton(self, text="Exit", command=self.destroy)
        self.exit_button.pack(pady=10)

    def send_order(self):
        data = {"order": []}
        order = data["order"]
        for product in self.products:
            value = product[2].get()
            order.append({"name": product[0], "price": product[1], "count": value})

        data["customer"] = self.customer_entry.get()

        orders_url = f"https://api.ordersystem.luova.club/orders/"
        product_response = requests.post(products_url, json=data)
        product_response.raise_for_status()

        


    def fetch_customer_info(self):
        # Get customer ID from entry widget
        customer_id = self.customer_id_entry.get()
        
        try:
            # Make API request to get customer info
            customer_url = f"https://api.ordersystem.luova.club/customer/{customer_id}"
            customer_response = requests.get(customer_url)
            customer_response.raise_for_status()
            customer_data = customer_response.json()

            # Create popup window with customer info and editing fields
            popup_window = customtkinter.CTkToplevel()
            popup_window.title("Customer Info")
            popup_window.geometry("300x500")
            
            first_name_label = customtkinter.CTkLabel(popup_window, text="First Name:")
            first_name_label.pack(pady=5)
            first_name_entry = customtkinter.CTkEntry(popup_window)
            first_name_entry.pack(pady=5)
            first_name_entry.insert(0, customer_data.get('FirstName'))
            
            last_name_label = customtkinter.CTkLabel(popup_window, text="Last Name:")
            last_name_label.pack(pady=5)
            last_name_entry = customtkinter.CTkEntry(popup_window)
            last_name_entry.pack(pady=5)
            last_name_entry.insert(0, customer_data.get('LastName'))
            
            balance_label = customtkinter.CTkLabel(popup_window, text="Balance:")
            balance_label.pack(pady=5)
            balance_entry = customtkinter.CTkEntry(popup_window)
            balance_entry.pack(pady=5)
            balance_entry.insert(0, customer_data.get('Balance'))
            
            save_button = customtkinter.CTkButton(popup_window, text="Save", command=lambda: self.save_customer_info(customer_id, first_name_entry.get(), last_name_entry.get(), balance_entry.get()))
            save_button.pack(pady=10)
            
            close_button = customtkinter.CTkButton(popup_window, text="Close", command=popup_window.destroy)
            close_button.pack(pady=10)
        except requests.exceptions.RequestException as e:
            # Show error message and technical details in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Error")
            popup_window.geometry("300x200")
            
            error_label = customtkinter.CTkLabel(popup_window, text=f"Error: {e}")
            error_label.pack(pady=10)
            
            show_details_button = customtkinter.CTkButton(popup_window, text="Show Technical Details", command=lambda: self.show_technical_details(traceback.format_exc()))
            show_details_button.pack(pady=10)
            
            close_button = customtkinter.CTkButton(popup_window, text="Close", command=popup_window.destroy)
            close_button.pack(pady=10)
    
