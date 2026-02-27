import numpy as np
import pickle, os
from par2solarwind import par2solarwind
# ------------------------------------------------------------
def bfield_charge4_spherical(bfile, n_lon=181, n_lat=91, n_r=31):

    B_lon=np.zeros((n_r, n_lat, n_lon),'f4')
    B_lat=np.zeros((n_r, n_lat, n_lon),'f4')
    B_r  =np.zeros((n_r, n_lat, n_lon),'f4')

    ri=np.array([[0.7*np.pi, 0.0, 0.8], \
                 [0.9*np.pi, 0.1, 0.8], \
                 [1.1*np.pi,-0.1, 0.8], \
                 [1.3*np.pi, 0.1, 0.8]],'f4')

    ri_car=ri.copy()
    for s in range(4): ri_car[s,:]= ri[s,2]* \
    np.array([np.cos(ri[s,1])*np.cos(ri[s,0]), np.cos(ri[s,1])*np.sin(ri[s,0]), np.sin(ri[s,1])],'f4')

    qi=np.array([1.,-1.,1.,-1.],'f4')

    lon_rad= np.linspace(0., 2.*np.pi, n_lon)
    lat_rad= np.linspace(-np.pi/2., np.pi/2., n_lat)
    radius = np.linspace(1., 2.5, n_r)

    cos_lon=np.cos(lon_rad)
    sin_lon=np.sin(lon_rad)
    cos_lat=np.cos(lat_rad)
    sin_lat=np.sin(lat_rad)
    
    for i in range(n_lon):
        e_lon=np.array([-sin_lon[i], cos_lon[i], 0.],'f4')
        for j in range(n_lat):
            e_lat=np.array([-sin_lat[j]*cos_lon[i], -sin_lat[j]*sin_lon[i], cos_lat[j]],'f4')
            e_r  =np.array([ cos_lat[j]*cos_lon[i],  cos_lat[j]*sin_lon[i], sin_lat[j]],'f4')
            for k in range(n_r):
                rp_car=radius[k]*e_r
                Bp_car=np.zeros((3),'f4')
                for s in range(4):
                    dr=rp_car-ri_car[s,:]
                    Bp_car=Bp_car+qi[s]*dr/(np.sum(dr**2)**1.5)
            
                B_lon[k,j,i]=np.dot(e_lon,Bp_car)
                B_lat[k,j,i]=np.dot(e_lat,Bp_car)
                B_r  [k,j,i]=np.dot(e_r  ,Bp_car)
    with open(bfile, 'wb') as file: pickle.dump((B_lon, B_lat, B_r, lon_rad, lat_rad, radius), file)
# ------------------------------------------------------------
bfile='charge4_spherical.pkl'
cdir = os.getcwd()+os.sep 
if bfile not in os.listdir(cdir): bfield_charge4_spherical(bfile)
with open(bfile, 'rb') as file: (b_lon, b_lat, b_r, lon_rad, lat_rad, radius) = pickle.load(file)

fs, theta_b, qsl= par2solarwind(b_lon, b_lat, b_r, lon_rad, lat_rad, radius, preview=True, bottomFlag=True)