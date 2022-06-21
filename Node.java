/* Node objects make up the octrees used in Barnes-Hut and FMM, and thus much of the heavy lifting in these algorithms is implemented in Node.java */

public class Node
{
   Node parent;          // parent Node of the current Node
   Node[] children;      // array of children of the current Node
   Particle multipole;   // Particle object storing the multipole moments of the current Node
   double sideLength;    // side length of the grid cell associated with this Node
   double[] cellCenter;  // center of the grid cell associated with this Node
   
   double[] C1;          // C^{1,3} coefficient of Taylor series associated with this Node
   double[][] C2;        // C^{2,3} coefficient of Taylor series associated with this Node
   double[][][] C3;      // C^{3,3} coefficient of Taylor series associated with this Node
   double[] force;       // force (actually acceleration) exerted on this Node (only non-zero for leaf nodes)
   
   
   /* given a parent Node, an array of children Nodes, a Particle object storing a set of multipole moments, the side length 
      of a grid cell, and the center of the grid cell, instantiate the corresponding Node object */
   public Node(Node parent, Node[] children, Particle multipole, double sideLength, double[] cellCenter)
   {
      this.parent = parent;
      this.children = children;
      this.multipole = multipole;
      this.sideLength = sideLength;
      this.cellCenter = cellCenter;
      
      this.C1 = new double[3];
      this.C2 = new double[3][3];
      this.C3 = new double[3][3][3];
      this.force = new double[3];
   }
   
   
   /* set the multipole moments associated with this Node */
   void setMultipole(Particle multipole)
   {
      this.multipole = multipole;
   }
   
   /* set the parent Node of the current Node */
   void setParent(Node parent)
   {
      this.parent = parent;
   }
   
   /* set the side length of the grid cell associated with this Node */
   void setSideLength(double sideLength)
   {
      this.sideLength = sideLength;
   }
   
   /* set the center of the grid cell associated with this Node */
   void setCellCenter(double[] cellCenter)
   {
      this.cellCenter = cellCenter;
   }
   
