from tkinter import *
from tkinter import ttk
from tkinter import Widget


class Block():
    def __init__(self, parent):

        self.frame = ttk.Frame(parent)
        self.frame.grid(column=0, row=0)

        self.label = ttk.Button(self.frame, text="Drag Me")
        self.label.grid(column=1,row=0)

        self.leftport = Label(self.frame, width = 1)
        self.leftport.configure(bg="blue")
        self.leftport.grid(column=0, row=0)

        self.rightport = Label(self.frame, width = 1)
        self.rightport.configure(bg="red")
        self.rightport.grid(column=2, row=0)

        bd.add_draggable(self.label)
        ld.add_draggable(self.leftport)
        ld.add_draggable(self.rightport)
        
class BlockDrag():
    def add_draggable(self, widget):
            widget.bind('<ButtonPress-1>', self.on_start)
            widget.bind('<B1-Motion>', self.on_drag)

    def on_start(self, event):
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName) 
        parent.startx = event.x
        parent.starty = event.y

    def on_drag(self, event):
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName)
        x = parent.winfo_x() - parent.startx + event.x
        y = parent.winfo_y() - parent.starty + event.y
        parent.place(x=x, y=y)

class LineDrag():
    def add_draggable(self, widget):
        widget.bind('<ButtonPress-1>', self.on_start)
        widget.bind('<B1-Motion>', self.on_drag)
    
    def on_start(self, event):
        print('port clicked')

    def on_drag(self, event):
        print('port dragged')

root = Tk()
root.title("dragndrop test")
root.geometry('500x500')
canvas = ttk.Frame(root, borderwidth = 5, relief="ridge", width=500, height=500)
canvas.grid(column = 0, row = 1)
root.grid_propagate(False)
canvas.grid_propagate(False)

bd = BlockDrag()
ld = LineDrag()
block1 = Block(canvas)
block2 = Block(canvas)

root.mainloop()