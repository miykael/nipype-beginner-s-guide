.. ########################################
   #                                      #
   #  Nipype Beginner's Guide             #
   #                                      #
   #  Author:   Michael Notter            #
   #            miykaelnotter@gmail.com   #
   #                                      #
   ########################################

.. |start| image:: _static/start.png
   :width: 80pt
.. |setup| image:: _static/setup.png
   :width: 80pt
.. |nipype| image:: _static/nipype.png
   :width: 80pt
.. |expert| image:: _static/expert.png
   :width: 80pt
.. |support| image:: _static/support.png
   :width: 80pt
.. |data| image:: _static/data.png
   :width: 60pt

.. only:: html

    ===================================
    Welcome to Nipype Beginner's Guide!
    ===================================

    This Beginner's guide will teach you all you need to know for your first steps with Nipype. You will see that Nipype is a really practical and easy to learn neuroimaging toolbox, written in Python, that helps to connect many of the different softwares used in neuroimaging, such as SPM, FSL, FreeSurfer and AFNI. The goal of this Beginner's guide is to teach you the basics about Neuroimaging and to show you each step along the way of a complete neuroimaging analysis. By learning Nipype, you will become an expert in neuroimaging and be able to analyze your own dataset in no time.


    Neuroimaging and Nipype
    =======================

    This part introduces you to Nipype, explains what it is and how it works. It will also introduce you to neuroimaging in general and tell you all you need to know for the analysis of a basic neuroimaging dataset. At the end, you should be able to understand what Nipype is, how it is working and why it is so useful in neuroimaging.

    +----------+-------------------------------------------+
    | |start|  |   .. toctree::                            |
    |          |      :maxdepth: 2                         |
    |          |                                           |
    |          |      nipype                               |
    |          |      neuroimaging                         |
    |          |      nipypeAndNeuroimaging                |
    +----------+-------------------------------------------+


    Get Nipype to run on your System
    ================================

    This part is all about downloading and installing Nipype and its dependencies. It will also show you how to set up all necessary environment variables and prepare everything, so that at the end you will be ready to run Nipype on your system.

    +----------+-------------------------------------------+
    | |setup|  |   .. toctree::                            |
    |          |      :maxdepth: 2                         |
    |          |                                           |
    |          |      installation                         |
    +----------+-------------------------------------------+


    First steps with Nipype
    =======================

    This part will show you how to use Nipype by analyzing an fMRI dataset. By going through a neuroimaging analysis step by step, you will learn all about Nipype, its building blocks and how to connect them to create your own analysis workflow. At the end you will be able to run your own neuroimaging analysis and make your first experiences with Nipype on real data.

    +----------+-------------------------------------------+
    | |nipype| |   .. toctree::                            |
    |          |      :maxdepth: 2                         |
    |          |                                           |
    |          |      prepareData                          |
    |          |      firstSteps                           |
    |          |      visualizePipeline                    |
    +----------+-------------------------------------------+


    From beginner to expert
    =======================

    This part contains many different implementations of Nipype. Amongst others, you will learn how to do a first and second level analysis, how to normalize your data, how to use Nipype in a more flexible way (e.g. import and reuse of other workflows), how to do a region of interest (ROI) analysis, how to do a surfaced based morphometry (SBM) analysis, how to use ANTs to create your own dataset template, how to quality control your data, how to use additional supporting toolboxes such as bips and mindboggle and more...

    +----------+-------------------------------------------+
    | |expert| |   .. toctree::                            |
    |          |      :maxdepth: 2                         |
    |          |                                           |
    |          |      firstLevel                           |
    |          |      normalize                            |
    |          |      secondLevel                          |
    +----------+-------------------------------------------+
       

    Support
    =======

    First things first: **Don't panic!** This part will show you how to tackle almost all problems you can encounter by using Nipype, iPython or this beginner's guide. And for everything else, there's always chocolate!

    +----------+-------------------------------------------+
    ||support| |   .. toctree::                            |
    |          |      :maxdepth: 1                         |
    |          |                                           |
    |          |      help                                 |
    |          |      links                                |
    |          |      faq                                  |
    |          |      glossary                             |
    |          |                                           |
    +----------+-------------------------------------------+


    Downloads
    =========

    +----------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
    ||data|    |   Everything important to download can be found in this section.                                                                                    |
    |          |                                                                                                                                                     |
    |          |   * Nipype can be downloaded `here <http://nipy.sourceforge.net/nipype/users/install.html>`_.                                                       |
    |          |   * All Scripts used in this Beginner's Guide can be found `here <http://github.com/miykael/nipype-beginner-s-guide/blob/master/scripts>`_.         |
    |          |   * The dataset `DS102: Flanker task (event-related) <https://openfmri.org/dataset/ds000102>`_ used as the tutorial dataset                         |
    |          |     for this beginner's guide can be directly downloaded `here <http://openfmri.s3.amazonaws.com/tarballs/ds102_raw.tgz>`_.                         |
    |          |   * This Beginner's Guide can be downloaded as a PDF                                                                                                |
    |          |     `here <http://github.com/miykael/nipype-beginner-s-guide/blob/master/NipypeBeginnersGuide.pdf?raw=true>`_.                                      |
    +----------+-----------------------------------------------------------------------------------------------------------------------------------------------------+


.. only:: latex

    ==========================================
    Welcome to the Beginner's Guide to Nipype!
    ==========================================

    
    .. toctree::
       :maxdepth: 2

       nipype
       neuroimaging
       nipypeAndNeuroimaging
       installation
       prepareData
       firstSteps
       visualizePipeline
       firstLevel
       normalize
       secondLevel
       help
       links
       faq
       glossary



    Downloads
    =========

    Download Nipype here: `Nipype Homepage <http://nipy.sourceforge.net/nipype/users/install.html>`_.

    Download this beginner's guide as a PDF here: `Nipype Beginner's Guide <http://github.com/miykael/nipype-beginner-s-guide/blob/master/NipypeBeginnersGuide.pdf?raw=true>`_.

    Download all scripts from this beginner's guide here:`Scripts <http://github.com/miykael/nipype-beginner-s-guide/blob/master/scripts>`_.

    Download the dataset `DS102: Flanker task (event-related) <https://openfmri.org/dataset/ds000102>`_ used as the tutorial dataset for this beginner's guide directly `here <http://openfmri.s3.amazonaws.com/tarballs/ds102_raw.tgz>`_.


