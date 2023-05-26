from tkinter import *
from tkinter import ttk
 
def add_dragable( widget):
        widget.bind('<ButtonPress-1>', on_start)
        widget.bind('<B1-Motion>', on_drag)

def on_start(event):
    widget = event.widget
    widget.startx = event.x
    widget.starty = event.y

def on_drag(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startx + event.x
    y = widget.winfo_y() - widget.starty + event.y
    widget.place(x=x, y=y)
    print(widget.winfo_rootx(), widget.winfo_rooty())

root = Tk()
root.title("dragndrop test")
root.geometry('500x500')
canvas = ttk.Frame(root, borderwidth = 5, relief="ridge", width=500, height=500)
canvas.grid(column = 0, row = 1)
root.grid_propagate(False)
canvas.grid_propagate(False)

btn = ttk.Button(canvas, text="Drag Me")
btn.grid(column=0, row=0)

add_dragable(btn)

root.mainloop()