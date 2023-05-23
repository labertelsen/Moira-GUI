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

root = Tk()
root.title("Build-a-Brain")

menubar = Menu(root)

file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='Run', command=None)
file.add_command(label='New', command=None)
file.add_command(label='Save', command=None)
file.add_command(label='Open', command=None)
file.add_command(label='Close Window', command=None)

edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)

view = Menu(menubar, tearoff=0)
menubar.add_cascade(label='View', menu=view)

help = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help)

canvas = ttk.Frame(root, borderwidth = 5, relief="ridge", width=500, height=500)
canvas.grid(column = 0, row = 1)
canvas.grid_propagate(False)

panel = ttk.Frame(root, borderwidth=5, relief="ridge", width=200, height=500)
panel.grid(column=1, row=1)
panel.grid_propagate(False)

root.config(menu=menubar)

#Replication  Section
def Replication(x): 
    Copy_Label = Label(canvas, text=x, borderwidth=5, relief="ridge")
    Copy_Label.grid(row=0, column=0)
    add_dragable(Copy_Label)

Frontal_Lobe = Button(panel,text="Frontal Lobe",  command=lambda: Replication("Frontal Lobe")).grid(row=1,column=1)
Occipital_Lobe = Button(panel, text="Occipital Lobe", command=lambda: Replication("Occipital Lobe")).grid(row=2,column=1)
Temporal_Lobe = Button(panel, text="Temporal Lobe", command=lambda: Replication("Temporal Lobe")).grid(row=3,column=1)
Parietal_Lobe = Button(panel,text="Parietal Lobe",command=lambda: Replication("Parietal Lobe")).grid(row=4,column=1)



root.mainloop()