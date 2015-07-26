###
# Import modules
from os.path import join as opj
from nipype.interfaces.afni import Despike
from nipype.interfaces.freesurfer import (BBRegister, ApplyVolTransform,
                                          Binarize, MRIConvert, FSCommand)
from nipype.interfaces.spm import (SliceTiming, Realign, Smooth, Level1Design,
                                   EstimateModel, EstimateContrast)
from nipype.interfaces.utility import Function, IdentityInterface
from nipype.interfaces.io import FreeSurferSource, SelectFiles, DataSink
from nipype.algorithms.rapidart import ArtifactDetect
from nipype.algorithms.misc import TSNR
from nipype.algorithms.modelgen import SpecifySPMModel
from nipype.pipeline.engine import Workflow, Node, MapNode

# MATLAB - Specify path to current SPM and the MATLAB's default mode
from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/usr/local/MATLAB/R2014a/toolbox/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")

# FreeSurfer - Specify the location of the freesurfer folder
fs_dir = '~/nipype_tutorial/freesurfer'
FSCommand.set_default_subjects_dir(fs_dir)


###
# Specify variables
experiment_dir = '~/nipype_tutorial'          # location of experiment folder
subject_list = ['sub001', 'sub002', 'sub003',
                'sub004', 'sub005', 'sub006',
                'sub007', 'sub008', 'sub009',
                'sub010']                     # list of subject identifiers
output_dir = 'output_fMRI_example_1st'        # name of 1st-level output folder
working_dir = 'workingdir_fMRI_example_1st'   # name of 1st-level working directory

number_of_slices = 40                         # number of slices in volume
TR = 2.0                                      # time repetition of volume
fwhm_size = 6                                 # size of FWHM in mm


###
# Specify Preprocessing Nodes

# Despike - Removes 'spikes' from the 3D+time input dataset
despike = MapNode(Despike(outputtype='NIFTI'),
                  name="despike", iterfield=['in_file'])

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

# TSNR - remove polynomials 2nd order
tsnr = MapNode(TSNR(regress_poly=2),
               name='tsnr', iterfield=['in_file'])

# Artifact Detection - determine which of the images in the functional series
#   are outliers. This is based on deviation in intensity or movement.
art = Node(ArtifactDetect(norm_threshold=1,
                          zintensity_threshold=3,
                          mask_type='file',
                          parameter_source='SPM',
                          use_differences=[True, False]),
           name="art")

# Smooth - to smooth the images with a given kernel
smooth = Node(Smooth(fwhm=fwhm_size),
              name="smooth")

# FreeSurferSource - Data grabber specific for FreeSurfer data
fssource = Node(FreeSurferSource(subjects_dir=fs_dir),
                run_without_submitting=True,
                name='fssource')

# BBRegister - coregister a volume to the Freesurfer anatomical
bbregister = Node(BBRegister(init='fsl',
                             contrast_type='t2',
                             out_fsl_file=True),
                  name='bbregister')

# Volume Transformation - transform the brainmask into functional space
applyVolTrans = Node(ApplyVolTransform(inverse=True),
                     name='applyVolTrans')

# Binarize -  binarize and dilate an image to create a brainmask
binarize = Node(Binarize(min=0.5,
                         dilate=1,
                         out_type='nii'),
                name='binarize')


###
# Specify Preprocessing Workflow & Connect Nodes

# Create a preprocessing workflow
preproc = Workflow(name='preproc')

# Connect all components of the preprocessing workflow
preproc.connect([(despike, sliceTiming, [('out_file', 'in_files')]),
                 (sliceTiming, realign, [('timecorrected_files', 'in_files')]),
                 (realign, tsnr, [('realigned_files', 'in_file')]),
                 (tsnr, art, [('detrended_file', 'realigned_files')]),
                 (realign, art, [('mean_image', 'mask_file'),
                                 ('realignment_parameters',
                                  'realignment_parameters')]),
                 (tsnr, smooth, [('detrended_file', 'in_files')]),
                 (realign, bbregister, [('mean_image', 'source_file')]),
                 (fssource, applyVolTrans, [('brainmask', 'target_file')]),
                 (bbregister, applyVolTrans, [('out_reg_file', 'reg_file')]),
                 (realign, applyVolTrans, [('mean_image', 'source_file')]),
                 (applyVolTrans, binarize, [('transformed_file', 'in_file')]),
                 ])


