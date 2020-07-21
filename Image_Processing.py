# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:22:08 2020

The script defines the post processing stages which must be carried out 
on synthetic images from the IllustrisTNG simulation to match SDSS
observations. This script should be applied to the images prior to their use
in the Convolutional Neural Network.

@author: Giovanni D'Addario
"""

import numpy as np
import os
import sys

from astropy.convolution import convolve, Gaussian2DKernel
from astropy.io import fits

"""Extract and assign parameters for the script; these can be modified in the
Bash script used to execute the script in the appropriate directory"""

# change format of and assign arguments passed into the script
parameters =  np.asarray([float(x) for x in sys.argv[1:]])
channels = int(parameters[0]) # number of filters, useful to separate params 
    # (N.B introduces a bit of redundancy as this number can be found from 
    # shape of image data)
median_seeing = parameters[1:1+channels] # median seeing (FWHM) in arcsec
noise_background = parameters[1+channels:1+2*channels] # noise background level
noise_std = parameters[1+2*channels:1+3*channels] # noise standard deviation
pixel_scale = parameters[-1] # pixel scale: arcsec per pixel

# convert useful quantities
FWHM_pix = median_seeing * pixel_scale # median seeing, pixels
std_pix = FWHM_pix/2.35 


def convolve_PSF(image):
    """
    Convolves a synthetic image with a Gaussian point spread function (PSF) to
    reproduce the effects of telescope optics and atmospheric noise on the 
    image.
    
    Parameters:
    image : array of shape (channels, N, N), assuming that the first value is
        the number of filters (channels)
        
    Returns:
    convolved_image : array of shape (channels, N, N) with the result of the
        convolution
    """
    channels = np.shape(image)[0] # assume channels are listed first
    convolved_image = np.zeros(shape=np.shape(image))
    for channel in range(channels):
        # default size of PSF kernel is 8 times std in each direction
        # originally defined std in both x, y axes; then changed to single
            # value (same for both axes) to work with astropy 2.0.9
        psf = Gaussian2DKernel(std_pix[channel])
        convolved_image[channel] = convolve(image[channel], psf)
    return convolved_image


def noise_modelling(image, noise_background, noise_std):
    """
    Incorporates sky background noise into a synthetic image. The noise is 
    sampled from a Gaussian distribution for which the mean and the
    standard deviation can be specified.
    
    Parameters:
    image : array of shape (channels, N, N), assuming that the first value is
        the number of filters (channels)
    noise_background : array with mean values of the noise distribution for 
        each filter
    noise_std : array with standard deviations of the noise distribution for
        each filter
    
    Returns:
    noisy_image : array of shape (channels, N, N) with the noise contribution
    """
    channels = np.shape(image)[0] # assume channels are listed first
    noisy_image = np.zeros(shape=np.shape(image))
    for channel in range(channels):
        noisy_image[channel] += image[channel] + np.random.normal(
            noise_background[channel], noise_std[channel], (np.shape(image)[1], 
                                          np.shape(image)[2]))
    noisy_image[noisy_image < 0] = 0 # set all values below 0 to 0 (no negative
        # value present before addition of random noise)
    return noisy_image


def image_postprocessing(image, noise_background, noise_std):
    """
    Carries out the post processing steps required to prepare a synthetic image
    for use in the Convolutional Neural Network model. Calls the convolve_PSF
    and noise_modelling functions as well as ensuring each 2D array of data
    has values between 0 and 1.
    
    Parameters:
    image : array of shape (channels, N, N), assuming that the first value is
        the number of filters (channels)
    noise_background : array with mean values of the noise distribution for 
        each filter
    noise_std : array with standard deviations of the noise distribution for
        each filter
    
    Returns:
    processed_image : array of shape (channels, N, N) corresponding to the
        processed image
    """
    convolved_image = convolve_PSF(image)
    noisy_convolved_image = noise_modelling(convolved_image, noise_background, 
                                            noise_std)
    channels = np.shape(noisy_convolved_image)[0]
    processed_image = np.zeros(shape=(np.shape(image)))
    for channel in range(channels):
        processed_image[channel] = noisy_convolved_image[channel]/np.max(
            noisy_convolved_image[channel])
    return processed_image


"""Assuming the files are in the current directory, run the processing script
on all the relavant .fits files in the directory and save changes to new
.fits files."""

for file in os.listdir('.'):
    if file.startswith('broadband') and file.endswith('.fits'):
        hdul = fits.open(file)
        data = hdul[0].data
        hdul[0].data = image_postprocessing(data, noise_background, noise_std)
        hdul.writeto('processed_'+file) # write changes to new fits file
        