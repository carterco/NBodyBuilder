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


'''
Creating Buttons
'''

def create_button():
	'''
	Options:
		state:
			DISABLED: greys out button so it is not clickable
		padx: (int) alters width of button
		pady: (int) alters height of button
		command: (function) function of button
		fg: (str) foreground (text) color, hex codes also work
		bg: (str) background (button) color, hex codes also work
	'''
	root = tk.Tk()

	# Function to define what the button does
	def myClick():
		myLabel = tk.Label(root, text='Look! I clicked a Button!!')
		myLabel.pack()

	# Button widget
	myButton = tk.Button(root, text="Click Me!", command = myClick)

	# Pack button
	myButton.pack()

	root.mainloop()


'''
Input Fields
'''

def input_box():

	'''
	Options:
		width: (int) width of box
		boarderwidth: (int) makes box boarder wider
		fg: (str) foreground (text) color, hex codes also work
		bg: (str) background (button) color, hex codes also work

	'''
	root = tk.Tk()

	# Entry widget
	entry = tk.Entry(root)
	entry.pack()

	# Puts default text inside textbox
	e.insert(0, "Name")

	# Function to define what the button does
	def myClick():
		hello = "Hello " + entry.get()
		myLabel = tk.Label(root, text=hello)
		myLabel.pack()

	# Button widget
	myButton = tk.Button(root, text="Enter your name:", command = myClick)
	myButton.pack()

	root.mainloop()