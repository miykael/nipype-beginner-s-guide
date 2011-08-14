"""
Import modules
"""

import os                                    # system functions
import nipype.interfaces.freesurfer as fs    # freesurfer
import nipype.interfaces.io as nio           # i/o routines
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine


"""
Define experiment specific parameters
"""

#to better access the parent folder of the experiment
experiment_dir = '~SOMEPATH/experiment'

# Tell freesurfer what subjects directory to use
subjects_dir = experiment_dir + '/freesurfer_data'
fs.FSCommand.set_default_subjects_dir(subjects_dir)

#dirnames for anatomical ROI pipeline
aROIOutput = 'aROI_output'         #location and name of aROI datasink
l1contrastDir = 'level1_output'    #name of first level datasink

#list of subjectnames
subjects = ['subject1', 'subject2', 'subject3']

#list of contrastnumbers the pipeline should consider
contrasts = ['01','02','03','04','05']

#name of the first session from the first level pipeline
nameOfFirstSession = 'func1'


"""
Define aROI specific parameters
"""

#Specification of the regions from the original and 
#the 2009 segmentation version of the FreeSurfer Color Table
ROIregionsorig = ['11','50','12','51','1007','2007','1022','2022']
ROIregions2009 = ['11134','12134']
      

"""
Define nodes
"""

#Node: IdentityInterface - to iterate over subjects and contrasts
inputnode = pe.Node(interface=util.IdentityInterface(fields=['subject_id','contrast_id']),
                    name='inputnode')
inputnode.iterables = [('subject_id', subjects),
                       ('contrast_id', contrasts)]


#Node: DataGrabber - to grab the input data
datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id','contrast_id'],
                                               outfields=['contrast','bb_id']),
                     name = 'datasource')
datasource.inputs.base_directory = experiment_dir + '/results/' + l1contrastDir
datasource.inputs.template = '%s/_subject_id_%s/%s%s%s'

info = dict(contrast = [['vol_contrasts','subject_id','con_00','contrast_id','.img']],
            bb_id = [['bbregister','subject_id','meana'+nameOfFirstSession+'_bbreg_',
                      'subject_id','.dat']])
   
datasource.inputs.template_args = info

#Node: FreeSurferSource - to grab FreeSurfer files from the recon-all process
fssource = pe.Node(interface=nio.FreeSurferSource(),name='fssource')
fssource.inputs.subjects_dir = subjects_dir

#Node: MRIConvert - to convert files from FreeSurfer format into nifti format
MRIconversion = pe.Node(interface=fs.MRIConvert(),name='MRIconversion')
MRIconversion.inputs.out_type = 'nii'

#Node: ApplyVolTransform - to transform contrasts into anatomical space
#                          creates 'con_*.anat.bb.mgh' files
transformation = pe.Node(interface=fs.ApplyVolTransform(),name='transformation')
transformation.inputs.fs_target = True
transformation.inputs.interp = 'nearest'


#Node: SegStatsorig - to extract specified regions from the original part of the color table
segmentationorig = pe.Node(interface=fs.SegStats(),name='segmentationorig')
segmentationorig.inputs.color_table_file = '/software/Freesurfer/5.1.0/FreeSurferColorLUT.txt'
segmentationorig.inputs.segment_id = ROIregionsorig #original segmentation ids

#Node: SegStats2009 - to extract specified regions from the 2009 part of the color table
segmentation2009 = pe.Node(interface=fs.SegStats(),name='segmentation2009')
segmentation2009.inputs.color_table_file = '/software/Freesurfer/5.1.0/FreeSurferColorLUT.txt'
segmentation2009.inputs.segment_id = ROIregions2009 #2009 segmentation ids

def getVersion(in_file, version):
    if version == 0:
       return in_file[0]
    else:
       return in_file[1]

#Node: Datasink - Creates a datasink node to store important outputs
datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = experiment_dir + '/results'
datasink.inputs.container = aROIOutput


"""
Definition of anatomical ROI workflow
"""

#Initiation of the ROI extraction workflow
aROIflow = pe.Workflow(name='aROIflow')
aROIflow.base_dir = experiment_dir + '/results/workingdir_aROI'

