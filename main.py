import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import traceback
global LOGGED_IN
LOGGED_IN = False

class LoginWindow(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
        self.geometry("300x500")
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.bind("<Alt-F4>", lambda event: None)
        self.bind("<Control-w>", lambda event: None)
        self.bind("<Control-W>", lambda event: None)
        
        # Create login form
        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_label.pack(pady=10)
        
        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.pack(pady=5)
        
        self.password_label = customtkinter.CTkLabel(self, text="Password:")
        self.password_label.pack(pady=10)
        
        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)
        
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        
        self.error_label = customtkinter.CTkLabel(self)
    
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

class OrderApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{1100}x{580}")
        self.title("Order")
        self.label = customtkinter.CTkLabel(self, text="Order")
        self.label.pack(padx=20, pady=20)

        self.build_main()
    
    def build_main(self):
        products_url = f"https://api.ordersystem.luova.club/products/"
        product_response = requests.get(products_url)
        product_response.raise_for_status()
        products_data = product_response.json()
        products = products_data["products"]
        
        for product in products:
            label = customtkinter.CTkLabel(master=self, text=f'{product["Name"]} {product["Price"]}€')
            label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            entry = customtkinter.CTkEntry(master=self, placeholder_text=f"1")
            entry.pack(padx=20, pady=10)
            
            
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
    
class CustomerApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{1100}x{580}")
        self.title("Customer")
        self.label = customtkinter.CTkLabel(self, text="Customer")
        self.label.pack(padx=20, pady=20)

        self.build_menu()

    def build_menu(self):
        # Create customer ID label and entry
        self.customer_id_label = customtkinter.CTkLabel(self, text="Customer ID:")
        self.customer_id_label.pack(pady=10)
        
        self.customer_id_entry = customtkinter.CTkEntry(self)
        self.customer_id_entry.pack(pady=5)
        
        # Create button to fetch customer info
        self.fetch_button = customtkinter.CTkButton(self, text="Fetch Customer Info", command=self.fetch_customer_info)
        self.fetch_button.pack(pady=10)

        # Create button to save customer info
        self.save_button = customtkinter.CTkButton(self, text="Save Customer Info", command=self.save_customer_info)
        self.save_button.pack(pady=10)
        
        # Create exit button
        self.exit_button = customtkinter.CTkButton(self, text="Exit", command=self.destroy)
        self.exit_button.pack(pady=10)
        
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
    
    def save_customer_info(self, customer_id, first_name, last_name, balance):
        # Create payload data
        payload = {
            "FirstName": first_name,
            "LastName": last_name,
            "Balance": balance
        }
        
        try:
            # Make API request to update customer info
            customer_url = f"https://api.ordersystem.luova.club/customer/{customer_id}"
            customer_response = requests.post(customer_url, json=payload)
            customer_response.raise_for_status()

            # Show success message in popup window
            popup_window = tk.Toplevel()
            popup_window.title("Success")
            popup_window.geometry("300x200")
            
            success_label = customtkinter.CTkLabel(popup_window, text="Customer info saved successfully.")
            success_label.pack(pady=10)
            
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
        
    def show_technical_details(self, technical_details):
        # Show technical details in popup window
        popup_window = tk.Toplevel()
        popup_window.title("Technical Details")
        popup_window.geometry("500x300")
        
        technical_details_label = customtkinter.CTkLabel(popup_window, text=technical_details)
        technical_details_label.pack(pady=10)
        
        close_button = customtkinter.CTkButton(popup_window, text="Close", command=popup_window.destroy)
        close_button.pack(pady=10)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        
        self.order_window = None

        self.customer_window = None
        
        #self.withdraw()
        self.logged_in = True

        
        
        self.show_login_window()

    def show_login_window(self):
        #self.withdraw()  # hide the main window
        self.login_window = LoginWindow(self)
        self.wait_window(self.login_window)

        if self.logged_in or LOGGED_IN:
            self.deiconify()  # show the main window
            self.build_main()
        else:
            self.show_login_window()
        
        

    def logout(self):
        self.logged_in = False
        global LOGGED_IN
        LOGGED_IN = False

        # Destroy all widgets in the main window
        for widget in self.winfo_children():
            widget.destroy()

        # Reset customer ID entry
        #self.customer_id_entry.delete(0, tk.END)

        # Hide the main window and show the login window
        self.withdraw()
        self.show_login_window()
    
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def build_main(self):
        self.build_sidebar()

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def open_order_menu(self):
        if self.order_window is None or not self.order_window.winfo_exists():
            self.order_window = OrderApp(self)  # create window if its None or destroyed
            self.order_window.focus()
        else:
            self.order_window.focus()  # if window exists focus it

    def open_customer_menu(self):
        if self.customer_window is None or not self.customer_window.winfo_exists():
            self.customer_window = CustomerApp(self)  # create window if its None or destroyed
            self.customer_window.focus()
        else:
            self.customer_window.focus()  # if window exists focus it

    def build_sidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="LuovaClub", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_order = customtkinter.CTkButton(self.sidebar_frame, command=self.open_order_menu, text="Order")
        self.sidebar_button_order.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_customer = customtkinter.CTkButton(self.sidebar_frame, command=self.open_customer_menu, text="Customer")
        self.sidebar_button_customer.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_logout = customtkinter.CTkButton(self.sidebar_frame, command=self.logout, text="Logout")
        self.sidebar_button_logout.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

if __name__ == "__main__":
    app = App()
    app.mainloop()
