# -*- coding: utf-8 -*-
import h5py
import numpy as np
import os
import csv
import math
from matplotlib import pyplot as plt
plt.switch_backend('agg')


def getFitsNumbers(dir_path, fileString='broadband_', dirs=None, savefilenames=False):
    """
    Retrieves the filenames in the directory given by dir_path, and returns the filenames as a list of strings. If savefilenames = True, saves the filenames in a txt file.
    """
    os.chdir(dir_path)
    filenames_dict = {}

    if dirs == None:
        filenames = os.listdir(dir_path)
        filenames_dict['filenames'] = filenames

    else:
        for subdir in dirs:
            subdir_path = os.path.join(dir_path, subdir)
            filenames = os.listdir(subdir_path)
            filenames_dict[subdir] = filenames

    if savefilenames == True:
        os.chdir('/scratch/anp793')
        txtfile = open('filenames.txt', 'w')
        txtfile.write(str(filenames_dict))
        txtfile.close()

    return filenames_dict

def getColours(hdf5_filename, files_dict, dest='/scratch/anp793'):
    """
    Opens the hdf5 file, and and retrieved lists of the subhalo ids, and corresponding photometry data. Writes the colour parameters (sdss_g - sdss_r) for each subhalo to a dictionary.
    """
    os.chdir(dest)
    colour_dict = {}

    f = h5py.File(hdf5_filename, 'r')

    keys = [key for key in f.keys()] # Two datasets
    photodata = f[keys[0]][()] # <class 'numpy.ndarray'>, shape = (4371211, 8, $
    subhalo_ids = f[keys[1]][()] # <class 'numpy.ndarray'>, shape = (4371211,)
    f.close()

    for subdir in files_dict:
        for fitsfilename in files_dict[subdir]:
            subhalo_id = int(''.join([c for c in fitsfilename if c.isdigit()]))
            index = np.where(subhalo_ids == subhalo_id)

    # 4371211 subhalos    
    # 8 photometric bands: sdss_u, sdss_g, sdss_r, sdss_i, sdss_z, wfc_acs_f606$
    # 12 corresponds to twelve different projection directions: can just pick t$

        subhalo = photodata[index]
        sdss_g = photodata[index][0][1][0] # Extra [0] after [index] to act$
        sdss_r = photodata[index][0][2][0]
        colour = sdss_g - sdss_r

        colour_dict[fitsfilename] = colour

    return colour_dict            

def writeValuesCSV(filenames, colour_dict, csv_name, value_name, dest='.'):
    """
    Writes the colour values to csv file, containing file name and colour
    """
    os.chdir(dest)

    # Write csv files
    for subdir in filenames:
        csv_cols = ['Filename', value_name]
        with open ((subdir+'_'+csv_name), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_cols)
            for fitsfilename in colour_dict:
                writer.writerow([fitsfilename, colour_dict[fitsfilename]])

    return None

def plotDistribution(colour_dict):
        """
        Plots the distribution of the colour values as a histogram
        """
        fig = plt.figure()
        colours = list(colour_dict.values())
        plt.hist(colours, bins=40, density=False)
        plt.xlabel('Colour (sdss_g - sdss_r)')
        plt.savefig('Colour_dist')

        return None

def cutoffColours(colour_dict, cutoff):
    """
    Assigns a value, 1 or 0, depending on whether the colour value is below or above the given cutoff
    """
    colour_flag_dict = {}
    for filename in colour_dict:
        colour_val = colour_dict[filename]
        if colour_val >= cutoff:
            colour_flag = 1 # Red 
        else:
            colour_flag = 0 # Blue

        colour_flag_dict[filename] = colour_flag

    return colour_flag_dict

    print('Generating dictionary of colours')
    colour_dict = getColours('StellarPhot.hdf5', filenames_dict)

    print('Generating csv files')
    writeValuesCSV(filenames_dict, colour_dict, 'colours.csv', 'ColourValue', dest=$

    plotDistribution(colour_dict)

    colour_flag_dict = cutoffColours(colour_dict, 0.65)
    writeValuesCSV(filenames_dict, colour_flag_dict, 'colour_flag.csv', 'ColourFlag$

    print('Done')

    # use the following line to run in hydra and write print statements to a log file:
    # nohup python filename.py & 