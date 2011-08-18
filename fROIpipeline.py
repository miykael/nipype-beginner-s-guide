"""
Import modules
"""

import os                                    # system functions
import nipype.interfaces.freesurfer as fs    # freesurfer
import nipype.interfaces.io as nio           # i/o routines
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.interfaces.fsl as fsl          # fsl module


"""
Define experiment specific parameters
"""

#to better access the parent folder of the experiment
experiment_dir = '~SOMEPATH/experiment'

#dirnames for functional ROI and of level1 datasink
fROIOutput = 'fROI_output'      #name of fROI datasink
l1contrastDir = 'level1_output' #name of first level datasink

#list of subjectnames
subjects = ['subject1','subject2','subject3']

#list of contrastnumbers the pipeline should consider
contrasts = [1,2,3,4,5]


"""
Define fROI specific parameters
"""

#define the coordination of the point of interest
centerOfROI = [179,129,107]

#define the radius of the sphere of interest
radius = 20

#calculates the beginning corner of the cubic ROI
corner = [centerOfROI[0]-radius,
          centerOfROI[1]-radius,
          centerOfROI[2]-radius]


"""
Definition of Nodes
"""

#Node: IdentityInterface - to iterate over subjects and contrasts
inputnode = pe.Node(interface=util.IdentityInterface(fields=['subject_id','contrast_id']),
                    name='inputnode')
inputnode.iterables = [('subject_id', subjects),
                       ('contrast_id', contrasts)]

#Node: DataGrabber - To grab the input data
datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id','contrast_id'],
                                               outfields=['contrast']),
                     name = 'datasource')
datasource.inputs.base_directory = experiment_dir + '/results/' + l1contrastDir
datasource.inputs.template = 'norm%s/%s/%s_%04d_ants.nii'
info = dict(contrast = [['cons','subject_id','con','contrast_id']])
datasource.inputs.template_args = info

#Node: ImageMaths - to create the cubic ROI with value 1
cubemask = pe.Node(interface=fsl.ImageMaths(),name="cubemask")
cubeValues = (corner[0],radius*2,corner[1],radius*2,corner[2],radius*2)
cubemask.inputs.op_string = '-mul 0 -add 1 -roi %d %d %d %d %d %d 0 1'%cubeValues
cubemask.inputs.out_data_type = 'float'
pathValues = (subjects[0],contrasts[0])
cubemask.inputs.in_file = '~SOMEPATH/experiment/normcons/%s/con_%04d_ants.nii'%pathValues

#Node: ImageMaths - to transform the cubic ROI to a spherical ROI
spheremask = pe.Node(interface=fsl.ImageMaths(),name="spheremask")
spheremask.inputs.op_string = '-kernel sphere %d -fmean -thr 0.5 -bin'%radius
spheremask.inputs.out_data_type = 'float'

#Node: ImageMaths - to mask the spherical ROI with a subject specific T-map
tmapmask = pe.Node(interface=fsl.ImageMaths(),name="tmapmask")
tmapmask.inputs.out_data_type = 'float'

#function to add the thresholded group T-map to op_string
def groupTMapPath(contrast_id):
    experiment_dir = '~SOMEPATH/experiment'
    op_string = '-mul %s/results/level2_output/l2vol_contrasts_thresh/_con_%d/spmT_0001_thr.hdr -bin'
    return op_string%(experiment_dir,contrast_id)

#Node: SegStats - to extract the statistic from a given segmentation
segstat = pe.Node(interface=fs.SegStats(),name='segstat')

#Node: Datasink - Create a datasink node to store important outputs
datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = experiment_dir + '/results'
datasink.inputs.container = fROIOutput


"""
Definition of functional ROI workflow
"""

#Initiation of the fROI extraction workflow
fROIflow = pe.Workflow(name='fROIflow')
fROIflow.base_dir = experiment_dir + '/results/workingdir_fROI'

#Connect up all components
fROIflow.connect([(cubemask, spheremask,[('out_file','in_file')]),
                  (spheremask, tmapmask,[('out_file','in_file')]),
                  (inputnode, tmapmask,[(('contrast_id',groupTMapPath),
                                         'op_string')
                                        ]),
                  (inputnode, datasource,[('subject_id','subject_id'),
                                          ('contrast_id','contrast_id')
                                          ]),
                  (tmapmask, segstat,[('out_file','segmentation_file')]),
                  (datasource, segstat,[('contrast','in_file')]),
                  (segstat, datasink,[('summary_file','@statistic')]),
                  ])
   

"""
Run the pipeline and generate the graph
"""

fROIflow.write_graph(graph2use='flat')
fROIflow.run(plugin='MultiProc', plugin_args={'n_procs' : 4})


"""
Summarizing the output in a cvs-file
"""

#creates the big list and its header
output = []
output.append(['coordinations:',centerOfROI,'radius:',radius])

#iterate over contrasts
for contrast in contrasts:

    #creates header for each contrast
    contrast = str(contrast)
    output.append(['contrast:',contrast])
   
    #iterate over subjects
    for subject in subjects:

        #specify path to fROI datasink for each variation of segmentation
        path2fROIOut = experiment_dir+'/results/'+fROIOutput + '/'
        path2Sumfile = '_contrast_id_'+contrast+'_subject_id_'+subject
        statFile = path2fROIOut + path2Sumfile + '/summary.stats'
   
        #extract the data from the output summary files
        dataFile = open(statFile, 'r')
        data = dataFile.readlines()
        dataFile.close()

        #add value of functional region   
        output.append([subject,data[-1].split()[5]])
   
    #add an empty line at the end of a contrast summary
    output.append([])
   
#store output into a cvs-file
f = open(path2fROIOut+'/fROI_spherical'+str(centerOfROI)+'_%s_result.csv'%radius,'wb')
import csv
outputFile = csv.writer(f)
for line in output:
    outputFile.writerow(line)
f.close()

