# Two Parameters Used for Modeling Solar Wind Speed

[Arge (2003)](https://pubs.aip.org/aip/acp/article-abstract/679/1/190/1010917/Improved-Method-for-Specifying-Solar-Wind-Speed?redirectedFrom=fulltext) found the Solar Wind Speed can be roughly modeled by
$v_\textrm{sw}=265+\dfrac{25}{f_s^{2/7}} \left(5-1.1\times \exp(1-(\theta_b/4)^2)\right)~\mathrm{km/s}, $
and two parameters in this formula are defined as:
* Magnetic field expansion factor
$
f_\mathrm{s}(\varphi, \vartheta, r)=
\left(\dfrac{R_0}{R_1}\right) ^2
\dfrac{B_r(\varphi_0, \vartheta_0, R_0)}
{B_r(\varphi_1, \vartheta_1, R_1)}, 
$
where $(\varphi_0, \vartheta_0, R_0)$ are the target coordinates traced from $(\varphi, \vartheta, r)$ to the inner boundary of $r=R_0$, and $(\varphi_1, \vartheta_1, R_1)$ are the target coordinates traced from $(\varphi, \vartheta, r)$ to the outer boundary of $r=R_1$.
* $\theta_b(\varphi, \vartheta, r)$, the minimum angular distance of an open-field footpoint from a coronal hole boundary.
* For a closed field line, its **rboundary** is 11, its $f_\mathrm{s}$ is set to 1000., its $\theta_b$ is set to 0., these default values can be adjusted in par2solarwind\.pro (par2solarwind\.py)


This program can be downloaded with the command
```
git clone https://github.com/el2718/par2solarwind
```


And FastQSL2 should be downloaded first
```
git clone https://github.com/el2718/FastQSL2
```

Please address comments and suggestions to [Dr. Chen, Jun (陈俊)](mailto:chenjun@pmo.ac.cn)

If your markdown reader can not can not render the formulae in README\.md, please read README.html directly.

-----------------------------
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This program is licensed under a [CC BY-NC-SA 4.0 License][cc-by-nc-sa].

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

-----------------------------
## Cite as

* Jun Chen*, Thomas Wiegelmann, Li Feng*, Bernhard Kliem, Chaowei Jiang, and Rui Liu. FastQSL 2: A Comprehensive Toolkit for Magnetic Connectivity Analysis.  2026, SCIENCE CHINA Physics, Mechanics & Astronomy, submitted

-----------------------------
## Computation of `theta_b.f90` with Fortran

* For Linux and macOS (either by ifx/ifort or gfortran):
    ```bash
    ifx -o theta_b.x theta_b.f90 -fopenmp -O3 -xHost -ipo
    ```
    ```bash
    ifort -o theta_b.x theta_b.f90 -fopenmp -O3 -xHost -ipo
    ```
    ```bash
    gfortran -o theta_b.x theta_b.f90 -fopenmp -O3 -march=native
    ```
* For Windows (either by ifort or gfortran):
  executing "C:\Program Files (x86)\Intel\oneAPI\setvars.bat" in cmd first would be necessary
  ```bash
  ifort /o theta_b.exe theta_b.f90 /Qopenmp /O3 /QxHost /Qipo
  ``` 
  ```bash
  gfortran -o theta_b.exe theta_b.f90 -fopenmp -O3 -march=native
  ``` 
  * In Windows 11, also in some upgraded Windows 10, the pop-up window for theta_b.exe can not be closed automatically, please uncomment this line in theta_b.f90 to kill the pop-up window (delete !):
    ```
    ! call system('taskkill /im theta_b.exe /f')
    ```
  * for ifx, the compilation should be the same as ifort, while I have not tested it
### Path of theta_b.x
* please specify the path of theta_b.x, 
  * in par2solarwind\.pro, please correct the line of
    ```idl
    spawn, '/path/of/theta_b.x'
    ```
  * in par2solarwind\.py, please correct the line of  
    ```python
    subprocess.run(r'/path/of/theta_b.x', shell=True)
    ```
* or move theta_b.x to the `$PATH` (e.g. `/usr/local/bin/`) of the system and delete the text `/path/of/`
  * you can append this line to `~/.bashrc`
    ```
    export PATH=$HOME/bin:$PATH
    ```
    then `$HOME/bin` is a `$PATH` of the system
* For Windows, use theta_b.exe instead of theta_b.x
