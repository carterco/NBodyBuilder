import numpy as np

class Hernquist():
    """Hernquist class

    Randomly draw intial conditions of particles from Hernquist distribution.

    Args:
        a (float): Scale raduis (See Binney and Tremaine Eqn. 2.66)
        M (float): Total mass
    """

    def __init__(self, a, M):
        self.a = a
        self.M = M
    
    def cumHern(self, y):
        """Cumulative distribution function for the Hernquist distribution, where y = 4pi/3 * r^3 = volume
        
        Agrs: 
            y ():
        
        Returns:
            array: Cumulative distribution function for the Hernquist distribution
        """
        return  self.M * np.power(3*y/(4*np.pi), 2./3) * np.power(self.a + np.power(3*y/(4*np.pi), 1./3), -2)
    
    def invHern(self, x):
        """Inverse of the cumulative distribution function for the Hernquist distribution.
        
        Agrs: 
            x ():
        
        Returns:
            array: Inverse of the cumulative distribution function
        """
        return 4*np.pi/3. * np.power(self.a,3) *np.power(x,1.5) * np.power(np.power(self.M,1./3) - np.power(x,0.5), -3)
    
    def sampleRadius(self):
        """Draw a random radius from the Hernquist distribution.
        
        Returns:
            array(?): 
        """
        randX = np.random()
        y = self.invHern(randX, self.a, self.M)
        return np.power(3*y/(4*np.pi), 1./3)
    
    def samplePointSphere(self):
        """Draw a random point (in spherical coordinates) from the Hernquist distribution.
        
        Returns:
            (3) arrays: randR (), randPhi (), randTheta ()
        """
        randR = self.sampleRadius(self.a, self.M)
        randPhi = 2*np.pi * np.random() 
        randTheta = np.pi * np.random()
        return randR, randPhi, randTheta

    def samplePointCart(self):
        """Draw a random point (in Cartesian coordinates) from the Hernquist distribution.
        
        Returns:
            (3) arrays: x (array of x-positions), y (array of y-positions), z (array of z-positions)
        """
        randPointSphere = self.samplePointSphere(self.a, self.M)
        r = randPointSphere[0]
        phi = randPointSphere[1]
        theta = randPointSphere[2]
        
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return x, y, z

    def generateHernquist(self, numParticles):
        """Sample numParticles Particles from a Hernquist distribution.

        Args:
            numParticles (integer): How many particles to draw from the distribution
            
        Returns:
            array: An array of particle positions of length numParticles
        """
        particles = np.arange(0, numParticles, 1)
        for i in range(len(particles)):
            particles[i] = Particle(1, self.samplePointCart(self.a, self.M))
        return particles