   /* check if this Node is a leaf node */
   boolean isLeaf()
   {
      for (Node c : children)
      {
         if (c != null) 
            return false; 
      }
   
      return true;
   }
   
   
   /* get the position of Node n's center of mass relative to the current Node's cell center; when adding Particles/Nodes to our octree,
      this relative position tells us which grid cell needs to be subdivided. This method returns both an integer corresponding to the  
      octant in which Node n's center of mass lies with respect to the current Node's cell center (e.g., 0 if the coordinates of Node n's center 
      of mass are all less than or equal to the coordinates of the current Node's cell center), as well as the coordinates of this octant's center. */ 
   double[] relPosition(Node n)
   {
      double x = n.multipole.com[0];
      double y = n.multipole.com[1];
      double z = n.multipole.com[2];
      
      double x0 = this.cellCenter[0];
      double y0 = this.cellCenter[1];
      double z0 = this.cellCenter[2];
      
      if ((x <= x0) && (y <= y0) && (z <= z0)) 
         return new double[]{0, x0 - sideLength/4., y0 - sideLength/4., z0 - sideLength/4.};
      if ((x <= x0) && (y <= y0) && (z > z0)) 
         return new double[]{1, x0 - sideLength/4., y0 - sideLength/4., z0 + sideLength/4.};
      if ((x <= x0) && (y > y0) && (z <= z0)) 
         return new double[]{2, x0 - sideLength/4., y0 + sideLength/4., z0 - sideLength/4.};
      if ((x > x0) && (y <= y0) && (z <= z0)) 
         return new double[]{3, x0 + sideLength/4., y0 - sideLength/4., z0 - sideLength/4.};
      if ((x <= x0) && (y > y0) && (z > z0)) 
         return new double[]{4, x0 - sideLength/4., y0 + sideLength/4., z0 + sideLength/4.};
      if ((x > x0) && (y <= y0) && (z > z0)) 
         return new double[]{5, x0 + sideLength/4., y0 - sideLength/4., z0 + sideLength/4.};
      if ((x > x0) && (y > y0) && (z <= z0)) 
         return new double[]{6, x0 + sideLength/4., y0 + sideLength/4., z0 - sideLength/4.};
      else 
         return new double[]{7, x0 + sideLength/4., y0 + sideLength/4., z0 + sideLength/4.};
   }
   
   
   /* add a child Node to the current Node and partition the simulation box accordingly */
   void addChild(Node child)
   {
      // to avoid overlapping particles, add a small shift to the child Node's center of mass if it coincides with the current Node's center of mass 
      // (this should be replaced with a more sophisticated gravitational softening procedure)
      if ((this.multipole.com[0] == child.multipole.com[0]) 
           && (this.multipole.com[1] == child.multipole.com[1]) 
           && (this.multipole.com[2] == child.multipole.com[2]))
      {
         child.multipole.com[0] += 1E-6;
      } 
      
      double[] relPosition = relPosition(child);  // find the position of the child Node relative to the current Node
      
      // if there are no Nodes/particles currently in the octant where the child should be placed, add the child to this octant
      // and subdivide the grid cell if appropriate
      if (children[(int)relPosition[0]] == null) 
      {
         child.setSideLength(this.sideLength / 2.);
         child.setCellCenter(new double[]{relPosition[1], relPosition[2], relPosition[3]});
         
         // if the current Node is a leaf node, add the child node and partition its associated cell into a new set of octants
         if (this.isLeaf())
         {
            Node parentCopy = new Node(this, new Node[8], this.multipole, this.sideLength / 2., new double[]{0,0,0});
            double[] copyPosition = relPosition(parentCopy);
            children[(int)copyPosition[0]] = parentCopy;
            parentCopy.setCellCenter(new double[]{copyPosition[1], copyPosition[2], copyPosition[3]});
         
            if (copyPosition[0] != relPosition[0])
            {
               children[(int)relPosition[0]] = child;
               child.setParent(this);
            }
            
            else 
               parentCopy.addChild(child);
         }
         
         // if the current Node is not a leaf node, then it is not necessary to partition the child Node's associated cell
         else 
         {
            children[(int)relPosition[0]] = child;
            child.setParent(this);
         }
      }
      
      // if there is already a Node in the octant where the child should be placed, add the new child to the children of this pre-existing Node
      else
         (children[(int)relPosition[0]]).addChild(child);
   }
   
   
   /* recursively traverse the tree from the leaves up to the root, appropriately updating the multipoles in each of the Nodes */
   Particle sumMultipole()
   {      
      if (this.isLeaf())
         return this.multipole;
         
      Particle newMultipole = new Particle();
   
      for (Node c : children)
      {
         if (c != null) 
            newMultipole.combine(c.sumMultipole());
      }
      
      this.multipole = newMultipole;
      return this.multipole;
   }
   
   
   /* compute the Taylor coefficients for the force (acceleration) exerted on the current Node by all the particles in Node b */  
   void interact(Node b)
   {
      double mtot_b = b.multipole.mass;
      double[] com_a = this.multipole.com;
      double[] com_b = b.multipole.com;
      double[][] quad_b = b.multipole.quadrupole;
    
      double rvec[] = Tensor.subtract(com_b, com_a);    // displacement vector between com_b and com_a
      double r = Math.sqrt(Tensor.dot(rvec, rvec));     // magnitude of displacement vector 
   
      double[] D1 = Tensor.dot(-1.0/Math.pow(r,3), rvec);  // derivative tensor D1
      double[][] D2 = new double[3][3];                    // derivative tensor D2
      double[][][] D3 = new double[3][3][3];               // derivative tensor D3
     
     
      /*if (this.isLeaf() && b.isLeaf())
      {
         double forceMag = mtot_b / (r*r); 
         
         double[] forceVec = Tensor.dot(forceMag, Tensor.dot(1./r, rvec));
         this.C1 = Tensor.add(this.C1, forceVec);
               
         return;
      }*/
     
      // compute the components of D2
      for (int j = 0; j < D2[0].length; j++)
         for (int i = 0; i < D2.length; i++)
         {
            D2[i][j] = 3.0/Math.pow(r,5) * rvec[i] * rvec[j];
            
            if (i == j) D2[i][j] -= 1.0/Math.pow(r,3);
         }
      
      // compute the components of D3
      for (int k = 0; k < D3[0][0].length; k++)
         for (int j = 0; j < D3[0].length; j++)
            for (int i = 0; i < D3.length; i++)
            {
               D3[i][j][k] = -15.0/Math.pow(r,7) * rvec[i] * rvec[j] * rvec[k];
            
               if (i == j) D3[i][j][k] += 3.0/Math.pow(r,5) * rvec[k];
               if (j == k) D3[i][j][k] += 3.0/Math.pow(r,5) * rvec[i];
               if (i == k) D3[i][j][k] += 3.0/Math.pow(r,5) * rvec[j];
            }
     
     
      // compute the coefficients of the Taylor expansion of acceleration due to the particles in Node b
      double[] deltaC1 = Tensor.add(Tensor.dot(mtot_b, D1), Tensor.dot(quad_b, Tensor.dot(0.5, D3)));
      double[][] deltaC2 = Tensor.dot(mtot_b, D2);
      double[][][] deltaC3 = Tensor.dot(mtot_b, D3);
   
      // add the coefficients for the new interaction to the coefficients already associated with this Node
      this.C1 = Tensor.add(this.C1, deltaC1);
      this.C2 = Tensor.add(this.C2, deltaC2);
      this.C3 = Tensor.add(this.C3, deltaC3);
   }
   
   
   /* take the Taylor coefficients of the parent Node, shift them to the current Node's center of mass, and add them to the 
      coefficients already associated with the current Node */
   void addTaylor()
   {
      Node parent = this.parent;
      double[] comShift = Tensor.subtract(parent.multipole.com, this.multipole.com);  // displacement of center of mass
      
      double[] shiftedParentC1_secondTerm = Tensor.dot(comShift, parent.C2);
      double[] shiftedParentC1_thirdTerm = Tensor.dot(Tensor.outer(comShift, comShift), Tensor.dot(0.5, parent.C3));
      double[] shiftedParentC1 = Tensor.add(Tensor.add(parent.C1, shiftedParentC1_secondTerm), shiftedParentC1_thirdTerm);
      
      double[][] shiftedParentC2 = Tensor.add(parent.C2, Tensor.dot(comShift, parent.C3));
      
      this.C1 = Tensor.add(this.C1, shiftedParentC1);
      this.C2 = Tensor.add(this.C2, shiftedParentC2);
      this.C3 = Tensor.add(this.C3, parent.C3);
   } 
   
   
   /* use the Taylor coefficients in the current Node to compute the acceleration of this Node's associated particle, saving 
      the result in this Node's "force" attribute. This method should only be called on leaf nodes */
   void evaluateForce()
   {
      double[] a = Tensor.subtract(this.multipole.com, this.multipole.com);
      
      double[] secondTerm = Tensor.dot(a, this.C2);
      double[] thirdTerm = Tensor.dot(Tensor.outer(a,a), Tensor.dot(0.5, this.C3));
      
      this.force = Tensor.add(Tensor.subtract(C1, secondTerm), thirdTerm);
   } 
   
   
   /* display the Node in a String format */
   public String toString()
   {
      String s = String.format("(mass: %.2f; COM: {%.2f, %.2f, %.2f}; center: {%.2f, %.2f, %.2f}; force: %.4f)", 
         multipole.mass, multipole.com[0], multipole.com[1], multipole.com[2], cellCenter[0], cellCenter[1], cellCenter[2],
         /* multipole.quadrupole[0][0], multipole.quadrupole[0][1], multipole.quadrupole[0][2], */ Math.sqrt(Tensor.dot(force, force)));
      return s;
   }
   
   
   
