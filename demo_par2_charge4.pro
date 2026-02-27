pro bfield_charge4_spherical, bfile, n_lon=n_lon, n_lat=n_lat, n_r=n_r

if ~keyword_set(n_lon) then n_lon=181
if ~keyword_set(n_lat) then n_lat=91
if ~keyword_set(n_r)   then n_r=31

B_lon=fltarr(n_lon, n_lat, n_r)
B_lat=fltarr(n_lon, n_lat, n_r)
B_r  =fltarr(n_lon, n_lat, n_r)

ri=[[0.7*!pi, 0.0, 0.8], $
    [0.9*!pi, 0.1, 0.8], $
    [1.1*!pi,-0.1, 0.8], $
    [1.3*!pi, 0.1, 0.8]]   

ri_car=fltarr(3, 4)
for s=0, 3 do ri_car[*,s]= ri[2,s]* $
[cos(ri[1,s])*[cos(ri[0,s]), sin(ri[0,s])], sin(ri[1,s])]

qi=[1.,-1.,1.,-1.]

lon_rad=findgen(n_lon)/(n_lon-1.)*2.*!pi
lat_rad=findgen(n_lat)/(n_lat-1.)*!pi-!pi/2.
radius=findgen(n_r)/(n_r-1.)*1.5+1.

cos_lon=cos(lon_rad)
sin_lon=sin(lon_rad)
cos_lat=cos(lat_rad)
sin_lat=sin(lat_rad)

for i=0, n_lon-1 do begin
    e_lon=[-sin_lon[i], cos_lon[i], 0.]
for j=0, n_lat-1 do begin
    e_lat=[-sin_lat[j]*cos_lon[i], -sin_lat[j]*sin_lon[i], cos_lat[j]]
    e_r  =[ cos_lat[j]*cos_lon[i],  cos_lat[j]*sin_lon[i], sin_lat[j]]
for k=0, n_r-1 do begin
    rp_car=radius[k]*e_r
	Bp_car=fltarr(3)
	for s=0, 3 do begin
		dr=rp_car-ri_car[*,s]
		Bp_car=Bp_car+qi[s]*dr/(total(dr^2.)^1.5)
	endfor
    
	B_lon[i,j,k]=total(e_lon*Bp_car)
	B_lat[i,j,k]=total(e_lat*Bp_car)
	B_r  [i,j,k]=total(e_r  *Bp_car)
endfor
endfor
endfor

save, filename=bfile, B_lon, B_lat, B_r, lon_rad, lat_rad, radius

end
;------------------------------------------------------------
; Examples for spherical grid
bfile='charge4_spherical.sav'
if ~file_test(bfile) then bfield_charge4_spherical, bfile
restore, bfile

par2solarwind, b_lon, b_lat, b_r, lon_rad, lat_rad, radius, fs=fs, theta_b=theta_b, qsl=qsl, /preview, /bottom

save, filename='bottom_fs,theta_b.sav', fs, theta_b

end
