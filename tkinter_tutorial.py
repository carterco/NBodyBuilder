import tkinter as tk

'''
Intro to Tkinter
'''
def intro():
	# Sets up GUI window environment
	root = tk.Tk()

	# Create text "Label" widget -- a "widget" is the base unit of the GUI
	myLabel = tk.Label(root, text="Hello World!")

	# "Pack" all widgets onto the screen - this is the most basic/straighforward way to position things on a GUI
	myLabel.pack()

	# Fun fact - did you know whindows are constantly looping and updating to keep track of the state of the environment? Eg- where your cursor is?
	# This displays the GUI
	root.mainloop()


'''
Positioning with Tkinter's Grid System
'''
# The grid system is set up just like a 2D array (start index 0 row/col)
def grid_sys():
	
	root = tk.Tk()

	myLabel1 = tk.Label(root, text="Hello World!")
	myLabel2 = tk.Label(root, text="My name is Jen!")

	# Place widgets on a grid with row and column indices
	# Note that indices are relative to each other. You cannot use this method to space widgets apart from each other.
	# If there are empty rows/columns, tkinter will simply ignore them and place widgets in only the correct relative positions.
	myLabel1.grid(row = 0, column = 0)
	myLabel2.grid(row = 1, column = 0)

	# Alternative, shorter code:
	# myLabel1 = tk.Label(root, text="Hello World!").grid(row = 0, column = 0)
	# myLabel2 = tk.Label(root, text="My name is Jen!").grid(row = 1, column = 0)

	root.mainloop()