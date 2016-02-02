===================================
How To Build A Pipeline For A First Level fMRI Analysis
===================================

In this section you will learn how to create a workflow that does a **first level analysis** on fMRI data. There are multiple ways how you can do this, as there are different ways and strategies to preprocess your data and different ways to create a model of your design. So keep in mind that the workflow in this section is just an example and may not suite your specific experiment or design. Having said that, it still contains the most common steps used in a first level analysis.


Define the structure of your pipeline
=====================================

A typical first level fMRI workflow can be divided into two sections: **preprocessing** and **first level analysis**. The first one deals with removing noise and confounding factors such as movement from your data and the second one deals with fitting the model of your experiment to the data. The best way to build a pipeline from scratch is to think about the steps the data has to go through:

In the **preprocessing** part of the pipeline we first want to ``Despike`` the data. This is a process that removes local and short timeline 'spikes' from the functional data. After that we want to correct for the slice wise acquisition of the data with ``SliceTiming`` and get rid of the movement in the scanner with ``Realign``. We want to detrend our data by removing polynomial to the 2nd order with ``TSNR``. Additional to that, we also want to check the realignment parameters for extreme movements, i.e. artifacts, with ``ArtifactDetect`` and prepare an inclusion mask for the first level model with ``DilateImage``. This inclusion mask is created by taking the ``aseg.mgz`` segmentation file from FreeSurfer (with the node ``FreeSurferSource``), binarizing the values with ``Binarize`` (values above 0.5 become 1 and below become 0) and than dilating this binarized mask by a smoothing kernel with ``DilateImage``. After all this is done we are ready to smooth our data with ``Smooth``.

In the **first level analysis** part of the pipeline we first want to specify our model with ``SpecifyModel``, than create the first level design with ``Level1Design``. After that we are able to estimate the model with ``EstimateModel`` and estimate the contrasts with ``EstimateContrast``. Before we're done we want to coregister our contrasts to the subject specific anatomy with ``BBRegister`` and ``ApplyVolTransform`` and convert the final output to zipped NIfTI files with ``MRIConvert``.

As with every workflow, we also need some input and output nodes which handle the data and an additional node that provides subject specific information. For that we need an ``Infosource`` node that knows on which subjects to run, a ``SelectFiles`` node that knows where to get the data, a ``getsubjectinfo`` node that knows subject specific information (e.g. onset times and duration of conditions, subject specific regressors, etc.) and a ``DataSink`` node that knows which files to store and where to store them.

To run all this we need some structure. Therefore, we will put the **preprocessing** and the **first level analysis** part in its own subworkflow and create a hierarchically higher workflow that contains those two subworkflows as well as the input and output nodes. I'd like to call this top workflow **metaflow**.

Those are a lot of different parts and it is confusing to make sense of it without actually seeing what we try to build. Here is how the metaflow should look like in the end:

.. only:: html

    .. image:: images/graph_colored.svg
       :align: center
       :width: 700pt

.. only:: latex

    .. image:: images/graph_colored.svg
       :align: center
       :width: 500pt

.. note::

   The normalization of the first level output into a common reference space (e.g. MNI-space) will not be done by this metaflow. This because I want to dedicate a whole section on different ways on `how to normalize your data <http://miykael.github.com/nipype-beginner-s-guide/normalize.html>`_. Normalizing your data is very important for the analysis on the group level and a good normalization can be the difference between super results or none at all.


Write your pipeline script
==========================

Before we can start with writing a pipeline script, we first have to make sure that we have all necessary information. We know how the structure of the metaflow should look like from the previous section. But what are the experiment specific parameters? Lets assume that we use the `tutorial dataset <http://miykael.github.com/nipype-beginner-s-guide/prepareData.html>`_ with the ten subjects ``sub001`` to ``sub010``, each having two functional scans ``run001.nii.gz`` and ``run002.nii.gz``. We know from the openfmri homepage `DS102: Flanker task (event-related) <https://openfmri.org/dataset/ds000102>`_ that this experiment has a a TR of 2.0 seconds and that each volume of the functional data consists of 40 slices, acquired in an ascending interleaved slice order. And we know that we can find condition specific onset times for each subject in the subject folder in our data folder, e.g. ``~/nipype_tutorial/data/sub001/``. So let's start!


