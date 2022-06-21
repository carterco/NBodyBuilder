/* the Particle Class keeps track of individual particles as well as the multipole moments of Nodes in Barnes-Hut and FMM */

public class Particle
{
   double mass;             // total mass of the Particle or Node
   double[] com;            // coordinates of the Particle, or center of mass of the Node
   double[][] quadrupole;   // quadrupole tensor of the Node
   double[] force;          // force on this particle
   
   
   /* given a mass, a center of mass, and a quadrupole tensor, instantiate a Particle object */
   public Particle(double mass, double[] com, double[][] quadrupole)
   {
      this.mass = mass;
      this.com = com;
      this.quadrupole = quadrupole;
      this.force = new double[3];
   }

   
   /* given a mass and a center of mass, instantiate a Particle object (with no quadrupole moment) */
   public Particle(double mass, double[] com)
   {
      this.mass = mass;
      this.com = com;
      this.quadrupole = new double[3][3];
      this.force = new double[3];
   } 
   
      
   /* instantiate a Particle object with no mass and no quadrupole moment, centered at the origin */
   public Particle()
   {
      this.mass = 0;
      this.com = new double[3];
      this.quadrupole = new double[3][3];
      this.force = new double[3];
   }
   
   void resetForce()
   {
      this.force = new double[3];
   }
   
   static void resetAll(Particle[] particles)
   {
      for (Particle p : particles)
         p.resetForce();
   }
   
   
   /* compute the distance from this Particle to an arbitrary Particle p */
   double distTo(Particle p)
   {
      double[] disp = Tensor.subtract(this.com, p.com);
      
      return Math.sqrt(Tensor.dot(disp, disp));
   }
   
   
   /* shift a quadrupole tensor to a new center */
   double[][] shiftQuadrupole(double[][] oldQuadrupole, double totMass, double[] oldCOM, double[] newCOM)
   {
      double[] disp = Tensor.subtract(newCOM, oldCOM);
   
      double[][] newQuadrupole = new double[3][3];
      for (int j = 0; j < newQuadrupole[0].length; j++)
         for (int i = 0; i < newQuadrupole.length; i++)
            newQuadrupole[i][j] = oldQuadrupole[i][j] + totMass * disp[i] * disp[j];
   
      return newQuadrupole;
   }
   
   
   /* sum the multipoles of this Particle with those of Particle p */
   void combine(Particle p)
   {
      double[] newCOM = new double[3];
      for (int i = 0; i < this.com.length; i++)
         newCOM[i] = (this.mass * this.com[i] + p.mass * p.com[i]) / (this.mass + p.mass);
   
      double[][] shiftedQThis = shiftQuadrupole(this.quadrupole, this.mass, this.com, newCOM);
      double[][] shiftedQThat = shiftQuadrupole(p.quadrupole, p.mass, p.com, newCOM);
      this.quadrupole = Tensor.add(shiftedQThis, shiftedQThat);
      
      this.com = newCOM;
      
      this.mass += p.mass; 
   }
   
   /* Kernel for gravitational softening (from Springel, Yoshida, White 2001) */
   double W2(double u)
   {
      if ((u >= 0) && (u < 0.5))
         return 16./3 * Math.pow(u,2) - 48./5 * Math.pow(u,4) + 32./5 * Math.pow(u,5) - 14./5;
      
      else if ((u >= 0.5) && (u < 1))
         return 1./15 * Math.pow(u,-1) + 32./3 * Math.pow(u,2) - 16 * Math.pow(u,3) + 48./5 * Math.pow(u,4) - 32./15 * Math.pow(u,5) - 16./5;
      
      else 
         return -1./u;
   }
   
   /* Gravitational softening law from Springel et al. 2013; r is the displacement and eps0 is the softening length. 
      The softening has a finite range, going to 0 for distances greater than r0 (with r0 being smaller than half the smallest
      box dimension)  */
   double epsilon(double r, double eps0, double r0)
   {
      if (r >= r0) 
         return 0;
      
      else 
         return -2.8 * eps0 / W2(r / (2.8 * eps0)) - r;
   }
   
   
   /* Compute the softened Newtonian (1/r^2) force on this Particle due to Particle p2, with softening length eps0 
      and cutoff distance r0  */
   double[] newtonForce(Particle p2, double eps0, double r0)
   {  
      double[] displacement = Tensor.subtract(this.com, p2.com);
      
      double dispNorm = Math.sqrt(Tensor.dot(displacement, displacement));  // norm of displacement vector
      double eps = epsilon(dispNorm, eps0, r0);                             // softening
      double softDisp = dispNorm + eps;                                     // softened displacement
      
      double forceMag = p2.mass / (softDisp*softDisp); // actually computing acceleration
      
      double[] forceVec = Tensor.dot(forceMag/softDisp, displacement);
        
      return forceVec;
   }
   
   /* Compute the (unsoftened) Newtonian (1/r^2) force on this Particle due to Particle p2 */
   double[] newtonForce(Particle p2)
   {  
      double[] displacement = Tensor.subtract(this.com, p2.com);
      double dispNorm = Math.sqrt(Tensor.dot(displacement, displacement));
      
      double forceMag = p2.mass / (dispNorm*dispNorm); // actually computing acceleration
      
      double[] forceVec = Tensor.dot(forceMag/dispNorm, displacement);
        
      return forceVec;
   }

   
   
   /* display the Particle in String format */
   public String toString()
   {
      String s = String.format("mass: %.2f; COM: {%.2f, %.2f, %.2f}", mass, com[0], com[1], com[2]);
      return s;
   }
   
   
   
   public static void main(String[] args)
   {
      Particle p1 = new Particle(2, new double[]{12,0,0});
      Particle p2 = new Particle(2, new double[]{0,1,0});
      
      System.out.println(p1);
      System.out.println(p1.distTo(p2));
      
      Tensor.display(p1.newtonForce(p2));
      System.out.println();
      
      
      double[] test = new double[5];
      test[0] = 2;
      test[2] = 5;
      System.out.println(test.length);
   }
}
