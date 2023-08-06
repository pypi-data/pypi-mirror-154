(Testing version for pip uploading)QT version of FITIT for XANES fitting submodule of a package
It is a testing version for try pip  Installation.
There are Three examples:
environmentPATH\Lib\site-packages\QTFITIT_example_Fephen3
environmentPATH\Lib\site-packages\QTFITIT_example_IHS500
environmentPATH\Lib\site-packages\QTFITIT_example_IHS729

Runnning Program:
(1)Find the example folder:
cd environmentPATH\Lib\site-packages\QTFITIT_example_IHS500
(2)run program
QTFITIT
then QTFITIT GUI will open.

Input file
"input.txt" main input file,there is only input file name.  
input_IHS500.txt：input file
file_energy$IHS_500_energy.txt$                          input file name of energy(eV)
file_x$IHS_500_params.txt$                               input file name of parameters
file_y$IHS_500_mu_conv.txt$                              input file name of X-ray absorption spectra
file_exp$exp_excited.txt$                                input file name of experiment spectrum
fmodel$tmp.pkl$                                                 input file name of machine learning model XXX.pkl
e1$7100$                                                        plot Energy range from e1 to e2,
e2$7200$                                                        plot Energy range,for instance Fe XANES from 7100eV to 7200eV 
norm$33$                                                        normalization factor,in this FDMNES example is 33. 
npar$3$                                                         structure parameter number
par_a$-0.3,-0.3,-0.3$                                           structure parameter lower bound,   float array of size npar
par_b$0.5,0.5,0.5$                                              structure parameter upper bound,   float array of size npar
x0$0.2,0.2,0.2$                                                 structure parameter initial value, float array of size npar
par_name$centralRings_Shift,sideRings_Elong,sideRings_Shift$    structure parameter name, string array of size npar

