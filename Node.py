import numpy as np
import Particle as part

# The Node class defines the elements that comprise the octree required for the Barnes-Hut algorithm
class Node(object):
    
    # Given an array of children Nodes, a Particle object storing a set of multipole moments, the side length of a grid cell, and the center of the grid cell, instantiate the corresponding Node object
    def __init__(self, children, multipole, sideLength, cellCenter):
        self.children = children
        self.multipole = multipole
        self.sideLength = sideLength
        self.cellCenter = cellCenter
        
    # Return a string representation of a Node displaying the Node's enclosed mass, COM, and cell center
    def __repr__(self):
        return "(mass: {}, COM: {}, center: {})".format(self.multipole.mass, self.multipole.com, self.cellCenter)
    
    # Set the multipole moments associated with this Node
    def setMultipole(self, multipole):
        self.multipole = multipole
    
    # Set the side length of the grid cell associated with this Node
    def setSideLength(self, sideLength):
        self.sideLength = sideLength
    
    # Set the center of the grid cell associated with this Node
    def setCellCenter(self, cellCenter):
        self.cellCenter = cellCenter
    
    # Check if this Node is a leaf Node
    def isLeaf(self):
        return all(c == 0 for c in self.children)
    
    # Get the position of Node n's center of mass relative to the current Node's cell center; when adding Particles/Nodes to our octree, this relative position tells us which grid cell needs to be subdivided. This method returns both an integer corresponding to the octant in which Node n's center of mass lies with respect to the current Node's cell center (e.g., 0 if the coordinates of Node n's center of mass are all less than or equal to the coordinates of the current Node's cell center), as well as the coordinates of this octant's center
    def relPosition(self, n):
        x, y, z = n.multipole.com
        x0, y0, z0  = self.cellCenter
        
        if ((x <= x0) and (y <= y0) and (z <= z0)):
            return 0, np.array([x0 - self.sideLength/4., y0 - self.sideLength/4., z0 - self.sideLength/4.])
        elif ((x <= x0) and (y <= y0) and (z > z0)): 
            return 1, np.array([x0 - self.sideLength/4., y0 - self.sideLength/4., z0 + self.sideLength/4.])
        elif ((x <= x0) and (y > y0) and (z <= z0)): 
            return 2, np.array([x0 - self.sideLength/4., y0 + self.sideLength/4., z0 - self.cellCentersideLength/4.])
        elif ((x > x0) and (y <= y0) and (z <= z0)): 
            return 3, np.array([x0 + self.sideLength/4., y0 - self.sideLength/4., z0 - self.sideLength/4.])
        elif ((x <= x0) and (y > y0) and (z > z0)): 
            return 4, np.array([x0 - self.sideLength/4., y0 + self.sideLength/4., z0 + self.sideLength/4.])
        elif ((x > x0) and (y <= y0) and (z > z0)): 
            return 5, np.array([x0 + self.sideLength/4., y0 - self.sideLength/4., z0 + self.sideLength/4.])
        elif ((x > x0) and (y > y0) and (z <= z0)):
            return 6, np.array([x0 + self.sideLength/4., y0 + self.sideLength/4., z0 - self.sideLength/4.])
        else: 
            return 7, np.array([x0 + self.sideLength/4., y0 + self.sideLength/4., z0 + self.sideLength/4.])
        
    
    # Add a child Node to the current Node and partition the simulation box accordingly
    def addChild(self, child):
        newOct, newCenter = self.relPosition(child)  # find the position of the child Node relative to the current Node
        
        # if there are no Nodes/particles currently in the octant where the child should be placed, add the child to this octant and subdivide the grid cell if appropriate
        if (self.children[newOct] == 0):
            child.setSideLength(self.sideLength / 2.)
            child.setCellCenter(newCenter)
            
            # if the current Node is a leaf node, add the child node and partition its associated cell into a new set of octants
            if (self.isLeaf()):
                parentCopy = Node([0]*8, self.multipole, self.sideLength / 2., np.zeros(3))
                copyOct, copyCenter = self.relPosition(parentCopy)
                self.children[copyOct] = parentCopy
                parentCopy.setCellCenter(copyCenter)
         
                if (copyOct != newOct):
                    self.children[newOct] = child
                else:
                    parentCopy.addChild(child)

            # if the current Node is not a leaf node, then it is not necessary to partition the child Node's associated cell
            else: 
                self.children[newOct] = child
        
        # if there is already a Node in the octant where the child should be placed, add the new child to the children of this pre-existing Node
        else: 
            (self.children[newOct]).addChild(child)
    
    
    # Recursively traverse the tree from the leaves up to the root, appropriately updating the multipoles in each of the Nodes    
    def sumMultipole(self):
        if (self.isLeaf()):
            return self.multipole
         
        newMultipole = part.Particle(0, np.zeros(3))
   
        for c in self.children:
            if (c != 0): 
                newMultipole.combine(c.sumMultipole())
      
        self.multipole = newMultipole
        return self.multipole
            
        
def main():
    p1 = part.Particle(1, np.array([-1,1,1]))
    p2 = part.Particle(2, np.array([1,1,1]))
    p3 = part.Particle(3, np.array([49,49,49]))
    
    n1 = Node([0]*8, p1, 100, np.zeros(3))
    n2 = Node([0]*8, p2, 0, np.zeros(3))
    n3 = Node([0]*8, p3, 0, np.zeros(3))
    
    print(n1)
    print(n2)
    
    n1.addChild(n2)
    print(n2)
    print(n2.sideLength)
    print(n2.children)
    print(n1.children)
    
    n1.sumMultipole()
    print(n1.multipole)
    print(n2.multipole)
    
    n1.addChild(n3)
    print(n3)
    print(n2.children)
    
    n1.sumMultipole()
    print(n1.multipole)
    print(n2.multipole)
    print(n3.multipole)
    
    
if __name__ == "__main__":
    main()
        