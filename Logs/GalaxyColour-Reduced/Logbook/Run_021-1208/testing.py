# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:48:57 2020

The script uses the Convolutional Neural Network (CNN) defined in training.py
and tests it on the selected images.

@author: Giovanni D'Addario & Alice Purdy
"""
import numpy as np
import os
import time

from astropy.io import fits
from training import cnn_model

start = time.perf_counter() # set a time counter for execution time

# set path to directory with files for testing the CNN
test_data_dir = './test_dir'

# get shape of images from first testing image (assumed same for all 
    # testing images)
file_shape = np.shape(fits.getdata(test_data_dir + '/' + os.listdir(test_data_dir)[0]))

# create 4D arrays to which the images will be assigned: arrays will be fed
    # into the CNN
test_data = np.zeros(shape=(len(os.listdir(test_data_dir)), file_shape[0], 
                            file_shape[1], file_shape[2]))

# assign training data to 4D array and create array of training labels
test_label_file = 'test_dir_Labels.csv' # file with file name/ label pairs
test_label_data = np.genfromtxt(test_label_file, delimiter=',', skip_header=1, dtype=None)
# create array to store labels of the testing images
test_labels = np.zeros(shape=(len(test_label_data)))
# loop through file name/ label pairs: assing label to label array and data 
    # from file to 4D data array, guaranteeing that entries with the same index
    # in both arrays correspond to the same file
for index, row in enumerate(test_label_data):
  filename, label = row
  data = fits.getdata(test_data_dir+'/'+filename.decode("utf-8"))
  test_data[index] = data
  test_labels[index] = int(label)


# define the path to the checkpoint as defined in training script
checkpoint_path = "./checkpoint/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
print('checkpoint_found')
# create a new model instance
model = cnn_model()
print('model_found')
# load the weights from training
model.load_weights(checkpoint_path)
print('weights_loaded')
# evaluate the model
loss, acc = model.evaluate(test_data, test_labels, verbose=1)
print("\nRestored model, accuracy: {:5.2f}%".format(100*acc))

# elapsed time
elapsed = time.perf_counter() - start
print('\nTesting: elapsed %.3f seconds.' % elapsed)
