import numpy as np
import os, subprocess
from fastqsl import fastqsl
import matplotlib.pyplot as plt

def par2solarwind(b_lon, b_lat, b_r, lon_rad, lat_rad, radius, \
                  RK4Flag=False, step=1.0, tol=1.0e-4, maxsteps=None, \
                  bottomFlag=False, nthreads=0, silent=False, preview=False):
    # ------------------------------------------------------------
    seed='original_bottom' if bottomFlag else 'original'
    cdir = os.getcwd()+os.sep
    odir = cdir+'fastqsl'+os.sep
    tmp_dir= cdir+'tmpFastQSL'+os.sep
    qsl=fastqsl(b_lon, b_lat, b_r, xa=lon_rad, ya=lat_rad, za=radius, spherical=True, \
                RK4Flag=RK4Flag, step=step, tol=tol, maxsteps=maxsteps, nthreads=nthreads, \
                seed=seed, rF_out=True, targetB_out=True, \
                silent=silent, tmp_dir=tmp_dir, keep_tmp=True, preview=preview)
    # ------------------------------------------------------------
    n_lon= len(lon_rad)
    n_lat= len(lat_rad)
    if bottomFlag:
        n_r1 = 1
        brs=qsl['Bs'][:,:,2]
        bre=qsl['Be'][:,:,2] 
        shape=(n_lat, n_lon)
    else:
        n_r1 = len(radius)
        brs=qsl['Bs'][:,:,:,2]
        bre=qsl['Be'][:,:,:,2]
        shape=(n_r, n_lat, n_lon)

    fs=np.zeros(shape,'f4')+1000.
    index12=qsl['rboundary'] == 12
    fs[index12]= (radius[0]/radius[-1])**2. * np.abs(brs[index12]/bre[index12])
    index21=qsl['rboundary'] == 21
    fs[index21]= (radius[0]/radius[-1])**2. * np.abs(bre[index21]/brs[index21])
    # ------------------------------------------------------------
    with open(tmp_dir+'dimension.bin','wb') as file:
        file.write(np.array([nthreads, n_lon, n_lat, n_r1], dtype='i4', order='C'))
    
    os.chdir(tmp_dir)
    subprocess.run(r'/path/of/theta_b.x', shell=True)
    os.chdir(cdir)

    theta_b=np.fromfile(tmp_dir+'theta_b.bin', dtype='f4').reshape(shape)

    for folder_name, subfolders, filenames in os.walk(tmp_dir):
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_name, subfolder)
            os.rmdir(subfolder_path)
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            os.remove(file_path)
    os.rmdir(tmp_dir)

    verbose= not silent
    if preview:
        if bottomFlag:
            fs1=fs
            theta_b1=theta_b
        else:
            fs1=fs[0,:,:]
            theta_b1=theta_b[0,:,:]       
        plt.imsave(odir+'bottom_fs.png', fs1, vmin=0., vmax=10., origin='lower', cmap='gray')
        plt.imsave(odir+'bottom_theta_b.png', theta_b1, vmin=0., vmax=0.5, origin='lower', cmap='gray')
        if verbose:
            print(odir+'bottom_fs.png')
            print(odir+'bottom_theta_b.png')

    if verbose:
        print('{0:<20}{1:<10}'.format('fs', fs.dtype.name), fs.shape)
        print('{0:<20}{1:<10}'.format('theta_b', theta_b.dtype.name), theta_b.shape)

    return fs, theta_b, qsl



