#!/bin/bash

# define arguments for image processing script
channels=4 # corresponds to number of filters (4 for SDSS case, u not considered)
median_seeing=(1.44 1.32 1.26 1.29) # seeing in arcsec in the filters (here g,r,i,z for SDSS)
noise_background=(0.0015 0.0029 0.0036 0.0029) # mean background level for each filter (here g,r,i,z for SDSS)
noise_std=(0.0286 0.0365 0.0523 0.1519) # standard deviation of noise for each filter (here g,r,i,z for SDSS)
pixel_scale=0.396 # arcsec per pixel (here for SDSS) # could get this from .fits file header for Illustris TNG SDSS sim
final_size=200 # size of processed .fits files. Images that are smaller than this level are padded with random noise.
	# Images that are larger than this threshold are discarded (motivated by efficiency concerns for CNN) 

python Image_Processing.py ${channels} ${median_seeing[@]} ${noise_background[@]} ${noise_std[@]} ${pixel_scale} ${final_size}

