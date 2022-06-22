def LeapFrog(x, v, m, dt):
	"""Performs one leap frog step
		x           = particle positions
		v           = particle velocities 
		m           = particle masses
		dt          = time step 
		returns:      positions(x) and velocities(v) for the next step."""
	x = x + dt*v
	a = ComputeAccel(x, m)
	v = v + dt*a
	return (x,v)

def Euler(x, v, m, dt):
	"""Takes a single Euler 1st order step
		x           = particle positions
		v           = particle velocities 
		m           = particle masses
		dt          = time step 
		returns:      positions(x) and velocities(v) for the next step."""

	dv = dt * ComputeAccel(x, m)
	dx = dt * v
	v += dv
	x += dx

	return (x,v)

def Euler_Cromer(x, v, m, dt):
	"""Takes a single Euler-Cromer energy conserving step
		x           = particle positions
		v           = particle velocities 
		m           = particle masses
		dt          = time step 
		returns:      positions(x) and velocities(v) for the next step."""

	dv = dt * ComputeAccel(x, m)
	v += dv
	dx = dt * v
	x += dx

	return (x,v)