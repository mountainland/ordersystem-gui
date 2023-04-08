import tkinter as tk

import requests
import winsound
import chime
global url
url = "https://api.ordersystem.luova.club/"

import json

global user
user = "vuoreol"
global password
password = "mau"
products = []

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
    global row
    global latest_order
    data = requests.get(f"{url}orders/", headers={"user": user, "password": password})
    
    data = data.text.replace("'", '"').replace("True", "true").replace("False", "false")
    
    data = json.loads(data)
    
    for item in data['orders']:
        if item["is_ready"] == True:
            continue
        customer = item['customer']
        
        order = item["order"]
        if not is_names(order):
            continue

        ID = item["ID"]

        text = f"ID: {ID}"
        for product in order:
            print(product)
            name = product.get("name")
            if not name == None:
                text += f"""\n{name}: {product.get("count")}"""
            else:
                continue
        
        tk.Message(root, width=800, text=text, highlightbackground="red", highlightcolor="red", highlightthickness=10).grid(column=column, row=row, padx=10, pady=10)
        if not column > 4:
            column += 1
        else:
            row += 1
            column = 0
        
        if latest_order < ID:
            chime.success()
            latest_order = ID
            

            
        
        
        # Ääni kun uusi tilaus
        
    

def reload_screen(row=row, column=column):
    for widget in root.winfo_children():
        widget.destroy()
        
    get_orders()

    root.after(5000, reload_screen)

root = tk.Tk()
root.title("LuovaClubin Tilausjärjestelmä")



reload_screen(row, column)

root.mainloop()
