=========================
Download and Install Nipype
=========================

All you need to know to download and install Nipype can be found on the official homepage under `Download and Install <http://nipy.sourceforge.net/nipype/users/install.html>`_. There you find a link to the newest version and more information about which dependencies are necessary or recommended.

Installing Nipype as described on the official homepage should be rather easy for most users. There are some tricky steps that sometimes seem to be less straight forward. But don't worry, I've written my own installation guide to help and assist users with less UNIX experience. The following instructions hopefully help everybody to install and run Nipype on their system. Note that some steps strongly depend on the system you are using and it might be possible that some dependencies are already installed on your system. Also, 

.. note::

    It is highly recommended to run Nipype on a machine with either a Mac or Linux OS, as most dependencies such as FSL or FreeSurfer don't run on Windows. If you have a Windows machine, I recommend you to install `Ubuntu <http://www.ubuntu.com/download/desktop>`_ on your system.

The following steps describe how I was able to set up and run Nipype on a System with a newly installed Ubuntu 14.04 LTS OS (64-bit), called "`trusty`". To people with older Ubuntu version, don't worry, Nipype does also run on much older versions, as long as they are not too ancient. To check which version of Ubuntu you are running use the command ``lsb_release -d``. You don't have to upgrade to version 14.04 if you have an older version as long as it isn't too ancient.

**To Mac Users**: I haven't installed Nipype on a Mac, yet. But the steps should be almost identical. If any major differences occur, please let me know.
  

Prepare your System
===================

Before we start, make sure that your Ubuntu system is up to date with the following command:

.. code-block:: sh

    #Update and upgrade your system
    sudo apt-get update && sudo apt-get upgrade


Anaconda
====================

.. image:: _static/logo/logoAnaconda.png
   :width: 90pt
   :align: left

As you can see under `Dependencies <http://nipy.sourceforge.net/nipype/users/install.html#dependencies>`_, there are a lot of software packages that have to be installed on your system to run Nipype. For example: `python`, `ipython`, `matplotlib`, `networkx`, `numpy`, `scipy`, `sphinx` etc. Luckily, most of the those required dependencies, most importantly a working Python environment, can be set up by installing `Anaconda <https://store.continuum.io/cshop/anaconda/>`_.


Install Anaconda
----------------

Instructions on how to install Anaconda can be found `here <http://docs.continuum.io/anaconda/install.html>`_. Following are the steps how I've installed the Anaconda package on my system:

1. Download the software under http://continuum.io/downloads and move the downloaded sh-file to your Download folder. In my case this folder is at ``/home/username/Downloads`` abbreviated with ``~/Downloads``.
2. Install the downloaded sh-file with the following command:

    .. code-block:: sh

        bash ~/Downloads/Anaconda-2.1.0-Linux-x86_64.sh

3. Specify the location of the installation (default is ok).
4. Add the anaconda binary directory to your PATH environment variable. This path is automatically added if you answer the question `"Do you wish the installer to prepend the Anaconda install location to PATH in your /home/username/.bashrc ? [yes|no]"` with yes. Otherwise, add the following line to your `.bashrc` file:

    .. code-block:: sh

        export PATH=/home/username/anaconda/bin:$PATH


.. note::

    ``.bashrc`` is read and executed whenever you run bash using an interactive shell, i.e. the terminal. This file usually is stored in your home folder at ``/home/username/.bashrc`` or in other words ``~/.bashrc``. The ``export`` command tells your system to export a variables from the specified package so that they can be used inside the current shell. For example, ``export PATH=/home/somepath:$PATH`` inserts ``/home/somepath`` to the beginning of the variable PATH and exports it.


Update Anaconda
---------------

To update anaconda to the newest version and to clean unused and older content use the following command:

.. code-block:: sh

    conda update conda && conda update anaconda && conda clean --packages --tarballs

Now make sure that you have all Nipype required dependencies up to date with the following command:

