# Two Parameters Used for Modeling Solar Wind Speed

This program can be downloaded with the command
```
git clone https://github.com/slipq
```


And FastQSL2 should be downloaded first
```
git clone https://github.com/FastQSL2
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
