from tkinter import *
from tkinter import ttk
from tkinter import Widget

coords = [0, 0, 0, 0]
lines = []
linedb = []
colors = ["gold", "red", "blue", "green"]

class Block():
    def __init__(self, parent, lefttype, righttype):

        self.frame = ttk.Frame(parent)
        self.frame.grid(column=0, row=0)

        self.label = ttk.Button(self.frame, text="Drag Me")
        self.label.grid(column=1,row=0)

        self.leftport = Label(self.frame, width = 1)
        self.leftport.configure(bg=colors[lefttype])
        self.leftport.grid(column=0, row=0)
        self.leftport.type = lefttype

        self.rightport = Label(self.frame, width = 1)
        self.rightport.configure(bg=colors[righttype])
        self.rightport.grid(column=2, row=0)
        self.rightport.type = righttype

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
        x = canvas.winfo_pointerx()-canvas.winfo_rootx()
        y = canvas.winfo_pointery()-canvas.winfo_rooty()
        coords[0] = x
        coords[1] = y
        lines.append(canvas.create_line(coords[0],coords[1],coords[0], coords[1]))

    def on_drag(self, event):
        x = canvas.winfo_pointerx()-canvas.winfo_rootx()
        y = canvas.winfo_pointery()-canvas.winfo_rooty()
        coords[2] = x
        coords[3] = y
        canvas.coords(lines[-1], coords[0], coords[1], x, y)

    def on_release(self, event):
        start_port = find_widget(canvas.coords(lines[-1])[0], canvas.coords(lines[-1])[1])
        end_port = find_widget(canvas.coords(lines[-1])[2], canvas.coords(lines[-1])[3])
        if start_port and end_port:
            if start_port.type == end_port.type:
                linedb.append(canvas.coords(lines[-1]))
                # normalize_line()
            else:
                canvas.delete(lines[-1])
                lines.pop() 
        else:
            canvas.delete(lines[-1])
            lines.pop()
        print(linedb)

root = Tk()
root.title("dragndrop test")
root.geometry('500x500')
canvas = Canvas(root, borderwidth = 5, relief="ridge", width=500, height=500)
canvas.grid(column = 0, row = 1)
root.grid_propagate(False)
canvas.grid_propagate(False)

def find_widget(x,y):
    root.update()
    for block in blockdb:
        x1 = block.frame.winfo_rootx() - root.winfo_rootx()
        y1 = block.frame.winfo_rooty() - root.winfo_rooty()
        x2 = x1 + block.frame.winfo_width()
        y2 = y1 + block.frame.winfo_height()
    

        if x1 <= x <= x2 and y1 <= y <= y2:
            leftx1 = block.leftport.winfo_rootx() - root.winfo_rootx()
            leftx2 = leftx1 + block.leftport.winfo_width()
            lefty1 = block.leftport.winfo_rooty() - root.winfo_rooty()
            lefty2 = lefty1 + block.leftport.winfo_height()

            rightx1 = block.rightport.winfo_rootx() - root.winfo_rootx()
            rightx2 = rightx1 + block.rightport.winfo_width()
            righty1 = block.rightport.winfo_rooty() - root.winfo_rooty()
            righty2 = righty1 + block.rightport.winfo_height()

            if leftx1 <= x <= leftx2 and lefty1 <= y <= lefty2:
                return(block.leftport)
            elif rightx1 <= x <= rightx2 and righty1 <= y <= righty2:
                return(block.rightport)
            else:
                return None
            
def normalize_line():
    pass
        

bd = BlockDrag()
ld = LineDrag()
block1 = Block(canvas, 3 , 2)
block2 = Block(canvas, 2, 1)
block3 = Block(canvas, 0, 1)
blockdb = [block1, block2, block3]

root.mainloop()