.. code-block:: sh

    conda update python ipython ipython-notebook matplotlib \
                 networkx numpy scipy sphinx traits dateutil nose pydot

.. note::

    To update a software package in anaconda use the command "conda update packagename". For example, if you want to update python use "conda update python"


Test Anaconda
-------------

Now that Anaconda is installed let's test if our python environment is ready to run.

1. Open a new terminal and type in the command ``ipython``. This should bring you to the IPython environment. IPython is used to run all your python scripts. Fore more information about Python and IPython see the `IPython support section <http://miykael.github.com/nipype-beginner-s-guide/ipython.html>`_ of this beginner's guide.
2. To check if everything is set up correctly try to import numpy with the following command: 

    .. code-block:: py

        import numpy

If you see no `ImportError` message, everything is fine and we can get on to the next step.


NeuroDebian
====================

.. image:: _static/logo/logoNeurodebian.png
   :width: 70pt
   :align: left

To facilitate the installation of some necessary and recommended software packages such as FSL and Nipype itself, Debian and Ubuntu based system should install the `NeuroDebian <http://neuro.debian.net/>`_ repository. To see which software packages are included in NeuroDebian, go to `NITRCT - NeuroDebian <http://www.nitrc.org/projects/neurodebian/>`_.

1. To install NeuroDebian on your System go to the `Get NeuroDebian <http://neuro.debian.net/#get-neurodebian>`_ and select the operating system and the server you want to use. In my case, the operating system is `'Ubuntu 14.04 "Trusty Tahr" (trusty)'`. If you have an Ubuntu OS but don't know which version, just type `lsb_release -a` in the terminal and it will show you.
2. Chose the option "All software"
3. Now you should see two lines of command. In my case they were the following:

    .. code-block:: sh

        wget -O- http://neuro.debian.net/lists/trusty.de-md.full | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
        sudo apt-key adv --recv-keys --keyserver pgp.mit.edu 2649A5A9

   Run those two lines of code in your terminal.

4. After all this is done, update your system with the following command: ``sudo apt-get update``

Now you are read to install Nipype, FSL, AFNI and more.

.. note::

    If you have problem with the ``wget`` command in the 3rd step it is most likely because of the root permission (the sudo command in the second half of the command). When the wget command seems to halt and do nothing type in your password and it should go on.


Nipype
====================

Install Nipype (and other python dependencies)
--------------------

.. image:: _static/logo/logoNipype.png
   :width: 100pt
   :align: left

Finally, it's time to install Nipype. And while doing so, let's also install additional python dependencies, such as: nibabel, rdflib, nipy, dipy and graphviz. Some of those packages might already be installed on your system when you've installed Anaconda.

So what do you have to do to install Nipype? It's simple, just use either ``pip install nipype`` or ``easy_install nipype``. More information about the installation of Nipype on a Mac or from sourcecode, go to the `main page <http://nipy.sourceforge.net/nipype/users/install.html>`_.

If you also want to install other python based dependencies use the following commands:

.. code-block:: sh

    #Install packages with pip
    pip install nipype
    pip install nibabel
    pip install rdflib
    pip install nipy
    pip install dipy

    #Install graphviz and pygraphviz separately
    sudo apt-get install graphviz libgraphviz-dev
    pip install --upgrade pygraphviz graphviz


Test Nipype
---------------

To test if everything worked fine and if you're able to use Nipype go into an IPython environment and import nipype with the command: ``import nipype``. If you see no `ImportError` message, everything is set up correctly.


Upgrade Nipype (and other python dependencies)
--------------------

If you want to be sure that you have the newest version or update a certain package use the ``pip install`` command with the flag ``--upgrade``. So, if you want to upgrade Nipype to the newest version use the following command:

.. code-block:: sh

    pip install --upgrade nipype 

If you want to upgrade all other required python dependencies as well use the following command:

.. code-block:: sh

    pip install --upgrade nibabel nipype rdflib nipy dipy pygraphviz graphviz


