# import statements
from tkinter import *
from tkinter import ttk
from tkinter import Widget
from functools import partial
import math

# variable setup
# temporary holidng for coords of current line
coords = [0, 0, 0, 0]
# holding for line ids, used for updating line coords on the canvas in linedrag on_drag()
lines = []
# permanent holding for line coordinates after line has been completed and validated
linedb = []
# colors for port styling
# colors = ["gold", "red", "blue", "green"]
colors = ['red', 'hot pink', 'maroon', 'violet red', 'pale violet red']

class Block():
    '''A class for creating block objects'''
    def __init__(self, parent, lobe_name, leftcount, rightcount, lefttypes, righttypes):
        ''' takes name of parent widget (canvas) and the text of the button (lobe name)'''

        # amount of rows required for block formatting
        total_height = (leftcount if leftcount >= rightcount else rightcount)

        # creates a frame that holds the entire block
        self.frame = ttk.Frame(parent)
        #places the block in the left top corner
        self.frame.grid(column=0, row=0)

        # creates the center portion of the block
        self.label = Label(self.frame, text=lobe_name, borderwidth = 2, relief = 'solid', height = total_height)
        self.label.grid(column=1,row=0, rowspan=total_height)

        # create each left port and append to list
        self.leftports = []
        for index in range(leftcount):
            self.leftports.append(Label(self.frame, width = 1))
            self.leftports[index].configure(bg=colors[lefttypes[index]])
            self.leftports[index].grid(column = 0, row = index)
            self.leftports[index].type = lefttypes[index]
            ld.add_draggable(self.leftports[index])

        # create each right port and append to list
        self.rightports = []
        for index in range(rightcount):
            self.rightports.append(Label(self.frame, width = 1))
            self.rightports[index].configure(bg=colors[righttypes[index]])
            self.rightports[index].grid(column = 2, row = index)
            self.rightports[index].type = righttypes[index]
            ld.add_draggable(self.rightports[index])

        # allows the block button and labels to react when clicked on- center label reacts differently than the ports
        bd.add_draggable(self.label)
        
class BlockDrag():
    '''A class for allowing blocks to drag and drop'''
    def add_draggable(self, widget):
            '''Bind events to functions'''
            widget.bind('<ButtonPress-1>', self.on_start)
            widget.bind('<B1-Motion>', self.on_drag)
            widget.bind("<Button-3>", self.on_rightclick)

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
    
    def on_rightclick(self,event):
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName)
        x = parent.winfo_x() - parent.startx + event.x
        y = parent.winfo_y() - parent.starty + event.y
        m = Menu(root, tearoff = 0)
        m.add_command(label ="Delete", command = lambda:parent.destroy())
        m.add_command(label ="test1")
        m.add_command(label ="test2")
        m.add_command(label ="test3")
        m.tk_popup(x, y)

    

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
        lines.append(canvas.create_line(coords[0],coords[1],coords[0], coords[1], width=3))

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
                # if line is not valid, remove visual line and line in memory
                canvas.delete(lines[-1])
                lines.pop() 
        else:
            canvas.delete(lines[-1])
            lines.pop()
    



    

def create_block(text, leftcnt, rightcnt, lefttypes, righttypes):
    '''function to create blocks on button click'''
    # takes the text that will appear on the block, the number of left ports, the number of right ports, a list of values corresponding to left port types (from top to bottom), and a list of right port values
    block = Block(canvas, text, leftcnt, rightcnt, lefttypes, righttypes)
    blockdb.append(block)

