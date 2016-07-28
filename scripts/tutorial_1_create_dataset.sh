#!/bin/bash

# Specify important variables
ZIP_FILE=~/Downloads/ds102_raw.tgz   #location of download file
TUTORIAL_DIR=~/nipype_tutorial       #location of experiment folder 
TMP_DIR=$TUTORIAL_DIR/tmp            #location of temporary folder
DATA_DIR=$TUTORIAL_DIR/data          #location of data folder

## To download the dataset to the Download folder use the following code:
#wget https://openfmri.s3.amazonaws.com/tarballs/ds102_raw.tgz ~/Downloads

# Unzip ds102 dataset into TMP_DIR
mkdir -p $TMP_DIR
tar -zxvf $ZIP_FILE -C $TMP_DIR

# Copy data of first ten subjects into DATA_DIR
for id in $(seq -w 1 10)
do
    echo "Creating dataset for subject: sub0$id"
    mkdir -p $DATA_DIR/sub0$id
    cp $TMP_DIR/ds102/sub0$id/anatomy/highres001.nii.gz \
       $DATA_DIR/sub0$id/struct.nii.gz

    for session in run001 run002
    do
        cp $TMP_DIR/ds102/sub0$id/BOLD/task001_$session/bold.nii.gz \
           $DATA_DIR/sub0$id/$session.nii.gz
        cp $TMP_DIR/ds102/sub0$id/behav/task001_$session/behavdata.txt \
           $DATA_DIR/sub0$id/behavdata_$session.txt

        for con_id in {1..4}
        do
            cp $TMP_DIR/ds102/sub0$id/model/model001/onsets/task001_$session/cond00$con_id.txt \
               $DATA_DIR/sub0$id/onset_${session}_cond00$con_id.txt
        done
    done
    echo "sub0$id done."
done

# Copy information about demographics, conditions and tasks into DATA_DIR
cp $TMP_DIR/ds102/demographics.txt $DATA_DIR/demographics.txt
cp $TMP_DIR/ds102/models/model001/* $DATA_DIR/.

# Delete the temporary folder
rm -rf $TMP_DIR
