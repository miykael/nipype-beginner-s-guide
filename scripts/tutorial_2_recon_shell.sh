#!/bin/bash

# Specify important variables
export TUTORIAL_DIR=~/nipype_tutorial         #location of experiment folder 
export DATA_DIR=$TUTORIAL_DIR/data            #location of data folder
export SUBJECTS_DIR=$TUTORIAL_DIR/freesurfer  #location of freesurfer folder

for id in {01..10}
do
    echo "working on sub0$id"
    mkdir -p $SUBJECTS_DIR/sub0$id/mri/orig
    mri_convert $DATA_DIR/sub0$id/struct.nii.gz \
                $SUBJECTS_DIR/sub0$id/mri/orig/001.mgz
    recon-all -all -subjid sub0$id #-nuintensitycor-3T
    echo "sub0$id finished"
done
