==============
Help & Support
==============

How Nipype Can Help You
=======================

Often times the first trouble with Nipype arise because of misunderstanding a node or its function. This can be because a mandatory input was forgotten, a input or output field is not what you thought it was or something similar. That's why the first step when running into a problem while building a pipeline should be to check out the description of the interface that causes the trouble. I've already described this `here <https://miykael.github.io/nipype-beginner-s-guide/firstSteps.html#nodes>`_ but to recap:

Let's assume that you've imported FreeSurfer's BBRegister with the command ``from nipype.interfaces.freesurfer import BBRegister``. Now, if you want to know what this module generally does, use the `?` character, i.e. ``BBRegister?``. This gives you a short description as well as an implementation example of this module. If you want to know a more detailed description of BBRegister, with all mandatory and possible inputs and outputs, use the ``help()`` function, i.e. ``BBRegister.help()``.

Also, I highly recommend to check out Nipype's official `Documentation <http://nipype.readthedocs.io/en/latest/documentation.html>`_ section, where you can browse through all possible interfaces, function and description of them.


How to Help Yourself
====================

If you have any **questions about or comments to this beginner's guide**, don't hesitate to leave a comment on the bottom of the corresponding homepage (you don't need an account to do so) or contact me directly by e-mail under: `miykaelnotter@gmail.com <miykaelnotter@gmail.com>`_.

If you have general **questions about what certain neuroimaging or nipype term** mean, check out the beginner's guide `Glossary <https://miykael.github.io/nipype-beginner-s-guide/glossary.html>`_ section.

If you have any **questions about Nipype or neuroimaging** itself please go directly to `neurostars.org <https://neurostars.org/>`_ or the beginner's guide `FAQ <https://miykael.github.io/nipype-beginner-s-guide/faq.html>`_ section. `Neurostars.org <https://neurostars.org/>`_ is a community driven Q&A platform that will help you to answer any nipype or neuroimaging related question that you possibly could have.


How to Help Me
==============

The list of interfaces Nipype supports grows everyday more and more and the best practice to analyze MRI data is changing all the time. It's impossible for one person to keep track of all of those softwares and to know the state of the art analysis. That's why I'm very much counting on the input and support of the community to help me to make this beginner's guide as detailed and complete as possible.

So, if you found any mistakes, want to point out some alternative ways to do something or have any scripts or tutorials to share, your input is highly appreciated!

The best way to help me is to fork my repo on github (`https://github.com/miykael/nipype-beginner-s-guide/tree/master/homepage <https://github.com/miykael/nipype-beginner-s-guide/tree/master/homepage>`_) and send me a pull request. Alternatively you can also contact me with your ideas or feedback under `miykaelnotter@gmail.com <miykaelnotter@gmail.com>`_.


How to Read Crash Files
=======================

Everytime Nipype crashes, it creates a nice crash file containing all necessary information. For a specific example see `this section <https://miykael.github.io/nipype-beginner-s-guide/firstSteps.html#common-issues-problems-and-crashes>`_. In this example the name of the crash file is ``crash-20141018-140440-mnotter-art.b0.pklz``.

The name of the file gives you already an information about when it crashed (``20141018-140440``) and which node crashed (``art.b0``). If you want to read the node you can use the terminal command ``nipype_display_crash``. In our example the command to read the crash file is:

.. code-block:: sh

    nipype_display_crash ~/nipype_tutorial/crash-20141018-140857-mnotter-art.b0.pklz

This leads to the following output:

.. code-block:: sh
    :linenos:

    File: crash-20141018-140857-mnotter-art.b0.pklz
    Node: preproc.art.b0
    Working directory: ~/nipype_tutorial/workingdir_firstSteps/
                         preproc/_subject_id_sub001/art

    Node inputs:

    bound_by_brainmask = False
    global_threshold = 8.0
    ignore_exception = False
    intersect_mask = <undefined>
    mask_file = <undefined>
    mask_threshold = <undefined>
    mask_type = spm_global
    norm_threshold = 0.5
    parameter_source = SPM
    plot_type = png
    realigned_files = <undefined>
    realignment_parameters = ['~/nipype_tutorial/workingdir_firstSteps/preproc/
                                 _subject_id_sub001/realign/rp_arun001.txt']
    rotation_threshold = <undefined>
    save_plot = True
    translation_threshold = <undefined>
    use_differences = [True, False]
    use_norm = True
    zintensity_threshold = 3.0

    Traceback (most recent call last):
      File "~/anaconda/lib/python2.7/site-packages/nipype/pipeline/plugins/linear.py",
           line 38, in run node.run(updatehash=updatehash)
      File "~/anaconda/lib/python2.7/site-packages/nipype/pipeline/engine.py",
           line 1424, in run self._run_interface()
      File "~/anaconda/lib/python2.7/site-packages/nipype/pipeline/engine.py",
           line 1534, in _run_interface self._result = self._run_command(execute)
      File "~/anaconda/lib/python2.7/site-packages/nipype/pipeline/engine.py",
           line 1660, in _run_command result = self._interface.run()
      File "~/anaconda/lib/python2.7/site-packages/nipype/interfaces/base.py",
           line 965, in run self._check_mandatory_inputs()
      File "~/anaconda/lib/python2.7/site-packages/nipype/interfaces/base.py",
           line 903, in _check_mandatory_inputs raise ValueError(msg)
    ValueError: ArtifactDetect requires a value for input 'realigned_files'.
                For a list of required inputs, see ArtifactDetect.help()

The first part of the crash report contains information about the node and the second part contains the error log. In this example, the last two lines tell us exactly, that the crash was caused because the input field `'realigned_files'` was not specified. This error is easy corrected, just add the required input and rerun the workflow.

Under certain circumstances it is possible and desired to rerun the crashed node. This can be done with the additional command flags to ``nipype_display_crash``. The following flags are available:

.. code-block:: sh
    :linenos:

    -h, --help       show this help message and exit
    -r, --rerun      rerun crashed node (default False)
    -d, --debug      enable python debugger when re-executing (default False)
    -i, --ipydebug   enable ipython debugger when re-executing (default False)
    --dir DIRECTORY  Directory to run the node in (default None)


.. note::

   For more information about how to debug your code and handle crashes go to `this official Nipype section <http://nipype.readthedocs.io/en/latest/users/debug.html>`_.
