import numpy as np

class Hernquist():
    """
    Randomly draw intial conditions of particles from Hernquist distribution.
    """

    def __init__(self, a, M):
        self.a = a
        self.M = M
    
    # CDF for the Hernquist distribution, where y = 4pi/3 * r^3 = volume
    def cumHern(self, y):
        return  self.M * np.power(3*y/(4*np.pi), 2./3) * np.power(self.a + np.power(3*y/(4*np.pi), 1./3), -2)
    
    # Inverse of the CDF for the Hernquist distribution
    def invHern(self, x):
        return 4*np.pi/3. * np.power(self.a,3) *np.power(x,1.5) * np.power(np.power(self.M,1./3) - np.power(x,0.5), -3)
    
    # Draw a random radius from the Hernquist distribution
    def sampleRadius(self):
        randX = np.random()
        y = self.invHern(randX, self.a, self.M)
        return np.power(3*y/(4*np.pi), 1./3)
    
    # Draw a random point (in spherical coordinates) from the Hernquist distribution
    def samplePointSphere(self):
        randR = self.sampleRadius(self.a, self.M)
        randPhi = 2*np.pi * np.random() 
        randTheta = np.pi * np.random()
        return randR, randPhi, randTheta

    # Draw a random point (in Cartesian coordinates) from the Hernquist distribution
    def samplePointCart(self):
        randPointSphere = self.samplePointSphere(self.a, self.M)
        r = randPointSphere[0]
        phi = randPointSphere[1]
        theta = randPointSphere[2]
        
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return x, y, z

    # Sample numParticles Particles from a Hernquist distribution
    def generateHernquist(self, numParticles):
        particles = np.arange(0, numParticles, 1)
        for i in range(len(particles)):
            particles[i] = Particle(1, self.samplePointCart(self.a, self.M))
        return particles
