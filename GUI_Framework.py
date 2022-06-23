import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()
root.title('NBodyBuilder')
#root.geometry('400x250')


# Make N particle slider
particleLabel = tk.Label(root, text="Enter number of particles:")

def read_slide(var):
	global N
	N = num_particles.get()
num_particles = tk.Scale(root, from_=2, to=10,orient ='horizontal',command = read_slide)

# Make dropdown for gravity solver
solverLabel = tk.Label(root, text="Choose a gravity solver:")

def show_solver(var):
	global S
	S = solver.get()

options_solver = [
	"Barnes-Hut",
	"Direct Force"]

solver = tk.StringVar()
solver.set(options_solver[0])
solver_drop = tk.OptionMenu(root, solver,*options_solver,command = show_solver)


# Make dropdown for potential
distLabel = tk.Label(root, text="Choose a distribution:")

def show_dist(var):
	global D
	D = dist.get()

options_dist = [
	"Hernquist",
]
dist = tk.StringVar()
dist.set(options_dist[0])
dist_drop = tk.OptionMenu(root, dist,*options_dist,command = show_dist)


# Make dropdown for stepping function
stepLabel = tk.Label(root, text="Choose a stepping function:")

def show_step(var):
	global D
	D = step.get()

options_step = [
	"Euler",
	"Euler-Cromer",
	"Leapfrog"
]
step = tk.StringVar()
step.set(options_step[0])
step_drop = tk.OptionMenu(root, step,*options_step,command = show_step)


# Make entry box for time step
timestepLabel = tk.Label(root, text="Choose a timestep:")

def show_timestep():
	global DT
	DT = dt.get() 
dt = tk.Entry(root)
# Puts default text inside textbox
dt.insert(0, "0.01")
# Button to get timestep value
timestep_botton = tk.Button(root, text="Submit", command = show_timestep)


# Make entry box for time
timeLabel = tk.Label(root, text="Choose a run time:")

def show_time():
	global T
	T = dt.get() 
t = tk.Entry(root)
# Puts default text inside textbox
t.insert(0, "1")
# Button to get timestep value
time_botton = tk.Button(root, text="Submit", command = show_time)


# Make button to plot result
def graph():
	house_prices = np.random.normal(200000,25000,5000)
	plt.hist(house_prices, 50)
	plt.show()
plot = tk.Button(root,text = "Run and Plot", command = graph)


# Place widgets on grid
particleLabel.grid(row = 0,column = 0)
num_particles.grid(row = 0,column = 1)
solverLabel.grid(row = 1, column = 0)
solver_drop.grid(row = 1, column = 1)
distLabel.grid(row = 2, column = 0)
dist_drop.grid(row = 2, column = 1)
stepLabel.grid(row = 3, column = 0)
step_drop.grid(row = 3, column = 1)
timestepLabel.grid(row = 4, column = 0)
dt.grid(row = 4, column = 1)
timestep_botton.grid(row = 4, column = 2)
timeLabel.grid(row = 5, column = 0)
t.grid(row = 5, column = 1)
time_botton.grid(row = 5, column = 2)
plot.grid(row = 6, column = 0, columnspan = 3)


root.mainloop()
