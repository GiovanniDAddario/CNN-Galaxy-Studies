'''Script to check if GetFileLabels.py has worked correctly: verifies that filenames
in training/testing/validation directory match those in corresponding csv file'''
import os
import pandas as pd

# specify a directory and the corresponding csv file
dir = './train_dir'
csv_file = 'train_dir_Labels.csv'
colnames = ['Filename', 'Central/Satellite Object'] # column names in csv file
# open csv file and save filenames (first column) to list
data = pd.read_csv(csv_file, names=colnames, skiprows=1)
filenames = data.Filename.tolist()

print('Files in directory (list):', len(filenames)) # check number of files in csv
print('Files in csv (list):', len(os.listdir(dir))) # check number of files in specified
	# directory, should match the line above
# convert the lists of files (in csv  and specified directory) to sets
directory_files = set(os.listdir(dir))
csv_filename = set(filenames)
# check if the files in the two exactly match. As these are sets, repeated
	# files are removed --> use the print statements above for lists too
print('Are the files equal?', directory_files == csv_filename) 
# check how many elements are in the two sets
print('Files in directory, csv (sets): ', len(directory_files), len(csv_filename))
# check the intersection of the two sets
print('Files in both: ', len(directory_files.intersection(csv_filename)))
# check how many files are in one set but not the other
print('Difference between the two: ', len(csv_filename.difference(directory_files)))