   public static void main(String[] args)
   {
      Particle p1 = new Particle(1, new double[]{-1, 1, 1});
      Particle p2 = new Particle(2, new double[]{1, 1, 1});
      // Particle p3 = new Particle(3, new double[]{2, 2, 2});
      Particle p3 = new Particle(3, new double[]{49, 49, 49});
   
      Node n1 = new Node(null, new Node[8], p1, 100, new double[]{0, 0, 0});
      Node n2 = new Node(null, new Node[8], p2, 0, new double[]{0, 0, 0});
      Node n3 = new Node(null, new Node[8], p3, 0, new double[]{0, 0, 0});
      
      System.out.println(n1);
      System.out.println(n2 + "\n");
      
      n1.addChild(n2);
      System.out.println(n2);
      System.out.println(n2.sideLength);
      System.out.println(n2.parent);
      for (Node n : n1.children) System.out.print(n + "  ");
      System.out.println("\n");
      
      n1.sumMultipole();
      System.out.println(n1.multipole);
      System.out.println(n2.multipole + "\n");
      
      n1.addChild(n3);
      System.out.println(n3);
      System.out.println(n3.sideLength + " " + n2.sideLength);
      System.out.println(n3.parent);
      for (Node n : n2.children) System.out.print(n + "  ");
      System.out.println("\n");
      
      n1.sumMultipole();
      System.out.println(n1.multipole);
      System.out.println(n2.multipole);
      System.out.println(n3.multipole + "\n");
     
   }
}
