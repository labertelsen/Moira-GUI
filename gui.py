# import statements
from tkinter import *
from tkinter import ttk
from tkinter import Widget
from functools import partial
from tkinter import filedialog
import csv

# variable setup
# temporary holding for coords of current line
coords = [0, 0, 0, 0]
# holding for line ids, used for updating line coords on the canvas in linedrag on_drag()
lines = []
# colors for port styling
colors = ["gold", "red", "blue", "green", "orange"]

# holding var for line on rightclick deletion
temp = None
# This holds the cordinates of the blocks 
blockcoords = []

blockinformation = []




class Block():
    '''A class for creating block objects'''
    def __init__(self, parent, lobe_name, leftcount, rightcount, lefttypes, righttypes):
        ''' takes name of parent widget (canvas) and the text of the button (lobe name)'''
        
        self.title = lobe_name
        self.leftcount = leftcount 
        self.rightcount = rightcount
        self.lefttypes = lefttypes
        self.rightypes = righttypes 
        

        # amount of rows required for block formatting
        total_height = (leftcount if leftcount >= rightcount else rightcount)
    
        # creates a frame that holds the entire block
        self.frame = ttk.Frame(parent)
        #places the block in the left top corner
        self.frame.grid(column=0, row=0)

        # creates the center portion of the block
        self.label = Label(self.frame, text=lobe_name, borderwidth = 2, relief = 'solid', height = total_height)
        self.label.grid(column=1,row=0, rowspan=total_height)

        # create each left port and append to list, create inner list of line IDs for each port
        self.leftports = []
        for index in range(leftcount):
            self.leftports.append(0)
            self.leftports[index] = [Label(self.frame, width=1), []]
            self.leftports[index][0].configure(bg=colors[lefttypes[index]])
            self.leftports[index][0].grid(column = 0, row = index)
            self.leftports[index][0].type = lefttypes[index]
            # not draggable to limit line flow

        # create each right port and append to list, create inner list of line IDs for each port
        self.rightports = []
        for index in range(rightcount):
            self.rightports.append(0)
            self.rightports[index] = [Label(self.frame, width = 1), []]
            self.rightports[index][0].configure(bg=colors[righttypes[index]])
            self.rightports[index][0].grid(column = 2, row = index)
            self.rightports[index][0].type = righttypes[index]
            ld.add_draggable(self.rightports[index][0])

        # allows the block button and labels to react when clicked on- center label reacts differently than the ports
        bd.add_draggable(self.label)


    # function for deleting blocks and scrubbing memory
    def destroy(widget):
        # given label, find parent frame
        parentName = widget.winfo_parent()
        parent = widget._nametowidget(parentName)
        # space to hold lines attatched to deleted block, to be scrubbed
        scrub_list = []

        delete_block = None
        # search db for object with matching frame
        for block in blockdb:
            if block.frame == parent:
                delete_block = block
                # for each left port
                for index in range(len(block.leftports)):
                    # get the inner list of line IDs
                    lines_list = block.leftports[index][1]
                    # for each line
                    for i2 in range(len(lines_list)):
                        line = lines_list[i2]
                        # add line to scrub list and delete the line visual
                        scrub_list.append(line)
                        line_delete_on_block_delete(line)

                # for each right port, do the same as above
                for index in range(len(block.rightports)):
                    lines_list = block.rightports[index][1]
                    for i2 in range(len(lines_list)):
                        line = lines_list[i2]
                        scrub_list.append(line)
                        line_delete_on_block_delete(line)

        # check each block for any lines in the scrub list and remove
        for block in blockdb:
            for port in block.leftports:
                lines_list = port[1]
                for index in range(len(lines_list)):
                    if lines_list[index] in scrub_list:
                        lines_list.remove(lines_list[index])
            for port in block.rightports:
                lines_list = port[1]
                for index in range(len(lines_list)):
                    if lines_list[index] in scrub_list:
                        lines_list.remove(lines_list[index])

        # remove block from block db
        blockdb.remove(delete_block)
        # destroy block visual
        parent.destroy()
    
    def values_of_block(self):
        return (self.title,self.leftcount,self.rightcount, self.lefttypes, self.rightypes)      

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
        # lines follow block in drag
        for block in blockdb:
            if block.frame == parent:
                curr_block = block
            else:
                pass
        
        # adjust lines on leftports
        for index in range(len(curr_block.leftports)):
            port = curr_block.leftports[index]
            port_connections = port[1]
            for line in port_connections:
                normalize_on_drag(line, port[0], 'L')
        # adjust lines on rightports
        for index in range(len(curr_block.rightports)):
            port = curr_block.rightports[index]
            port_connections = port[1]
            for line in port_connections:
                normalize_on_drag(line, port[0], 'R')
            
        
    
    def on_rightclick(self,event):
        widget = event.widget
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName)
        x = canvas.winfo_pointerx()
        y = canvas.winfo_pointery()
        m = Menu(root, tearoff = 0)
        # on delete button, call destroy function in block class and pass the label of the clicked block
        m.add_command(label ="Delete", command = partial(Block.destroy, widget))
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
        start_return = find_widget(canvas.coords(lines[-1])[0], canvas.coords(lines[-1])[1])
        end_return = find_widget(canvas.coords(lines[-1])[2], canvas.coords(lines[-1])[3])
        if start_return and end_return:
            start_block = start_return[0]
            start_port_index = start_return[1]
            end_block = end_return[0]
            end_port_index = end_return[1]
            
            start_port = start_block.rightports[start_port_index]
            end_port = end_block.leftports[end_port_index]

            # verify line is not output to output
            if start_return[2] != 'R' and end_return[2] != 'L':
                start_port = None
                end_port = None

            if start_port and end_port:
                if (start_port[0].type == end_port[0].type):
                    # linedb.append(canvas.coords(lines[-1]))
                    
                    # add lines to port inner list
                    start_block.rightports[start_port_index][1].append(lines[-1])
                    end_block.leftports[end_port_index][1].append(lines[-1])

                    normalize_line(lines[-1], start_port[0], end_port[0])
                else:
                    # if line is not valid, remove visual line and line in memory
                    canvas.delete(lines[-1])
                    lines.pop() 
            else:
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


