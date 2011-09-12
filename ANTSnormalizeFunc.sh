#!/bin/bash

#Define environment parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#specify where ANTS is installed
export PATH=/software/ANTS:$PATH
export ANTSPATH=/software/ANTS/

#specify where FreeSurfer is installed
export FREESURFER_HOME=/software/Freesurfer/5.1.0
source $FREESURFER_HOME/SetUpFreeSurfer.sh


#Define experiment specific parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#specify list of subjects
subjectList='subject1 subject2 subject3'

#specify list of contrasts. (empty = all contrasts will be normalized
contrastList=''

#specify folder names
experimentDir=~SOMEPATH/experiment               #parent folder
inputDir=$experimentDir/result/vol_contrasts     #folder containing functional images
templateName=$experimentDir/data/normtemp.nii.gz #path to and name of normtemplate
normAnatDir=$experimentDir/normAnat              #outputdir of normalized T1 images
funcOutDir=$inputDir                             #outputdir of normalized functional images

#Do you want to overwrite existing output files? (1 = yes, 0 = no)
overwrite=0


#Write the main script
#~~~~~~~~~~~~~~~~~~~~~

#If not created yet, let's create a new output folder
if [ ! -d $funcOutDir ]
then
   mkdir -p ${funcOutDir}
fi

#go through all subjects
for subj in $subjectList
do

   #If not created yet, let's create a subject specific folder
   if [ ! -d $funcOutDir/$subj ]
   then
      mkdir ${funcOutDir}/${subj}
   fi

   #If not created yet, let's create a folder for the normalized cons
   if [ ! -d $funcOutDir/$subj/normcons ]
   then
      mkdir -p $funcOutDir/$subj/normcons
   fi

   #If not created yet, let's create a folder for the normalized spmTs
   if [ ! -d $funcOutDir/$subj/normspmTs ]
   then
      mkdir -p $funcOutDir/$subj/normspmTs
   fi

   #checks if all necessary output of antsIntroduction.sh exists
   if [ ! -e $normAnatDir/${subj}deformed.nii.gz ] || [ ! -e $normAnatDir/${subj}Warpxvec.nii.gz ] || [ ! -e $normAnatDir/${subj}Warpyvec.nii.gz ] || [ ! -e $normAnatDir/${subj}Warpzvec.nii.gz ] || [ ! -e $normAnatDir/${subj}Affine.txt ]
   then
      echo -e "NOTICE: A necessary ANTS output file of subject ${subj} was not found.\
                       Skipping to next subject."
      continue
   fi

   #create a list that contains numbers of contrasts if not specified above
   if [ $contrastList=='' ]
   then
      contrast=`ls $inputDir/$subj/con_*.img`
      con_ID=''
      for con in $contrast
      do
         length=${#con}
         ID=`echo $con | cut -c $(($length-7))-$(($length-4))`
         con_ID=${con_ID}' '$ID
      done #con done
   else
      con_ID=$contrastList
   fi

   #go through all contrasts
   for ID in $con_ID
   do

      #to normalize 'con' and 'spmT' files
      for type in con spmT
      do

         #specify input image and name of normalized output image
         InImg=$inputDir/$subj/${type}"_"${ID}.img
         OutNii=$funcOutDir/$subj/norm${type}"s/ants_"${type}"_"${ID}.nii

         #checks if input image exists
         if [ ! -e $InImg ]
         then
            echo -e "NOTICE: Cannot find ${type}_${ID}.img of subject ${subj}"
            continue
         fi

         #contrast will be normalized if contrast wasn't normalized yet
         # or if overwrite was set to 1=yes
         if [ ! -e $OutNii ] || [ $overwrite == 1 ]
         then

            #assemble the command for the conversion of img to nii
            cmd1="mri_convert "${InImg}" "${OutNii}

            #assemble the command for the normalization
            cmd2="WarpImageMultiTransform 3 ${OutNii} ${OutNii} \
                     -R $normAnatDir/${subj}deformed.nii.gz \
                     $normAnatDir/${subj}Warp.nii.gz \
                     $normAnatDir/${subj}Affine.txt"
            eval $cmd1 #execute cmd1
            eval $cmd2 #execute cmd2
         else
            echo -e "NOTICE: ${OutNii} already exists. Skipping to next contrast."
         fi

      done #type done
   done #ID done
done #subj done

