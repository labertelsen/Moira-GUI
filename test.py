from tkinter import *
from tkinter import ttk
from tkinter import Widget

coords = [0, 0, 0, 0]
lines = []
linedb = []

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
        widget.bind('<ButtonRelease-1>', self.on_release)
    
    def on_start(self, event):
        print('port clicked')
        
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName) 
        parent.startx = event.x + parent.winfo_x()
        parent.starty = event.y + parent.winfo_y()

        coords[0] = parent.startx
        coords[1] = parent.starty

        lines.append(canvas.create_line(coords[0],coords[1],coords[0], coords[1]))

    def on_drag(self, event):
        print('port dragged')

        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName)
        # x = parent.winfo_pointerx() - parent.startx + event.x
        # y = parent.winfo_pointery() - parent.starty + event.y


        grandparent = event.widget.master.master
        
        # x = grandparent.winfo_x() + root.winfo_rootx()
        # y = grandparent.winfo_y() + root.winfo_rooty()
        # x = root.winfo_rootx() + event.x
        # y = root.winfo_rooty() + event.y
        x = canvas.winfo_pointerx() - 80
        y = canvas.winfo_pointery() - 80
        # x = event.x
        # y = event.y

        coords[2] = x
        coords[3] = y
        print(event.x, event.y, canvas.winfo_pointerx(), canvas.winfo_pointery())
        # canvas.coords(lines[-1], coords[0],coords[1],x,y)

    def on_release(self, event):
        linedb.append(canvas.coords(lines[-1]))
        print(linedb)

root = Tk()
root.title("dragndrop test")
root.geometry('500x500')
canvas = Canvas(root, borderwidth = 5, relief="ridge", width=500, height=500)
canvas.grid(column = 0, row = 1)
root.grid_propagate(False)
canvas.grid_propagate(False)

bd = BlockDrag()
ld = LineDrag()
block1 = Block(canvas)
block2 = Block(canvas)

root.mainloop()