# Place Block function
def create_from_file(reference):
    for container in reference:
        for ele in container:
            if ele.isdigit():
                swap_location = container.index(ele)
                container[swap_location] = int(container[swap_location])

        x1 = container[0]
        y1 = container[1]
        x2 = container[2]
        y2 = container[3]
        x = (x1+x2)/2
        y= (y1+y2)/2
        text = container[4]
        leftcnt = container[5]
        rightcnt = container[6]
        pre_lefttypes =  list(container[7].split(" "))
        lefttypes = []
        pre_righttypes = list(container[8].split(" "))
        righttypes = []
        for primary in pre_lefttypes:            
            for ele in primary:
                if ele.isdigit():
                    lefttypes.append(int(ele))
        if pre_righttypes.count('[]')>0:
            righttypes = []
        else:   
             for primary in pre_righttypes:            
                 for ele in primary:
                    if ele.isdigit():
                        righttypes.append(int(ele))

        block_placement(text, leftcnt,rightcnt,lefttypes,righttypes,x,y)            
       
  
def block_placement(text, leftcnt,rightcnt,lefttypes,righttypes,x,y):

    block= Block(canvas, text, leftcnt, rightcnt, lefttypes, righttypes)
    blockdb.append(block)

            



def find_widget(x,y):
    '''function to find the widget under the mouse. Iterates through blockdb and checks if mouse is in the bounds of a port'''
    root.update()
    for block in blockdb:

        x1, y1, x2, y2 = find_position(block.frame)
    
        # if in port area
        if x1 <= x <= x2 and y1 <= y <= y2:
            # check each left port of the block
            for index in range(len(block.leftports)):
                port = block.leftports[index][0]
                portx1, porty1, portx2, porty2 = find_position(port)
                # if mouse location is in the boundary, return the port
                if portx1 <= x <= portx2 and porty1 <= y <= porty2:
                    return block, index, 'L'
                
            # if mouse is not in a left port, check each right port
            for index in range(len(block.rightports)):
                port = block.rightports[index][0]
                portx1, porty1, portx2, porty2 = find_position(port)
                if portx1 <= x <= portx2 and porty1 <= y <= porty2:
                    return block, index, 'R'
                
    # returns None if mouse is in a block but NOT in a port, or is not in a block at all
    return None

def find_position(widget):
    # returns boundary values of a widget
    x1 = widget.winfo_rootx()-root.winfo_rootx()
    y1 = widget.winfo_rooty()-root.winfo_rooty()
    x2 = x1 + widget.winfo_width()
    y2 = y1 + widget.winfo_height()
    return(x1, y1, x2, y2)


            
def normalize_line(lineid, startport, endport):
    # normalize both ends of line on release
    startx1, starty1, startx2, starty2 = find_position(startport)
    endx1, endy1, endx2, endy2 = find_position(endport)
    canvas.coords(lineid, (startx1+startx2)/2, (starty1+starty2)/2, (endx1+endx2)/2, (endy1+endy2)/2)

def normalize_on_drag(lineid, port, side):
    # normalize a single end of line on block drag
    if side == 'R':
        x1, y1, x2, y2 = find_position(port)
        endx = canvas.coords(lineid)[2]
        endy = canvas.coords(lineid)[3]
        canvas.coords(lineid, (x1+x2)/2, (y1+y2)/2, endx, endy)

    elif side == 'L':
        x1, y1, x2, y2 = find_position(port)
        startx = canvas.coords(lineid)[0]
        starty = canvas.coords(lineid)[1]
        canvas.coords(lineid, startx, starty, (x1+x2)/2, (y1+y2)/2)
    

