import numpy as np

# The Particle class keeps track of individual particles as well as the "superparticles" associated with non-leaf Nodes in Barnes-Hut 
class Particle(object):
    
    # Given a mass and a center of mass (or a position, for individual particles), instantiate a Particle object with no acceleration
    def __init__(self, mass, com):
        self.mass = mass
        self.com = com
        self.accel = np.zeros(3) 
        self.vel = np.zeros(3) #: array representing Particle velocity
    
    # Return a string representation of a Particle displaying the Particle's mass, COM, and acceleration
    def __str__(self):
         return "mass: {}, COM: {}, Accel: {}".format(self.mass, self.com, self.accel)
    
    # Set this Particle's acceleration to accel
    def setAccel(self, accel):
        self.accel = accel
    
    # Set this Particle's acceleration to 0
    def resetAccel(self):
        self.accel = np.zeros(3)
        
    # Set this Particle's velocity to to vel
    def setVel(self, vel):
        self.vel = vel
    
    # Return the distance between this Particle and another Particle p
    def distTo(self, p):
        disp = self.com - p.com
        return np.linalg.norm(disp)
    
    # Combine the mass and COM of this Particle with another Particle p 
    def combine(self, p):
        self.com = (self.mass * self.com + p.mass * p.com) / (self.mass + p.mass)
        self.mass += p.mass 
    
    # Compute the 1/r^2 acceleration induced on this Particle due to another Particle p
    def newtonAccel(self, p):
        r = self.distTo(p)
        displacement = p.com - self.com
        
        accelMag = p.mass / r**2   # G = 1
        accelVec = accelMag * displacement / r
        
        return accelVec
    
    # Compute the 1/r^2 acceleration induced on this Particle due to another Particle p, with gravitational softening length eps0 and cutoff distance r0
    def newtonAccelSmooth(self, p, eps0, r0):
        r = self.distTo(p)
        displacement = p.com - self.com
        
        eps = self.epsilon(r, eps0, r0)   # gravitational softening
        softDisp = r + eps                # softened displacement
        
        accelMag = p.mass / softDisp**2
        accelVec = accelMag * displacement / softDisp
        
        return accelVec
    
    # Gravitational softening law from Springel et al. 2013; r is the displacement and eps0 is the softening length. The softening has a finite range, going to 0 for distances greater than r0 (with r0 being smaller than half the smallest box dimension)
    def epsilon(self, r, eps0, r0):
        if (r >= r0):
            return 0
        
        else:
            return -2.8 * eps0 / self.W2(r / (2.8 * eps0)) - r
     
    # Kernel for gravitational softening (from Springel, Yoshida, White 2001)    
    def W2(self, u):
        if ((u >= 0) and (u < 0.5)):
            return 16./3 * u**2 - 48./5 * u**4 + 32./5 * u**5 - 14./5
      
        elif ((u >= 0.5) and (u < 1)):
            return 1./15 * u**-1 + 32./3 * u**2 - 16 * u**3 + 48./5 * u**4 - 32./15 * u**5 - 16./5
      
        else: 
            return -1./u
        
        
def main():
    print("Hello World!")
        
    p1 = Particle(2, np.array([1,2,3]))
    p2 = Particle(3, np.array([1,1,1]))
    p3 = Particle(2, np.array([1,2,3.001]))
    print(p1)
        
    print(p1.distTo(p2) - np.sqrt(5))
    
    p1.combine(p2)
    print(p1)
    
    l = [1, np.NaN]*8
    print(l)
    print(np.all(np.isnan(l)))
    
    print("\n\n")
    
    print(p1.newtonAccel(p3))
    print(p1.newtonAccelSmooth(p3, 0.1, 5))

if __name__ == "__main__":
    main()

