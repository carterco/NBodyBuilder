import tkinter as tk
#import PIL as ImageTk,Image  # Needs to be pip installed?
import numpy as np
import matplotlib.pyplot as plt

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
def grid_sys():
	
	root = tk.Tk()

	myLabel1 = tk.Label(root, text="Hello World!")
	myLabel2 = tk.Label(root, text="My name is Jen!")

	# Place widgets on a grid with row and column indices
	# The grid system is set up just like a 2D array (start index 0 row/col)
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
		borderwidth: (int) makes box boarder wider
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

'''
Simple Calculator App
'''
def calculator_ex():
	root = tk.Tk()

	# Entry widget
	entry = tk.Entry(root, width = 35, borderwidth = 5)
	entry.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

	def button_click(number):
		current = entry.get()
		# Delete current box entry so numbers are not continuously appended
		entry.delete(0,'end')
		# Use buttons to populate entry box, for multiple digit numbers, add new click after previous clicks
		entry.insert(0, str(current) + str(number))

	def button_clear():
		entry.delete(0,'end')

	def button_add():
		global a
		global math
		math = 'addition'
		a = int(entry.get())
		entry.delete(0,'end')

	def button_subtract():
		global a
		global math
		math = 'subtraction'
		a = int(entry.get())
		entry.delete(0,'end')

	def button_multiply():
		global a
		global math
		math = 'multiplication'
		a = int(entry.get())
		entry.delete(0,'end')

	def button_divide():
		global a
		global math
		math = 'division'
		a = int(entry.get())
		entry.delete(0,'end')

	def button_equals():
		b = int(entry.get())
		entry.delete(0,'end')
		if math == 'addition':
			entry.insert(0, a+b)
		if math == 'subtraction':
			entry.insert(0, a-b)
		if math == 'multiplication':
			entry.insert(0, a*b)
		if math == 'division':
			entry.insert(0, a/b)



	# Button widgets
	b1 = tk.Button(root, text = "1", padx = 40, pady = 20, command = lambda: button_click(1))
	b2 = tk.Button(root, text = "2", padx = 40, pady = 20, command = lambda: button_click(2))
	b3 = tk.Button(root, text = "3", padx = 40, pady = 20, command = lambda: button_click(3))
	b4 = tk.Button(root, text = "4", padx = 40, pady = 20, command = lambda: button_click(4))
	b5 = tk.Button(root, text = "5", padx = 40, pady = 20, command = lambda: button_click(5))
	b6 = tk.Button(root, text = "6", padx = 40, pady = 20, command = lambda: button_click(6))
	b7 = tk.Button(root, text = "7", padx = 40, pady = 20, command = lambda: button_click(7))
	b8 = tk.Button(root, text = "8", padx = 40, pady = 20, command = lambda: button_click(8))
	b9 = tk.Button(root, text = "9", padx = 40, pady = 20, command = lambda: button_click(9))
	b0 = tk.Button(root, text = "0", padx = 40, pady = 20, command = lambda: button_click(0))
	add = tk.Button(root, text = "+", padx = 39, pady = 20, command = button_add)
	sub = tk.Button(root, text = "-", padx = 39, pady = 20, command = button_subtract)
	mult = tk.Button(root, text = "*", padx = 39, pady = 20, command = button_multiply)
	div = tk.Button(root, text = "/", padx = 39, pady = 20, command = button_divide)
	equals = tk.Button(root, text = "=", padx = 91, pady = 20, command = button_equals)
	clear = tk.Button(root, text = "Clear", padx = 79, pady = 20, command = button_clear)

	# Place buttons on grid
	b1.grid(row = 3, column = 0)
	b2.grid(row = 3, column = 1)
	b3.grid(row = 3, column = 2)

	b4.grid(row = 2, column = 0)
	b5.grid(row = 2, column = 1)
	b6.grid(row = 2, column = 2)

	b7.grid(row = 1, column = 0)
	b8.grid(row = 1, column = 1)
	b9.grid(row = 1, column = 2)

	b0.grid(row = 4, column = 0)
	clear.grid(row = 4, column = 1, columnspan=2)
	add.grid(row = 5, column = 0)
	equals.grid(row = 5, column = 1, columnspan=2)

	sub.grid(row = 6, column = 0)
	mult.grid(row = 6, column = 1)
	div.grid(row = 6, column = 2)

	root.mainloop()

'''
Icons, Images, and Exit Buttons
'''
def icons_images_exits():
	root = tk.Tk()
	# Adds title to window
	root.title('Learn Icons, Images, and Exits')
	#root.iconbitmap('') # Need .ico icon file

	# Using images
	#img = ImageTk.PhotoImage(Image.open('')) # Need image file
	#label = tk.Label(image = img)
	#label.pack()

	# Add quit button widget
	quit = tk.Button(root,text='Exit',command = root.quit)
	quit.pack()
	root.mainloop()

'''
Building Image Viewer App
'''
# SKIPPED

'''
Status Bar
'''
# SKPPED

'''
Frames
'''
# SKIPPED

'''
Radio Buttons
'''
# SKIPPED

'''
Message Boxes
'''
# SKIPPED

'''
New Windows
'''
# SKIPPED

'''
Open Files Dialog Box
'''
# SKIPPED

'''
Slider
'''
# SKIPPED

'''
Checkboxes
'''
# SKIPPED

'''
Dropdown Menu
'''
def dropdown():
	root = tk.Tk()
	root.title('Dropdown Menus')

	def show():
		myLabel = tk.Label(root, text = clicked.get()).pack()

		options = [
			"Monday",
			"Tuesday",
			"Wednesday",
			"Thursday",
			"Friday"
		]
		# "clicked" is the variable the chosen option is assigned to
		clicked = tk.StringVar()
		# Set default menu item
		clicked.set(options[0])
		drop = tk.OptionMenu(root, clicked,*options)
		drop.pack()

		myButton = tk.Button(root,text = 'Show Selection', command = show).pack()

		root.mainloop()

'''
Using Databases
'''
# SKIPPED

'''
Building out GUI for Database App
'''
# SKIPPED

'''
Delete Record from Database
'''
# SKIPPED

'''
Update Record with SQLite
'''
# SKIPPED

'''
Build Weather App
'''
# SKIPPED

'''
Change Weather App Colors
'''
# SKIPPED

'''
Zipcode Lookup Form
'''
# SKIPPED

'''
Matplotlib Charts
'''
#def plotting():
root = tk.Tk()

def graph():
	house_prices = np.random.normal(200000,25000,5000)
	plt.hist(house_prices, 50)
	plt.show()
myGraph = tk.Button(root,text = "Graph it!", command = graph)
myGraph.pack()

root.mainloop()