from tkinter import *

class Block():
    def __init__(self, parent):

        self.frame = Frame(parent)
        self.frame.grid(column=0, row=0)

        self.label = Button(self.frame, text="Drag Me")
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
        
coords = [0, 0, 0, 0]
lines = []
linedb = []

def click(event):
    coords[0] = event.x
    coords[1] = event.y
    lines.append(canvas.create_line(coords[0],coords[1],coords[0],coords[1]))

def drag(event):
    coords[2] = event.x
    coords[3] = event.y
    canvas.coords(lines[-1], coords[0],coords[1],coords[2],coords[3])
    
def release(event):
    linedb.append(canvas.coords(lines[-1]))
    print(linedb)

root = Tk()
canvas = Canvas(root, height=500, width=500)
canvas.grid_propagate(False)
canvas.grid(column=0, row=0)

bd = BlockDrag()
ld = LineDrag()
block1 = Block(canvas)
block2 = Block(canvas)

root.bind('<ButtonPress-1>', click)
root.bind('<B1-Motion>', drag)
root.bind('<ButtonRelease-1>', release)

root.mainloop()