###
# Specify 1st-Level Analysis Nodes

# SpecifyModel - Generates SPM-specific Model
modelspec = Node(SpecifySPMModel(concatenate_runs=False,
                                 input_units='secs',
                                 output_units='secs',
                                 time_repetition=TR,
                                 high_pass_filter_cutoff=128),
                 name="modelspec")

# Level1Design - Generates an SPM design matrix
level1design = Node(Level1Design(bases={'hrf': {'derivs': [0, 0]}},
                                 timing_units='secs',
                                 interscan_interval=TR,
                                 model_serial_correlations='AR(1)'),
                    name="level1design")

# EstimateModel - estimate the parameters of the model
level1estimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      name="level1estimate")

# EstimateContrast - estimates contrasts
conestimate = Node(EstimateContrast(), name="conestimate")

# Volume Transformation - transform contrasts into anatomical space
applyVolReg = MapNode(ApplyVolTransform(fs_target=True),
                      name='applyVolReg',
                      iterfield=['source_file'])

# MRIConvert - to gzip output files
mriconvert = MapNode(MRIConvert(out_type='niigz'),
                     name='mriconvert',
                     iterfield=['in_file'])


###
# Specify 1st-Level Analysis Workflow & Connect Nodes

# Initiation of the 1st-level analysis workflow
l1analysis = Workflow(name='l1analysis')

# Connect up the 1st-level analysis components
l1analysis.connect([(modelspec, level1design, [('session_info',
                                                'session_info')]),
                    (level1design, level1estimate, [('spm_mat_file',
                                                     'spm_mat_file')]),
                    (level1estimate, conestimate, [('spm_mat_file',
                                                    'spm_mat_file'),
                                                   ('beta_images',
                                                    'beta_images'),
                                                   ('residual_image',
                                                    'residual_image')]),
                    (conestimate, applyVolReg, [('con_images',
                                                 'source_file')]),
                    (applyVolReg, mriconvert, [('transformed_file',
                                                'in_file')]),
                    ])


###
# Specify Meta-Workflow & Connect Sub-Workflows
metaflow = Workflow(name='metaflow')
metaflow.base_dir = opj(experiment_dir, working_dir)

metaflow.connect([(preproc, l1analysis, [('realign.realignment_parameters',
                                          'modelspec.realignment_parameters'),
                                         ('smooth.smoothed_files',
                                          'modelspec.functional_runs'),
                                         ('art.outlier_files',
                                          'modelspec.outlier_files'),
                                         ('binarize.binary_file',
                                          'level1design.mask_image'),
                                         ('bbregister.out_reg_file',
                                          'applyVolReg.reg_file'),
                                         ]),
                  ])


###
# Specify Model - Condition, Onset, Duration, Contrast

# Condition names
condition_names = ['congruent', 'incongruent']

# Contrasts
cont01 = ['congruent',   'T', condition_names, [1, 0]]
cont02 = ['incongruent', 'T', condition_names, [0, 1]]
cont03 = ['congruent vs incongruent', 'T', condition_names, [1, -1]]
cont04 = ['incongruent vs congruent', 'T', condition_names, [-1, 1]]
cont05 = ['Cond vs zero', 'F', [cont01, cont02]]
cont06 = ['Diff vs zero', 'F', [cont03, cont04]]

contrast_list = [cont01, cont02, cont03, cont04, cont05, cont06]