def find_widget(x,y):
    '''function to find the widget under the mouse. Iterates through blockdb and checks if mouse is in the bounds of a port'''
    root.update()
    for block in blockdb:
        # boundary values of the block
        x1 = block.frame.winfo_rootx()-root.winfo_rootx()
        y1 = block.frame.winfo_rooty()-root.winfo_rooty()
        x2 = x1 + block.frame.winfo_width()
        y2 = y1 + block.frame.winfo_height()
    
        # if in port area
        if x1 <= x <= x2 and y1 <= y <= y2:
            # check each left port of the block
            for index in range(len(block.leftports)):
                port = block.leftports[index]
                # boundary values of the port
                portx1 = port.winfo_rootx() - root.winfo_rootx()
                portx2 = portx1 + port.winfo_width()
                porty1 = port.winfo_rooty() - root.winfo_rooty()
                porty2 = porty1 + port.winfo_height()
                # if mouse location is in the boundary, return the port
                if portx1 <= x <= portx2 and porty1 <= y <= porty2:
                    return block.leftports[index]
            # if mouse is not in a left port, check each right port
            for index in range(len(block.rightports)):
                port = block.rightports[index]
                portx1 = port.winfo_rootx() - root.winfo_rootx()
                portx2 = portx1 + port.winfo_width()
                porty1 = port.winfo_rooty() - root.winfo_rooty()
                porty2 = porty1 + port.winfo_height()
                if portx1 <= x <= portx2 and porty1 <= y <= porty2:
                    return block.rightports[index]
    # returns None if mouse is in a block but NOT in a port, or is not in a block at all
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

# create buttons in the panel and bind to creating Block objects with expected values
frontal_btn = Button(panel,text="Frontal Lobe", command = partial(create_block, "Frontal Lobe", 1, 1, [0], [1]))
frontal_btn.grid(row=1,column=1)
occipital_btn = Button(panel, text="Occipital Lobe", command = partial(create_block, "Occipital Lobe", 1, 2, [2], [0, 4]))
occipital_btn.grid(row=2,column=1)
temporal_btn = Button(panel, text="Temporal Lobe", command = partial(create_block, "Temporal Lobe", 2, 3, [4, 1], [1, 2, 3]))
temporal_btn.grid(row=3,column=1)
parietal_btn = Button(panel,text="Parietal Lobe", command = partial(create_block, "Parietal Lobe", 3, 0, [1, 2, 3], []))
parietal_btn.grid(row=4,column=1)


#this funcion checks when a line is clicked and deletes it both on the canvas and in lines
def on_rightline(e):
    x = e.x
    y = e.y
    m = Menu(root, tearoff = 0)
    lineDelete = canvas.find_overlapping(x,y,x,y)
    if lineDelete:
        m.add_command(label ="Delete", command = lambda:line_delete(lineDelete))
        m.add_command(label ="test1")
        m.add_command(label ="test2")
        m.add_command(label ="test3")
        x = canvas.winfo_pointerx()
        y = canvas.winfo_pointery()
        m.tk_popup(x, y)
    

def line_delete(lineDelete):
    if lineDelete:
        linecheck = [canvas.coords(lineDelete[0])[0], canvas.coords(lineDelete[0])[1], canvas.coords(lineDelete[0])[2], canvas.coords(lineDelete[0])[3]]
        linedb.remove(linecheck)
        canvas.delete(lineDelete[0])
        lines.remove(lineDelete[0])
        

temp = None

def find_line(e):
    x = e.x
    y = e.y

    overlaps = canvas.find_overlapping(x,y,x,y)
    if overlaps:
        global temp
        temp = overlaps[0]


def move_line(e):
    x = e.x
    y = e.y
    if temp:
        canvas.coords(temp, canvas.coords(temp)[0], canvas.coords(temp)[1], x, y)

def verify_line(e):
    global temp
    if temp:
        start_port = find_widget(canvas.coords(temp)[0], canvas.coords(temp)[1])
        end_port = find_widget(canvas.coords(temp)[2], canvas.coords(temp)[3])
        if start_port and end_port:
            if start_port.type == end_port.type:
                linedb.append(canvas.coords(temp))
                # normalize_line()
            else:
                # if line is not valid, remove visual line and line in memory
                canvas.delete(temp)
                lines.pop() 
        else:
            canvas.delete(temp)
            lines.pop()
        temp = None
    

canvas.bind("<Button-3>", on_rightline)
canvas.bind("<ButtonPress-1>", find_line)
canvas.bind("<B1-Motion>", move_line)
canvas.bind("<ButtonRelease-1>", verify_line)

# loop the root window to listen for events
root.mainloop()