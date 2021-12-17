# pitchtrackingcomparison
A program that looks at the values produced by the YIN [1] and CREPE [2] methods of fundamental frequency estimation, produced in real-time.

The YIN and CREPE methods were implemented in Python using the aubio (https://aubio.org/) and CREPE (https://github.com/marl/crepe) libraries.

pitchTrackCompare.py is the primary script that runs the application.
pitchestimators.py accesses the aubio and CREPE libraries to process the incoming microphone audio to estimate its fundamental frequency and output a value.
notevalues.py categorizes all of the frequency values that have been established in the western standard musical notation, as well as their note names.
micbutton.py was intended to locate the position of the cursor and perform a switching function to turn the microphone signal on and off. It is currently not functioning.
yinAtempt.py was an attempt to replicate the YIN algorithm as it is described in [1]
setup.py allows for the python file to be converted into a .dmg file.

[1] De Cheveigné, A., & Kawahara, H. (2002). YIN, a fundamental frequency estimator for speech and music. The Journal of the Acoustical Society of America, 111(4), 1917-1930. https://doi.org/10.1121/1.1458024

[2] Kim, J. W., Salamon, J., Li, P., & Bello, J. P. (2018, April). Crepe: A convolutional representation for pitch estimation. In 2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 161-165). IEEE. https://doi.org/10.1109/ICASSP.2018.8461329
