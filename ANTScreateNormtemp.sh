#!/bin/bash

#Define environment parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#specify where ANTS is installed
export PATH=/software/ANTS:$PATH
export ANTSPATH=/software/ANTS/

#If you want to grab the scull stripped anatomical images
# from your freesurfer folder uncomment the following part
###export FREESURFER_HOME=/software/Freesurfer/5.1.0
###source $FREESURFER_HOME/SetUpFreeSurfer.sh


#Define experiment specific parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#specify list of subjects
subjectList='subject1 subject2 subject3'

#specify folder names
experimentDir=~SOMEPATH/experiment            #parent folder
inputDir=$experimentDir/AnatomicalImages      #folder containing anatomical images
normtempOutDir=$experimentDir/data            #where the normtemp should be stored at
workingDir=$experimentDir/normtemp_workingDir #temporary dir

#specify parameters for buildtemplateparallel.sh
#compulsory arguments
ImageDimension=3
OutPrefix='PREFIX'

#optional arguments
ParallelMode=2
GradientStep='0.25'
IterationLimit=4
Cores=2
MaxIteration=30x90x20
N3Correct=1
Rigid=0
MetricType='PR'
TransformationType='GR'


#Write the main script
#~~~~~~~~~~~~~~~~~~~~~

#If not created yet, let's create a new output folder
if [ ! -d $workingDir ]
then
   mkdir -p $workingDir
fi

#go into the folder where the script should be run
cd $workingDir

#Let's get the input, the subject specific anatomical images. You might
# have to alter this part a bit to satisfy the structure of your system
#Assuming that the name of your subject specific anatomical image is
# 'subjectname.nii' the loop to grab the files would look something like this

for subj in $subjectList
do
   cp $inputDir/$subj.nii $workingDir/$subj"_antsT1.nii"
done #subj done


#If you want to use your skull stripped freesurfer images, use the following loop instead
# of the code above. Assuming that ``inputDir=$experimentDir/freesurfer_data`` is specified.

####This loop grabs your skull stripped anatomical files from your freesurfer folder
###for subj in $subjectList
###do
###   cmd="mri_convert $inputDir/$subj/mri/brain.mgz $workingDir/$subj_antsT1.nii"
###   echo $cmd #state the command
###   eval $cmd #execute the command
###done #subj done


#assemble the command for the script from the input parameters defined above
cmd="bash $ANTSPATH/buildtemplateparallel.sh -d $ImageDimension -c $ParallelMode \
     -g $GradientStep -i $IterationLimit -j $Cores -m $MaxIteration -n $N3Correct  \
     -r $Rigid -s $MetricType -t $TransformationType -o $OutPrefix *_antsT1.nii"

echo $cmd #state the command
eval $cmd #execute the command


#Delete unnecessary output (optional)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#move the normtemplate to a safe place
lastIterationFolder=${TransformationType}_iteration_$(($IterationLimit-1))
cmd="mv $workingDir/$lastIterationFolder/${OutPrefix}template.nii.gz \
        $normtempOutDir/normtemp.nii.gz"
echo $cmd #state the command
eval $cmd #execute the command

#delete the workingdir
rm -rf $workingDir

