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

panel = ttk.Frame(root, borderwidth=5, relief="ridge", width=200, height=500)
panel.grid(column=1, row=1)
panel.grid_propagate(False)

opt1='test'
widget1 = ttk.Combobox(panel, text='test2', textvariable=opt1)
widget1['values'] = ('Choice 1', 'Choice 2', 'Choice 3')
widget1.state(["readonly"])
widget1.grid(row=0, column=0)

root.config(menu=menubar)
root.mainloop()