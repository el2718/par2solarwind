pro par2solarwind, b_lon, b_lat, b_r, lon_rad, lat_rad, radius,           $
RK4Flag=RK4Flag, step=step, tol=tol, maxsteps=maxsteps,                   $
bottomFlag=bottomFlag, nthreads=nthreads, silent=silent, preview=preview, $
fs=fs, theta_b=theta_b, qsl=qsl
;------------------------------------------------------------
n_lon= n_elements(lon_rad)
n_lat= n_elements(lat_rad)
n_r  = n_elements(radius)

if keyword_set(bottomFlag) then begin 
    seed='original_bottom' 
    n_r1=1
endif else begin
    seed='original'
    n_r1=n_r
endelse

fastqsl, b_lon, b_lat, b_r, xa=lon_rad, ya=lat_rad, za=radius, /spherical, $
RK4Flag=RK4Flag, step=step, tol=tol, maxsteps=maxsteps,                    $
seed=seed, /rf, /targetB, tmp_dir=tmp_dir, /keep, odir=odir,               $
nthreads=nthreads, silent=silent, preview=preview, qsl=qsl
;fs----------------------------------------------------------
brs=reform(qsl.bs[2,*,*,*])
bre=reform(qsl.be[2,*,*,*])

fs=fltarr(n_lon, n_lat, n_r1)+1000.

index12=where(qsl.rboundary eq 12)
if (index12[0] ne -1) then $
fs[index12]= (radius[0]/radius[n_r-1])^2.* abs(brs(index12)/bre(index12))

index21=where(qsl.rboundary eq 21)
if (index21[0] ne -1) then $
fs[index21]= (radius[0]/radius[n_r-1])^2.* abs(bre(index21)/brs(index21))
;theta_b-----------------------------------------------------
get_lun, unit
openw,  unit, tmp_dir+'dimension.bin'
writeu, unit, long([nthreads, n_lon, n_lat, n_r1])
close,  unit

cd, current = cdir
cd, tmp_dir
spawn, '/path/of/theta_b.x'
cd, cdir

theta_b=fltarr(n_lon, n_lat, n_r1)
openr,  unit, tmp_dir+'theta_b.bin'
readu,  unit, theta_b
close,  unit
;-------------------------------------------------------------------------------s
free_lun, unit, /force
file_delete, tmp_dir, /recursive

verbose  =~keyword_set(silent)
if preview then begin
    write_png, odir+'bottom_fs.png', bytscl(fs[*,*,0], min=0, max=10, /nan)
    write_png, odir+'bottom_theta_b.png', bytscl(theta_b[*,*,0], min=0, max=0.5, /nan)
    if verbose then begin
        print, odir+'bottom_fs.png'
        print, odir+'bottom_theta_b.png'
    endif
endif

if verbose then begin
    help, fs, OUTPUT=OUTPUT
    print, OUTPUT
    help, theta_b, OUTPUT=OUTPUT
    print, OUTPUT
endif

end
