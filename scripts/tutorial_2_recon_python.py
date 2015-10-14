# Import modules
import os
from os.path import join as opj
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.utility import IdentityInterface
from nipype.pipeline.engine import Workflow, Node

# Specify important variables
experiment_dir = '~/nipype_tutorial'           # location of experiment folder
data_dir = opj(experiment_dir, 'data')         # location of data folder
fs_folder = opj(experiment_dir, 'freesurfer')  # location of freesurfer folder
subject_list = ['sub001', 'sub002', 'sub003',
                'sub004', 'sub005', 'sub006',
                'sub007', 'sub008', 'sub009',
                'sub010']                        # subject identifier
T1_identifier = 'struct.nii.gz'                  # Name of T1-weighted image

# Create the output folder - FreeSurfer can only run if this folder exists
os.system('mkdir -p %s' % fs_folder)

# Create the pipeline that runs the recon-all command
reconflow = Workflow(name="reconflow")
reconflow.base_dir = opj(experiment_dir, 'workingdir_reconflow')

# Some magical stuff happens here (not important for now)
infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")
infosource.iterables = ('subject_id', subject_list)
# This node represents the actual recon-all command
reconall = Node(ReconAll(directive='all',
                        #flags='-nuintensitycor- 3T',
                         subjects_dir=fs_folder),
                name="reconall")

# This function returns for each subject the path to struct.nii.gz
def pathfinder(subject, foldername, filename):
    from os.path import join as opj
    struct_path = opj(foldername, subject, filename)
    return struct_path

# This section connects all the nodes of the pipeline to each other
reconflow.connect([(infosource, reconall, [('subject_id', 'subject_id')]),
                   (infosource, reconall, [(('subject_id', pathfinder,
                                             data_dir, T1_identifier),
                                            'T1_files')]),
                   ])

# This command runs the recon-all pipeline in parallel (using 8 cores)
reconflow.run('MultiProc', plugin_args={'n_procs': 8})