#Connect up all components
aROIflow.connect([(inputnode, datasource,[('subject_id','subject_id'),
                                          ('contrast_id','contrast_id'),
                                          ]),
                  (inputnode, fssource,[('subject_id','subject_id')]),
                  (fssource, segmentationorig,[(('aparc_aseg',getVersion,0),
                                                 'segmentation_file')]),
                  (fssource, segmentation2009,[(('aparc_aseg',getVersion,1),
                                                 'segmentation_file')]),
                  (datasource, MRIconversion,[('contrast','in_file')]),
                  (MRIconversion, transformation,[('out_file','source_file')]),
                  (datasource, transformation,[('bb_id','reg_file')]),
                  (transformation, segmentationorig,[('transformed_file',
                                                      'in_file')]),
                  (transformation, segmentation2009,[('transformed_file',
                                                      'in_file')]),
                  (segmentationorig, datasink,[('summary_file', 'segstatorig')]),
                  (segmentation2009, datasink,[('summary_file', 'segstat2009')]),
                  ])
   

"""
Run pipeline and generate graph
"""

aROIflow.write_graph(graph2use='flat')
aROIflow.run(plugin='MultiProc', plugin_args={'n_procs' : 2})


"""
Summarizing the output in a cvs-file
"""
  
#iterate over contrasts and create a cvs-file for each
for contrast in contrasts:

    #creates a list with an empty entry for each segmentation id
    output = []
    for i in range(15000):
        output.append([i,None])

    #to keep track of added subjects
    subjectNumber = 1

    path2aROIOut = experiment_dir+'/results/'+aROIOutput

    #iterate over subjects and entering values into output
    for subject in subjects:
   
        #specify path to aROI datasink for each variaton of segmentation
        path2Sumfile = '_contrast_id_'+contrast+'_subject_id_'+subject+'/summary.stats'
        statsFileorig = path2aROIOut+'/segstatorig/'+path2Sumfile
        statsFile2009 = path2aROIOut+'/segstat2009/'+path2Sumfile
   
        #extract the data from the output summary files
        dataFile = open(statsFileorig, 'r')
        dataorig = dataFile.readlines()
        dataFile.close()
        dataFile = open(statsFile2009, 'r')
        data2009 = dataFile.readlines()
        dataFile.close()
       
        #function to check where the data starts
        def findStartOfData(datafile):
            for line in range(100):
                if datafile[line][0] != '#':
                   return line
       
        #get data and store it in tempresult
        tempresult = []
   
        for line in range(len(dataorig)):
            if line < findStartOfData(dataorig):
                pass
            else:
                temp = dataorig[line].strip('\n').split()
                tempresult.append([int(temp[1]),temp[4],float(temp[5])])

        for line in range(len(data2009)):
            if line < findStartOfData(data2009):
                pass
            else:
                temp = data2009[line].strip('\n').split()
                tempresult.append([int(temp[1]),temp[4],float(temp[5])])
   
        tempresult.sort()
   
        result = []

        for line in range(len(tempresult)):
            #pass if region has already been added
            if line > 0 and tempresult[line] == tempresult[line-1]:
                pass
            else:
                result.append(tempresult[line])
   
        for ROI in result:
            #if id wasn't extracted before, adds name of id to row
            if output[ROI[0]][1] == None:
               output[ROI[0]][1] = ROI[1]
            #adds value of id into row
            output[ROI[0]].append(ROI[2])
   
        #if no value for an id was entered for a subject
        #   the value 0.0 gets added
        for ROI in output:
            if len(ROI) < subjectNumber+2:
               ROI.append(0.0)
   
        subjectNumber += 1
   
    #adds labels to the first row of the output
    output.insert(0,['SegId','StructName'])
    output[0].extend(subjects)

    #adds segment if it was extracted
    output = [ROI for ROI in output if ROI[1] != None]
   
    #define name of the output csv-file
    summaryFileName = 'aROI_'+contrast+'.csv'

    #store output into a cvs-file
    f = open(path2aROIOut+'/'+summaryFileName,'wb')
    import csv
    outputFile = csv.writer(f)
    for line in output:
        outputFile.writerow(line)
    f.close()