Upgrade Nipype to the developer version
--------------------

If you want or have to upgrade Nipype to the developer version us the following steps. Such an upgrade is only recommended to people who know what they are doing or need a certain fix that isn't distributed yet in the general Nipype version.

The most current developer version of Nipype can be found on `GitHub <https://github.com/>`_ under `Nipype @ GitHub <https://github.com/nipy/nipype>`_. The following steps assume assume that you've already set up your own GitHub account and are ready to download the Nipype repository:

1. First, open a terminal and download the Nipype repository at the current location with ``git clone https://github.com/nipy/nipype.git``, or download the repository directly by using `this link <https://github.com/nipy/nipype/archive/master.zip>`_.
2. The just downloaded nipype folder contains another folder called `nipype``. This is the folder that contains the newest version of Nipype.
3. Now, either add the path to this folder to the ``PYTHONPATH`` list (make sure that ``PYTHONPATH`` only contains one Nipype folder) or delete the current nipype folder and move the new github ``nipype`` folder to this location. This can be done with the following command:

    .. code-block:: sh

        rm -rf ~/anaconda/lib/python2.7/site-packages/nipype
        cp -R ~/Downloads/nipype/nipype ~/anaconda/lib/python2.7/site-packages/nipype


.. note::

    If you haven't set up a GitHub account yet but don't know how to set everything up, see this link: `Set Up Git <https://help.github.com/articles/set-up-git>`_.


=========================
Download and Install Interfaces
=========================


FSL
====================

Download and Installation
---------------

.. image:: _static/logo/logoFSL.jpg
   :width: 70pt
   :align: left

`FSL <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/>`_ is a comprehensive library of analysis tools for fMRI, MRI and DTI data. An overview of FSL's tools can be found `here <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslOverview>`_.

The installation of `FSL <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSL>`_ is simple if you've already installed the NeuroDebian repository.

Just run the following command:

.. code-block:: sh

    sudo apt-get install fsl

Otherwise, go through the official FSL installation guide, found `here <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation>`_.

Configuration
---------------

Before you can run FSL, your system first needs to know where the software is installed at. On a ubuntu system, this is usually under ``/usr/share/fsl``. Therefore, add the following code to your `.bashrc` file. (To open and edit your `.bashrc` file on Ubuntu, us the following command: ``gedit ~/.bashrc``)

.. code-block:: sh

    #FSL
    FSLDIR=/usr/share/fsl
    . ${FSLDIR}/5.0/etc/fslconf/fsl.sh
    PATH=${FSLDIR}/5.0/bin:${PATH}
    export FSLDIR PATH


Test FSL
---------------

To test if FSL is correctly installed, open a new terminal and type in the command ``fsl``. If everything was set up correctly you should see the FSL GUI with the version number in the header. In my case this is version 5.0.7.


FreeSurfer
====================

.. image:: _static/logo/logoFreeSurfer.jpg
   :height: 55pt
   :align: left

`FreeSurfer <http://surfer.nmr.mgh.harvard.edu/>`_ is an open source software suite for processing and analyzing (human) brain MRI images. The installation of `FreeSurfer <http://surfer.nmr.mgh.harvard.edu/>`_ includes abit more steps than the other installations, but the official `FreeSurfer: Download and Install <http://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall>`_ homepage is written very well and should get you through it without any problem. Nonetheless, following are the steps how I've installed FreeSurfer on my system.


Download and Installation
-------------------------

1. Go to `FreeSurfer: Download <http://surfer.nmr.mgh.harvard.edu/fswiki/Download>`_ and download the corresponding version for your system. In my case this was the `Linux CentOS 6 x86_64 (64b) stable v5.3.0` version. The file is called ``freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0.tar.gz``.
2. Unpack FreeSurfer's binary folder to the place where you want the software to be at. In my case, I want to install FreeSurfer at ``/usr/local/freesurfer``, which in my case needs root privilege. In my case this all can be done with the following command:

    .. code-block:: sh

        sudo tar xzvf \
            ~/Downloads/freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0.tar.gz
            -C /usr/local/

