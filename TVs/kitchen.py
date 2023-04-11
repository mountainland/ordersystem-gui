import tkinter as tk

import requests
import winsound
import chime
global url
url = "https://api.ordersystem.luova.club/"

import json

global user
user = ""
global password
password = ""
products = []

if user == "":
    user = input("Please enter your username: ")
    
if password == "":
    password = input("Please enter your password: ")

def login():
    print("\a")
    global user
    global password
    user = input("Enter your username: ")
    password = input("Enter your password: ")

    

global latest_order
latest_order = 0

global row
row = 0

global column
column = 0

def make_sound():
    Freq = 1000 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
    print("mau")

def is_names(order):
    for product in order:
        if product.get("name") == None or product.get("count") == None:
            return False
    return True

def get_orders():
    global column
    column = 0
    global row
    column = 0
    global latest_order
    data = requests.get(f"{url}orders/", headers={"user": user, "password": password})
    if data.status_code == 401:
        login()
        return
    data = data.text.replace("'", '"').replace("True", "true").replace("False", "false")
    print(data)
    data = json.loads(data)
    
    orders = data.get('orders')
    if not orders == None:    
        for item in orders:
            if item["is_ready"] == False and item["picked"] == False:
            
                order = item["order"]
                if not is_names(order):
                    continue

                ID = item["ID"]

                text = f"ID: {ID}"
                for product in order:
                    name = product.get("name")
                    if not name == None:
                        text += f"""\n{name}: {product.get("count")}"""
                    else:
                        continue
                
                tk.Message(root, width=800, text=text, highlightbackground="red", highlightcolor="red", highlightthickness=10).grid(column=column, row=row, padx=10, pady=10)
                if not column > 2:
                    column += 1
                else:
                    row += 1
                    column = 0
                
                if latest_order < ID:
                    chime.success()
                    latest_order = ID
            

            
        
        
        # Ääni kun uusi tilaus
        
    

def reload_screen():
    for widget in root.winfo_children():
        widget.destroy()
        
    get_orders()

    root.after(5000, reload_screen)

root = tk.Tk()
root.title("LuovaClubin Tilausjärjestelmä")



reload_screen()

root.mainloop()
