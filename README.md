# Characterising galaxies with Convolutional Neural Networks (CNNs)

This repository contains the scripts developed during a project on the application of Convolutional Neural Networks (CNN) to images from the IllustrisTNG100 cosmological simulation; the objective was to assess the suitablity of this deep learning method for studies in galaxy formation and evolution. As part of this project, two studies were completed; the first was a classification of galaxies as central or satellite galaxies while the second study was a red or blue colour classification. Although the neural network included in this repository may be tuned to these problems, the entirety of the scripts of which this repository is comprised should allow for future extensions with other studies.

The code was run on Python 3.6.8: other versions were not tested. Other than standard ones, the following libraries and versions were used:

astropy: version 3.1.1\
numpy: version 1.14.2\
tensorflow: version 1.9.0 .

These are not the most recent versions. The documentation for tensorflow 1.9 can be found [here](https://github.com/tensorflow/docs/tree/r1.9/site/en/api_docs); as of the time of writing, the most recent version is 2.3.0, for which the documentation can be found [here](https://www.tensorflow.org/api_docs/python/tf).

## Structure of the repository

The repository is structured as follows:

- **cnn.py** defines the CNN.
- The CNN is trained by running **training.py**; within this script, images (fits files in the case of IllustrisTNG simulations) for training and validating the CNN are loaded from the specified training and validation directories, while the corresponding labels are taken from csv files. This script creates a callback in a *checkpoint* directory; the weights obtained during training are saved here.
- **testing.py** imports the images used to test the CNN from the testing directory and the corresponding labels from a csv file. The weights obtained in training are loaded from the *checkpoint* directory; the network is subsequently tested.
- Prior to being used in training, validating and testing the CNN, images from the IllustrisTNG simulations can be processed so that they become similar to data from observations. This can be done with the scripts within the *Image_Processing* directory. **Image_Processing.py** convolves images with a point-spread function, adds random Gaussian noise and ensures that the pixel values are between 0 and 1. **run.sh** allows the user to specify parameters which are then fed into **Image_Processing.py**, including the median seeing of the observational data which is being mimicked, as well as the mean and standard deviation of the distribution from which the noise added to the image is sampled.
- The *Miscellaneous_Scripts* directory contains some utility functions which may be useful for preparing the training, validation and testing images and labels but that can othewise be ignored. **Sort_CNN_data.sh** creates training, validation and testing directories and sorts all of the (processed) fits files into them. The sorting process is random; currently about 80% of the files are sent to the training directory, while the other 20% are split between the validation and testing directories. **csv_checker.py**
checks that the filenames of the files in the training, validation and testing directories match those of the entries in the corresponding csv files with the labels.
- The *Logs* directory was used to keep track of runs used to debug the CNN, training and testing processes or to improve the performance of the CNN. Within this directory there are five subdirectories, three for the central or satellite galaxy classification and two for the red or blue colour classification. Each of these five directories has a directory for each of the runs that were carried out; the latter contains a brief description of the changes made in between successive runs, any scripts used (for a few runs this is not the case) as well as any useful results.