3. The usage of FreeSurfer requires a license file. Therefore, before you can use FreeSurfer, make sure to register `here <https://surfer.nmr.mgh.harvard.edu/registration.html>`_. The content of the license file looks something like this:

    .. code-block:: sh

        username@gmail.com
        12345
         *A3zKO68mtFu5

    This key has to be saved under a file with the name `.license` and has to be stored at your ``$FREESURFER_HOME`` location. In my case, this is ``/usr/local/freesurfer``. To create this file in an Ubuntu environment use the following command:

    .. code-block:: sh

        sudo gedit /usr/local/freesurfer/.license

    Now copy the license code into this file, and save and close it.

4. The last thing you have to do before you can use FreeSurfer is to tell your system where the software package is. To do this, add the following code to your `.bashrc` file:

    .. code-block:: sh

        #FreeSurfer
        export FREESURFER_HOME=/usr/local/freesurfer
        source $FREESURFER_HOME/SetUpFreeSurfer.sh


Test FreeSurfer
---------------

After setting everything up, we can test if FreeSurfer is set up correctly and run a test with the following command:

.. code-block:: sh

    #Test 1
    freeview -v $SUBJECTS_DIR/bert/mri/brainmask.mgz \
             -v $SUBJECTS_DIR/bert/mri/aseg.mgz:colormap=lut:opacity=0.2 \
             -f $SUBJECTS_DIR/bert/surf/lh.white:edgecolor=yellow \
             -f $SUBJECTS_DIR/bert/surf/rh.white:edgecolor=yellow \
             -f $SUBJECTS_DIR/bert/surf/lh.pial:annot=aparc:edgecolor=red \
             -f $SUBJECTS_DIR/bert/surf/rh.pial:annot=aparc:edgecolor=red

    #Test 2
    tksurfer bert lh pial -curv -annot aparc.a2009s.annot

.. note:: 

    On a new Ubuntu System this might lead to the following error: ``freeview.bin: error while loading shared libraries: libjpeg.so.62: cannot open shared object file: No such file or directory``. This is a common error on Ubuntu and can be solved with the following command:

    .. code-block:: sh

        cd /usr/lib/x86_64-linux-gnu
        sudo ln -s libjpeg.so.8 libjpeg.so.62
        sudo ln -s libtiff.so.4 libtiff.so.3

    Alternately, this error can sometimes also be overcome by installing the libjpeg62-dev package with the following command: ``sudo apt-get install libjpeg62-dev``


MATLAB
====================

.. image:: _static/logo/logoMatlab.png
   :width: 70pt
   :align: left

Nowadays almost all scientific fields take advantage of `MATLAB <http://www.mathworks.ch/>`_. Neuroscience is no exception in this and also some of Nipype's recommended interfaces can (but don't have to) take advantage of MATLAB, e.g. SPM, FSL, FreeSurfer.

Having MATLAB is always a good thing, and as I myself rely often on algorithms from the `SPM <http://www.fil.ion.ucl.ac.uk/spm/>`_ interface, I need it to be on my system. A detailed documentation on how to install MATLAB can be found `here <http://www.mathworks.com/help/install/index.html>`_. In my case, MATLAB is installed at the following location: ``/usr/local/MATLAB/R2014a``.

The only thing you need to do to run MATLAB on your Ubuntu System is to add the following lines to your ``.bashrc`` file:

.. code-block:: sh

    #MATLAB
    export PATH=/usr/local/MATLAB/R2014a/bin:$PATH
    export MATLABCMD=/usr/local/MATLAB/R2014a/bin/glnxa64/MATLAB

To test if everything is set up correctly. Open a new Terminal and type in the command: "matlab".


SPM12
====================

.. only:: html

    .. image:: _static/logo/logoSPM12.png
       :width: 80pt
       :align: right


