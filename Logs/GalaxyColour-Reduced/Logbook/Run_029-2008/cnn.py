import numpy as np
import os
import tensorflow as tf

from astropy.io import fits
from tensorflow.keras import layers, models, optimizers

train_data_dir = './train_dir'

# get shape of images from first training image (assumed same for all
    # validation/training images)
file_shape = np.shape(fits.getdata(train_data_dir + '/' + os.listdir(train_data_dir)[0]))


def cnn_model():
    """
    Defines a CNN model.

    Returns:
    model : keras model: linear stack of layes
    """
    model = models.Sequential()
    model.add(layers.Conv2D(100, (3,3), activation='relu',
                    data_format='channels_first', input_shape=file_shape))
    model.add(layers.Dropout(rate=0.8))
    model.add(layers.MaxPool2D((2,2), data_format='channels_first'))
    model.add(layers.Conv2D(200, (4,4), data_format='channels_first', activation='relu'))
    model.add(layers.Dropout(rate=0.8))
    model.add(layers.MaxPool2D((2,2), data_format='channels_first'))
    model.add(layers.Conv2D(200, (2,2), data_format='channels_first', activation='relu'))
    model.add(layers.Dropout(rate=0.8))
    model.add(layers.MaxPool2D((2,2), data_format='channels_first'))
    model.add(layers.Conv2D(200, (3,3), data_format='channels_first', activation='relu'))
    model.add(layers.Dropout(rate=0.8))
    model.add(layers.Flatten())
    model.add(layers.Dense(200, activation='relu'))
    model.add(layers.Dropout(rate=0.8))
    model.add(layers.Dense(2, activation='sigmoid'))
    model.compile(optimizer=optimizers.Adam(lr=1e-4),
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

