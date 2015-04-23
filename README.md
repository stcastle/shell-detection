# shell-detection
Image processing algorithms to detect the shells of galaxy NGC 3923. Project with the Gemini South Observatory and CTIO.

Automated Image Processing to Detect Galactic Shells
Samuel T. Castle
NOAO CTIO and Gemini Observatories
Jan-Mar 2014

This project is part of research conducted in a 2015 REU Program
hosted by the Cerro-Tololo Inter-American Observatory and funded by the NSF.

---------- Doc format -----------

This document describes scripts used detect shells in shell galaxies.
The file name, path, usage, and any additional notes are given for every
script.
A description of the test data is also included.

---------- Python reqs ----------

Many of these scripts use the Python libraries numpy, scipy, OpenCV (cv2),
astropy.io, and matplotlib, as well as the fileinput module.

---------- .fits files ----------

Unless scripts explicitly require fits-proc.py, they generally only support
image formats, such as .png, recognized by the OpenCV library functions.
It is not difficult to adapt a script to also work with .fits files.
To do so, see an example file, such as

/shell-detection/contour-fitting/contours.py
or

/shell-detection/fmfed/main.py
or

/shell-detection/convolutions/std-kernel/convolution-plot.py

--------------------------------------------------------------------------------
Test data

notes: Test data were made by varying 3 factors:
signal-to-noise ratio (SNR), shape, and the amount of Gaussian blur.
Data are sorted in folders by shape and then in subfolders by
the size of the Gaussian blur kernel in pixels (a larger kernel means more
blurring).
Files are named according to the SNR of the image.
Poisson noise was added to every test image using a custom python script
described later in this document.

The process for creating the test data was as follows:

1. Draw desired shapes using GNU Image Manipulation Program (GIMP).

2. Color shapes based on desired SNR.

3. Blur via Gaussian convolution, built into GIMP.

4. Add Poisson noise with the python script apply-poisson-noise.py


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Python scripts
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

Python scripts are organized in the shell-detection folder.
They are presented here in order of their subfolder.
All file paths are:
/shell-detection/<subfolder>/<script-name>

--------------------------------------------------------------------------------
subfolder: add-noise
--------------------------------------------------------------------------------
overview: This collection of scripts was used to add Poisson noise to test data.

name: apply-poisson-noise.py
usage: python apply-poisson-noise.py <input_files>
dependencies: noise.py
notes: Adds Poisson noise to the input file.
Use this version rather than apply-poisson-noise-stdin.py

name: apply-poisson-noise-stdin.py
usage: python apply-poisson-noise-stdin.py <input_files>
dependencies: noise.py
notes: Adds Poisson noise to the input file.
An early attempt at a different implementation than the previous script.
Use instead apply-poisson-noise.py.

name: noise.py
usage: none
notes: Generates the noise function used by apply-poisson-noise.py.

name: file-reader.py
usage: none
dependencies: noise.py
notes: Used only for developmental testing purposes.

name: noise-experiment.py
usage: none
dependencies: none
notes: Used only for developmental testing purposes.

--------------------------------------------------------------------------------
subfolder: coherence-elliptical-kernel
--------------------------------------------------------------------------------
overview: These files implement the explicit coherence enhancing filter with
spatial adaptive elliptical kernel from F. Li et al. 2012.

name: main.py
usage: python main.py
dependencies: none
notes: This script is still in development.
For a description of the algorithm, see F. Li et al. 2012.
Because this is the development version, no convenient method for file input
has been added; rather, the name of the input filename must be changed in
the sourcecode.

name: main-iter.py
usage: python main.py
dependencies: none
notes: This script is still in development.
Repeatedly applies the algorithm used in the previous script.
Adjust the input file and number of iterations within the source code.

--------------------------------------------------------------------------------
subfolder: compilation
--------------------------------------------------------------------------------
overview: These files combine several ``classic'' edge detection algorithms,
so they can all be executed in a single python script. This is very useful
for trying many algorithms on a large dataset.

name: process-all.py
usage: python process_all.py <input_files>
dependencies: canny-write-image.py, contours-write-image.py,
fmfe-main-write-image.py, threshold-write-image.py
notes: Runs thresholding, contour, Canny, and FMFE algorithms on the
input data. See the following scripts for details on each algorithm.
** Many of the algorithms use various smoothing filters in a preprocessing step.
This is reflected in the names of the output files returned by process-all.py.