.. only:: latex

    .. image:: _static/logo/logoSPM12.png
       :width: 80pt
       :align: left


`SPM <http://www.fil.ion.ucl.ac.uk/spm/>`_ stands for Statistical Parametric Mapping and is probably one of the most widely-used neuroimaging analysis software package worldwide. SPM is based on MATLAB and therefore needs it to be installed on your system. Luckily, the previous step just made that sure.

As of 1st October 2014, SPM released it's newest version `SPM12 <http://www.fil.ion.ucl.ac.uk/spm/software/spm12/>`_. The `Release Notes <http://www.fil.ion.ucl.ac.uk/spm/software/spm12/SPM12_Release_Notes.pdf>`_ mention some important updates and I therefore recommend to use `SPM12 <http://www.fil.ion.ucl.ac.uk/spm/software/spm12/>`_ instead of `SPM8 <http://www.fil.ion.ucl.ac.uk/spm/software/spm8/>`_. Nonetheless, Nipype has no issue with either `SPM8 <http://www.fil.ion.ucl.ac.uk/spm/software/spm8/>`_ or `SPM12 <http://www.fil.ion.ucl.ac.uk/spm/software/spm12/>`_. Therefore, you can install the version that you prefer.

.. note::

    There is a standalone version of SPM available that doesn't need MATLAB, but so far it isn't recommended as a lot of additional toolboxes don't work with the standalone, yet. For more information go `here <http://en.wikibooks.org/wiki/SPM/Standalone>`_.


Download and Installation
---------------

To download and install the newest version `SPM12 <http://www.fil.ion.ucl.ac.uk/spm/software/spm12/>`_ do as follows:

1. Got to SPM12's `Download and registration <http://www.fil.ion.ucl.ac.uk/spm/software/download.html>`_ page and fill out the form. Under **Select SPM version required**, chose SPM12 (or SPM8 if preferred) and download the zip file.
2. Now, unpack the zip file and copy the content to the recommended folder ``/usr/local/MATLAB/R2014a/toolbox/`` use the following code:

    .. code-block:: sh

        sudo unzip ~/Downloads/spm12.zip -d /usr/local/MATLAB/R2014a/toolbox/

    **Note:** You don't have to put the spm12 folder into this folder, just make sure that you tell your system where to find it.
3. Now tell your system where it can find SPM12 by adding the following line to your ``.bashrc`` file:

    .. code-block:: sh

        #SPM12
        export SPM_PATH=/usr/local/MATLAB/R2014a/toolbox/spm12/

4. Now, set up your MATLAB ``startup.m`` script so that MATLAB knows where SPM12 is stored at. If you've already installed FreeSurfer, than the ``startup.m`` file should be at ``~/matlab/startup.m``. Otherwise create it and save it at this location. Now add the following code to this file:

    .. code-block:: sh

        %-SPM12-
        spm_path = getenv('SPM_PATH');
        if spm_path,
           addpath(spm_path);
        end

.. note::

    There are some interesting ways on how you can change the default behaviors of your SPM.

    * **Example 1:** By default, SPM uses only 64MB of memory during GLM estimation. This can be changed by changing the ``defaults.stats.maxmem`` parameter. Change this value to ``2^29`` and use 512MB or to ``2^30`` and use 1GB of memory during GLM estimation. Another option only available in SPM12 is to set ``defaults.stats.resmem = true;``. Setting this parameter to true means that the temporary files during GLM estimation are kept in memory and not stored on disk (if value is set to false). For more information about increasing the speed of your SPM see the official `Faster SPM <http://en.wikibooks.org/wiki/SPM/Faster_SPM>`_ section.
    * **Example 2**: One computational unimportant but nice parameter to change is ``defaults.ui.colour = [0.141 0 0.848];``. Change it to the recommended value and see the nice color change in your SPM GUI.

    **How to change those values:** SPM8 and SPM12 differ a bit in how those changes have to be implemented. In SPM8 you can change the default behavior by directly changing the parameters in the ``spm_defaults.m`` file, stored in the ``spm8`` folder. If you want to change default values in SPM12, you should create a new file called ``spm_my_defaults.m``, store it in your ``spm12`` folder. The first line of your ``spm_my_defaults.m`` file has to be ``global defaults``, followed by all the parameters you want to change, e.g. ``defaults.ui.colour = [0.141 0 0.848];``


