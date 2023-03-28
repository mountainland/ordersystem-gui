import tkinter as tk
import requests
import json

import traceback


global LOGGED_IN
LOGGED_IN = False


class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
        self.geometry("300x200")

        # Create login form
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.error_label = tk.Label(self, fg="red")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # TODO: Validate username and password with backend API

        if username == "admin" and password == "password":
            self.destroy()
            self.logged_in = True
            global LOGGED_IN
            LOGGED_IN = True
        else:
            self.error_label.config(text="Invalid username or password")
            self.error_label.pack(pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Customer Info")
        self.geometry("300x200")

        self.withdraw()
        self.logged_in = False

        self.show_login_window()

    def show_login_window(self):
        self.login_window = LoginWindow(self)
        self.wait_window(self.login_window)

        if self.logged_in or LOGGED_IN:
            self.deiconify()
            self.setup_main_window()
        else:
            self.show_login_window()

    def setup_main_window(self):
        # Create customer ID label and entry
        self.customer_id_label = tk.Label(self, text="Customer ID:")
        self.customer_id_label.pack(pady=10)

        self.customer_id_entry = tk.Entry(self)
        self.customer_id_entry.pack(pady=5)

        # Create button to fetch customer info
        self.fetch_button = tk.Button(
            self, text="Fetch Customer Info", command=self.fetch_customer_info)
        self.fetch_button.pack(pady=10)

        # Create logout button
        self.logout_button = tk.Button(
            self, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def logout(self):
        self.logged_in = False
        global LOGGED_IN
        LOGGED_IN = False
        self.withdraw()  # hide the main window
        self.show_login_window()
        # self.login_window.deiconify()  # show the login window

    def fetch_customer_info(self):
        # Get customer ID from entry widget
        customer_id = self.customer_id_entry.get()

        try:
            # Make API request to get customer info
            customer_url = f"https://api.ordersystem.luova.club/customer/{customer_id}"
            customer_response = requests.get(customer_url)
            customer_response.raise_for_status()
            customer_data = customer_response.json()

            # Show customer info in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Customer Info")
            popup_window.geometry("300x200")

            first_name_label = tk.Label(
                popup_window, text=f"First Name: {customer_data.get('FirstName')}")
            first_name_label.pack(pady=10)

            last_name_label = tk.Label(
                popup_window, text=f"Last Name: {customer_data.get('LastName')}")
            last_name_label.pack(pady=10)

            balance_label = tk.Label(
                popup_window, text=f"Balance: {customer_data.get('Balance')}")
            balance_label.pack(pady=10)

            close_button = tk.Button(
                popup_window, text="Close", command=popup_window.destroy)
            close_button.pack(pady=10)
        except requests.exceptions.RequestException as e:
            # Show error message and technical details in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Error")
            popup_window.geometry("300x200")

            error_label = tk.Label(popup_window, text=f"Error: {e}")
            error_label.pack(pady=10)

            show_details_button = tk.Button(popup_window, text="Show Technical Details",
                                            command=lambda: self.show_technical_details(traceback.format_exc()))
            show_details_button.pack(pady=10)

            close_button = tk.Button(
                popup_window, text="Close", command=popup_window.destroy)
            close_button.pack(pady=10)

    def show_technical_details(self, technical_details):
        # Show technical details in popup window
        popup_window = tk.Toplevel()
        popup_window.title("Technical Details")
        popup_window.geometry("500x300")

        technical_details_label = tk.Label(
            popup_window, text=technical_details)
        technical_details_label.pack(pady=10)

        close_button = tk.Button(
            popup_window, text="Close", command=popup_window.destroy)
        close_button.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
