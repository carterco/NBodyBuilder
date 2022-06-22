import numpy as np

class Particle(object):
    
    def __init__(self, mass, com):
        self.mass = mass
        self.com = com
        
    def __str__(self):
         return "{}, {}".format(self.mass, self.com)
        
        
    def distTo(self, p):
        disp = self.com - p.com
        return np.linalg.norm(disp)
    
    def combine(self, p):
        self.com = (self.mass * self.com + p.mass * p.com) / (self.mass + p.mass)
        self.mass += p.mass 
    
def main():
    print("Hello World!")
        
    p1 = Particle(2, np.array([1,2,3]))
    p2 = Particle(3, np.array([1,1,1]))
    print(p1)
        
    print(p1.distTo(p2) - np.sqrt(5))
    
    p1.combine(p2)
    print(p1)
        

if __name__ == "__main__":
    main()

