

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

def create(root, ID):
    canvas = tk.Canvas(root, width=200, height=200)
    canvas.grid(row=row, column=column, padx=10, pady=10)

    canvas.create_oval(50, 50, 150, 150, fill="blue")
    canvas.create_text(100, 100, text=ID, fill="white", font=("Arial", 50))

def get_orders():
    global column
    column = 0
    global row
    column = 0
    global latest_order
    data = requests.get(f"{url}orders/", headers={"user": user, "password": password})
    
    data = data.text.replace("'", '"').replace("True", "true").replace("False", "false")
    
    data = json.loads(data)
    
    for item in data['orders']:
        if item["is_ready"] == False:
            continue

        ID = item["ID"]
        
        create(root, ID)
        
        if not column > 3:
            column += 1
        else:
            row += 1
            column = 0    

            
        
        
        # Ääni kun uusi tilaus
        
    

def reload_screen():
    for widget in root.winfo_children():
        widget.destroy()
        
    get_orders()

    root.after(200, reload_screen)

root = tk.Tk()
root.title("LuovaClubin Tilausjärjestelmä")



reload_screen()

root.mainloop()
