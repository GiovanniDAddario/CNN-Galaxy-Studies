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
pixel_scale = parameters[-2] # pixel scale: arcsec per pixel
final_size = int(parameters[-1]) # size of processed .fits files. Images that
    # are smaller than this level are padded with random noise. Images that
    # are larger than this threshold are discarded (motivated by efficiency
    # concerns for CNN)

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
    # create an array to store results of convolution
    convolved_image = np.zeros(shape=np.shape(image))
    for channel in range(channels):
        # default size of PSF kernel is 8 times std in each direction
        # originally defined std in both x, y axes; then changed to single
            # value (same for both axes) to work with astropy 2.0.9
        psf = Gaussian2DKernel(std_pix[channel])
        convolved_image[channel] = convolve(image[channel], psf)
    return convolved_image


def noise_modelling(image, final_size, noise_background, noise_std):
    """
    Incorporates sky background noise into a synthetic image. The noise is 
    sampled from a Gaussian distribution for which the mean and the
    standard deviation can be specified.
    
    Parameters:
    image : array of shape (channels, N, N), assuming that the first value is
        the number of filters (channels)
    final_size : integer M >= N: processed images will have shape 
        (channels, M, M)
    noise_background : array with mean values of the noise distribution for 
        each filter
    noise_std : array with standard deviations of the noise distribution for
        each filter
    
    Returns:
    noisy_image : array of shape (channels, N, N) with the noise contribution
    """
    channels = np.shape(image)[0] # assume channels are listed first
    # create array to store results of noise modelling and padding
    noisy_image = np.zeros(shape=(channels, final_size, final_size))
    for channel in range(channels):
        initial_size = np.shape(image[channel])[-1]
        if final_size == initial_size:
            noisy_image[channel] += image[channel]
        # padding is done slightly differently depending on whether the
            # difference between the initial/final image size is even or odd
        elif (final_size - initial_size) % 2 == 0: # even case
            noisy_image[channel] = np.pad(image[channel], int((
                final_size-initial_size)/2), mode='constant',constant_values=0)
        else: # odd case
            noisy_image[channel] = np.pad(image[channel], (int((
                final_size-initial_size)/2 - 0.5), int((
                final_size-initial_size)/2 + 0.5)), mode='constant', 
                constant_values=0)
        # add noise sampled from a normal distribution to the padded image
        noisy_image[channel] += np.random.normal(noise_background[channel], 
                                 noise_std[channel], (final_size, final_size))
    noisy_image[noisy_image < 0] = 0 # set all values below 0 to 0
    return noisy_image


def image_postprocessing(image, final_size, noise_background, noise_std):
    """
    Carries out the post processing steps required to prepare a synthetic image
    for use in the Convolutional Neural Network model. Calls the convolve_PSF
    and noise_modelling functions as well as ensuring each 2D array of data
    has values between 0 and 1.
    
    Parameters:
    image : array of shape (channels, N, N), assuming that the first value is
        the number of filters (channels)
    final_size : integer M >= N: processed images will have shape 
        (channels, M, M)
    noise_background : array with mean values of the noise distribution for 
        each filter
    noise_std : array with standard deviations of the noise distribution for
        each filter
    
    Returns:
    processed_image : array of shape (channels, N, N) corresponding to the
        processed image
    """
    convolved_image = convolve_PSF(image)
    noisy_convolved_image = noise_modelling(convolved_image, final_size, 
                                            noise_background, noise_std)
    channels = np.shape(noisy_convolved_image)[0]
    # create array to store results of rescaling of data
    processed_image = np.zeros(shape=(channels, final_size, final_size))
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
        # .fits files that are larger than the selected size are ignored
        if np.shape(data)[-1] > final_size:
            pass
        else:
            hdul[0].data = image_postprocessing(data, final_size, 
                                                noise_background, noise_std)
            hdul.writeto('processed_'+file) # write changes to new fits file
        