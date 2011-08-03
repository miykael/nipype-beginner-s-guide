"""
Prepare modules and important variables
"""
import os                                    # system functions
import nipype.interfaces.freesurfer as fs    # freesurfer
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
  
#Specification of the folder where the dicom-files are located at
experiment_dir = '~SOMEPATH/experiment'
  
#Specification of a list containing the identifier of each subject
subjects_list = ['subject1','subject2','subject3','subject4']

#Specification of the output folder - where the T1 file can be found
data_dir_name = 'data'
 
#Node: SubjectData - we use IdentityInterface to creat our own node, to specify
#      the list of subjects the pipeline should be executed on
infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                                                      name="infosource")
infosource.iterables = ('subject_id', subjects_list)
 
#Node: Recon-All - to generate surfaces and parcellations of structural
#                  data from anatomical images of a subject.
reconall = pe.Node(interface=fs.ReconAll(), name="reconall")
reconall.inputs.directive = 'all'

#Because the freesurfer_data folder doesn't exist yet
os.system('mkdir %s'%experiment_dir+'/freesurfer_data')

reconall.inputs.subjects_dir = experiment_dir + '/freesurfer_data'
T1_identifier = 'struct.nii' #This is the name we manually gave the T1-file


"""
Implement pipeline and connect its components
"""
#implementation of the workflow   
reconflow = pe.Workflow(name="reconflow")
reconflow.base_dir = experiment_dir + '/workingdir_reconflow'
  
#defenition of the pathfinder function
def pathfinder(subject, foldername, filename):
    import os
    experiment_dir = '~SOMEPATH/experiment/experiment'
    return os.path.join(experiment_dir, foldername, subject, filename)

#connection of the nodes
reconflow.connect([(infosource, reconall,[('subject_id', 'subject_id')]),
                   (infosource, reconall,[(('subject_id', pathfinder, data_dir_name,
                                            T1_identifier),'T1_files')]),
                   ])

#run the recon-all pipeline (as recommended in serial mode)
reconflow.run(plugin='Linear')
  
#to delete the workingdir of the reconflow we use again the shell-command "rm".
#The important recon-all files are already stored in the "freesurfer_data" folder
os.system('rm -rf %s'%reconflow.base_dir)

