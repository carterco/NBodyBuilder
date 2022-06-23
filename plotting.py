import imageio
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize 
from scipy.interpolate import interpn
import matplotlib.animation as animation


# Needs to be tested... 
# times should be giant martix where array[0] is time 1 and array[1] is time 2 and so on...

# Maybe don't use pandas at all?
def output_files(times): 
    counter = 0
    for t in times:
        m = [particle[0] for particle in t]
        x = [particle[1] for particle in t]
        y = [particle[2] for particle in t]
        z = [particle[3] for particle in t]

        d = {'m': m, 'x': x, 'y': y, 'z': z}
        #df["string{0}".format(counter)] = pd.DataFrame(data=d)
        #df.to_csv('snapshot_'+str(counter),index=False)
        # HELP
        counter += 1
    return df_list


# Density scatter based on reference: https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib

def density_scatter( x , y, ax = None, fig = None, sort = True, bins = 20, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """
    if ax is None :
        fig , ax = plt.subplots()
    
    data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True )
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False)

    # To be sure to plot all data
    z[np.where(np.isnan(z))] = 0.0

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
        
    ax.set_facecolor('black')
    ax.scatter( x, y, c=z, **kwargs )

    norm = Normalize(vmin = np.min(z), vmax = np.max(z))

    return ax

# filenames = "snapshot.*"
# f = glob.glob(filenames)
# nums = [file.split('_')[1] for file in f]
# idx = np.argsort(nums)
# ordered_files = np.array(f)[idx]
# skip_some = ordered_files[::10] # Plot every 10 images, adjust as needed

def quick_plot(df):
    # df = pd.read_csv(filename)
    
    fig, axs = plt.subplots(1, 1, figsize=(4.2, 4))

    density_scatter( df['x'], df['y'], bins = [100,100], ax = axs, fig=fig, s=1,alpha=.1, cmap='summer')
    plt.tight_layout()
    
    fig.patch.set_facecolor('white')
    
    axs.scatter(0,0, marker='x', c='white', lw=.5, s=10)
    
    axs.set_xlabel('x-position')
    axs.set_ylabel('y-position')

    axs.set_xlim(-100,100)
    axs.set_ylim(-100,100)
    
    # plt.savefig('frame_'+str(count), dpi=100, bbox_inches='tight') 
    # plt.close(fig)
    
    return

# HELP
def main(times, df):
    numframes = len(times)
    scat = quick_plot(df)
    ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes), fargs=(df))
    plt.show()

# HELP
def update_plot(i, df_list, scat):
    scat.set_array(df_list[i])
    return scat

main()

# count = 0
# for filename in skip_some:
#     quick_plot(filename)
#     count += 1

# images = []
# imgnames = "frame_*"

# p = glob.glob(imgnames)
# nums = [file.split('_')[1] for file in p]
# nums_arr = [int(x) for x in nums]
# idx = np.argsort(nums_arr)
# ordered_imgs = np.array(p)[idx]

# for imgname in ordered_imgs:
#     images.append(imageio.imread(imgname))
    
# imageio.mimsave('x_y_animate.gif', images, fps=5) # Frames per second is up to you!