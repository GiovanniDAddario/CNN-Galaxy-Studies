#!/bin/bash

# create three directories if not already present
if [ ! -d "test_dir" ];
then
	mkdir test_dir
fi
if [ ! -d "train_dir" ];
then
        mkdir train_dir
fi
if [ ! -d "val_dir" ];
then
        mkdir val_dir
fi 

# for index, file in enumerate(len(directory)): if index < 80% len(directory) send to train, if 80-90 % send to validation else test

FILES=./*.txt
range=10

for f in $FILES
do
	number=$RANDOM
	sort_number=$(($number%$range))
	if (($sort_number >= 0 && $sort_number <= 7)); then
		mv $f train_dir 
	elif (($sort_number == 8)); then
		mv $f val_dir
	else 
		mv $f test_dir
	fi
done