name: canny-write-image.py
usage: none
dependencies: none
notes: Canny edge detection.

name: contours-write-image.py
usage: none
dependencies: none
notes: Algorithms using contours from the OpenCV library.

name: fmfe-main-write-image.py
usage: none
dependencies: fmfe.py
notes: Fast Multilevel Fuzzy Edge Detection Algorithm from J. We et al. 2007.

name: threshold-write-image.py
usage: none
dependencies: none
notes: adaptive mean threshold, adaptive Gaussian threshold, and Otsu's
threshold.

name: fmfe.py
usage: none
dependencies: fmfe-edge-detect.py
notes: Fast Multilevel Fuzzy Edge Detection Algorithm from J. We et al. 2007.
Helper for fmfe-main-write-image.py

name: fmfe-edge-detect.py
usage: none
dependencies: none
notes: Fast Multilevel Fuzzy Edge Detection Algorithm from J. We et al. 2007.
The edge detection portion of the algorithm.
Called by fmfe.py.

--------------------------------------------------------------------------------
subfolder: contour-fitting
--------------------------------------------------------------------------------
overview: These scripts run edge detection algorithms based on the contour
fitting functions provided in the OpenCV library.

name: contours-ellipse.py
usage: python contours-ellipse.py <input_files>
dependencies: fits-proc.py  (for handling .fits files)
fits-proc.py is located in the fits-algs subdirectory.
notes: Filters the images with a bilateral filter,
finds the contours, and fits an ellipse to the contours.
Displays the results using matplotlib.

name: contours.py
usage: python contours.py <input_files>
dependencies: fits-proc.py  (for handling .fits files)
fits-proc.py is located in the fits-algs subdirectory.
notes: Filters the images with a bilateral filter and finds the contours.
Displays the results using matplotlib.

name: ellipse.py
usage: python ellipse.py
dependencies: none
notes: This script was used for experimental development and is not updated.
Use of this script is not recommended.

--------------------------------------------------------------------------------
subsubfolder: convolutions/custom-kernel
--------------------------------------------------------------------------------
overview: These five scripts each are an attempt to define a convolution
kernel which matches an elliptical shape, thus enhancing ellipses when
applied to images.
The scripts are identical except for the particular kernel created.

name: arc-kernel1.py
usage: python arc-kernel1.py <input_files>
dependencies: none
notes: Simple kernel with a single spike to look for sharp edges.

name: arc-kernel2.py
usage: python arc-kernel2.py <input_files>
dependencies: none
notes: Gaussian with an arc shape.

name: arc-kernel3.py
usage: python arc-kernel3.py <input_files>
dependencies: none
notes: Similar to arc-kernel1.py, but a greater curve eccentricity.

name: arc-kernel4.py
usage: python arc-kernel4.py <input_files>
dependencies: none
notes: Sobel-type filter with an arc shape.

name: arc-kernel5.py
usage: python arc-kernel5.py <input_files>
dependencies: none
notes: Similar to arc-kernel4.py, but a skinnier curve.

--------------------------------------------------------------------------------
subsubfolder: convolutions/std-kernel
--------------------------------------------------------------------------------

name: main.py
usage: python main.py <input_files>
dependencies: smooth-write-image.py
notes: Handles file I/O for testing many standard
convolutions on various images.
Calls smooth-write-image to process and write the input images.

name: smooth-write-image.py
usage: none
dependencies: none
notes: Called by main.py.
Convolves each input image with a bilateral, median, Gaussian, Laplacian,
and Sobel filter separately.
Writes each filtered image as a distinct file.

name: bilat-write-image.py
usage: python bilat-write-image.py <input_files>
dependencies: none
notes: Smooths input images with a bilateral filter and writes resulting images.

name: convolutions-plot.py
usage: python convolutions-plot.py <input_files>
dependencies: fits-proc.py  (for handling .fits files)
fits-proc.py is located in the fits-algs subdirectory.
notes: Convolves input images with a bilateral, median, and Gaussian filter
and displays the results using matplotlib.
Handles .fits files.

--------------------------------------------------------------------------------
subfolder: fft
--------------------------------------------------------------------------------
overview: Scripts for using the Fast Fourier Transform (FFT) function in numpy.
In this implementation, images are converted to frequency space using the FFT.
Then, the high-frequency domain is truncated off the image, and the image
is reconverted using the inverse FFT.
In this way, the algorithm acts as a low-pass filter.
This removes high-frequency features such as edges sharper than those we
are attempting to detect, such as the sharp edges around stars.

