def LeapFrog(x, v, m, dt):
	"""Leapfrog stepper

	Calculate the position and velocity of a particle at time t+dt

	Args:
		x (array): numpy array of particle positions
		v (array): numpy array of particle velocities
		m (array): numpy array of particle masses
		dt (float): time step 
	
	Returns:
		array: positions(x) for the next time step
		array: velocities(v) for the next time step
	"""
	x = x + dt*v
	a = ComputeAccel(x, m)
	v = v + dt*a
	return (x,v)

def Euler(x, v, m, dt):
	"""Euler stepper

	Calculate the position and velocity of a particle at time t+dt

	Args:
		x (array): numpy array of particle positions
		v (array): numpy array of particle velocities
		m (array): numpy array of particle masses
		dt (float): time step 
	
	Returns:
		array: positions(x) for the next time step
		array: velocities(v) for the next time step
	"""

	dv = dt * ComputeAccel(x, m)
	dx = dt * v
	v += dv
	x += dx

	return (x,v)

def Euler_Cromer(x, v, m, dt):
	"""Euler-Cromer stepper

	Calculate the position and velocity of a particle at time t+dt

	Args:
		x (array): numpy array of particle positions
		v (array): numpy array of particle velocities
		m (array): numpy array of particle masses
		dt (float): time step 
	
	Returns:
		array: positions(x) for the next time step
		array: velocities(v) for the next time step
	"""

	dv = dt * ComputeAccel(x, m)
	v += dv
	dx = dt * v
	x += dx

	return (x,v)