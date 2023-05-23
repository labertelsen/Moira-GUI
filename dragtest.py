from tkinter import *
from tkinter import ttk

def add_dragable( widget):
        widget.bind('<ButtonPress-1>', on_start)
        widget.bind('<B1-Motion>', on_drag)
        widget.bind('<ButtonRelease>', on_drop)
        print('draggable')

def on_start(event):
    print('start')
    pass

def on_drag(event):
    pass

def on_drop(event):
    # print('drop')
    # x,y = event.widget.winfo_pointerxy()
    # print(x,y)
    # target = event.widget.winfo_containing(x,y)
    # print('****')
    # print(event)
    # print(event.widget)
    # print(event.widget.winfo_containing(x,y))
    # print('****')
    # try:
    #     event.widget.place(x=x,y=y)
    # except:
    #     print('except')
    print('drop')
    x=event.x
    y=event.y
    print(x,y)
    target = event.widget.winfo_containing(x,y)
    print('****')
    print(event)
    print(event.widget)
    print(event.widget.winfo_containing(x,y))
    print('****')
    try:
        event.widget.place(x=x,y=y)
    except:
        print('except')
        pass



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

btn.bind('<ButtonPress-1>', on_start)
btn.bind('<B1-Motion>', on_drag)
btn.bind('<ButtonRelease-1>', on_drop)

root.mainloop()