###
# Import modules
from os.path import join as opj
from nipype.interfaces.spm import SliceTiming, Realign, Smooth
from nipype.interfaces.utility import IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.algorithms.rapidart import ArtifactDetect
from nipype.algorithms.misc import Gunzip
from nipype.pipeline.engine import Workflow, Node


###
# Specify variables
experiment_dir = '~/nipype_tutorial'             # location of experiment folder
subject_list = ['sub001', 'sub002', 'sub003',
                'sub004', 'sub005', 'sub006',
                'sub007', 'sub008', 'sub009',
                'sub010']                        # list of subject identifiers
session_list = ['run001', 'run002']              # list of session identifiers

output_dir = 'output_firstSteps'          # name of output folder
working_dir = 'workingdir_firstSteps'     # name of working directory

number_of_slices = 40                     # number of slices in volume
TR = 2.0                                  # time repetition of volume
smoothing_size = 8                        # size of FWHM in mm


###
# Specify Nodes

# Gunzip - unzip functional
gunzip = Node(Gunzip(), name="gunzip")

# Slicetiming - correct for slice wise acquisition
interleaved_order = range(1,number_of_slices+1,2) + range(2,number_of_slices+1,2)
sliceTiming = Node(SliceTiming(num_slices=number_of_slices,
                               time_repetition=TR,
                               time_acquisition=TR-TR/number_of_slices,
                               slice_order=interleaved_order,
                               ref_slice=2),
                   name="sliceTiming")

# Realign - correct for motion
realign = Node(Realign(register_to_mean=True),
               name="realign")

# Artifact Detection - determine which of the images in the functional series
#   are outliers. This is based on deviation in intensity or movement.
art = Node(ArtifactDetect(norm_threshold=1,
                          zintensity_threshold=3,
                          mask_type='spm_global',
                          parameter_source='SPM'),
           name="art")

# Smooth - to smooth the images with a given kernel
smooth = Node(Smooth(fwhm=smoothing_size),
              name="smooth")


###
# Specify Workflows & Connect Nodes

# Create a preprocessing workflow
preproc = Workflow(name='preproc')
preproc.base_dir = opj(experiment_dir, working_dir)

# Connect all components of the preprocessing workflow
preproc.connect([(gunzip, sliceTiming, [('out_file', 'in_files')]),
                 (sliceTiming, realign, [('timecorrected_files', 'in_files')]),
                 (realign, art, [('realigned_files', 'realigned_files'),
                                 ('mean_image', 'mask_file'),
                                 ('realignment_parameters',
                                  'realignment_parameters')]),
                 (realign, smooth, [('realigned_files', 'in_files')]),
                 ])


###
# Input & Output Stream

# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id',
                                            'session_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list),
                        ('session_id', session_list)]

# SelectFiles
templates = {'func': 'data/{subject_id}/{session_id}.nii.gz'}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

# Datasink
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_subject_id', ''),
                 ('_session_id_', '')]
datasink.inputs.substitutions = substitutions

# Connect SelectFiles and DataSink to the workflow
preproc.connect([(infosource, selectfiles, [('subject_id', 'subject_id'),
                                            ('session_id', 'session_id')]),
                 (selectfiles, gunzip, [('func', 'in_file')]),
                 (realign, datasink, [('mean_image', 'realign.@mean'),
                                      ('realignment_parameters',
                                       'realign.@parameters'),
                                      ]),
                 (smooth, datasink, [('smoothed_files', 'smooth')]),
                 (art, datasink, [('outlier_files', 'art.@outliers'),
                                  ('plot_files', 'art.@plot'),
                                  ]),
                 ])


###
# Run Workflow
preproc.write_graph(graph2use='flat')
preproc.run('MultiProc', plugin_args={'n_procs': 8})