Test SPM12
---------------

To test if SPM12 is set up correctly, open MATLAB and type in the command ``spm fmri``. This can also be achieved in one command: ``matlab -r "spm fmri"``.


ANTs
====================

.. image:: _static/logo/logoANTS.png
   :width: 70pt
   :align: left

`ANTs <http://stnava.github.io/ANTs/>`_ stands for Advanced Normalization Tools and is a great software package for registration, segmentation and normalization of MRI data. I highly recommend to use ANTs for the normalization of your data. **Side note**: ANTs can also be used to create a very cool looking average brain (template) out of a your own population of subjects.

There are two ways how you can set up ANTS on your own system:

The **first** way is very fast and simple. Just download the newest release of ANTs from their `official github homepage <https://github.com/stnava/ANTs/releases>`_. Decompress the downloaded files and store them somewhere on your system, e.g. under ``/usr/local/antsbin``. After you've done that, just add the following line to your ``.bashrc`` file so that your system knows where to find the ANTs binaries:

    .. code-block:: sh

        #ANTs
        export PATH=/usr/local/antsbin/bin:$PATH
        export ANTSPATH=/usr/local/antsbin/bin/


The **second** way to get ANTs on your system takes a bit longer, but guarantees that you have the newest version of ANTs, specifically compiled for your system. Do as follows:

1. Download the data from the official homepage `http://stnava.github.io/ANTs/ <http://stnava.github.io/ANTs/>`_. I chose the "Download TAR Ball" option.
2. Unpack the just downloaded files to a subfolder in your download folder (or wherever you want) with the following command:

    .. code-block:: sh

        tar xzvf ~/Downloads/stnava-ANTs-b4eb279.tar.gz -C ~/Downloads

3. The installation of ANTs differs from other installation by the fact that the software first has to be compiled before it can run on your system. The code has to be compiled to create the binary files specific for your system. To do this, we first need to create a temporary folder to store all important files. This can bed one with the following code: 

    .. code-block:: sh

        mkdir ~/Downloads/stnava-ANTs-b4eb279/antsbin