Import modules
~~~~~~~~~~~~~~

First we have to import all necessary modules. Which modules you have to import becomes clear while you’re adding specific nodes.

.. code-block:: py
   :linenos:

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



Specify interface behaviors
~~~~~~~~~~~~~~

To make sure that the MATLAB and FreeSurfer interface run correctly, add the following code to your script.

.. code-block:: py
   :linenos:

   # MATLAB - Specify path to current SPM and the MATLAB's default mode
   from nipype.interfaces.matlab import MatlabCommand
   MatlabCommand.set_default_paths('/usr/local/MATLAB/R2014a/toolbox/spm12')
   MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")

   # FreeSurfer - Specify the location of the freesurfer folder
   fs_dir = '~/nipype_tutorial/freesurfer'
   FSCommand.set_default_subjects_dir(fs_dir)

   
Define experiment specific parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I suggest to keep experiment specific parameters that change often between experiments like subject names, output folders, scan parameters and name of functional runs at the beginning of your script. Like this they can be accessed and changed more easily.

.. code-block:: py
   :linenos:

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


Create preprocessing pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's first create all nodes needed for the preprocessing subworkflow:

.. code-block:: py
   :linenos:

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
   bbregister = Node(BBRegister(init='header',
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


After implementing the nodes we can create the preprocessing subworkflow and add all those nodes to it and connect them to each other.

.. code-block:: py
   :linenos:

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


If you are wondering how we know which parameters to specify and which connections to establish. It is simple: First, specify or connect all mandatory inputs of each node. Second, add the additional inputs that your data requires. For more informations about what is mandatory and what's not, go either to `Interfaces and Algorithms <http://nipy.org/nipype/interfaces/index.html>`_ or use the ``.help()`` method (e.g. ``realign.help()``), as shown `here <http://miykael.github.com/nipype-beginner-s-guide/firstSteps.html#input-and-output-fields>`_.


Create first level analysis pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, let us define the pipeline for the first level analysis. Again, first we need to implement the nodes:

.. code-block:: py
   :linenos:

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


Now that this is done, we create the first level analysis subworkflow and add all the nodes to it and connect them to each other.

.. code-block:: py
   :linenos:

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


Define meta workflow and connect subworkflows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After we've created the subworkflows ``preproc`` and ``l1analysis`` we are ready to create the meta workflow ``metaflow`` and establish the connections between the two subworkflows.

.. code-block:: py
   :linenos:

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


Define model specific parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The procedure of how we get subject specific parameters into our metaflow is a bit tricky but can be done as shown below. First, we have to specify the conditions of our paradigm and what contrasts we want to compute from them. In our case, the names of the condition are ``'congruent'`` and ``'incongruent'``. The original condition of the tutorial dataset also include a subdivision into correct and incorrect trials (see ``~/nipype_tutorial/data/condition_key.txt``). This example will not consider this subdivision, as there are very few or no occurrences of incorrect responses per subject.

.. code-block:: py
   :linenos:

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


The definition of contrasts is rather straight forward. For a T-contrast, just specify the name of the contrast, the type, the name of all conditions and the weights to those conditions. The implementation of an F-contrast only needs a name for the contrast, the type of the contrast, followed by a list of T-contrasts to use in the F-contrast. One important addition: If you want to have run specific contrasts add an additional list to the end of the contrast, which specifies for which run the contrast should be used. For example, if you want the 3rd contrast only computed in the 2nd run, use the following code:

``cont03 = ['congruent', 'T', condition_names, [1, 0], [0, 1]]``

Now let's get to the more tricky part: How do we get the subject and run specific onset times for the 'congruent' and the 'incongruent' condition into our pipeline? Well, with the following function:

.. code-block:: py
   :linenos:

   # Function to get Subject specific condition information
   def get_subject_info(subject_id):
       from os.path import join as opj
       path = '~/nipype_tutorial/data/%s'%subject_id
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


So what does it do? **Line 3 to 34** are specific to the tutorial dataset and will most certainly not apply for any other study, which are not from the `openfmri.org <https://openfmri.org/>`_. This part of the function goes through the subject folder under ``~/nipype_tutorial/data/`` and reads out the values in the files ``onset_run00?_cond00?.txt``. The result of line 3 to 34 is an array called ``onset_list`` with four arrays, containing the onset for the condition ``congruent_run1``, ``incongruent_run1``, ``congruent_run2`` and ``incongruent_run2``. In the case of ``sub001`` this looks like this:

.. code-block:: py

   onset_list=[[20.0, 30.0, 52.0, 64.0, 88.0, 116.0, 130.0, 140.0, 184.0, 196.0, 246.0, 274.0],
               [0.0, 10.0, 40.0, 76.0, 102.0, 150.0, 164.0, 174.0, 208.0, 220.0, 232.0, 260.0],
               [10.0, 20.0, 30.0, 42.0, 102.0, 116.0, 164.0, 174.0, 208.0, 220.0, 232.0, 260.0],
               [0.0, 54.0, 64.0, 76.0, 88.0, 130.0, 144.0, 154.0, 184.0, 196.0, 246.0, 274.0]]

**Line 36 to 50** is the part of the ``get_subject_info`` function that has to be included in almost all first level analysis workflows. For more information see `Model Specification for First Level fMRI Analysis <http://nipy.sourceforge.net/nipype/users/model_specification.html>`_. Important to know are the following things: The for loop ``for r in range(2)`` in line 40 is set to 2 because we have two runs per subject. The idea is to create an output variable ``subjectinfo`` that contains a ``Bunch`` object for each run. The content of this ``Bunch`` object depends on the subject and contains the name of the conditions, onsets of them, duration of each event, as well as possible amplitude modifications, temporal or polynomial derivatives or regressors. **Note:** The duration of all events per condition were set to ``[0]``, as this assumes that the events should be modeled as impulses.

Now that the tricky part is done, we only need to create an additional node that applies this function and has the value of the ``subjectinfo`` variable as an output field. This can be done with a function node (as shown in the `previous section <http://miykael.github.com/nipype-beginner-s-guide/firstSteps.html#individual-nodes>`_)

.. code-block:: py
   :linenos:

   # Get Subject Info - get subject specific condition information
   getsubjectinfo = Node(Function(input_names=['subject_id'],
                                  output_names=['subject_info'],
                                  function=get_subject_info),
                         name='getsubjectinfo')


Establish Input & Output Stream
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As always, our metaflow needs an input stream to have data to work and an output stream to know where to store the computed output. This can be done with the following three nodes:

* ``infosource``: This node will iterate over the ``subject_list`` and feed the ``contrast_list`` to the first level analysis.
* ``selectfiles``: This node will grab the functional files from the subject folder and feed them to the preprocessing pipeline, specifically the ``Despike`` node.
* ``datasink``: This node will store the metaflow output in an output folder and rename or delete unwanted post- or prefixes.

And here's the code to do this:

.. code-block:: py
   :linenos:

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


Run the pipeline and generate the graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, after everything is set up correctly we can run the pipeline and let it draw the graph of the workflow.

.. code-block:: py
   :linenos:
   
   metaflow.write_graph(graph2use='colored')
   metaflow.run('MultiProc', plugin_args={'n_procs': 8})

.. hint::

   You can download the code for this first level pipeline as a script here: `example_fMRI_1_first_level.py <http://github.com/miykael/nipype-beginner-s-guide/blob/master/scripts/example_fMRI_1_first_level.py>`_


Visualize your pipeline
=======================

The visualization of this graph can be seen in all different graph types under the section `How to visualize a pipeline <http://miykael.github.com/nipype-beginner-s-guide/visualizePipeline.html>`_ or as a colored graph at the beginning of this section.


Resulting Folder Structure
==========================

After we've run our **first level analysis pipeline** our folder structure should look like this:

After we’ve executed the first level workflow we have two new folders under ``~/nipype_tutorial``. The working directory ``workingdir_fMRI_example_1st`` which contains all files created during the execution of the metaflow, and the output folder ``output_fMRI_example_1st`` which contains all the files that we sent to the DataSink. Let’s take a closer look at the DataSink folder:

.. code-block:: sh

    output_fMRI_example_1st
    |-- bbregister
    |   |-- sub001
    |   |   |-- meanarun001_bbreg_sub001.dat
    |   |   |-- meanarun001_bbreg_sub001.mat
    |   |-- sub0..
    |   |-- sub010
    |-- contrasts
    |   |-- sub001
    |   |   |-- con_0001.nii
    |   |   |-- con_0002.nii
    |   |   |-- con_0003.nii
    |   |   |-- con_0004.nii
    |   |   |-- con_0005.nii
    |   |   |-- ess_0005.nii
    |   |   |-- ess_0006.nii
    |   |   |-- _mriconvert0
    |   |   |   |-- con_0001_out.nii.gz
    |   |   |-- _mriconvert1
    |   |   |   |-- con_0002_out.nii.gz
    |   |   |-- _mriconvert2
    |   |   |   |-- con_0003_out.nii.gz
    |   |   |-- _mriconvert3
    |   |   |   |-- con_0004_out.nii.gz
    |   |   |-- _mriconvert4
    |   |   |   |-- ess_0005_out.nii.gz
    |   |   |-- _mriconvert5
    |   |   |   |-- ess_0006_out.nii.gz
    |   |   |-- spmF_0005.nii
    |   |   |-- spmF_0006.nii
    |   |   |-- SPM.mat
    |   |   |-- spmT_0001.nii
    |   |   |-- spmT_0002.nii
    |   |   |-- spmT_0003.nii
    |   |   |-- spmT_0004.nii
    |   |-- sub0..
    |   |-- sub010
    |-- preprocout
        |-- sub001
        |   |-- art.rarun001_outliers.txt
        |   |-- art.rarun002_outliers.txt
        |   |-- brainmask_thresh.nii
        |   |-- meanarun001.nii
        |   |-- plot.rarun001.png
        |   |-- plot.rarun002.png
        |   |-- rp_arun001.txt
        |   |-- rp_arun002.txt
        |-- sub0..
        |-- sub010

The ``bbregister`` folder contains two files that both contain the registration information between the functional mean image and the anatomical image. The ``.dat`` file is the registration matrix in FreeSurfer and the ``.mat`` file in FSL format.

The ``contrast`` folder contains the estimated beta (``con`` and ``ess`` files) and statistical spm (``spmT`` and ``spmF`` files) contrasts. It also contains the ``SPM.mat`` file as well as 5 folders (``_mriconvert0`` to ``_mriconvert4``) which contain the coregistered and converted ``con*_out.nii.gz`` files.

The ``preprocout`` folder contains different informative and necessary output from the preprocess workflow:

- The ``art.rarun00?_outliers.txt`` files contain the number of outlier volumes, detected by the ``ArtifactDetection`` node.
- The ``plot.rarun00?.png`` images show the volume to volume change in intensity or movement, plotted by the ``ArtifactDetection`` node. Red vertical lines mean that the specified volume was detected as an outlier.
- The ``rp_arun00?.txt`` files contain the movement regressors calculated by the ``Realign`` node.
- The ``brainmask_thresh.nii`` file is the computed binary mask used in the ``Level1Design`` node.
- The file ``meanarun001.nii`` is the functional mean file computed by the ``Realign`` node.
