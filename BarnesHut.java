import java.util.*;   
import java.lang.StringBuilder;

/* implement the Barnes-Hut algorithm to compute the gravitational interactions between an arbitrary number of particles */

public class BarnesHut extends GravitySolver
{
   Node root;               // root node of the octree
   double openAngle;        // opening angle
   Particle[] particles;    // array of particles with which to construct octree
   
   
   /* given the size of the simulation box, the opening angle, and an array of particles, compute the force on each of the
      particles via the Barnes-Hut algorithm */
   public BarnesHut(double boxSize, double openAngle, Particle[] particles)
   {
      this.root = new Node(null, new Node[8], particles[0], boxSize, new double[]{0, 0, 0});
      this.openAngle = openAngle;
      this.particles = particles;
      super.particles = particles;
       
      buildTree();           // assemble the octree
      root.sumMultipole();   // update the multipoles in each Node (see Node.java)
   }
   
   
   /* given the size of the simulation box, the opening angle, the number of particles in the simulation, and a seed for a random
      number generator, generate a random array of particles of length numParticles and compute the force on each of these particles
      via the Barnes-Hut algorithm */
   public BarnesHut(double boxSize, double openAngle, int numParticles, long seed)
   {
      this.particles = makeParticleArray(numParticles, boxSize, seed);
      super.particles = this.particles;
       
      this.root = new Node(null, new Node[8], particles[0], boxSize, new double[]{0, 0, 0});
      this.openAngle = openAngle;
       
      buildTree();
      root.sumMultipole();
   }
   
   
   /* assemble the octree by progressively adding particles to the simulation box and partitioning space accordingly */
   void buildTree()
   {
      for (int i = 1; i < particles.length; i++)
      {
         Node n = new Node(null, new Node[8], particles[i], 0, new double[]{0, 0, 0});
         root.addChild(n);
      }
   }
   
   
   /* recursive helper method for computeForce(). Computes the force on Particle p due to Node n */
   double[] computeForceHelper(Particle p, Node n)
   {
      double dist = p.distTo(n.multipole);
      
      // ignore interactions between overlapping particles
      if (dist == 0)
         return new double[]{0,0,0};
            
      double[] totForce = new double[]{0, 0, 0};
      double[] force;
      
      // if the current Node is a leaf or satisfies the opening angle criterion, compute the Newtonian (1/r^2) force 
      // on Particle p due to the particles in Node n
      if ((n.isLeaf()) || (n.sideLength < openAngle * dist))
      {
         force = newtonForce(p, n.multipole, dist);
         totForce = Tensor.add(totForce, force);
         
         return force;
      }
      
      // if the current Node does not satisfy the opening angle criterion, split the Node and recurse
      else 
      {
         for (Node c : n.children)
         {
            if (c != null)
            {
               force = computeForceHelper(p, c);
               totForce = Tensor.add(totForce, force);
            }
         }
      }
      
      return totForce;
   }
   
   /* compute the total force on Particle p due to all the other particles in the octree */
   double[] computeForce(Particle p)
   {
      double[] totForce = computeForceHelper(p, root);
      return totForce;
   }


   /* display the octree in String format */
   public String toString()
   {
      Queue<Node> q = new LinkedList<>();
      q.add(root);
      
      double levelTracker = root.sideLength;
      StringBuilder s = new StringBuilder();
      
      while (!q.isEmpty())
      {
         Node n = q.remove();
         
         if (n.sideLength < levelTracker)
         {
            s.append("\n");
            levelTracker = n.sideLength;
         }
            
         s.append(n + "   ");
                  
         for (Node child : n.children)
         {
            if (child != null)
               q.add(child);   
         }
         
      }
      
      return s.toString();
   }
   
   public static void main(String[] args)
   {
            
      //BarnesHut tree = new BarnesHut(100, 0.5, 5, 123459);
      
      //Particle A = new Particle(10, new double[]{5, 5, 0});
      //Particle B = new Particle(10, new double[]{15, 15, 0});
      //BarnesHut tree = new BarnesHut(40, 0.5, new Particle[]{A, B}); 
      
      Particle A = new Particle(10, new double[]{5, 5, 0});
      Particle B = new Particle(10, new double[]{-5, -5, 0});
      Particle C = new Particle(10, new double[]{0, 0, 0});
      BarnesHut tree = new BarnesHut(40, 0.5, new Particle[]{A, B, C});
      
      System.out.print(tree);
      System.out.println("\n");
      
      /* Particle test = new Particle(10, new double[]{0,0,0});
      double[] testForce = tree.computeForce(test);
      for (double f : testForce)
         System.out.print(f + " "); */
      
     
      double[] forceMags = tree.computeAllForces();
      
      System.out.println(forceMags[0]);
      for (double f : forceMags)
         System.out.print(f + " ");      
      
   }
}