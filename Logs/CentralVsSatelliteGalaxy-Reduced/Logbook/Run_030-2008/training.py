# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:48:24 2020

The script defines a Convolutional Neural Network (CNN) and performs training
and validation using specified images. The weights obtained while training
are saved to a checkpoint file to facilitate testing of the CNN.

@author: Giovanni D'Addario & Alice Purdy
"""
#import matplotlib.pyplot as plt
import gc
import numpy as np
import os
import tensorflow as tf
import time

from astropy.io import fits
from cnn import cnn_model
from tensorflow.keras import layers, models, optimizers


start = time.perf_counter() # set a time counter for execution time

# set paths to directories with files for training and validating the CNN
train_data_dir = './train_dir'
val_data_dir = './val_dir'

# get shape of images from first training image (assumed same for all 
    # validation/training images)
file_shape = np.shape(fits.getdata(train_data_dir + '/' + os.listdir(train_data_dir)[0]))

# create 4D arrays to which the images will be assigned: arrays will be fed
    # into the CNN
train_data = np.zeros(shape=(len(os.listdir(train_data_dir)), file_shape[0], 
                             file_shape[1], file_shape[2]))
val_data = np.zeros(shape=(len(os.listdir(val_data_dir)), file_shape[0],
                           file_shape[1], file_shape[2]))

# assign training data to 4D array and create array of training labels
train_label_file = 'train_dir_Labels.csv' # file with file name/ label pairs
train_label_data = np.genfromtxt(train_label_file, delimiter=',',
                                    skip_header=1, dtype=None)
# create array to store labels of the training images
train_labels = np.zeros(shape=(len(train_label_data)))
# loop through file name/ label pairs: assing label to label array and data 
    # from file to 4D data array, guaranteeing that entries with the same index
    # in both arrays correspond to the same file
for index, row in enumerate(train_label_data):
    filename, label = row
    data = fits.getdata(train_data_dir+'/'+filename.decode("utf-8"))
    train_data[index] = data
    train_labels[index] = int(label)
print('Normalisation check:', np.min(train_data), np.max(train_data))  
# assign validation data to 4D array and create array of validation labels
val_label_file = 'val_dir_Labels.csv' # file with file name/ label pairs
val_label_data = np.genfromtxt(val_label_file,  delimiter=',', skip_header=1, dtype=None)
# create array to store labels of the validation images
val_labels = np.zeros(shape=(len(val_label_data)))
# loop through file name/ label pairs: assing label to label array and data 
    # from file to 4D data array, guaranteeing that entries with the same index
    # in both arrays correspond to the same file
for index, row in enumerate(val_label_data):
    filename, label = row
    data = fits.getdata(val_data_dir+'/'+filename.decode("utf-8"))
    val_data[index] = data
    val_labels[index] = int(label)

print('Training data shape: ', np.shape(train_data))

#def cnn_model():
#    """
#    Defines a CNN model.
#    
#    Returns:
#    model : keras model: linear stack of layes
#    """
#    model = models.Sequential()
#    model.add(layers.Conv2D(100, (4,4), activation='relu', 
#                    data_format='channels_first', input_shape=file_shape))
#    model.add(layers.MaxPool2D((2,2), data_format='channels_first'))
#    model.add(layers.Conv2D(200, (4,4), data_format='channels_first', activation='relu'))
#    model.add(layers.MaxPool2D((2,2), data_format='channels_first'))
#    model.add(layers.Conv2D(200, (4,4), data_format='channels_first', activation='relu'))
#    model.add(layers.MaxPool2D((2,2), data_format='channels_first'))
#    model.add(layers.Conv2D(200, (4,4), data_format='channels_first', activation='relu'))
#    model.add(layers.Flatten())
#    model.add(layers.Dense(200, activation='relu'))
#    model.add(layers.Dense(2))    
#    model.compile(optimizer=optimizers.Adam(lr=1e-5), 
#                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#     	
#    return model

#print('model defined')

# create checkpoint to save model during and at the end of training. 
checkpoint_path = "./checkpoint/cp.ckpt" # defines checkpoint path
checkpoint_dir = os.path.dirname(checkpoint_path)

class CustomCallback(tf.keras.callbacks.Callback):
	def on_epoch_end(self, epoch, logs=None):
    		gc.collect()

# create a model instance
model = cnn_model()
print(model.summary())

# create a callback that saves the model's weights
#cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, 
#                                                 save_weights_only=True,
#                                                 verbose=1)
print('callback created')

# train the model with the callback
history = model.fit(train_data, train_labels, epochs=10,
                    validation_data=(val_data, val_labels),
 					callbacks=[CustomCallback()])
print('model trained')

print('Accuracy ', history.history['acc'])
print('Val accuracy: ', history.history['val_acc'])
#fig = plt.figure(figsize=(10,10))
#plt.plot(history.history['acc'], c='blue', label='Training accuracy')
#plt.plot(history.history['val_acc'], c='red', 
#         label = 'Validation accuracy')
#plt.xlabel('Epoch')
#plt.ylabel('Accuracy')
#plt.ylim([0, 1])
#plt.legend(loc='lower right')
#plt.savefig('CentralVsSatellite_Reduced_Accuracy')
#print('complete')
# elapsed time
#print()
#predictions = model.predict(val_data)
#results = []
#for line in predictions:
#	results.append(np.argmax(line))
#print('validation predictions:', results)
#print()
#train_pred = model.predict(train_data)
#train_res = []
#for entry in train_pred:
#	train_res.append(np.argmax(entry))
#print('training predictions:', train_res)
#
elapsed = time.perf_counter() - start
print('\nTraining: elapsed %.3f seconds.' % elapsed)
