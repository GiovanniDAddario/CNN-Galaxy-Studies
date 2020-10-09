import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

import requests
import os
import csv


def get(path, params=None):
    """
    Function from the Illustris API tutorial, navigates to the API at the given path.
    """
    # make HTTP GET request to path
    r = requests.get(path, params=params, headers={"api-key":"a4c17a07666a0e719a666ded98e0d208"})
    # raise exception if response code is not HTTP SUCCESS (200)
    r.raise_for_status()
    if r.headers['content-type'] == 'application/json':
        return r.json() # parse json responses automatically
    return r

def getGroupFirstSub(subhalo_id, snapshot=99, baseurl='http://www.tng-project.org/api/TNG100-1/'):
    """
    For a subhalo ID, returns which subhalo ID is it's primary subhalo. If this is equal to its own subhalo ID, then the subhalo is a central subhalo, otherwise it is a satellite subhalo.
    """
    url= baseurl+'snapshots/'+ str(snapshot) + '/subhalos/' + str(subhalo_id)
    subhalo = get(url)
    logging.debug('Subhalo URL: {}'.format(url))
    logging.debug('Parent halo of subhalo {}: {}'.format(subhalo['id'], subhalo['related']['parent_halo']))
    logging.debug('FoF Group number: {}'.format(subhalo['grnr']))

    parent_halo = get(subhalo['related']['parent_halo']+'info.json')
    group_first_sub = parent_halo['GroupFirstSub']
    logging.debug('GroupFirstSub: {}'.format(group_first_sub))

    return group_first_sub

def getFitsNumbers(dir_path, fileString='broadband_', dirs=None):
    """
    Retrieves the file names in the directory given by dir_path
    """
    os.chdir(dir_path)
    logging.debug('Current directory: {}'.format(os.getcwd()))

    if dirs == None:
        filenames = os.listdir(dir_path)
        # id_numbers = [int(''.join([c for c in file if c.isdigit()])) for file in filenames]
    else:
        # id_nums_dict = {}
        filenames_dict = {}
        for subdir in dirs:
            subdir_path = os.path.join(dir_path, subdir)
            filenames = os.listdir(subdir_path)
            filenames_dict[subdir] = filenames

    return filenames_dict

def writeValuesCSV(filenames, csv_name, dest=None):
    """
    For each filename in the dictionary, retrieves the subhalo id number, and gets the groupFirstSub value for that subhalo. Uses this value to determine whether it is a central or satellite subhalo, and assigns it the corresponding flag. Writes these flags to a csv file of filenames and flags.
    """
    centralSatelliteDict = {}

    # For each subhalo, find the group first sub value
    for subdir in filenames:
        subdir_len = len(filenames[subdir])
        count = 1
        for filename in filenames[subdir]:
            id_num = int(''.join([c for c in filename if c.isdigit()]))
            groupFirstSubVal = getGroupFirstSub(id_num)
            # If GroupFirstSub equals the objects id number; the object is central, cent_sat = 0
            if groupFirstSubVal == id_num:
                cent_sat = 0
            # Else the object is a satellite, cent_sat = 1
            elif groupFirstSubVal != id_num:
                cent_sat = 1
            centralSatelliteDict[filename] = cent_sat
            logging.info('{}/{} files in {} Directory'.format(count, subdir_len, subdir))
            count += 1

        # Write the dictionaries to a csv file

    # Write csv files to current dir
            csv_cols = ['Filename', 'Central/Satellite Object']
            with open ((subdir+'_'+csv_name), 'w') as file:
                writer = csv.writer(file)
                writer.writerow(csv_cols)
                for filename in centralSatelliteDict:
                    writer.writerow([filename, centralSatelliteDict[filename]])
                
    return None

# filenames = getFitsNumbers('/Users/Alice/Desktop/Summer Proj/Data', dirs=('Training','Validation', 'Testing')) # For testing 

# filenames = getFitsNumbers('/Volumes/AlicePurdy/Summer Project 2020/TNG Data/sdss/snapnum_099/data') # Using data on Alice's external volume

filenames = getFitsNumbers('/../../../../scratch/gxd743/sdss/snapnum_099/CNN', dirs=('test_dir', 'train_dir', 'val_dir'))

writeValuesCSV(filenames, 'Labels.csv', dest='../../../../anp793')
# /scratch/gxd743/scripts_tests/sorting_test$ 

# # Inspect a single subhalo:
# subhalo = get(subhalos['results'][0]['url'])
# # Full subhalo information: useful keys
#     # primary_flag = 1 indicates that this is the central (i.e. most massive, or "primary") subhalo of this FoF halo.
#     # grnr indicates the FoF group that the subhalo is a member of
#     # Further info in 'related':
#         # parent_halo: gives the parent halo (if it is the central halo, the parent halo will be itself)