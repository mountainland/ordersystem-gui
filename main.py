import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class OrderApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{1100}x{580}")
        self.title("Order")
        self.label = customtkinter.CTkLabel(self, text="Order")
        self.label.pack(padx=20, pady=20)

        self.build_menu()

    def start_ordering(self):
        print("mau")    
    
    #def send_order(self):


    def build_menu(self):
        button = customtkinter.CTkButton(master=self, text="CTkButton", command=self.start_ordering)
        button.pack(padx=20, pady=10)
        entry = customtkinter.CTkEntry(master=self, placeholder_text="CTkEntry")
        entry.pack(padx=20, pady=10)

class CustomerApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{1100}x{580}")
        self.title("Customer")
        self.label = customtkinter.CTkLabel(self, text="Customer")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        self.build_main()

        self.order_window = None

        self.customer_window = None

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
        self.sidebar_button_logout = customtkinter.CTkButton(self.sidebar_frame, command=quit, text="Logout")
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
