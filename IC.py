import numpy as np
import numpy.random as rand
import Particle as part
import Hernquist_IC as hern

class IC(object):
    
    def __init__(self, numParticles, ic, seed=12345, boxSize = 50, hern_a = 10, hern_m = 10):
        
        if (ic == "random"):
            self.particles = self.randParticles(numParticles, boxSize, seed)
        
        elif (ic == "hernquist"):
            self.particles = hern.Hernquist(numParticles, hern_a, hern_m)
            
        else:
            self.particles = self.randParticles(numParticles, boxSize, seed)
            
            
    def __repr__(self):
        
        s = ""
        for p in self.particles:
            s += "{} \n\n".format(p)
            
        return s
    
    def randParticles(self, numParticles, boxSize, seed):
        
        particles = []
        generator = rand.default_rng(seed)
        randMasses = generator.random(numParticles)
        randCOMS = generator.random((numParticles, 3))
        
        for i in range(numParticles):
            mass = 10 * randMasses[i]
            com = boxSize * randCOMS[i] - boxSize/2.
            
            p = part.Particle(mass, com)
            particles.append(p)
            
        return particles
    
def main():
    ic = IC(10, "random")
    print(ic)
    
    
    
if __name__ == "__main__":
    main()