###
# Import modules
from os.path import join as opj
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.interfaces.spm import (OneSampleTTestDesign, EstimateModel,
                                   EstimateContrast, Threshold)
from nipype.interfaces.utility import IdentityInterface
from nipype.pipeline.engine import Workflow, Node

# Specification to MATLAB
from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/usr/local/MATLAB/R2014a/toolbox/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")


###
# Specify variables
experiment_dir = '~/nipype_tutorial'            # location of experiment folder
output_dir = 'output_fMRI_example_2nd_ants'     # name of 2nd-level output folder
input_dir_norm = 'output_fMRI_example_norm_ants'# name of norm output folder
working_dir = 'workingdir_fMRI_example_2nd_ants'# name of working directory
subject_list = ['sub001', 'sub002', 'sub003',
                'sub004', 'sub005', 'sub006',
                'sub007', 'sub008', 'sub009',
                'sub010']                       # list of subject identifiers
contrast_list = ['con_0001', 'con_0002', 'con_0003',
                 'con_0004', 'ess_0005', 'ess_0006'] # list of contrast identifiers


###
# Specify 2nd-Level Analysis Nodes

# One Sample T-Test Design - creates one sample T-Test Design
onesamplettestdes = Node(OneSampleTTestDesign(),
                         name="onesampttestdes")

# EstimateModel - estimate the parameters of the model
level2estimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      name="level2estimate")

# EstimateContrast - estimates simple group contrast
level2conestimate = Node(EstimateContrast(group_contrast=True),
                         name="level2conestimate")
cont1 = ['Group', 'T', ['mean'], [1]]
level2conestimate.inputs.contrasts = [cont1]


###
# Specify 2nd-Level Analysis Workflow & Connect Nodes
l2analysis = Workflow(name='l2analysis')
l2analysis.base_dir = opj(experiment_dir, working_dir)

# Connect up the 2nd-level analysis components
l2analysis.connect([(onesamplettestdes, level2estimate, [('spm_mat_file',
                                                          'spm_mat_file')]),
                    (level2estimate, level2conestimate, [('spm_mat_file',
                                                          'spm_mat_file'),
                                                         ('beta_images',
                                                          'beta_images'),
                                                         ('residual_image',
                                                          'residual_image')]),
                    ])


###
# Input & Output Stream

# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['contrast_id']),
                  name="infosource")
infosource.iterables = [('contrast_id', contrast_list)]

# SelectFiles - to grab the data (alternative to DataGrabber)
con_file = opj(input_dir_norm, 'warp_complete', 'sub*', 'warpall*',
               '{contrast_id}_trans.nii')
templates = {'cons': con_file}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_contrast_id_', '')]
datasink.inputs.substitutions = substitutions

# Connect SelectFiles and DataSink to the workflow
l2analysis.connect([(infosource, selectfiles, [('contrast_id',
                                                'contrast_id')]),
                    (selectfiles, onesamplettestdes, [('cons', 'in_files')]),
                    (level2conestimate, datasink, [('spm_mat_file',
                                                    'contrasts.@spm_mat'),
                                                   ('spmT_images',
                                                    'contrasts.@T'),
                                                   ('con_images',
                                                    'contrasts.@con')]),
                    ])


###
# Run Workflow
l2analysis.write_graph(graph2use='colored')
l2analysis.run('MultiProc', plugin_args={'n_procs': 8})