name: main.py
usage: python main.py <input_files>
dependencies: fft-write-image.py
notes: Reads in a sequence of file paths of arbitrary length and calls
fft-write-image.py on each file.

name: fft-write-image.py
usage: none
dependencies: none
notes: Called by main.py. This is the bulk of the algorithm.

name: fft-plot.py
usage: python fft-plot.py
dependencies: none
notes: This script was used for testing and development purposes only.
As such, there is no convenient way to work with input files---the input
file must be specified in the source code.
Use of this script is not recommended.

--------------------------------------------------------------------------------
subfolder: fits-algs
--------------------------------------------------------------------------------
overview: All of these scripts have been adapted to working with .fits files.

name: adapt-mean-iterative-fits.py
usage: python adapt-mean-iterative-fits.py <input_files>
dependencies: none
notes: Repeatedly apply adaptive mean thresholding to each input image.
The number of iterations is specified by the user.
The user can also add an object mask for each image.

name: canny-write-image-fits.py
usage: python canny-write-image-fits.py <input_files>
dependencies: none
notes: Canny edge detection with various preprocessing steps.

name: contours-ellipse.py
usage: python contours-ellipse.py <input_files>
dependencies: fits-proc.py
notes: Find contours and fit an ellipse using OpenCV functions.

name: contours-write-image-fits.py
usage: python contours-write-image-fits.py <input_files>
dependencies: none
notes: Find contours then apply thresholding or Canny edge detection.

name: convolutions-plot.py
usage: python convolutions-plot.py <input_files>
dependencies: fits-proc.py
notes: Plot standard smoothing filters.

name: edge-detect.py
usage: none
dependencies: none
notes: Called by fmfe-main-write-image_fits.py for the second step
implementation of the FMFED algorithm from J. Wu et al. 2007.

name: fft-fits.py
usage: python fft-fits.py <input_files>
dependencies: none
notes: Plot result of FFT algorithm.

name: fft-plot-fits.py
usage: python fft-plot-fits.py <input_files>
dependencies: none
notes: Different version but essentially the same as fft-fits.py.

name: fft-write-fits.py
usage: python fft-write-fits.py <input_files>
dependencies: none
notes: Write the output image from the FFT algorithm.

name: fits-proc.py
usage: none
dependencies: fmfe.py, edge-detect.py
notes: Class used to handle .fits files.
Commonly used by many other scripts.

name: fmfe-main-write-image_fits.py
usage: none
dependencies: none
notes: Called by process-all.py to apply the FMFE algorithm from
J. We et al. 2007 to each input image and write the result.

name: otsu-iterative-fits.py
usage: python otsu-iterative-fits.py <input_files>
dependencies: none
notes: Repeatedly apply Otsu's thresholding to each input image.
The number of iterations is specified by the user.
The user can also add an object mask for each image.

name: process-all-fits.py
usage: python process-all-fits.py <input_files>
dependencies: contours-write-image_fits.py, threshold-write-image-fits.py,
canny-write-image-fits.py, fmfe-main-write-image-fits.py
notes: Run contours-write-image_fits.py, threshold-write-image-fits.py,
canny-write-image-fits.py, and fmfe-main-write-image-fits.py
independently on all input images.

name: threshold-write-image-fits.py
usage: python threshold-write-image-fits.py <input_files>
dependencies: none
notes: Apply a bilateral filter then various thresholding algorithms to each
image independently and save the results as separate images.

--------------------------------------------------------------------------------
subfolder: fmfed
--------------------------------------------------------------------------------
overview: These scripts are used to implement the Fast Multilevel Fuzzy
Edge Detection (FMFED) algorithm and the Fast Multilevel Fuzzy
Enhancement (FMFE) algorithm from J. Wu et al. 2007.

name: edge-detect.py
usage: none
dependencies: none
notes: Used by fits-proc.py to add the edge detection step after FMFE,
completing FMFED.
Warning: This script has not been thoroughly tested.

name: fits-proc.py
usage: python fits-proc.py <input_files>
dependencies: fmfe.py, edge-detect.py
notes: Class used to handle .fits files.
Commonly used by many other scripts.