#this funcion checks when a line is clicked and creates a pop up for choices
def on_rightline(e):
    x = e.x
    y = e.y
    #creates the menu dropdown
    m = Menu(root, tearoff = 0)
    #checks what is being clicked
    lineDelete = canvas.find_overlapping(x,y,x,y)
    if lineDelete: 
        m.add_command(label ="Delete", command = lambda:line_delete(lineDelete))
        m.add_command(label ="test1")
        m.add_command(label ="test2")
        m.add_command(label ="test3")
        x = canvas.winfo_pointerx()
        y = canvas.winfo_pointery()
        #click is where the popup shows
        m.tk_popup(x, y)

#this funcion deletes a line when input with the list of clicked on items
def line_delete(lineDelete):
    if lineDelete:
        line = lineDelete[0]
        canvas.delete(line)
        lines.remove(line)

        # scrub blocks for line to be deleted
        for block in blockdb:
            for port in block.leftports:
                lines_list = port[1]
                for index in range(len(lines_list)):
                    if lines_list[index] == line:
                        lines_list.remove(line)
            for port in block.rightports:
                lines_list = port[1]
                for index in range(len(lines_list)):
                    if lines_list[index] == line:
                        lines_list.remove(line)

        lineDelete= ()

def line_delete_on_block_delete(line):
    if line:
        canvas.delete(line)
        
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
        start_return = find_widget(canvas.coords(temp)[0], canvas.coords(temp)[1])
        end_return = find_widget(canvas.coords(temp)[2], canvas.coords(temp)[3])
        
        if start_return and end_return:
            start_block = start_return[0]
            start_port_index = start_return[1]
            end_block = end_return[0]
            end_port_index = end_return[1]
            
            start_port = start_block.rightports[start_port_index]
            end_port = end_block.leftports[end_port_index]

            # verify line is not output to output
            if start_return[2] != 'R' and end_return[2] != 'L':
                start_port = None
                end_port = None

            if start_port and end_port:
                if start_port[0].type == end_port[0].type:
                    pass
                else:
                    # if line is not valid, remove visual line and line in memory
                    canvas.delete(temp)
                    lines.pop() 
            else:
                canvas.delete(temp)
                lines.pop()
        else:
                canvas.delete(temp)
                lines.pop()
        temp = None


# basic tkinter setup
root = Tk()
root.title("Build-a-Brain")
root.rowconfigure(1,weight=1)
root.columnconfigure(0,weight=1)
#Save set up
def save_as_file():
    merger = [] 
    for i in blockdb:
        block_info =  i.values_of_block()
        blockinformation.append(block_info)

    for i in blockdb:
        blockcoords.append(find_position(i.frame))

    for i in range(len(blockinformation)):
        merger.append(blockinformation[i])
        merger.append(blockcoords[i])

    data_file = filedialog.asksaveasfile(defaultextension=".*",mode='w',initialdir=r"C:\Users\ljwil\OneDrive\Documents\GitHub\Moira-GUI", title="Save File", filetypes = (("CSV Files","*.csv"),))
    
    if data_file:
        data_file_writer =  csv.writer(data_file, delimiter=',')

        for i in range(1,len(merger),2):
            data_file_writer.writerow(merger[i]+merger[i-1])         

        merger.clear()
        blockcoords.clear()
        blockinformation.clear() 
        data_file.close()

#open file set up and placing blocks 
def open_file():
      data_file = filedialog.askopenfile(mode='r',initialdir=r"C:\Users\ljwil\OneDrive\Documents\GitHub\Moira-GUI", title="Open File", filetypes = (("CSV Files","*.csv"),))
      #data_file = open(data_file, "r")
      #content  =  data_file.read()
      #print(content)
      reference = []
      if data_file:
          data_file_reader = csv.reader(data_file)
          for i in data_file_reader:
              if i == []:
                  continue
              reference.append(i)
        
      create_from_file(reference)
      reference.clear()
      data_file.close()



      

# window is divided into three portions: menu, panel, and canvas
menubar = Menu(root)
root.config(menu=menubar)

# menu setup
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='Run', command=None)
file.add_command(label='New', command=None)
file.add_command(label='Save As', command=lambda :save_as_file())
file.add_command(label="Save",command=None)
file.add_command(label='Open', command=lambda : open_file())
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

# bind canvas clicks to events
canvas.bind("<Button-3>", on_rightline)
canvas.bind("<ButtonPress-1>", find_line)
canvas.bind("<B1-Motion>", move_line)
canvas.bind("<ButtonRelease-1>", verify_line)
#reading out details of blocks

# loop the root window to listen for events
root.mainloop()