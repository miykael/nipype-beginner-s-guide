###
# Import modules
from os.path import join as opj
from nipype.interfaces.spm import Normalize12
from nipype.interfaces.utility import IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.algorithms.misc import Gunzip
from nipype.pipeline.engine import Workflow, Node, MapNode

# Specification to MATLAB
from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/usr/local/MATLAB/R2014a/toolbox/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")


###
# Specify variables
experiment_dir = '~/nipype_tutorial'         # location of experiment folder
input_dir_1st = 'output_fMRI_example_1st'    # name of 1st-level output folder
output_dir = 'output_fMRI_example_norm_spm'  # name of norm output folder
working_dir = 'workingdir_fMRI_example_norm_spm'  # name of working directory
subject_list = ['sub001', 'sub002', 'sub003',
                'sub004', 'sub005', 'sub006',
                'sub007', 'sub008', 'sub009',
                'sub010']                    # list of subject identifiers

# location of template in form of a tissue probability map to normalize to
template = '/usr/local/MATLAB/R2014a/toolbox/spm12/tpm/TPM.nii'


###
# Specify Normalization Nodes

# Gunzip - unzip the structural image
gunzip_struct = Node(Gunzip(), name="gunzip_struct")

# Gunzip - unzip the contrast image
gunzip_con = MapNode(Gunzip(), name="gunzip_con",
                     iterfield=['in_file'])

# Normalize - normalizes functional and structural images to the MNI template
normalize = Node(Normalize12(jobtype='estwrite',
                             tpm=template,
                             write_voxel_sizes=[1, 1, 1]),
                 name="normalize")

###
# Specify Normalization-Workflow & Connect Nodes
normflow = Workflow(name='normflow')
normflow.base_dir = opj(experiment_dir, working_dir)

# Connect up ANTS normalization components
normflow.connect([(gunzip_struct, normalize, [('out_file', 'image_to_align')]),
                  (gunzip_con, normalize, [('out_file', 'apply_to_files')]),
                  ])


###
# Input & Output Stream

# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]

# SelectFiles - to grab the data (alternative to DataGrabber)
anat_file = opj('data', '{subject_id}', 'struct.nii.gz')
con_file = opj(input_dir_1st, 'contrasts', '{subject_id}',
                        '_mriconvert*/*_out.nii.gz')
templates = {'anat': anat_file,
             'con': con_file,
             }
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_subject_id_', '')]
datasink.inputs.substitutions = substitutions

# Connect SelectFiles and DataSink to the workflow
normflow.connect([(infosource, selectfiles, [('subject_id', 'subject_id')]),
                  (selectfiles, gunzip_struct, [('anat', 'in_file')]),
                  (selectfiles, gunzip_con, [('con', 'in_file')]),
                  (normalize, datasink, [('normalized_files',
                                          'normalized.@files'),
                                         ('normalized_image',
                                          'normalized.@image'),
                                         ('deformation_field',
                                          'normalized.@field'),
                                         ]),
                  ])

###
# Run Workflow
normflow.write_graph(graph2use='colored')
normflow.run('MultiProc', plugin_args={'n_procs': 8})