name: fmfe.py
usage: none
dependencies: none
notes: Used by fits-proc.py for FMFE.

name: main-png.py
usage: python main-png.py <input_files>
dependencies: fits-proc.py, fmfe.py, edge-detect.py
notes: Runs FMFED on the input images and plots the results using matplotlib.
Works for both .png and .fits files.

name: main.py
usage: python main.py <input_files>
dependencies: fits-proc.py
notes: Runs FMFED on .fits images and writes the resulting images.

name: png-proc.py
usage: python png-proc.py <input_files>
dependencies: fmfe.py, edge-detect.py
notes: Runs FMFED on .png images and writes the resulting images.

name: sub-mask.py
usage: python sub-mask.py
dependencies: fits-proc.py
notes: Subtract a mask from an input .fits image and write the result.
This script is still under development. At this time, the user cannot
specify the mask file; rather, it is specified in the source code.

name: test.py
usage: python test.py
dependencies: edge-detect.py
notes: This script exists solely for experimental purposes during development.
Theres is no reason to use this script for a purpose other than testing.

--------------------------------------------------------------------------------
subfolder: larson-filters
--------------------------------------------------------------------------------
overview: Implementations of the Larson-Sekanina and Larson-Slaughter filters.

name: larson-filters.py
usage: none
dependencies: none
notes: Directly from
ftp://ftp.ster.kuleuven.ac.be/dist/maarten/pieterdg/thesis.pdf

name: larson-filters-png.py
usage: none
dependencies: none
notes: The previous algorithm adapted to work smoothly with .png files.

name: larson-main.py
usage: python larson-main.py <input_files>
dependencies: larson-filters-png.py
notes: Executes either the Larson-Sekanina or the Larson-Slaughter algorithm
on each input image and writes the result.
This code was not fully developed, so the choice of algorithm resides solely
within the source code.

--------------------------------------------------------------------------------
subfolder: manual-filters
--------------------------------------------------------------------------------
overview: Both subsubfolders contain skeleton code for creating convolution
kernels from scratch.
Because of the convenient convolution functions in the OpenCV library,
these scripts were not required or used extensively in this research project.
Thus, they are not fully developed and need not be fully explained in this
document.
They are interesting for study, and the subfolder includes a set of files
written in C++ as well as a set written in Python.

--------------------------------------------------------------------------------
subfolder: open-cv-edge-detection
--------------------------------------------------------------------------------
overview: These scripts employ edge detection algorithms from
the OpenCV library.
These are all configured to work with either .fits or .png images.

name: canny.py
usage: python canny.py <input_files>
dependencies: fits-proc.py
notes: Applies Canny edge detection to each image and displays results in a plot.

name: edges-trackbar.py
usage: python edges-trackbar.py <input_files>
dependencies: fits-proc.py
notes: Runs Canny edge detection on the input images, displays the result,
and allows the user to slide trackbars to adjust the Canny parameter values.

name: laplace-sobel.py
usage: python laplace-sobel.py <input_files>
dependencies: fits-proc.py
notes: Applies the Laplacian and Sobel edge detection algorithms to each
image and displays the results in a matplotlib plot.

name: sift.py
usage: python sift.py <input_files>
dependencies: fits-proc.py
notes: Runs Scale-Invariant Feature Transform (SIFT) on each image
and displays the results.
** SIFT is patented and users are required to pay for it.
A good alternative my be OpenCV's open-source ORB (Oriented FAST and
Rotated BRIEF) algorithm.

name: trackbar.py
usage: python trackbar.py
dependencies: none
notes: A test of using OpenCV to create a trackbar.

--------------------------------------------------------------------------------
subfolder: thresholds
--------------------------------------------------------------------------------
overview: These scripts allow experimentation with global thresholding,
adaptive mean thresholding, adaptive Gaussian thresholding,
and Otsu's thresholding.

name: threshold-write-image.py
usage: python threshold-write-image.py <input_files>
dependencies: none
notes: Runs Otsu's thresholding after no filter, a median filter,
a Gaussian filter, and a bilater filter.
Writes the result for each input image.

name: threshold.py
usage: python threshold.py <input_files>
dependencies: fits-proc.py
notes: Runs each of the thresholding algorithms after no filter,
a median filter, a Gaussian filter, and a bilater filter.
Displays the results in a plot using matplotlib.
