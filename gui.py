# import statements
from tkinter import *
from tkinter import ttk
from tkinter import Widget
from functools import partial

# variable setup
coords = [0, 0, 0, 0]
lines = []
linedb = []
colors = ["gold", "red", "blue", "green"]

class Block():
    '''A class for creating block objects'''
    def __init__(self, parent, lobe_name, lefttype, righttype):
        ''' takes name of parent widget (canvas) and the text of the button (lobe name)'''

        # creates a frame that holds the entire block
        self.frame = ttk.Frame(parent)
        self.frame.grid(column=0, row=0)

        # creates the center portion of the block
        self.label = ttk.Button(self.frame, text=lobe_name)
        self.label.grid(column=1,row=0)

        # creates the left port and configures according to type
        self.leftport = Label(self.frame, width = 1)
        self.leftport.configure(bg=colors[lefttype])
        self.leftport.grid(column=0, row=0)
        self.leftport.type = lefttype

        # creates the right port and configures according to type
        self.rightport = Label(self.frame, width = 1)
        self.rightport.configure(bg=colors[righttype])
        self.rightport.grid(column=2, row=0)
        self.rightport.type = righttype

        # allows the block button and labels to react when clicked on- center label reacts differently than the ports
        bd.add_draggable(self.label)
        ld.add_draggable(self.leftport)
        ld.add_draggable(self.rightport)
        
class BlockDrag():
    '''A class for allowing blocks to drag and drop'''
    def add_draggable(self, widget):
            '''Bind events to functions'''
            widget.bind('<ButtonPress-1>', self.on_start)
            widget.bind('<B1-Motion>', self.on_drag)

    def on_start(self, event):
        '''when button is clicked, record the starting location in the parent'''
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName) 
        parent.startx = event.x
        parent.starty = event.y

    def on_drag(self, event):
        '''when button is dragged, replace the button in the new location at every movement'''
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName)
        x = parent.winfo_x() - parent.startx + event.x
        y = parent.winfo_y() - parent.starty + event.y
        parent.place(x=x, y=y)

class LineDrag():
    '''A class for allowing ports to react when clicked'''
    def add_draggable(self, widget):
        '''Bind events to functions'''
        widget.bind('<ButtonPress-1>', self.on_start)
        widget.bind('<B1-Motion>', self.on_drag)
        widget.bind('<ButtonRelease-1>', self.on_release)
    
    def on_start(self, event):
        '''when port is clicked, create a line with start and end at the same location'''
        x = canvas.winfo_pointerx()-canvas.winfo_rootx()
        y = canvas.winfo_pointery()-canvas.winfo_rooty()
        coords[0] = x
        coords[1] = y
        lines.append(canvas.create_line(coords[0],coords[1],coords[0], coords[1]))

    def on_drag(self, event):
        '''when port is dragged, edit the existing line from the startpoint to the mouse's current location'''
        x = canvas.winfo_pointerx()-canvas.winfo_rootx()
        y = canvas.winfo_pointery()-canvas.winfo_rooty()
        coords[2] = x
        coords[3] = y
        canvas.coords(lines[-1], coords[0],coords[1], x, y)

    def on_release(self, event):
        '''when port is released, do some final checks before adding the line to memory. If line position is invalid, delete the line and remove it from memory'''
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

def find_widget(x,y):
    '''function to find the widget under the mouse. Iterates through blockdb and checks if mouse is in the bounds of a port'''
    root.update()
    for block in blockdb:
        x1 = block.frame.winfo_rootx()-root.winfo_rootx()
        y1 = block.frame.winfo_rooty()-root.winfo_rooty()
        x2 = x1+ block.frame.winfo_width()
        y2 = y1+ block.frame.winfo_height()
    

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

# basic tkinter setup
root = Tk()
root.title("Build-a-Brain")
root.rowconfigure(1,weight=1)
root.columnconfigure(0,weight=1)

# window is divided into three portions: menu, panel, and canvas
menubar = Menu(root)
root.config(menu=menubar)

# menu setup
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

# canvas setup
canvas = Canvas(root, borderwidth=5, relief="ridge", width=500, height=500)
canvas.grid(column=0, row=1, sticky="nswe", columnspan=1, rowspan=1)
canvas.grid_propagate(False)

# panel setup
panel = ttk.Frame(root, borderwidth=5, relief="ridge", width=200, height=500)
panel.grid(column=1, row=1,sticky="nswe", columnspan=1, rowspan=1)
panel.grid_propagate(False)

# setup class objects for enabling block reactivity
bd = BlockDrag()
ld = LineDrag()
blockdb = []

def create_block(text, left, right):
    block = Block(canvas, text, left, right)
    blockdb.append(block)
    print(blockdb)

# create buttons in the panel and bind to creating Block objects
frontal_btn = Button(panel,text="Frontal Lobe", command = partial(create_block, "Frontal Lobe", 0, 1))
frontal_btn.grid(row=1,column=1)
occipital_btn = Button(panel, text="Occipital Lobe", command = partial(create_block, "Occipital Lobe", 1, 2))
occipital_btn.grid(row=2,column=1)
temporal_btn = Button(panel, text="Temporal Lobe", command = partial(create_block, "Temporal Lobe", 2, 3))
temporal_btn.grid(row=3,column=1)
parietal_btn = Button(panel,text="Parietal Lobe", command = partial(create_block, "Parietal Lobe", 3, 0))
parietal_btn.grid(row=4,column=1)


# block1 = Block(canvas, "button 1", 3 , 2)
# block2 = Block(canvas, "button 2", 2, 1)
# block3 = Block(canvas, "button 3", 0, 1)
# blockdb = [block1, block2, block3]


# loop the root window to listen for events
root.mainloop()