# Function to get Subject specific condition information
def get_subject_info(subject_id):
    from os.path import join as opj
    path = '~/nipype_tutorial/data/%s' % subject_id
    onset_info = []
    for run in ['01', '02']:
        for cond in ['01', '02', '03', '04']:
            onset_file = opj(path, 'onset_run0%s_cond0%s.txt'%(run, cond))
            with open(onset_file, 'rt') as f:
                for line in f:
                    info = line.strip().split()
                    if info[1] != '0.00':
                        onset_info.append(['cond0%s'%cond,
                                           'run0%s'%run,
                                           float(info[0])])
    onset_run1_congruent = []
    onset_run1_incongruent = []
    onset_run2_congruent = []
    onset_run2_incongruent = []

    for info in onset_info:
        if info[1] == 'run001':
            if info[0] == 'cond001' or info[0] == 'cond002':
                onset_run1_congruent.append(info[2])
            elif info[0] == 'cond003' or info[0] == 'cond004':
                onset_run1_incongruent.append(info[2])
        if info[1] == 'run002':
            if info[0] == 'cond001' or info[0] == 'cond002':
                onset_run2_congruent.append(info[2])
            elif info[0] == 'cond003' or info[0] == 'cond004':
                onset_run2_incongruent.append(info[2])

    onset_list = [sorted(onset_run1_congruent), sorted(onset_run1_incongruent),
                  sorted(onset_run2_congruent), sorted(onset_run2_incongruent)]

    from nipype.interfaces.base import Bunch
    condition_names = ['congruent', 'incongruent']

    subjectinfo = []
    for r in range(2):
        onsets = [onset_list[r*2], onset_list[r*2+1]]
        subjectinfo.insert(r,
                           Bunch(conditions=condition_names,
                                 onsets=onsets,
                                 durations=[[0], [0]],
                                 amplitudes=None,
                                 tmod=None,
                                 pmod=None,
                                 regressor_names=None,
                                 regressors=None))
    return subjectinfo

# Get Subject Info - get subject specific condition information
getsubjectinfo = Node(Function(input_names=['subject_id'],
                               output_names=['subject_info'],
                               function=get_subject_info),
                      name='getsubjectinfo')


###
# Input & Output Stream

# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id',
                                            'contrasts'],
                                    contrasts=contrast_list),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]

# SelectFiles - to grab the data (alternativ to DataGrabber)
templates = {'func': 'data/{subject_id}/run*.nii.gz'}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_subject_id_', ''),
                 ('_despike', ''),
                 ('_detrended', ''),
                 ('_warped', '')]
datasink.inputs.substitutions = substitutions

# Connect Infosource, SelectFiles and DataSink to the main workflow
metaflow.connect([(infosource, selectfiles, [('subject_id', 'subject_id')]),
                  (infosource, preproc, [('subject_id',
                                          'bbregister.subject_id'),
                                         ('subject_id',
                                          'fssource.subject_id')]),
                  (selectfiles, preproc, [('func', 'despike.in_file')]),
                  (infosource, getsubjectinfo, [('subject_id', 'subject_id')]),
                  (getsubjectinfo, l1analysis, [('subject_info',
                                                 'modelspec.subject_info')]),
                  (infosource, l1analysis, [('contrasts',
                                             'conestimate.contrasts')]),
                  (preproc, datasink, [('realign.mean_image',
                                        'preprocout.@mean'),
                                       ('realign.realignment_parameters',
                                        'preprocout.@parameters'),
                                       ('art.outlier_files',
                                        'preprocout.@outliers'),
                                       ('art.plot_files',
                                        'preprocout.@plot'),
                                       ('binarize.binary_file',
                                        'preprocout.@brainmask'),
                                       ('bbregister.out_reg_file',
                                        'bbregister.@out_reg_file'),
                                       ('bbregister.out_fsl_file',
                                        'bbregister.@out_fsl_file'),
                                       ('bbregister.registered_file',
                                        'bbregister.@registered_file'),
                                       ]),
                  (l1analysis, datasink, [('mriconvert.out_file',
                                           'contrasts.@contrasts'),
                                          ('conestimate.spm_mat_file',
                                           'contrasts.@spm_mat'),
                                          ('conestimate.spmT_images',
                                           'contrasts.@T'),
                                          ('conestimate.con_images',
                                           'contrasts.@con'),
                                          ]),
                  ])


###
# Run Workflow
metaflow.write_graph(graph2use='colored')
metaflow.run('MultiProc', plugin_args={'n_procs': 8})
