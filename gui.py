from tkinter import *
from tkinter import ttk

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
    Copy_Label = Label(canvas, text=x)
    Copy_Label.grid(row=0, column=0)
    #Window REACT
    
Frontal_Lobe = Button(panel,text="Frontal Lobe",  command=lambda: Replication("Frontal Lobe")).grid(row=1,column=1)
Occipital_Lobe = Button(panel, text="Occipital Lobe", command=lambda: Replication("Occipital Lobe")).grid(row=2,column=1)
Temporal_Lobe = Button(panel, text="Temporal Lobe", command=lambda: Replication("Temporal Lobe")).grid(row=3,column=1)
Parietal_Lobe = Button(panel,text="Parietal Lobe",command=lambda: Replication("Parietal Lobe")).grid(row=4,column=1)



root.mainloop()