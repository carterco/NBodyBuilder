import numpy as np
import Particle as part
import Node as node

# The BH class implements the Barnes-Hut algorithm to compute the gravitational interactions between an arbitrary number of particles
class BH(object):
    
    # Given the size of the simulation box, the opening angle, and an array of particles, compute the force on each of the particles via the Barnes-Hut algorithm
    def __init__(self, boxSize, openAngle, particles):
        self.root = node.Node([0]*8, particles[0], boxSize, np.zeros(3))  # create the root of the octree
        self.openAngle = openAngle
        self.particles = particles
        
        self.buildTree()
        self.root.sumMultipole()
    
    # Return a string representation of the Barnes-Hut octree
    def __repr__(self):
        q = []
        q.append(self.root)
        
        levelTracker = self.root.sideLength
        s = ""
        
        while (len(q) > 0):
            n = q.pop()
            
            if (n.sideLength < levelTracker):
                s += "\n"
                levelTracker = n.sideLength
            
            s += "{}  ".format(n)
            
            for c in n.children:
                if (c != 0):
                    q.append(c)
        return s
        
    # Assemble the octree by progressively adding particles to the simulation box and partitioning space accordingly
    def buildTree(self):
        for i in range(1, self.particles.size):
            n = node.Node([0]*8, self.particles[i], 0, np.zeros(3))
            self.root.addChild(n)
            
    # Compute the total acceleration on Particle p induced by the other particles/superparticles in the octree
    def computeAccel(self, p):
        totAccel = self.computeAccelHelper(p, self.root)
        return totAccel
    
    # Recursive helper method for computeAccel(). Computes the acceleration of Particle p due to Node n
    def computeAccelHelper(self, p, n):
        dist = p.distTo(n.multipole)
        
        # ignore interactions between overlapping particles
        if (dist == 0):
            return np.zeros(3)
        
        totAccel = np.zeros(3)
        
        # if the current Node is a leaf or satisfies the opening angle criterion, compute the Newtonian (1/r^2) force on Particle p due to the particles in Node n
        if ((n.isLeaf()) or (n.sideLength < self.openAngle * dist)):
            accel = p.newtonAccel(n.multipole)
            totAccel += accel
        
        # if the current Node does not satisfy the opening angle criterion, split the Node and recurse
        else:
            for c in n.children:
                if (c != 0):
                    accel = self.computeAccelHelper(p, c)
                    totAccel += accel
                    
        return totAccel
    
    # Compute the pairwise forces/accelerations for all Particles in the simulation
    def computeAllAccels(self):
        for p in self.particles:
            accel = self.computeAccel(p)
            p.setAccel(accel)
            
def main():
    p1 = part.Particle(2, np.array([0, 0, 0]))
    p2 = part.Particle(2, np.array([1, 1, 1]))
    p3 = part.Particle(2, np.array([0.5, 0.5, 0.5]))
    p4 = part.Particle(10, np.array([0.1, -10, -25]))
    
    tree = BH(40, 0.5, np.array([p1, p2, p3, p4]))
    # print(tree)
    # print("\n")
    
    tree.computeAllAccels()
    
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    
if __name__ == "__main__":
    main()
        