4. Go into this folder with ``cd ~/Downloads/stnava-ANTs-b4eb279/antsbin`` and proceed with the following steps:

    .. code-block:: sh

        #1. Install ccmake and other dependencies to be able to compile the code
        sudo apt-get install cmake-curses-gui build-essential zlib1g-dev

        #2.
        ccmake ../../stnava-ANTs-b4eb279

        #3. Press the [c] button to configure the compilation options

        #4. Change the CMAKE_INSTALL_PREFIX value to /usr/local/antsbin

        #5. First press the [c] and than the [g] button to generate the code
        
        #6. Now everything is set up to compile the code
        make -j 4

        #7. Now you're ready to install ANTs with the following commands:
        cd ANTS-build/
        sudo make install

        #8. Use the following command to copy important scripts from
        #   the ANTs folder 'stnava-ANTs-b4eb279/Scripts' into the folder
        #   where you've stored the ANTs binaries
        sudo cp ~/Downloads/stnava-ANTs-b4eb279/Scripts/* /usr/local/antsbin/bin/

        #9. Now that everything is done you can delete the temporary folder
        #   'stnava-ANTs-b4eb279' again.

5. Just one last thing before your can run ANTs, add the following lines to your ``.bashrc`` file:

    .. code-block:: sh

        #ANTs
        export PATH=/usr/local/antsbin/bin:$PATH
        export ANTSPATH=/usr/local/antsbin/bin/


AFNI
====================

.. image:: _static/logo/logoAFNI.png
   :width: 70pt
   :align: left

`AFNI <http://afni.nimh.nih.gov/afni>`_ is an open source software package specialized on the analysis of functional MRI. To see a list of all AFNI algorithms that can be used with Nipype go to `interfaces.afni.preprocess <http://nipy.sourceforge.net/nipype/interfaces/generated/nipype.interfaces.afni.preprocess.html>`_.

If you've installed the NeuroDebian repository, just use the following command to install AFNI on your system: ``sudo apt-get install afni``

To be able to run AFNI make sure to add the following lines of code to your ``.bashrc`` file:

.. code-block:: sh

    #AFNI
    export PATH=/usr/lib/afni/bin:$PATH


Additional interfaces
====================

There are many additional interfaces, such as `Camino <http://cmic.cs.ucl.ac.uk/camino/>`_, `MRtrix <http://www.brain.org.au/software/mrtrix/index.html>`_, `Slicer <http://slicer.org/>`_, `ConnectomeViewer <http://www.connectomics.org/viewer/>`_, for which I haven't created an installation guide yet. This is also due to my lack of knowledge about them. Feel free to help me to complete this list.


=========================
Clean up your System
=========================

Now that everything is downloaded and installed, make sure that everything is correctly updated with the following command:

.. code-block:: sh

    #Update and upgrade your system
    sudo apt-get update && sudo apt-get upgrade

    #Optional 1: Upgrade your distribution with 
    sudo apt-get dist-upgrade

    #Optional 2: Clean your system and remove unused packages
    sudo apt-get autoremove && sudo apt-get autoclean
    sudo apt-get remove && sudo apt-get clean


=========================
Test your System
=========================

Nipype is installed, recommended interfaces are ready to go and so are you. But before you want to start your first steps with Nipype, I recommend you to test your system first. To do this open up an IPython environment (open a terminal and start IPython with the command ``ipython``) and run the following code:

.. code-block:: py

    # Import the nipype module
    import nipype

    # Optional: Use the following lines to increase verbosity of output
    nipype.config.set('logging', 'workflow_level',  'CRITICAL')
    nipype.config.set('logging', 'interface_level', 'CRITICAL')
    nipype.logging.update_logging(nipype.config)

    # Run the test: Increase verbosity parameter for more info
    nipype.test(verbose=0) 

This test can take some minutes but if all goes well you will get an output more or less like this:

.. code-block:: py

    Ran 7454 tests in 71.160s

    OK (SKIP=10)
    Out[7]: <nose.result.TextTestResult run=7454 errors=0 failures=0>

Don't worry if some modules are being skipped or some side modules show up as errors or failures during the run. As long as no main modules cause any problems, you're fine. The number of tests and time will vary depending on which interfaces you have installed on your system. But if you receive an ``OK``, ``errors=0`` and ``failures=0`` then everything is ready.

**Congratulation! You now have a system with a fully working Nipype environment. Have fun!**

.. note::

    The first time I used MATLAB in Nipype I got the following error message:

    .. code-block:: none

       Standard error:
       MATLAB code threw an exception:
       SPM not in matlab path
       File:/home/username/workingdir/sliceTiming/pyscript_slicetiming.m
       Name:pyscript_slicetiming
       Line:6
       Return code: 0
       Interface MatlabCommand failed to run. 
       Interface SliceTiming failed to run. 

    As mentioned in the error message `SPM not in matlab path`, Nipype can't find the path to SPM. To change that, you can either add ``addpath /usr/local/MATLAB/R2014a/toolbox/spm12b`` to your ``startup.m`` file, stored at ``~/matlab/startup.m`` or add the following line of code at the beginning of your Nipype script:

        .. code-block:: py

            from nipype.interfaces.matlab import MatlabCommand
            MatlabCommand.set_default_paths('/usr/local/MATLAB/R2014a/toolbox/spm12b')
