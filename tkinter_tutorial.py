import tkinter as tk

# Sets up GUI window environment
root = tk.Tk()

# Create text "Label" widget -- a "widget" is the base unit of the GUI
myLabel = tk.Label(root, text="Hello World!")

# "Pack" all widgets onto the screen - this is the most basic/straighforward way to position things on a GUI
myLabel.pack()

# Fun fact - did you know whindows are constantly looping and updating to keep track of the state of the environment? Eg- where your cursor is?
# This displays the GUI
root.mainloop()