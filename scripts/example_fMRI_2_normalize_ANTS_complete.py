###
# Import modules
from os.path import join as opj
from nipype.interfaces.ants import Registration, ApplyTransforms
from nipype.interfaces.freesurfer import FSCommand, MRIConvert, BBRegister
from nipype.interfaces.c3 import C3dAffineTool
from nipype.interfaces.utility import IdentityInterface, Merge
from nipype.interfaces.io import SelectFiles, DataSink, FreeSurferSource
from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces.fsl import Info

# FreeSurfer - Specify the location of the freesurfer folder
fs_dir = '~/nipype_tutorial/freesurfer'
FSCommand.set_default_subjects_dir(fs_dir)


###
# Specify variables
experiment_dir = '~/nipype_tutorial'          # location of experiment folder
input_dir_1st = 'output_fMRI_example_1st'     # name of 1st-level output folder
output_dir = 'output_fMRI_example_norm_ants'  # name of norm output folder
working_dir = 'workingdir_fMRI_example_norm_ants'  # name of norm working directory
subject_list = ['sub001', 'sub002', 'sub003',
                'sub004', 'sub005', 'sub006',
                'sub007', 'sub008', 'sub009',
                'sub010']                     # list of subject identifiers

# location of template file
template = Info.standard_image('MNI152_T1_1mm_brain.nii.gz')


###
# Specify Normalization Nodes

# Registration - computes registration between subject's structural and MNI template.
antsreg = Node(Registration(args='--float',
                            collapse_output_transforms=True,
                            fixed_image=template,
                            initial_moving_transform_com=True,
                            num_threads=1,
                            output_inverse_warped_image=True,
                            output_warped_image=True,
                            sigma_units=['vox']*3,
                            transforms=['Rigid', 'Affine', 'SyN'],
                            terminal_output='file',
                            winsorize_lower_quantile=0.005,
                            winsorize_upper_quantile=0.995,
                            convergence_threshold=[1e-06],
                            convergence_window_size=[10],
                            metric=['MI', 'MI', 'CC'],
                            metric_weight=[1.0]*3,
                            number_of_iterations=[[1000, 500, 250, 100],
                                                  [1000, 500, 250, 100],
                                                  [100, 70, 50, 20]],
                            radius_or_number_of_bins=[32, 32, 4],
                            sampling_percentage=[0.25, 0.25, 1],
                            sampling_strategy=['Regular',
                                               'Regular',
                                               'None'],
                            shrink_factors=[[8, 4, 2, 1]]*3,
                            smoothing_sigmas=[[3, 2, 1, 0]]*3,
                            transform_parameters=[(0.1,),
                                                  (0.1,),
                                                  (0.1, 3.0, 0.0)],
                            use_histogram_matching=True,
                            write_composite_transform=True),
               name='antsreg')

# FreeSurferSource - Data grabber specific for FreeSurfer data
fssource = Node(FreeSurferSource(subjects_dir=fs_dir),
                run_without_submitting=True,
                name='fssource')

# Convert FreeSurfer's MGZ format into NIfTI format
convert2nii = Node(MRIConvert(out_type='nii'), name='convert2nii')

# Coregister the median to the surface
bbregister = Node(BBRegister(init='fsl',
                             contrast_type='t2',
                             out_fsl_file=True),
                  name='bbregister')

# Convert the BBRegister transformation to ANTS ITK format
convert2itk = Node(C3dAffineTool(fsl2ras=True,
                                 itk_transform=True),
                   name='convert2itk')

# Concatenate BBRegister's and ANTS' transforms into a list
merge = Node(Merge(2), iterfield=['in2'], name='mergexfm')

# Transform the contrast images. First to anatomical and then to the target
warpall = MapNode(ApplyTransforms(args='--float',
                                  input_image_type=3,
                                  interpolation='Linear',
                                  invert_transform_flags=[False, False],
                                  num_threads=1,
                                  reference_image=template,
                                  terminal_output='file'),
                  name='warpall', iterfield=['input_image'])

# Transform the mean image. First to anatomical and then to the target
warpmean = Node(ApplyTransforms(args='--float',
                                input_image_type=3,
                                interpolation='Linear',
                                invert_transform_flags=[False, False],
                                num_threads=1,
                                reference_image=template,
                                terminal_output='file'),
                name='warpmean')


###
# Specify Normalization Workflow & Connect Nodes

# Initiation of the ANTS normalization workflow
normflow = Workflow(name='normflow')
normflow.base_dir = opj(experiment_dir, working_dir)

# Connect up ANTS normalization components
normflow.connect([(fssource, convert2nii, [('T1', 'in_file')]),
                  (convert2nii, convert2itk, [('out_file', 'reference_file')]),
                  (bbregister, convert2itk, [('out_fsl_file',
                                              'transform_file')]),
                  (convert2itk, merge, [('itk_transform', 'in2')]),
                  (antsreg, merge, [('composite_transform',
                                     'in1')]),
                  (merge, warpmean, [('out', 'transforms')]),
                  (merge, warpall, [('out', 'transforms')]),
                  ])


###
# Input & Output Stream

# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]

# SelectFiles - to grab the data (alternative to DataGrabber)
anat_file = opj('freesurfer', '{subject_id}', 'mri/brain.mgz')
func_file = opj(input_dir_1st, 'contrasts', '{subject_id}',
                '_mriconvert*/*_out.nii.gz')
func_orig_file = opj(input_dir_1st, 'contrasts', '{subject_id}', '[ce]*.nii')
mean_file = opj(input_dir_1st, 'preprocout', '{subject_id}', 'mean*.nii')

templates = {'anat': anat_file,
             'func': func_file,
             'func_orig': func_orig_file,
             'mean': mean_file,
             }

selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_subject_id_', ''),
                 ('_apply2con', 'apply2con'),
                 ('_warpall', 'warpall')]
datasink.inputs.substitutions = substitutions

# Connect SelectFiles and DataSink to the workflow
normflow.connect([(infosource, selectfiles, [('subject_id', 'subject_id')]),
                  (infosource, fssource, [('subject_id', 'subject_id')]),
                  (infosource, bbregister, [('subject_id', 'subject_id')]),
                  (selectfiles, bbregister, [('mean', 'source_file')]),
                  (selectfiles, antsreg, [('anat', 'moving_image')]),
                  (selectfiles, convert2itk, [('mean', 'source_file')]),
                  (selectfiles, warpall, [('func_orig', 'input_image')]),
                  (selectfiles, warpmean, [('mean', 'input_image')]),
                  (antsreg, datasink, [('warped_image',
                                        'antsreg.@warped_image'),
                                       ('inverse_warped_image',
                                        'antsreg.@inverse_warped_image'),
                                       ('composite_transform',
                                        'antsreg.@transform'),
                                       ('inverse_composite_transform',
                                        'antsreg.@inverse_transform')]),
                  (warpall, datasink, [('output_image', 'warp_complete.@warpall')]),
                  (warpmean, datasink, [('output_image', 'warp_complete.@warpmean')]),
                  ])


###
# Run Workflow
normflow.write_graph(graph2use='colored')
normflow.run('MultiProc', plugin_args={'n_procs': 8})
