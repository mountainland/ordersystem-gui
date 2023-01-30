import tkinter as tk

from requesting import Ordersystem

api = Ordersystem("https://dev.backend.order.mountainland.fi")

products = []

def reload_screen():
    for widget in root.winfo_children():
        widget.destroy()
        
    root.geometry("200x400")

    puh = tk.Label(root, text='Customer ID')
    puh.pack()

    puh_entry = tk.Entry(root)
    puh_entry.pack()
    products.append(puh_entry)
    for product in api.list_product_list_apis():
        label = tk.Label(root, text=f'{product["name"]}')
        label.pack()

        entry = tk.Entry(root)
        entry.pack()

        products.append((entry, label))

    button = tk.Button(root, text="Lähetä tilaus", command=show_entry_contents)
    button.pack()

def show_entry_contents():
    order = {}

    for item in products[1:]:
        order[item[1]["text"]] = item[0].get()

    request_data = {"order": order, "ready": False, "customer": products[0].get()}

    api.create_order_list_api(request_data)
    reload_screen()

root = tk.Tk()
root.title("LuovaClubin Tilausjärjestelmä")


reload_screen()

root.mainloop()
