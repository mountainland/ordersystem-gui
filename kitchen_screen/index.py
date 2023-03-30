import tkinter as tk

from requesting import Ordersystem

api = Ordersystem("https://dev.backend.order.mountainland.fi")

products = []


row = 0


column = 0

def reload_screen(row=row, column=column):
    for widget in root.winfo_children():
        widget.destroy()
        

    for product in api.list_order_list_apis():
        text = ""
        text += f'\nTilaaja: {product["customer"]}'
        for product1 in product["order"]:
            text += f"\n{product1}: {product['order'][product1]}"
        tk.Message(root, width=800, text=text, highlightbackground="red", highlightcolor="red", highlightthickness=10).grid(column=column, row=row, padx=10, pady=10)
        if not column > 4:
            column += 1
        else:
            row += 1
            column = 0
            

    root.after(5000, reload_screen)

root = tk.Tk()
root.title("LuovaClubin Tilausjärjestelmä")



reload_screen(row, column)

root.mainloop()
