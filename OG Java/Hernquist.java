import java.util.Random;
import java.util.Arrays;

public class Hernquist
{
   
   /* CDF for the Hernquist distribution, where y = 4pi/3 * r^3 = volume */
   static double cumHern(double y, double a, double M)
   {
      return M * Math.pow(3*y/(4*Math.PI), 2./3) * Math.pow(a + Math.pow(3*y/(4*Math.PI), 1./3), -2);
   }
   
   /* Inverse of the CDF for the Hernquist distribution */
   static double invHern(double x, double a, double M)
   {
      return 4*Math.PI/3. * Math.pow(a,3) * Math.pow(x,1.5) * Math.pow(Math.pow(M,1./3) - Math.pow(x,0.5), -3); 
   } 
   
   /* Draw a random radius from the Hernquist distribution */
   static double sampleRadius(double a, double M)
   {
      double randX = Math.random();            // generate a random number uniformaly in [0,1)
      double y = invHern(randX, a, M);         // plug the random number into the inverted CDF to generate y
       
      return Math.pow(3*y/(4*Math.PI), 1./3);  // convert y into a radius
   }
   
   /* Draw a random point (in spherical coordinates) from the Hernquist distribution */
   static double[] samplePointSphere(double a, double M)
   {
      double randR = sampleRadius(a, M);
      double randPhi = 2*Math.PI * Math.random();
      double randTheta = Math.PI * Math.random();
   
      return new double[]{randR, randPhi, randTheta};
   }
   
   /* Draw a random point (in Cartesian coordinates) from the Hernquist distribution */
   static double[] samplePointCart(double a, double M)
   {
      double[] randPointSphere = samplePointSphere(a, M);
      double r = randPointSphere[0];
      double phi = randPointSphere[1];
      double theta = randPointSphere[2];
   
      double x = r * Math.sin(theta) * Math.cos(phi);
      double y = r * Math.sin(theta) * Math.sin(phi);
      double z = r * Math.cos(theta);
   
      return new double[]{x, y, z};
   }
   
   /* Sample numParticles Particles from a Hernquist distribution */
   static Particle[] generateHernquist(int numParticles, double a, double M)
   {
      Particle[] particles = new Particle[numParticles];
      
      for (int i = 0; i < numParticles; i++)
         particles[i] = new Particle(1, samplePointCart(a, M));
         
      return particles;
   }
   
   static void HernquistTest(int numParticles, double a, double boxSize)
   {
      double M = numParticles;
      
      Particle[] particles = generateHernquist(numParticles, a, M);
      
      // compute forces directly
      directForce df = new directForce(particles);
      double[] forceMags_df = df.computeAllForces();
      
      // compute forces with FMM
      FMMplus fmm01 = new FMMplus(2, boxSize, 0.1, particles);
      double[] forceMags_fmm01 = fmm01.computeAllForces();
      Particle.resetAll(particles);
      
      FMMplus fmm05 = new FMMplus(6, boxSize, 0.5, particles);
      double[] forceMags_fmm05 = fmm05.computeAllForces();
      Particle.resetAll(particles);
      
      FMMplus fmm1 = new FMMplus(2, boxSize, 1.0, particles);
      double[] forceMags_fmm1 = fmm1.computeAllForces();
      
      // compute forces with Barnes-Hut
      BarnesHut bh01 = new BarnesHut(boxSize, 0.1, particles);
      BarnesHut bh05 = new BarnesHut(boxSize, 0.5, particles);
      BarnesHut bh1 = new BarnesHut(boxSize, 1.0, particles);
      double[] forceMags_bh01 = bh01.computeAllForces();
      double[] forceMags_bh05 = bh05.computeAllForces();
      double[] forceMags_bh1 = bh1.computeAllForces();
      
      
      // force error arrays for Barnes-Hut
      double[] forceError_bh01 = new double[numParticles];
      double[] forceError_bh05 = new double[numParticles];
      double[] forceError_bh1 = new double[numParticles];
      
      // cumulative force error for Barnes-Hut
      double cumForceError_bh01 = 0;
      double cumForceError_bh05 = 0;
      double cumForceError_bh1 = 0;
      
      // force error arrays for FMM
      double[] forceError_fmm01 = new double[numParticles];
      double[] forceError_fmm05 = new double[numParticles];
      double[] forceError_fmm1 = new double[numParticles];
      
      // cumulative force error for FMM
      double cumForceError_fmm01 = 0;
      double cumForceError_fmm05 = 0;
      double cumForceError_fmm1 = 0;
      
      
      for (int i = 0; i < numParticles; i++)
      {
         // compute fractional error for Barnes-Hut
         double err_bh01 = Math.abs(forceMags_bh01[i+1] - forceMags_df[i+1]) / Math.abs(forceMags_df[i+1]);
         double err_bh05 = Math.abs(forceMags_bh05[i+1] - forceMags_df[i+1]) / Math.abs(forceMags_df[i+1]);
         double err_bh1 = Math.abs(forceMags_bh1[i+1] - forceMags_df[i+1]) / Math.abs(forceMags_df[i+1]);
         
         
         cumForceError_bh01 += err_bh01;
         cumForceError_bh05 += err_bh05;
         cumForceError_bh1 += err_bh1;
         
         forceError_bh01[i] = err_bh01;
         forceError_bh05[i] = err_bh05;
         forceError_bh1[i] = err_bh1;
      
      
         // compute fractional error for FMM
         
         double err_fmm01 = Math.abs(forceMags_fmm01[i] - forceMags_df[i+1]) / Math.abs(forceMags_df[i+1]);
         double err_fmm05 = Math.abs(forceMags_fmm05[i] - forceMags_df[i+1]) / Math.abs(forceMags_df[i+1]);
         double err_fmm1 = Math.abs(forceMags_fmm1[i] - forceMags_df[i+1]) / Math.abs(forceMags_df[i+1]);
         
         cumForceError_fmm01 += err_fmm01;
         cumForceError_fmm05 += err_fmm05;
         cumForceError_fmm1 += err_fmm1;
         
         forceError_fmm01[i] = err_fmm01;
         forceError_fmm05[i] = err_fmm05;
         forceError_fmm1[i] = err_fmm1;
      }
   
      Arrays.sort(forceError_bh01);
      Arrays.sort(forceError_bh05);
      Arrays.sort(forceError_bh1);
      Arrays.sort(forceError_fmm01);
      Arrays.sort(forceError_fmm05);
      Arrays.sort(forceError_fmm1);
   
      System.out.println("BH average percent error: " + 100*cumForceError_bh01/numParticles + "%, " + 100*cumForceError_bh05/numParticles + "%, " 
                          + 100*cumForceError_bh1/numParticles + "%");
                          
      System.out.println("BH 90th percentile error: " + 100*forceError_bh01[(int)(0.9*numParticles)] + "%, " + 100*forceError_bh05[(int)(0.9*numParticles)] + "%, " 
                          + 100*forceError_bh1[(int)(0.9*numParticles)] + "%");
            
      System.out.println("FMM average percent error: " + 100*cumForceError_fmm01/numParticles + "%, " + 100*cumForceError_fmm05/numParticles + "%, "
                          + 100*cumForceError_fmm1/numParticles + "%");
                          
      System.out.println("FMM 90th percentile error: " + 100*forceError_fmm01[(int)(0.9*numParticles)] + "%, " + 100*forceError_fmm05[(int)(0.9*numParticles)] + "%, " 
                          + 100*forceError_fmm1[(int)(0.9*numParticles)] + "%");
   }

   
   public static void main(String[] args)
   {
      HernquistTest(8000, 10, 100);
   }

}