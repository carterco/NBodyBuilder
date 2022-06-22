import numpy

def LeapFrog(x, v, m, dt):
	""" Performs one leap frog step, returns updated (x,v) """
	x = x + dt*v
	a = ComputeAccel(x, m)
	v = v + dt*a
	return (x, v)

def Euler(x, v, m, dt):
	"""Takes a single Euler 1st order step using the same variables as rk4 step
		values      = dependent variables
		deriv       = derivatives 
		start       = initial time
		delta       = tj+1 - t_j = time step 
		returns:      values for the next step."""

	dv = dt * ComputeAccel(x,m)
	dx = dt * v
	v += dv
	x += dx

	return (x,v)

def Euler_Cromer(x, v, m, dt):

	dv = dt * ComputeAccel(x,m)
	v += dv
	dx = dt * v
	x += dx

	return (x,v)