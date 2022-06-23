import numpy as np

# The Particle class keeps track of individual particles as well as the "superparticles" associated with non-leaf Nodes in Barnes-Hut 
class Particle(object):
    
    # Given a mass and a center of mass (or a position, for individual particles), instantiate a Particle object with no acceleration
    def __init__(self, mass, com):
        self.mass = mass
        self.com = com
        self.accel = np.zeros(3)
        self.vel = np.zeros(3)
    
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
        
    
def main():
    print("Hello World!")
        
    p1 = Particle(2, np.array([1,2,3]))
    p2 = Particle(3, np.array([1,1,1]))
    print(p1)
        
    print(p1.distTo(p2) - np.sqrt(5))
    
    p1.combine(p2)
    print(p1)
    
    l = [1, np.NaN]*8
    print(l)
    print(np.all(np.isnan(l)))

if __name__ == "__main__":
    main()

