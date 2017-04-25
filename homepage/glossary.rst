========
Glossary
========

This Glossary wasn't created by myself. Its content is almost exclusively from the `Imaging Knowledge Base - Glossary <http://mindhive.mit.edu/node/71>`_ from the `Gabrieli Lab at MIT <http://gablab.mit.edu/>`_. It is my thanks to them, for generating such an exhaustive Glossary.

**Index**: A_ | B_ | C_ | D_ | E_ | F_ | G_ | H_ | I_ | J_ | K_ | L_ | M_ | N_ | O_ | P_ | Q_ | R_ | S_ | T_ | U_ | V_ | W_ | X_ | Y_ | Z_ | Numbers_

.. note::

    To help me to extend this glossary, please feel free to leave a comment at the bottom to recommend additions and to clear misapprehension.


A
=

AC-PC, AC-PC line
*****************
Stands for "anterior commissure-posterior commissure." Used to describe the hypothetical line between the anterior commissure (a frontal white matter tract used as the origin of the Talairach coordinate system) and the posterior commissure (another white matter tract in the midbrain). A brain which is properly aligned to Talairach space has the line between the AC and the PC as exactly horizontal.

affine
******
In fMRI, a term for certain types of spatial transformations which add together linearly. From `Mathworld <http://mathworld.wolfram.com/AffineTransformation.html>`_: "An affine transformation is any transformation that preserves collinearity (i.e., all points lying on a line initially still lie on a line after transformation) and ratios of distances (e.g., the midpoint of a line segment remains the midpoint after transformation)." This includes all translations, rotations, zooming, or shearing (think 'squeezing' one end of a square such that it becomes a trapezoid). Importantly, affine transformations affect the whole image; no affine transformation can tweak one local part of an image and leave the rest exactly the same. The first step in SPM's normalization process is affine, generally followed by nonlinear normalization.

anatomical ROI
**************
A region of interest (ROI) in the brain that is constructed from anatomical data (as opposed to functional activation data). Any ROI that is an anatomical structure in the brain - the inferior frontal gyrus, the amygdala, the posterior half of BA 32 - is an anatomical ROI.

anisotropic
***********
The opposite of isotropic_. In other words, *not* the same size in all directions. Anisotropy (the degree of anisotropic-ness) is one measure used in `Diffusion Tensor Imaging (DTI)`_ to determine the direction of white-matter fibers. A `smoothing kernel`_ or voxels_ can also be anisotropic.

ANOVA
*****
Stands for ANalysis Of VAriance. A standard statistical tool used to find differences between the distributions of several groups of numbers. Differs from simpler tests like the t-test in that it can test for differences among many groups, not just two groups. The standard ANOVA model is used in neuroimaging primarily at the group level, to test for differences between several groups of subjects. However, the ANOVA is essentially the same thing as an F-test (test of the F-statistic), which is often used at the individual level as well to test several linear constraints on a model simultaneously. Check out `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ for more info on group testing, and `Contrasts FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#contrasts>`_ for more info on F-tests.

AR(1)
*****
**AR(1) or AR(1) + w (or (AR(2), AR(3), etc.)**: Terms used to describe different models of autocorrelation_ in your fMRI data. See autocorrelation_ below for more info. AR stands for autoregression. AR models are used to estimate to what extent the noise at each time point in your data is influenced by the noise in the time point (or points) before it. The amount of autocorrelation of noise is estimated as a model parameter, just like `beta weights`_. The difference between AR(1), AR(2), AR(1) + w, etc., is in which parameters are estimated. An AR(1) model describes the autocorrelation function in your data by looking only at one time point before each moment. In other words, only the correlation of each time point to the first previous time point is considered. In an AR(2) model, the correlation of each time point to the first previous time point and the second previous time point is considered; in an AR(3) model, the three time points before each time point are considered as parameters, etc. The "w" in AR(1) + w stands for "white noise." An AR(1) + w model assumes the value of noise isn't solely a function of the previous noise; it also includes a random white noise parameter in the model. AR(1) + w models, which are used in SPM2 and other packages, seem to do a pretty good job describes the "actual" fMRI noise function. A good model can be used to remove the effects of noise correlation in your data, thus validating the assumptions of the general linear model. See `Temporal Filtering FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#temporal-filtering>`_ for more info.

artifact
********
Essentially any noise in the fMRI signal that's localized in either space or time is generally referred to as an artifact. Common artifacts are caused by head motion, physiological motion (cardiac, respiration, etc.), or problems in the scanner itself.

autocorrelation
***************
One major problem in the statistical analysis of fMRI data is the shape of fMRI noise. Analysis with the `general linear model (GLM)`_ assumes each timepoint is an independent observation, implying the noise at each timepoint is independent of the noise at the next timepoint. But several empirical studies have shown that in fMRI, that assumption's simply not true. Instead, the amount of noise at each timepoint is heavily correlated with the amount of noise at the timepoints before and after. fMRI noise is heavily "autocorrelated," i.e., correlated with itself. This means that each timepoint isn't an independent observation - the temporal data is essentially heavily smoothed, which means any statistical analysis that assumes temporal independence will give biased results.

The way to deal with this problem is pretty well-established in other scientific domains. If you can estimate what the autocorrelation function is - in other words, what, exactly, is the degree of correlation of the noise from one timepoint to the next - than you can remove the amount of noise that is correlated from the signal, and hence render your noise "white," or random (rather than correlated). This strategy is called `pre-whitening`_, and is referred to in some fMRI packages as autocorrelation correction. The models used to do this in fMRI are mostly `AR(1)`_ + w models, but sometimes more complicated ones are used. See `Basic Statistical Modeling FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#basic-statistical-modeling>`_ for more info on autocorrelation correction.


B
=

B-spline, B-spline interpolation
********************************
A type of spline which is the generalization of the Bezier curve. Don't know what I'm talking about? Neither do I. The nice folks at `MathWorld - Wolfram <http://mathworld.wolfram.com/>`_ have this to say about them: `B-Spline <http://mathworld.wolfram.com/B-Spline.html>`_. Essentially, though, a B-spline is a type of easily describable and computable function which can take many locally smooth but globally arbitrary shapes. This makes them very nice for interpolation. SPM2 has ditched sinc interpolation in all of its resampling/interpolation functions (like normalization or coregistration - anything involving resampling and/or reslicing). Instead, it's now using B-spline interpolation, improving both computational speed and accuracy.

band-pass filter
****************
The combination of a `high-pass filter`_ and `low-pass filter`_. Band-pass filters only allow through a certain "band" of frequencies, while attenuating or knocking out everything outside that band. A well-designed band-pass filter would be great for fMRI experiments, because fMRI experiments generally have most of their frequencies in a certain band that's separable from the frequencies of fMRI noise. So if you could focus a band-pass filter on your experimental frequencies, you could knock out almost all of your noise. In practice, though, it's tricky to design a really good band-pass filter, and since most of the noise in fMRI is low-frequency, using only a high-pass filter works almost as well as band-pass filtering.

baseline
********
A) The point from which deviations are measured. In a signal measure like % signal change, the baseline value is the answer to, "Percent signal change *from what?*" It's the zero point on a % signal change plot.

B) A condition in your experiment that's intended to contain all of the cognitive tasks of your experimental condition - except the task of interest. In fMRI, you generally can only measure differences between two conditions (not anything absolute about one condition). So an fMRI baseline task is one where the person is doing everything you're not interested in, and not doing the thing you're interested in. This way you can look at signal during the baseline, subtract it from signal during the experimental condition, and be left with only the signal from the task of interest. Designing a good baseline is crucially important to your experiment. Resting with the eyes open is a common baseline for certain types of experiment, but inappropriate for others, where cognitive activity during rest may corrupt your results. In order to get good estimates of the shape of your HRF, you need to have a baseline condition (as opposed to several experimental conditions). Check out `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ for more.

basis function
**************
One way to look for fMRI activation in the brain is to assume you know the exact shape of the HRF, and look for signals that match that shape. This is the most common way to analyze fMRI data. It suffers, though, in the case where the HRF may not be exactly the same shape from one subject, one region, or even one task, to the next - which we know is true to some degree. Another way is to assume you know nothing about the shape of the HRF and separately estimate its value at every timepoint at every voxel. This is a `FIR (Finite Impulse Response) model`_, and it's more common these days. But it suffers because it gives up many degrees of freedom in order to estimate a ton of parameters. A third way is to assume you know *something* about the shape of the response - maybe something as simple as "it's periodic," or something as complicated as "it looks kind of like one of these three or four functions here." This is the basis function approach, and the basis functions are the things you think "look" kind of like the HRF you want to estimate. They could be sines or cosines of different periods, which assumes very little about the shape except its periodicity, or they could be very-HRF looking things like the temporal and dispersion derivatives of the HRF. The basis function approach is kind of a middle way between the standard analysis and the FIR model. You only estimate parameters for each of your basis functions, so you get more power than the FIR model. But you aren't assuming you know the exact shape of your HRF, so you get more efficiency and flexibility than the standard analysis. You allow the HRF to vary somewhat - within the space defined by your basis functions - from voxel to voxel or condition to condition, but you still bring some prior knowledge about the HRF to bear to help you. Check out `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ and `HRF FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#hrf>`_ for more info on the basis function approach.

batch, batch script
*******************
Analysis programs with graphical interfaces are nice. But sometimes you don't want to have to push sixteen buttons and type in fourteen options to have to analyze every individual subject in your experiment. It takes a bunch of your time, and you'll probably screw it up and have to start over at some point. So many programs - SPM, AFNI, BrainVoyager - offer a "batch mode," where you can enter in the options you'd like in some sort of scripting language and then just set it to run the program in an automated function, according to the instructions in your batch script.

beta images
***********
Also called a parameter images. It's a voxel-by-voxel summary of the `beta weights`_ for a given condition. Usually it's written as an actual image file or sub-dataset, so you could look at it just like a regular brain image, exploring the beta weight at each voxel. In SPM, you get one of these written out for every column in your design matrix - one for each experimental effect for which you're estimating parameter values.

beta weights
************
Also called parameter weights, parameter values, etc. This is the value of the parameter estimated for a given effect / column in your design matrix. If you think of the general linear model as a multiple regression, the beta weight is the slope of the regression line for this effect. The parameter gets its name as a "beta" weight from the standard regression equation: Y = BX + E. Y is the signal, X is the design matrix, E is error, and B is a vector of beta weights, which estimate how much each column of the design matrix contributes to the signal. Beta weights can be examined, summed, and contrasted at the voxel-wise level for a standard analysis of fMRI results. They can also be aggregated across regions or correlated between subjects for a more region-of-interest-based analysis. Check out `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for more info on beta weights and ROIs.

block design
************
A type of experiment in which different types of trials are not intermixed randomly, but rather happen in blocks. So you might have 30 seconds in a row of condition A, followed by 30 seconds of condition B, followed by 30 seconds of A again, etc. Used even with shorter trials - that 30 seconds might be looking at a single flashing checkerboard, or it might be six trials of faces to look at. Block designs were the earliest type of design for fMRI and PET, and remain among the simpler designs to analyze and interpret. They have very high power, because the summing of HRF responses across repeated trials means you can often get higher peaks of activation during a block than for an isolated shorter trials. They suffer from very low efficiency (ability to estimate the shape of the HRF).

BOLD (blood oxygen level-dependent) signal
******************************************
This is the type of signal that is measured during an fMRI acquisitiom. Check out `Wikipedia's fMRI page <https://en.wikipedia.org/wiki/Functional_magnetic_resonance_imaging>`_ for a primer on fMRI signal, but the nutshell version is this: When neurons fire (or increase their firing rate), they use up oxygen and various nutrients. The brain's circulatory system responds by flooding the firing region with more highly-oxygenated blood than it needs. The effect is that the blood oxygen level in the activated region increases slightly. Oxygenated blood has a slightly different magnetic signature than de-oxygenated blood, due to the magnetic characteristics of hemoglobin. So with the right `pulse sequence`_, an MRI scanner can detect this difference in blood oxygen level. The signal that is thus read in fMRI is called BOLD, or blood oxygen level-dependent. MRI can be used to measure other things in the brain as well - perfusion_ being among them - but BOLD signal is the primary foundation of most fMRI research. Check out `Physiology and fMRI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#physiology-and-fmri>`_ for more details.

bootstrapping
*************
A statistics method used when you have to test a distribution without knowing much about its true underlying variance or mean or anything. The skeleton of the method is essentially to build up a picture of the possible space of the distribution by re-shuffling the elements it's made up of to form new, random distributions. Bootstrapping is widely used in many quantitative scientific domains, but it's only recently become of interest in neuroimaging analysis. Some papers have argued that under certain conditions, bootstrapping and other nonparametric ways of testing hypotheses make the most sense to test statistical hypotheses in fMRI. `Permutation test`_ is the neuroimaging concept most related to boostrapping, and it's explored in `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_.

Brodmann areas
**************
An area of the brain that is distinct at the cytoarchitectonic (cellular) level from those around it. There are 52 Brodmann areas, originally defined by Korbinian Brodmann. Many of them map onto various distinct anatomical structures, but many also simply subdivide larger gyri or sulci. Mark Dubin at the University of Colorado has a great map of the areas: `Brodmann map <http://spot.colorado.edu/~dubin/talks/brodmann/brodmann.html>`_. They are often used as `anatomical ROI`_, but be careful: they have significant variability from person to person in location and function. It's not clear how well functional activation maps onto most Brodmann areas. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for more.


C
=

canonical HRF
*************
A model of an "average" HRF. Intended to describe the shape of a generic HRF; given this shape and the design matrix, an analysis package will look for signals in the fMRI data whose shape matches the canonical HRF. The different analysis packages (SPM, AFNI, BrainVoyager, etc.) use slightly different canonical HRFs, but they all share the same basic features - a gradual rise up to a peak around six seconds, followed by a more gradual fall back to baseline. Some progams model a slight undershoot; some don't. See `HRF FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#hrf>`_ for more.

chronometry
***********
A technique in psychology in which the experimenter tries to figure out something about the processes underlying a task by the time taken to do the task and various portions of it. Some of the original chronometric experiments were done with reaction times, having subjects do various stages of an experiment to see whether some parameter might vary the reaction time for one stage and not another. Chronometric experiments have just started cropping up in fMRI. They attempt to determine not just the location of activations, but their sequence as well. This is generally done by getting an extremely accurate estimate of the shape of the HRF and exactly when it begins during the task. See `Mental Chronometry FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#mental-chronometry>`_ for more.

cluster
*******
A group of active voxels that are all adjacent, without any breaks. Clusters may include holes, but there has to be a contiguous link (vertical, horizontal or diagonal) from any voxel in the cluster to any other voxel in the cluster. Clusters are often taken to represent a set of neurons all involved in some single computation. They can also serve as the basis for `functional ROI`_.

coregistration
**************
The process of bringing two brain images into alignment ideally, you'd like them lined up so that their edges line up and the point represented by a given voxel in one image represents the same point in the other image. Coregistration generally refers specifically to the problem of aligning two images of different modalities - say, T1 fMRI images and PET images, or anatomical MRI scans and functional MRI scans. It goes for some of the same goals as realignment_, but it generally uses different algorithms to make it more robust. See `Coregistration FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#coregistration>`_ for more.

contrast image
**************
A voxel-by-voxel summary of the value of some contrast_ you've defined. This is often created as a voxel-by-voxel weighted sum of `beta images`_, with the weights given by the value of the contrast vector. In SPM, it's actually written out as a separate image file; in other programs, it's usually written as a separate sub-bucket or the equivalent. It shouldn't be confused with the statistic image, which is a voxel-by-voxel of the test statistic associated with each contrast value. (In SPM, those statistic images are labeled spmT or spmF images.) **Only the contrast images - not the statistic images - are suitable for input to a second-level group analysis**. See `Contrasts FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#contrasts>`_ for more info on contrasts, and `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ for more info on group analyses.

conjunction analysis
********************
A way of combining contrasts, to look for activations that are shared between two conditions as opposed to differing between two conditions. It's implemented in SPM and other packages as essentially a logical AND-ing of contrasts - a way of looking for all the areas that are active in *both* one contrast and another. It's tricky to implement at the group level, though. Look at `Contrasts FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#contrasts>`_ for more info, and possibly `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ as well.

contrast
********
The actual signal in fMRI data is unfortunately kind of arbitrary. The numbers at each voxel in your functional images don't have a whole lot of connection to any physiological parameter, and so it's hard to look at a single functional image (or set of images) and know the state of the brain. On the other hand, you can easily look at two functional images and see what's different between them. If those functional images are taken during different experimental conditions, and the difference between them is big enough, then you know something about what's happening in the brain during those conditions, or at least you can probably write a paper claiming you do. Which is good! So the fundamental test in fMRI experiments is not done on individual signal values or `beta weights`_, but rather on differences of those things. A contrast is a way of specifying which images you want to include in that difference. A given contrast is specified as a vector of weights, one for each experimental condition / column in your design matrix. The contrast values are then created by taking a weighted sum of `beta weights`_ at each voxel, where the weights are specified by the contrast vector. Those contrast values are then tested for statistical significance in a variety of ways. Check out `Contrasts FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#contrasts>`_ for more info on contrasts in fMRI.

cutoff period
*************
The longest length of time you want to preserve with your `high-pass filter`_. A high-pass filter attentuates low frequencies, or slow oscillations; everything that repeats with a period slower than two minutes, say, you might reject as being clearly unrelated to your experiment. The cutoff period would be two minutes in the example above; it's the longest length of time you could possibly be interested in for your experiment. You generally want to set it to be way longer than an individual trial or block, but short enough to knock out most of the low-frequency noise. See `Temporal Filtering FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#temporal-filtering>`_ for more.

cytoarchitectonic
*****************
Relating to the look/type/architecture of individual cells. Not all neurons look exactly the same, and they're not all organized in exactly the same way throughout the brain. You can look in the brain and find distinct places where the "type" of neuron changes from one to another. You might theorize that a cell-level architecture difference might relate to something difference in the functions subserved by those cells. That's exactly what Brodmann theorized, and his `Brodmann areas`_ are based on cytoarchitectonic boundaries he found in the brain. Check out `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for how cytoarchitectonic differences can be used


D
=

deconvolution
*************
A mathematical operation in which the values from one function are removed from the values of another. In fMRI, where the signal is generally interpreted to be the result of a neuronal timeseries (which is modeled by the design matrix) convolved with a hemodynamic response function (which is modeled by a `canonical HRF`_, `basis function`_, or a `FIR (Finite Impulse Response) model`_), the operation is usually used to separate the contributions of those two functions. SPM's `psychophysiological interaction (PPI)`_ function attempts to model the interaction of neuronal timeseries (as opposed to fMRI timeseries) by first deconvolving the canonical HRF and then checking the interaction at the neuronal, rather than hemodynamic level.

design matrix
*************
A model of your experiment and what you expect the neuronal response to it to be. In general represented as a matrix (funnily enough), where each row represents a time point / TR / functional image and each column represents a different experimental effect. It becomes the model in a multiple regression, following the vector equation: Y = BX + E. Y is a vector of length a (equal to nframes from the scanner), usually representing the signal from a single voxel. B is a vector of b, representing the effect sizes for each of b experimental conditions. E is an error vector the same length as Y. X is your design matrix, of size a x b. Check out `Basic Statistical Modeling FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#basic-statistical-modeling>`_ for more.

detrending
**********
There are multiple sources of noise in fMRI - head movement, transient scanner noise, gradual warming of the RF coils, etc. Many of them are simple, gradual changes in signal over the course of the session - a drift_ that can be linear, quadratic, or some higher polynomial that has very low frequency. Assuming that you don't have any experimental effect that varies linearly over the whole experiment, then, simply removing any very low-frequency drifts can be a very effective way of knocking out some noise. Detrending is exactly that - the removal of a gradual trend in your data. It often refers simply to linear detrending, where any linear effect over your whole experiment is removed, but you can also do a quadratic detrending, cubic detrending, or something else. Studies have shown that you're not doing much good after a quadratic detrending - most of the gradual noise is modeled well by a linear and/or quadratic function.

Diffusion Tensor Imaging (DTI)
******************************
A relatively newer technique in MRI that highlights white matter tracts rather than gray matter. It can be used to derive maps showing the prevailing direction of white matter fibers in a given voxel, which has given rise to a good deal of interest in using to derive connectivity data. Check out `Connectivity FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#connectivity>`_ for more.

dispersion derivative
*********************
The derivative with respect to the dispersion parameter in a gamma function. In SPM, the dispersion derivative of the `canonical HRF`_ looks a lot like the HRF but can be used as a `basis function`_, to model some uncertainty in how wide you expect the HRF to be at each voxel.

drift
*****
Some noise in an fMRI signal that is extremely gradual, usually varying linearly or quadratically over the course of a whole run of the scanner. This noise is usually called a drift, or a scanner drift. Sources of drifts are generally from the scanner - things like gradual warming of the magnet, gradual expansion of some physical element, etc. - but can also come from the subject, as in a gradual movement of the head downwards. Drifts often comprises a substantial fraction of the noise in a session, and can often be substantially removed by detrending_.

dropout
*******
The fMRI signal is contingent on having an extremely even, smooth, homogenous background magnetic field and a precisely calculated gradient field. If anything distorts the background field or the gradient field in a localized fashion, the signal in that region can drop to almost nothing due to the distortions. This is called dropout or signal dropout. This is most common in regions of high susceptibility_ - brain regions near air/tissue interfaces, where the differing magnetic signatures of the two materials causes major local distortions. In those regions, it's difficult to get much signal from the scanner, and `Signal-to-Noise Ratio (SNR)`_ shrinks drastically, meaning it's hard to find activations there. A good deal of research has been done to ameliorate dropout; recently, it's been shown spiral in-out imaging does a pretty good job avoiding dropout in the traditionally bad regions. See `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for more.

Dynamic Causal Modeling (DCM)
*****************************
A new statistical analysis technique for making inferences about `functional connectivity`_. It allows the user to specify a small set of `functional ROI`_ and a design matrix, and then given some data, produces a set of connectivity parameters. These parameters include both a "default" measure of connectivity between the ROIs, as well as a dynamic measure of how that connectivity changed across the experiment - specifically, whether any experimental effect changed the connectivity between regions. Has been used, for example, to investigate whether category effects in vision are modulated by bottom-up or top-down pathways. See `Connectivity FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#connectivity>`_ for much more.


E
=

Echo-planar Imaging (EPI)
*************************
A type of pulse sequence in which lines of `k-space`_ are sampled in order. This is the more conventionally-used pulse sequence around the world, and has some advantages over other sequences of being slightly easier to analyze and pretty fast. It is quite susceptible to various artifact_ and distortions, though. Check out `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for more.

EEG (Electroencephalogram)
**************************
Stands for electroencephalogram. A neuroimaging technique in which electrodes are pasted to the skull to directly record the electrical oscillations caused by neuronal activity - sometimes called "brain waves". Allows the recording of electrical activity at millisecond resolution, far better than PET or fMRI, but suffers from a lack of regional specificity, as it's extremely difficult to tell where in the brain a given EEG signal originated. The exact nature of the neuronal activity that gives rise to the EEG signal is not entirely clear, but active efforts are underway at several facilities to combine EEG and fMRI to try and get excellent spatial and temporal resolution in the same experiment. See also `Event-related Potential (ERP)`_ below.

effective connectivity
**********************
A term introduced by `Karl Friston <https://en.wikipedia.org/wiki/Karl_J._Friston>`_ in order to highlight the difference between "correlational" methods of inferring brain connectivity and the actual concept of causal connection between brain areas. The distinction made is one between correlation and causation. Effective connectivity (EC) stands in contrast to `functional connectivity`_, which goes more with correlation. EC between brain areas is defined as "the influence one neural system exerts over another either directly or indirectly." It doesn't imply a direct physical connection - simply a causative influence. It's a lot harder to establish that two regions are effectively connected than it is to establish that they're functionally connected, but EC supports more interesting inferences than FC does.

efficiency
**********
A statistical concept in experimental design, used to describe how accurately one can model the shape of a response. It's at the other end of a tradeoff with power_, which is used to describe how well you can detect any effect at all. Block experiments are very low in efficiency; because the trials come on top of each other, it's difficult to tell how much signal comes from one trial and how much from another, so the shape is muddled. Fully-randomized event-related experiments have high efficiency; you can sample many different points of the HRF and know exactly which HRF you're getting. Experiments that have very high power must necessarily have lower efficiency - you can't be perfect at both. Check `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ our for more on the efficiency/power tradeoff. Also check out `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_ for how to maximize efficiency in your experiment.

Event-related Potential (ERP)
*****************************
A variation on EEG in which you focus not on the ongoing progression of activity, but rather electrical activity in response to a particular stimulus (or lack thereof). Instead of looking at a whole EEG timecourse or frequency spectrum, you take a small window of time (1 second, say) after each presentation of a trial A, and average those windows together to get the average response to your stimulus A. This creates a `peristimulus timecourse`_, not unlike that for an HRF in fMRI. You can then compare the time-locked average from one condition to that from another condition, or analyze a single time-locked average for its various early and late components. ERPs and the advent of a `event-related design`_ in fMRI allow the same designs to be used in both EEG and fMRI, presenting the promise of combining the two into one super-imaging modality which will grow out of control and destroy us all. Or not.

event-related design
********************
An experimental design in which different trial types are intermixed throughout the experiment, usually in random or pseudo-random fashion. Contrasts with a `block design`_, where trials of the same type are collected into chunks. Event-related designs sacrifice power_ in exchange for higher efficiency_, as well as psychological unpredictability, which allow new kinds of paradigms in fMRI. Check out `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ for way more about event-related designs, and `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_ for why randomization is all the rage amongst the kiddies.


F
=

F-contrast
**********
A type of contrast_ testing a F-statistic, as opposed to a t-statistic or something else. Allows you to test several linear constraints on your model at once, joining them in a logical OR. In other words, it would allow you to test the hypothesis that A and B are different OR A and C are different OR B and C are different at a given voxel. Another way of describing that would be to say you're testing whether there are any differences among A, B and C at all. F-contrasts can be tricky (if not impossible) to bring forward to a random-effects group analysis. See `Contrasts FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#contrasts>`_ and `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ for more.

False Discovery Rate (FDR)
**************************
A statistical concept expressing the fraction of accepted hypotheses in some large dataset that are false positives. The idea in controlling FDR instead of `Family-wise error correction (FWE)`_ is that you accept the near-certainty of a small number of false positives in your data in exchange for a more liberal, flexible, reasoned correction for multiple comparisons. Since most researchers accept the likelihood of a small amount of false positives in fMRI data anyways, FDR control seems like an idea whose time may have arrived in neuroimaging. Check out `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_ for more.

Family-wise error correction (FWE)
**********************************
In a dataset of tens of thousands of voxels, how do you decide on a statistical threshold for true activation? The scientific standard of setting the statistic such that p < 0.05 isn't appropriate on the voxel level, since with tens of thousands of voxels you'd be virtually guaranteed hundreds of false positives - voxels whose test statistic was highly improbably just by chance. So you'd like to correct for multiple comparisons, and you'd like to do it over the whole data set at once - correcting the family-wise error. Family-wise error correction methods allow you to set a global threshold for false positives; if your family-wise threshold is p < 0.05, you're saying there's a 95% chance there are NO false positives in your dataset. There are several accepted methods to control family-wise error:  Bonferroni, various Bonferroni-derived methods, `Gaussian random field`_, etc. FWE stands in contrast to `False Discovery Rate (FDR)`_ thresholding, which threshold the *number* of false positives in the data, rather than the chance of *any* false positives in the data. See `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_ for more.

FIR (Finite Impulse Response) model
***********************************
A type of design matrix which assumes nothing about the shape of the `Hemodynamic Response Function (HRF)`_. With an FIR model, you don't convolve your design matrix with a `canonical HRF`_ or any `basis function`_. Instead, you figure out how long an HRF you'd like to estimate - maybe 10 or 15 TRs following your stimulus. You then have a separate column in your design matrix for every time point of the HRF for every different condition. You separately estimate `beta weights`_ for every time point, and then line them up to form the timecourse of your HRF. The advantage is that you can separately estimate an unbiased HRF at every voxel for every condition - tremendous flexibility. The disadvantage is that the confidence in any one of your estimates will drop, because you use so many more degrees of freedom in estimation. Full FIR models may not be useable for very complex experiments or certain types of designs. Check out `Percent Signal Change FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#percent-signal-change>`_ for more on FIR models.

fishing expedition
******************
What happens when your data doesn't really offer any compelling or interpretable story about your task... so you try every conceivable way of analyzing it and every conceivable contrast possible to find something interesting looking. Then, of course, it behooves you to write your paper as if you'd been looking for that all along.

fixed-effects
*************
An analysis that assumes that the subjects (or scanning sessions, or scanner runs, or whatever) you're drawing measurements from are fixed, and that the differences between them are therefore not of interest. This allows you to lump them all into the same design matrix, and consider only the variance between timepoints as important. This allows you to gain in power, due to the increased number of timepoints you have (which leads to better estimates and more degrees of freedom). The cost is a loss of inferential power - you can only make inferences in this case about the actual group of subjects (or scanner sessions, or whatever) that you measured, as opposed to making inferences about the population from which they were drawn. Making population inferences requires analyzing the variance between subjects (/scanner/sessions... you get the idea) and treating them as if they were drawn randomly from a population - in other words, a random-effects analysis. Check out `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ for more.

fixed ISI
*********
Stands for fixed inter-stimulus interval. A type of experiment in which the same time separates the beginning of all stimuli - trials needn't be all exactly the same length, but the onsets of stimuli are all separated by exactly the same amount of time. `Event-related design`_ or `block design`_ experiments can be fixed ISI. fixed ISI event-related experiments, though, are pretty bad at both efficiency_ and power_, especially as the ISI increases. In general, several empirical studies have shown that for event-related designs, `variable ISI`_ is the way to go. For block designs, the difference is fairly insignificant, and variable ISI can make the design less powerful, depending on how it's used. See `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_ for more on the difference between fixed and variable.

flattening
**********
One inconvenient thing about mapping the brain is the way that it's all folded and scrunched into that little head like so much wadded-up tissue. Voxels that appear to be neighboring, for example, might in fact be widely separated on the cortical sheet, but have that distance obscured by the folds of a gyrus in between them. In order to study the spatial organization of a particular cortical region, it may then be useful to "unfold" the brain and look at it as if the cortical sheet had been flattened out on a table. Indeed, some phenomena like retinotopy are near-impossible to find without cortical flattening. Several software packages, then, allow you to create a surface map of the brain - a 3D graphical representation fo the cortical surface - and then apply several automated algorithms to flatten it out, and project your functional activations onto the flattened representation. FreeSurfer is best known for this type of analysis.

fMRI
****
Stands for functional magnetic resonance imaging. The small 'f' is used to distinguish functional MRI, often used for scanning brains, from regular old static MRI, used for taking pictures of knees and things. Check out `Physiology and fMRI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#physiology-and-fmri>`_ for more info on the physics and theory behind fMRI, or `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for useful (with any luck) answers about how to set parameters for your experiment.

FreeSurfer
**********
`FreeSurfer <http://freesurfer.net/>`_ is a brain imaging software package developed by the Athinoula A. Martinos Center for Biomedical Imaging at Massachusetts General Hospital for analyzing MRI data. It is an important tool in functional brain mapping and facilitates the visualization of the functional regions of the highly folded cerebral cortex. It contains tools to conduct both volume based and surface based analysis, which primarily use the white matter surface. FreeSurfer includes tools for the reconstruction of topologically correct and geometrically accurate models of both the gray/white and pial surfaces, for measuring cortical thickness, surface area and folding, and for computing inter-subject registration based on the pattern of cortical folds. In addition, an automated labeling of 35 non-cortical regions is included in the package. (Taken from `Wikipedia: FreeSurfer <https://en.wikipedia.org/wiki/FreeSurfer>`_)

FSL (FMRIB Software Libraryand)
*******************************
`FSL <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSL>`_ is a comprehensive library of analysis tools for fMRI, MRI and DTI brain imaging data. It runs on Apple and PCs (both Linux, and Windows via a Virtual Machine), and is very easy to install. Most of the tools can be run both from the command line and as GUIs. For an overview of the algorithms included in FSL go to the `overview section <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslOverview>`_ on their homepage.

Fourier basis set
*****************
A particular and special type of `basis function`_. Instead of using a standard `design matrix`_, an analysis with a Fourier basis set simply uses a set of sines or cosines of varying frequency for the design matrix columns for each condition. Because a combination of cosines can be used to model almost any periodic function at all, this design matrix is extremely unbiased - in particular as to when your activations took place, since you don't have to specify any onsets. You simply let your software estimate the best match to the period parts of your signal (even if they're infrequent). This allows you, like an `FIR (Finite Impulse Response) model`_, to estimate a separate HRF for every voxel and every condition, as well as come up with detailed maps of onset lag at each voxel and other fun stuff. The disadvantages of this model include relatively lower power, due to how many degrees of freedom are used in the basis set, and some limitations on what functions can be modeled (edge effects, etc.) It also requires you to use an `F-contrast`_ to test it, since the individual parameters have no physiological interpretation.

functional connectivity
***********************
A term introduced by `Karl Friston`_ to highlight the differences between "correlational" methods of inferring brain connectivity and the causational concepts and inferences that you might want to make. The difference is between correlation and causation; functional connectivity is more correlational. Brain regions which are functionally connected merely must have some sort of correlation in their signal, rather than having any direct causal influence over each other. This is in contrast to `effective connectivity`_, which demands some causation be included. Functional connectivity is rather easier to establish, but supports perhaps less interesting inferences. Most methods out there looking at connectivity are good only for functional connectivity, with TMS being a notable exception. See `Connectivity FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#connectivity>`_ for more.

functional ROI
**************
Any region-of-interest (ROI) that is generated by looking at functional brain activation data is considered a functional ROI. It may also have reference to anatomical information; you may be looking for all active voxels within the amygdala, say. That would be both an anatomical and functional ROI. Any subsset of voxels generated from a list of functionally active voxels, though, can comprise a functional ROI. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for ways you can use 'em.


G
=

Gaussian random field
*********************
Whoo, that's a heck of a way to start a letter. Essentially, a type of `random field <https://en.wikipedia.org/wiki/Random_fields>`_ that satisfies a Gaussian distribution, I guess. As it applies to fMRI, the key thing to know is that SPM's default version of `Family-wise error correction (FWE)`_ operates by assuming your test statistics make up a Gaussian random field and are therefore subject to several inferences about their spatial distribution. FWE correction based on Gaussian random fields has been shown to be conservative for fMRI data that has not been smoothed rather heavily. See `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_ for more info.

general linear model (GLM)
**************************
The general linear model is a statistical tool for quantifying the relationship between several independent and several dependent variables. It's a sort of extension of multiple regression, which is itself an extension of simple linear regression. The model assumes that the effects of different independent variables on a dependent variable can be modeled as linear, which sum in a standard linear-type fashion. THe standard GLM equation is Y = BX + E, where Y is signal, X is your `design matrix`_, B is a vector of `beta weights`_, and E is error unaccounted for by the model. Most neuroimaging software packages use the GLM as their basic model for fMRI data, and it has been a very effective tool at testing many effects. Other forms of discovering experimental effects exist, notably non-model-based methods like `principal components analysis (PCA)`_. Check out `Basic Statistical Modeling FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#basic-statistical-modeling>`_ for more info on how the GLM is used in fMRI analysis.

GitHub
******

`GitHub <https://github.com/>`_ is a Git repository web-based hosting service that offers distributed revision control and source code management (SCM). GitHub is a web-based graphical interface that allows programmers to develope and contribute code together. For more, see `Wikipedia's GitHub page <https://en.wikipedia.org/wiki/GitHub>`_ or go to the `offical homepage <https://github.com/>`_.

global effects
**************
Any change in your fMRI signal that affects the whole brain (or whole volume) at once. Sources of these effects can be external (scanner drift_, etc.) or physiological (motion, respiration, etc.). They are generally taken to be non-neuronal in nature, and so generally you'd like to remove any global effects from your signal, since it's extremely unlike to be caused by any actual neuronal firing. See `Physiology and fMRI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#physiology-and-fmri>`_ and `Realignment FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#realignment>`_ for thoughts on how to account for global effects in your dataset.

global scaling
**************
An analysis step in which the voxel values in *every image* are divided by the global mean intensity of *that image*. This effectively makes the global mean identical for every image in the analysis. In other words, it effectively removes any differences in mean global intensity between images. This is different than `grand mean scaling`_! Global scaling (also called proportional scaling) was introduced in PET, where the signal could vary significantly image-to-image based on the total amount of cerebral blood flow, but it doesn't make very much sense to do generally in fMRI. The reason is because if your activations are large, the timecourse of your global means may correlate with your task - if you have a lot of voxels in the brain going up and down with your task, your global mean may well be going up and down with your task as well. So if you divide that variation out by scaling, you will lose those activations and possibly introduce weird negative activations! There are better ways to take care of `global effects`_ in fMRI (see `Physiology and fMRI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#physiology-and-fmri>`_ for some), considering that moment-to-moment global variations are very small in fMRI compared to PET. They can be quite large session-to-session, though, so `grand mean scaling`_ is generally a good idea.

grand mean scaling
******************
An analysis step in which the voxel values in every image are divided by the average global mean intensity of the *whole session*. This effectively removes any mean global differences in intensity between sessions. This is different than `global scaling`_! This step makes a good deal of sense in fMRI, because differences between sessions can be substantial. By performing it at the first (within-subject) level, as well, it means you don't have to do it at the second (between-subject) level, since the between-subject differences are already removed as well. This step is performed by default by all the major analysis software packages.

Granger causality, Granger causality modeling
*********************************************
A statistical concept imported from econometrics intended to provide some new leverage on tests of `functional connectivity`_. Granger causality is somewhat different from regular causality; testing Granger causality essentially boils down to testing whether information about the values or lagged values of one timecourse give you any ability to predict the values of another timecourse. If they do, then there's some degree of Granger causality. The concept is still somewhat controversial in econometrics, and the same goes for neuroimaging. What's clear is the test is still effectively a correlational test, though far more sophisticated than just a standard cross-correlation. So establishing Granger causality between regions is enough to establish `functional connectivity`_ and some degree of temporal precedence, but probably not enough to establish `effective connectivity`_ between those regions. Check out `Connectivity FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#connectivity>`_ for more.


H
=

hand-waving
***********
An explanatory technique frequently used in fMRI research to obscure the fact that no one really knows what the hell is going on.

Hemodynamic Response Function (HRF)
***********************************
When a set of neurons in the brain becomes more active, the brain responds by flooding the area with more highly-oxygenated blood, enabling an MRI scanner to detect the `BOLD (blood oxygen level-dependent) signal`_ contrast in that region. But that "flooding" process doesn't happen instantaneously. In fact, it takes a few seconds following the onset of neuronal firing for BOLD signal to gradually ramp up to a peak, and then several more seconds for BOLD signal to diminish back to baseline, possibly undershooting the baseline briefly. This gradual rise followed by gradual fall in BOLD signal is described as the hemodynamic response function. Understanding its shape correctly is crucial to analyzing fMRI data, because the neuronal signals you're looking to interpret aren't directly present in the data; they're all filtered through this temporally extended HRF. A great deal of statistical thought and research has gone into understanding the shape of the HRF, how it sums over time and space, and what physiological processes give rise to it. Check out `HRF FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#hrf>`_ for more about how it's modeled in fMRI analysis.

hierarchical model
******************
A type of `mixed-effects`_ model in which both random and fixed effects are modeled but separated into different "compartments" of "levels" of the modeling. The standard group model approach in fMRI is hierarchical - you model all the fixed (within-subjects) effects first, then enter some summary of those fixed effects (the `beta weights`_ or `contrast image`_) into a `random-effects`_ model, where all the random (between-subject) effects are modeled. This allows separate treatment of the between- and within-subject variance. Check out `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ for more info.

high-pass filter
****************
A type of frequency filter which "passes through" high frequencies and knocks out low frequencies. Has the effect, therefore, of reducing all very low frequencies in your data. Since fMRI noise is heavily weighted towards low frequencies, far lower than the frequencies of common experimental manipulations, high-pass filters can be a very effective way of removing a lot of fMRI noise at little cost to the actual signal. Setting the `cutoff period`_ is of crucial importance in high-pass filter construction. Contrasts with `low-pass filter`_ and `band-pass filter`_. See `Temporal Filtering FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#temporal-filtering>`_ for more info.


I
=

Impulse Response Function (IRF)
*******************************
In linear systems theory, you can predict a system's response to any arbitrary stimulus if you a) assume that its response to stimuli obeys certain assumptions about linearity (summation, etc.) and b) you know how the system responds to a single instantaneous impulse stimulus. The system's response in this case is called the IRF, or impulse response function. Many analyses - the `general linear model (GLM)`_, primarily - of the brain's response to stimuli proceed along linear systems methods, assuming that the IRF is equivalent to the hemodynamic response function (HRF). This HRF can be measured or simply assumed. IRF and HRF are sometimes used interchangeably in fMRI literature.

Independent Components Analysis (ICA)
*************************************
A statistical technique for analyzing signals that are presumed to have several independent sources mixed into the single measure signal. In fMRI, it's used as a way of analyzing data that doesn't require a model or `design matrix`_, but rather breaks the data down into a set of statistically independent components. These components can be then (hopefully) be localized in space in some intelligible way. This enables you, theoretically, to *discover* what effects were "really" present in your experiment, rather than hypothesizing the existence of some effects and testing the significance of your hypothesis. It's been used more heavily in `EEG (Electroencephalogram)`_ research, but is beginning to be applied in fMRI, although not everything about the results it gives is well understood. Its use in artifact_ detection is clear, though. It differs from `principal components analysis (PCA)`_, an algorithm with similar goals, because the components it chooses have maximal statistical independence, rather than maximizing the explained variance of the dataset.

inflation
*********
Related to flattening_. A downer about superimposing activation results on the brain is that brains are kind of inconveniently wrinkled up. This makes it difficult to see the exact spatial relationship of nearby activations. Two neighboring voxels might well be separated by a large distance on the cortical sheet, but one is buried deep in a sulcus and one is on top of a gyrus. Inflation and flattening are visualization techniques that aim to work around that problem. Inflation works by first doing `surface mapping`_ to construct a 3-D model of the subject's cortical surface, and then applies graphics techniques to slowly blow up the brain, as if inflating it. This gradually reduces the wrinkling, spreading out the sulci and gyri until, ultimately, you could inflate the brain all the way to spherical shape. Usually inflation stops when most of the smaller sulci and gyri are flattened out, as this allows much nicer visualization of phenomena like retinotopy.

Interfaces
**********
Interfaces in the context of Nipype are program wrappers that allow Nipype which runs in Python_ to run a program or function in any other programming language. As a result, Python_ becomes the common denominator of all neuroimaging software packages and allows Nipype to easily connect them to each other. For a full list of software interfaces supported by Nipype go `here <http://nipype.readthedocs.io/en/latest/documentation.html>`_. For more see the `introduction section of this beginner's guide <http://miykael.github.io/nipype-beginner-s-guide/nipype.html#interfaces>`_.

Inter-stimulus Interval (ISI)
*****************************
The length of time in between trials in an experiment. Usually measure from the onset of one trial to the onset of the next. The length and variability of your ISI are crucial factors in determing how much power_ and efficiency_ your experimental design provide, and thus how nice your results will look. See `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ and `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_ for info about figuring out the proper length of your ISI.

IPython
*******
`IPython <http://ipython.org/>`_ is an interactive interpreter for the Python_ language. At the beginning it was only a command shell but with time and with the introduction of `Jupyter Notebook <http://jupyter.readthedocs.org/en/latest/>`_ becomes more and more the best Python_ computational environment at hand. IPython is capable to compute in multiple programming languages and offers enhanced introspection, rich media, additional shell syntax, tab completion, and rich history. For more, go to `IPython's offical homepage <http://ipython.org/>`_.

isotropic
*********
The same size in all directions. A sphere is isotropic. An ovoid is not. Isotropy is the degree to which something is isotropic. Smoothing kernels are often isotropic, but they don't have to be - they can be anisotropic_. Voxels_ are often anisotropic originally, but are resample to be isotropic later in processing.


J
=

jittered
********
A term used to describe varying the `Inter-stimulus Interval (ISI)`_ during your experiment, in order to increase efficiency_ in the experimental design. Can also be used (although less frequently these days) to describe offsetting the TR by a small amount to avoid trial lengths being an exact multiple of the TR. Used as a noun - "I made sure there was some jitter in my design" - or a verb - "We're going to jitter this design a little." Check out `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_ for all the gory details.


K
=

k-space
*******
One way to take a 3-D picture would be to sample various points in space for the intensity of light there, and then reassemble those samples into a volume - an easy reassembly process, since the sampled intensity is exactly what you want to see. But that's not how MRI scanners take their pictures. Instead of sampling real space for the intensity of light at a given point, they sample what's called k-space. A given point in k-space describes both a frequency and a direction of oscillation. Very low frequencies correspond to slow oscillations and gradual changes in the picture at that direction; higher frequncies correspond to fast oscillations and sharp changes (i.e., edges) in the picture at that direction. The points in k-space don't correspond to any real-world location! They correspond only to frequency and direction. This is the space that MRI scanner samples. K-space can be sample in different patterns; these correspond to different `pulse sequence`_ at the scanner.

kernel
******
See `smoothing kernel`_.


L
=

linear drift
************
See drift_.

localizer
*********
One way of dealing with the sizeable differences in brain anatomy between subjects is to use an analysis that focuses on regions of interest, rather than individual voxels. The danger in using anatomically defined regions of interest is that the mapping between function and anatomy varies widely between subjects, so one subject might activate the whole calcarine sulcus during a visual stimulus and another might only activate a third of it. One way around this variability is to use functionally-defined regions of interest. A localizer task is one designed to find these functional ROI. The idea is to design a simple task that reliably activates a particular region in all or most subjects, and use the set of voxels activated by that localizer task as an ROI for analyzing another task. The simple task is called a localizer because it is designed to localize activation to a particular set of voxels within or around an anatomical structure. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for more on the region-of-interest approach.

long event-related designs
**************************
An experimental design in which single trials are the basic unit, and those single trials are separated by enough time to allow the `Hemodynamic Response Function (HRF)`_ to fully return to baseline before the next trial - usually 20-30 seconds. This design is a subtype of a `event-related design`_, contrasting with the other subtype, `rapid event-related designs`_. Long event-related designs have the advantage of being very straightforward to analyze, and incredibly easy to extract timecourses from. They have the disadvantage, though, of having many fewer trials per unit time than a `block design`_ or rapid event-related design, and so long event-related designs are both very low-powered and very inefficient. They're not widely used in fMRI any more, unless the experiment calls for testing assumptions about `Hemodynamic Response Function (HRF)`_ summation or something. See `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ for more.

low-pass filter
***************
A type of filter that "passes through" low frequencies and suppresses high frequencies. This has the effect of smoothing your data in the temporal (rather than spatial) domain - very fast little jiggles and quick jumps in the signal are suppressed and the timecourse waveform is smoothed out. If temporal-domain noise is random and independent across time, low-pass filtering helps increase `Signal-to-Noise Ratio (SNR)`_ ratio in the same way `spatial smoothing`_ does. But, unfortunately, fMRI temporal-domain noise is highly colored, and so low-pass filtering usually ends up suppressing signal. Check out `Temporal Filtering FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#temporal-filtering>`_ for lots more on the low-pass filtering controversy.


M
=

MapNode
*******
See Workflow_.

mask, mask image
****************
A special type of image file used in `SPM (Statistical Parametric Mappin)`_ (and other programs) which is used to specify a particular region of the brain. Every voxel in that region has intensity 1; everything outside of that region has intensity 0. Such an image is also called a binarized map. You might have a `Region of Interest (ROI)`_ mask, to specify the location of a ROI, or you might have a brain mask, where the mask shows you where all of the in-brain voxels are (so that you can analyze only the in-brain voxels, for example). Most ROI programs that create image files create masks. SPM standardly creates a mask image file based on intensity thresholds during model estimation, and only estimates voxels within its brain mask.

mat file (or dot-mat file, .mat file, etc.)
*******************************************
 1) A MATLAB_ file format which contains saved Matlab variables, and allows you to save variables to disk and load them into the workspace again from disk. Format is binary data, so it's not accessible with text editors.

2) One special kind of .mat file in SPM is the .mat file which can go along with a format .img/.hdr pair. A .mat file with the same filename as a .hdr/.img pair is interpreted in a special way by SPM; when that image file is read, SPM looks into the .mat file for a matrix specifying a position and orientation transform of the image. In this way, SPM can save a rigid-body transformation of the image (rotation, zoom, etc.) without actually changing the data in the .img file. Almost every SPM image-reading function automatically reads the .mat file if it's present, and many functions which move the image around (realignment_, `slice timing`_, etc.) give you the option to save the changes as a .mat file instead of actually re-slicing the image.

MATLAB
******
The dominant software package in scientific and mathematical computing and visualization. Originally built to do very fast computations and manipulations of very large arbitrary matrices; now includes things like a scripting language, graphical user interface builder, extensive mathematical reference library, etc. See `MATLAB Basics FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#matlab-basics>`_ for basic information on how to use MATLAB. For everything else, check out the `Matlab Documentation <http://www.mathworks.com/help/>`_.

mental chronometry
******************
See chronometry_ or `Mental Chronometry FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#mental-chronometry>`_.

microanatomy
************
A level of anatomical detail somewhere around and above cytoarchitectonic_, but smaller than the standard anatomic strucures. This level of detail refers to things like cell type, or the organization of cell layers and groups. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for information on using microanatomical detail in your study.

mixed-effects
*************
A model which combines both `fixed-effects`_ and `random-effects`_. Most fMRI group effects model are mixed-effects models of a special type; they are generally hierarchical, where the fixed effects and random effects are partitioned and evaluated separately. Check out `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ for more info.

MNI space, MNI templates
************************
The Montreal Neurological Institute (MNI) has published several "template brains," which are generic brain shapes created by averaging together hundreds of individual anatomical scans. The templates are blurry, due to the averaging, but represent the approximate shape of an "average" human brain. One of these templates, the MNI152, is used as the standard normalization_ template in SPM. This differs from Talairach_ normalization, which uses the Talairach_ brain as a template. So normalized SPM results aren't quite in line with Talairach-normalized results. The MNI brain differs slightly from the Talairach brain in several ways, particularly in the inferior parts of the brain. In order to report normalized SPM results in Talairach coordinates for ease of reference, it's necessary to convert the MNI coordinates into Talairach space with a script called mni2tal.m from Matthew Brett. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ and `Normalization FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#normalization>`_ for more.

motion correction
*****************
See realignment_.

mutual information
******************
A concept imported from information theory into image analysis. If you have two random variables, A and B, and would like to quantify the amount of statistical dependence between them, one way you might do it is by asking: how much *more* certain are you about the value of B if you know the value of A? That amount is the amount of mutual information between A and B. In more precise terms, it's the distance (measured by a K-L statistic) between the joint probability distribution P(ab) and the product of their individual distributions, P(a) * P(b). It comes up in fMRI primarily in coregistration_. Mutual information-based methods provide a much more robust way of lining up two images than simple intensity-based methods do, and so most current coregistration programs use it or a measure derived from it. See `Coregistration FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#coregistration>`_ for more info.


N
=

NIfTI
*****
`NIfTI <http://nifti.nimh.nih.gov/>`_ stands for Neuroimaging Informatics Technology Initiative and is a file format most commenly used in neuroimaging. For more information see `this blog <http://brainder.org/2012/09/23/the-nifti-file-format/>`_.

Nipype
******
Nipype stands for Neuroimaging in Python - Pipelines and Interfaces and is this amazing software package for which this beginner's guide is written for. For more information go to the `introductory page <http://miykael.github.io/nipype-beginner-s-guide/nipype.html>`_ of this guide.

neurological convention
***********************
Radiological images (like fMRI) that are displayed where the left side of the image corresponds to the left side of the brain (and vice versa) are said to be in "neurological convention" or "neurological format." In radiological convention, left is right and right is left. Those crazy radiologists.

Node
****
See Workflow_.

normalization
*************
A spatial preprocessing technique in which anatomical and/or functional MRI images are warped in order to more closely match a template brain. This is done in order to reduce intersubject variability in brain size and shape. The warping can be affine in nature or nonlinear, and can be done on a voxelwise basis or with respect to the surfaces of the brains only. All the major neuroimaging packages support some form of normalization, but there are many questions about how much variability it actually removes. See `Normalization FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#normalization>`_ for more answers than you can shake a stick at, and even more questions than that.


O
=

onset
*****
In order to create a `design matrix`_ for your experiment, you need to know when, in time, each of your trials started and how long they lasted. The beginning of a trial is commonly called an onset. An onset vector is a list of starting times for the trials of a particular condition. If you have 15 trials in condition A, your onset vector for condition A will have 15 numbers, each one specifying the moment in time when a particular trial started. The times are usually specified in either seconds or in TR. Generally all neuroimaging software packages require you to enter your onset vectors somehow, or construct a design matrix from them, as input before they can estimate a model. Check out `Basic Statistical Modeling FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#basic-statistical-modeling>`_ for more.

outlier
*******
Any point in a dataset (of any kind) whose value lies wayyyyy outside the distribution of the rest of the points. Outliers are often removed from datasets in many scientific domains, because their extreme values can give them undue influence over the description of the data distribution; as one example, outliers can severely skew statistics like mean or variance. Figuring out just how far an outlier need be from the center of the distribution to be removed, though, is a tricky procedure, and often extremely arbitrary. Outlier detection and removal is one key aim of artifact detection schemes and programs.

orthogonal, orthogonalize, orthogonality
****************************************
Orthogonal means perpendicular. Two things that are orthogonal to each other are perpendicular, to orthogonalize two things means to make them orthogonal, etc. The terms, though, are generally used less for real lines in space than for vectors. Any list of numbers can be taken to represent a point or a line in some space, and those lists of numbers can thus be made orthogonal by tweaking their elements such that the lines they represent become perpendicular. In more common terms, this corresponds to removing correlations between two lists of numbers. Two lists are "collinear" to the degree that they have some correlation in their elements, and they are orthogonal to the degree to that they have no correlation whatsoever in their elements. Two perfectly orthogonal lists have values that are totally independent of one another, and vice versa. Having columns in a `design matrix`_, or elements in two contrasts, not be orthogonal can pose problems for estimating the proper `beta weights`_ for those columns or contrasts, so many programs either require certain structures be orthogonal or do their own orthogonalization when the issue comes up. Check out `Basic Statistical Modeling FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#basic-statistical-modeling>`_ and `Contrasts FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#contrasts>`_ for more info.


P
=

p-threshold
***********
A particular probability value which is used as a threshold for deciding which voxels in a contrast_ are active and which are not. The contrast image is rendered in terms of some statistic, like a T or F, at each voxel, and each statistic can then be assigned a particular p-value - the likelihood that such a value would occur under the null hypothesis of no real activation. Voxels with p-values smaller than the threshold are declared active; other voxels are declared inactive. P-thresholds can be manipulated to account for multiple comparisons, spatial and temporal correlation, etc. See `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_ for lots, lots more.

parameter weights
*****************
See `beta weights`_.

partial voluming
****************
In doing segmentation_, a major problem in assigning a particular voxel to a tissue-type category or anatomical structure is that tissue and structure boundaries rarely line up exactly with voxel boundaries. So a given voxel might contain signal from two or more different tissue types. If one of the assumptions of segmentation is that different tissue types give off different signals (usually MR intensity), voxels with a mixture of tissue types pose a problem, because their intensity may lie in between the canonical intensity of any one tissue type. Oftentimes segmentation algorithms simply make a guess based on which tissue type the voxel seems closest to, but this can pose a problem in calculating, say, the total volume of gray matter in a brain. If half of your "white-matter" voxels have some gray matter in them, but you count them only as white matter, you're missing a whole lot of gray matter in your volume calculation. This is the partial volume problem, and a partial voluming effect is this type of tissue mixing. See `Segmentation FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#segmentation>`_ for more.

peak voxel
**********
The most active voxel in a cluster, or the voxel in a cluster that has the highest test statistic (T-stat or F-stat or whatever). Often the coordinates of only the peak voxel are reported for a cluster in papers, and sometimes timecourses or `beta weights`_ are extracted only from the peak voxel. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ and `Percent Signal Change FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#percent-signal-change>`_ for more info on why that would be.

percent signal change
*********************
A measure of signal intensity that ignores the arbitrary baseline values often present in MR signal. A timecourse of signal can be viewed as a timecourse of changes from some baseline value, rendered in units of percent of that baseline value. The baseline is then chosen on a session-specific basis in some reasoned way, like "the mean of the timecourse over the whole session," or "the mean of the signal during all rest periods." This gets around the problem that MR signal is often scaled between sessions by some arbitrary value, due to how the scanner feels at that moment and the physiology of the subject. Two signal timecourses that are identical except for an arbitrary scaling factor will be totally identical when converted to percent signal change. Percent signal changes timecourses are thus used to show intensity timecourses from a given region or voxel during some experimental manipulation. `Percent Signal Change FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#percent-signal-change>`_ has everything you ever wanted to know about the measure, or at least everything I could think of before noon.

peristimulus timecourse
***********************
Means "with respect to the stimulus." A peristimulus timecourse is one that starts at the onset_ of a given stimulus. Sometimes a peristimulus timecourse will start with negative time and count down to a zero point before counting up again; the zero point is always the onset of a given stimulus. This is the same as a time-locked average timecourse. See `Percent Signal Change FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#percent-signal-change>`_ for more on why you would want to look at these.

perfusion
*********
A type of fMRI imaging which doesn't look at BOLD contrast. Instead, blood is magnetically "labeled" just before it gets to the brain, and it's then tracked through the brain over time. Perfusion imaging has several advantages over BOLD - a different and flatter noise profile, possibly less variability over subjects, and a readily interpretable physiological meaning for the absolute units are chief among those. The major disadvantage is that `Signal-to-Noise Ratio (SNR)`_ is significantly smaller in perfusion imaging, at least in single subjects. This probably makes it less suitable for most current fMRI designs, but it may be a better option for novel designs (blocks lasting several minutes, for example). See `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for a fuller discussion of the pros and cons of each.

permutation test
****************
A type of statistical test, like a T-test or F-test, but one which assumes much less about the distribution of the random variable in question. This is a type of nonparametric test related to bootstrapping_. It has significant advantages over standard parametric tests under certain conditions, like low degrees of freedom, as in a group analysis. `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_ delves into more detail about this.

phantom
*******
Any object you scan in an MRI machine that's intended only to help you calibrate your scanner. Phantoms can range from very simple (a tank of water) to very complicated (a plastic skull with a gelatin brain controlled by several motors to simulate head movements). The fact that they don't have brain responses is the key; you can use them to check your scanner or preprocessing paradigm, or introduce fake signal into a phantom scan and know that you won't be corrupted by real brain responses.

Plugin
******
In the context of Nipype, plugins are components that describe how a workflow should be executed. They allow seamless execution across many architectures and make the usage of parallel computation look so easy. For more see the `introduction section <http://miykael.github.io/nipype-beginner-s-guide/nipype.html#execution-plugins>`_ of this beginner's guide.

Positron Emission Tomography (PET)
**********************************
An imaging method in which subjects are injected with a slightly radioactive tracer, and an extremely sophisticated and sensitive radition detector is used to localize increased areas of blood metabolism during some experimental task. PET offers better spatial resolution than `EEG (Electroencephalogram)`_, but not as much as fMRI - on the order of tens of millimeters at best. Its temporal resolution is pretty poor, as well - within tens of seconds at best, making `block design`_ the only feasible design for PET studies. As well, PET scanners are very expensive, and so aren't around at many institutions. Nonetheless, studies have demonstrated one extremely useful aspect of PET - the ability to selectively label particular neurotransmitters, like dopamine, and hence get a chemically-specific picture of how one neurotransmitter is being used. SPM was originally developed for use with PET.

power
*****
A statistical concept which quantifies the ability of your study to reliably detect an effect of a particular size. Studies with higher power can reliably detect smaller effects. A tremendous number of factors influence your study's power, from the ordering of your stimuli presentation to the noise characteristics of the scanner, but the one that's most under your control is your experimental design. High power is very desirable for fMRI studies, where effect sizes can often be extremely small, but it doesn't come without a cost; increasing the power of your study requires decreasing the efficiency_, which can also be seen as assuming more information about the shape of your response. See `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ (and `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_) for tons more on power and efficiency and how to manipulate them both.

pre-whitening
*************
A process by which signals that are corrupted by non-white noise - i.e., colored noise, or noise that is more prevalent at some frequencies than others - can be improved, by making the noise "whiter." This involves estimating the autocorrelation_ function of the noise, and then removing the parts of the noise that are influenced by previous noise values, leaving only independent or `white noise`_. Whatever analysis is to be done on the signal is then carried out. Because this process makes "colored" noise into white noise, it's called whitening, and the "pre" part is because it happens before the model estimation (or other analysis) is done on the signal. This is a standard technique in many signal processing domains. See `Basic Statistical Modeling FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#basic-statistical-modeling>`_ for more details.

preprocessing
*************
Any manipulation of your data done before you estimate your model. Usually this refers to a set of spatial transformations and manipulations like realignment_, normalization_, or smoothing_ done to decrease noise and increase signal strength. There are various preprocessing steps you can take in the temporal domain as well, like `temporal filtering`_ or `pre-whitening`_. In SPM, "preprocessing" often refers to the specific set, in order, of slice timing correction, realignment, normalization and smoothing, which are grouped together in the interface and generally comprise the first steps of any analysis.

Principal Components Analysis (PCA)
***********************************
A statistical technique for identifying components of your signal that explain the greatest amount of variance. In fMRI, it's used as a way of analyzing data that doesn't require a model or `design matrix`_, but rather breaks the data down into a set of distinct components, which can be interpreted in some case as distinct sources of signal. These components can then (hopefully) be localized in space in some intelligible way. This enables you, theoretically, to discover what effects were "really" present in your experiment, rather than hypothesizing the existence of some effects and testing the significance of your hypothesis. It's been used more heavily in `EEG (Electroencephalogram)`_ research, but is beginning to be applied in fMRI, although not everything about the results it gives is well understood. Its use in artifact_ detection is clear, though. It differs from `Independent Components Analysis (ICA)`_, an algorithm with similar goals, because the components it chooses explain the maximum amount of variance in the dataset, rather than maximizing the statistical independence of the components.

prospective motion correction
*****************************
A form of realignment_ that is performed within the scanner, while the subject is actually being scanned. Rather than waiting until after the scan and trying to line up each functional image with the previous after the fact, prospective motion correction techniques aim to line up each functional image immediately after it is taken, before the next image is taken. Since TRs are typically on the order of a few seconds, these algorithms must operate very fast. Standard methods call for an extra RF pulse or two to be taken during one TR's pulse sequence, essentially to quantify how much the subject has moved during the TR. These algorithms can avoid some of the major problems of standard realignment algorithms, like biasing by activation and warping near susceptible regions. That extra functionality comes at the cost of time - it usually takes tens of milliseconds per TR to perform, which might mean taking one fewer slice or two.

psychophysiological interaction (PPI)
*************************************
A term invented by `Karl Friston`_ and the SPM group to describe a certain type of analysis for `functional connectivity`_. They have argued that looking at simple correlations of signal between two regions may not be as interesting as looking at how those correlations change due to the experiment; i.e., does condition A induce a closer connection between two regions than condition B does? If so, these regions have a psychophysiological interaction (or PPI) - an interaction influenced both by psychological factors (the experimental condition) and physiological factors (the brain signal from another region). Check out `Connectivity FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#connectivity>`_ for more.

pulsatility
***********
A type of artifact_ induced by the cardiac cycle. The beating of the heart pushes blood through the arteries and into the brain, and the rhythmic influx of blood actually causes small swellings and deflations in brain tissue, as well as other small movements, all timed to the heartbeat. As the heartbeat is often faster but around the same timescale as the TR, signal changes induced by cardiac movements can be unpredictable and difficult to quantify and remove. See `Physiology and fMRI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#physiology-and-fmri>`_ for more on physiological sources of artifacts.

pulse sequence
**************
fMRI works by stimulating the brain with rapid magnetic pulses in an intense baseline magnetic field. The exact nature of those rapid pulses determines exactly what kind of fMRI signal you're going to get out. Many things about those pulses are standardized, but not all, and you can use different pulse sequences to take functional images, depending on your scanner characteristics and different parameters of your experiment. `Echo-planar Imaging (EPI)`_ and `spiral imaging`_ are two well-known functional pulse sequences; there are many others for other types of scans. Check out `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ and `Physiology and fMRI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#physiology-and-fmri>`_ for a little bit more.

Python
******
`Python <https://www.python.org/>`_ is a widely used general-purpose, high-level programming language. Python supports multiple programming paradigms, including object-oriented, imperative and functional programming or procedural styles. Python becomes more and more the programming language for the scientific Neuroimaging field. This because the language is easy to learn and can be mastered by also none programmer in a rather short time. For more see `Python's Wikipedia page <https://en.wikipedia.org/wiki/Python_%28programming_language%29>`_.


Q
=



R
=

radiological convention
***********************
Radiological images (like fMRI) that are displayed where the left side of the image corresponds to the right side of the brain (and vice versa) are said to be in "radiological convention" or "radiological format." In radiological convention, left is right and right is left. Those crazy radiologists. This contrasts with `neurological convention`_. Some image formats do not contain information saved as to what convention they're in, and Side Flipping can be an issue with those images. So be careful.

random-effects
**************
An analysis that assumes that the subjects (or scanning sessions, or scanner runs, or whatever) you're drawing measurements from are randomly drawn from some distribution. The differences between them must thus be accounted for in accounting for the average effect size. This generally means evaluating effects within each subject (session/run/etc.) separately, to allow for the possibility of differential responses, which means separate design matrices and estimations. This costs you a significant amount of power_ from a fixed-effects analysis, because you only end up having as many degrees of freedom in your test as you have subjects (sessions/runs/etc.), which is generally far smaller than the number of measurements (i.e., functional images). The advantage is a gain in inferential power: a random-effects analysis allows you to make inferences about the population from which the subjects were drawn, not just the subjects themselves. Fixed-effects analyses of any kind do not allow this type of inference. The analyses generally done in neuroimaging programs is technically a `mixed-effects`_ analysis, because they include both fixed and random effects. Check out `Random and Fixed Effects FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#random-and-fixed-effects>`_ for more.

rapid event-related designs
***************************
Any `event-related design`_ in which trials occur too fast for the `Hemodynamic Response Function (HRF)`_ to return to baseline in between trials. This generally corresponds to an `Inter-stimulus Interval (ISI)`_ of less than 20-30 seconds or so. These designs contrast with `long event-related designs`_. They are more difficult to analyze than long event-related designs, because you have to make assumptions about the way that the hemodynamic response to different events adds up. They compensate for this difficulty by being having much more power_ and efficiency_ than long event-related designs - *so long* as the mean ISI in the design is properly varied or jittered_. This gain comes from the increased number of trials per unit time, but necessitates proper jitter. See `Design FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#design>`_ for more, and `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_ for a good deal about rapid designs specifically.

realignment
***********
Also called motion correction. A spatial preprocessing step in which functional images are lined up together, so a single voxel in the grid corresponds to the same anatomical location during the whole experiment. This step is needed due to subtle head motions from the subjects; even with a bite bar or head mount, subjects move their head slightly during an experiment, and so the functional images that are taken end up being slightly out of register with each other. Realignment aims to line them back up again. See `Realignment FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#realignment>`_ for much much more.

reference slice
***************
A term used in `slice timing`_ correction to denote the slice of the brain that no correction is done on. All other slices of each functional image will have their voxels' timecourses slightly shifted in the temporal domain so that they take on the values they "would have had" if the whole brain had been sampled at the same moment as the reference slice. See `Slice Timing FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#slice-timing>`_ for more, and for how to choose a reference slice.

Region of Interest (ROI)
************************
Any subset of Voxels_ within the brain that you want to investigate further. They might comprise an anatomical structure, or a cluster of activated voxels during your task. A ROI needn't be spatially contiguous, although they often are. Subtypes are `anatomical ROI`_ and `functional ROI`_. They can be identified before or after a standard `general linear model (GLM)`_ analysis, and they often represent some area of pre-existing theoretical interest. They're often saved as either lists of coordinates (all coordinates in the list make up the ROI) or image masks, a special type of image file where every voxel in the ROI has intensity 1 and every voxel not in the ROI has intensity 0. Several further analyses can be performed once you've identified some regions of interest. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for some thoughts on them.

render, rendering
*****************
A three-dimensional object like the brain can be difficult to visualize in a two-dimensional picture. Several graphics packages provide facilities to make a three-dimensional picture of the brain that shows the folds of the surface, and often allows zooming and rotation of the whole 3-D object. This process of making a 3-D image is called rendering. All the major neuroimaging software packages provide some rendering package. They all allow you to superimpose patterns of activation on those 3-D objects, to allow a better visualization of the 3-D nature of the activations. Rendering is often connected with other 3-D visualization methods, like inflation_ or flattening_.

reverse / inverse normalization
*******************************
After normalization_, you have some set of transformation parameters which specify how the individual subject's brain was warped and shifted to match the standard template brain. One thing you could do at that point would be to identify some `functional ROI`_ in the normalized group results, or some `anatomical ROI`_ on a standard brain like the MNI template or Talairach brain. Reverse normalization would entail, then, inverting the transformation matrix of normalization and applying the reversed matrix to some anatomical or functional ROI made at the normalized, standard brain level. This reverse-normalized ROI would then be warped to fit your individual subject's brain, and you could then analyze any non-normalized images you had of theirs with it. Given that normalization induces some interpolation errors and localization problems into your images, this might be a great way to save labor on hand-drawing ROIs but still look at non-normalized results. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for more info on why you'd want to analyze data at the individual level, and `Normalization FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#normalization>`_ for more about the normalization process.

run
***
A term used to describe a single pass-through of a given experimental paradigm, which generally corresponds with a single chunk of time between turning the scanner on and turning it off. A given experiment for one subject often consists of several runs, which are often all modeled together in a `fixed-effects`_ analysis. Generally, it does not mean the whole time a subject is in the scanner if there are several chunks of scanning time in there. Often used interchangeable (and confusingly) with session_.


S
=

scanner drift
*************
See drift_.

script
******
in MATLAB_, a type of .m file that doesn't take arguments or give output, but merely operates in the base workspace. Essentially scripts are just a text file containing a bunch of Matlab commands exactly as if you'd typed them, in order, at the Matlab prompt when you ran the script. Scripts are contrasted with functions, which have their own workspaces and don't have access to the base workspace. Most SPM sub-programs are functions, but not all of them.

segmentation
************
A spatial step in which an automated algorithm classifies a brain image into different tissue types. Standard segmentation programs start with an MRI image - generally, but not always, an anatomical scan - and give out images of all the gray matter in the brain, all the white matter, and all the cerebrospinal fluid (CSF). Each voxel is thus labeled uniquely as being one of the three standard tissue types. Those images can then be used to make mask images (to restrict analysis to gray matter only, for example) or to do `Voxel-based Morphometry (VBM)`_, or a lot of other things. Segmentation can be pretty inexact, due to problems like `partial voluming`_ and other issues, so advanced segmentation algorithms these days sometimes do a "soft classification," where voxels are labeled only with a probability of being a certain tissue type, rather than a definite label. Other segmentation algorithms go farther and use anatomical information to classify voxels into different structures as well as different tissue types. See `Segmentation FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#segmentation>`_ for lots more.

session
*******
An ambiguous term usually used to denote the exact same thing as run_: the chunk of time in an experiment between turning the scanner on and turning it off, during which you have one pass of your experimental paradigm. Oftentimes, the experiment on one subject will have several sessions, which might all be the same paradigm or different ones. Unfortunately, this term has also been used to denote the whole single-subject experiment; i.e., one scanning session is the whole time you have the person in the scanner, which might include several different runs.

Signal-to-Noise Ratio (SNR)
***************************
One of the most self-explanatory terms out there. If you can quantify the amount of signal you have in a measurement and the amount of noise, then you divide the former by the latter to get a ratio - specifically, your signal-to-noise ratio, or SNR. Your SNR is a far more valuable measure of how much power_ your measurement will have than, say, average intensity; if the measurement is brighter, that could mean more signal or more noise. Things like smoothing_ change average intensity unpredictably, but always aim to increase SNR. Calculating SNR can be tricky, because it requires some determination (or at least estimation) of how much noise your measurement has, which may not be known. But things like phantom_ measurements can help. See `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for a little bit of commentary on how your scanning parameters can tweak your SNR.

single-subject canonical
************************
An image distributed with `SPM (Statistical Parametric Mappin)`_ that is a very clear anatomical scan of a single brain (as opposed to the average scan of many brains, which is how brain templates like the MNI brain are made). The single-subject canonical is often used as a background to superimpose normalized results onto, because the brain is roughly average in shape and more or less lines up with the MNI template. It's also a very, very clear scan (made by averaging many scans of the same brain together) and so is much clearer than a standard in-plane anatomical scan for a single subject might be. However, the single-subject canonical is not an exact map onto the MNI or Talairach templates; activation which appears to be in one structure on the canonical image may not lie in that structure in either template brain. This image is generally found in the SPM directory, in the /canonical subdirectory.

slice timing
************
A spatial preprocessing_ step which aims to correct for the fact that not all slices of a functional volume are sampled at the same instant. Functional images aren't acquired instantly - they are sampled across the whole TR, so with a descending `pulse sequence`_ and a 2-second TR, the bottom of the brain is sampled almost two seconds after the two of the brain. If every voxel in the brain is analyzed with exactly the same model, then the onsets you've specified are going to be correct for some parts of the brain and wrong for others. If you say a trial happens at time 1, in the above example, and the TR starts right then, your onset is almost 2 seconds off for voxels at the bottom of the brain, because by the time you sample them, they're 2 seconds into their hemodynamic response already. Slice timing correction aims to fix this problem by simply time-shifting or interpolating all the voxels in the brain to line up with a `reference slice`_. The methods for doing this are fairly uncontroversial and generally accepted as necessary for all `event-related design`_. See `Slice Timing FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#slice-timing>`_ for more.

slice thickness
***************
Sometimes when you take a functional MRI sequence, your Voxels_ aren't isotropic_ - there is a given matrix within a slice (often 64x64 voxels), and a certain set of slices (usually ranging from a few to a few dozen). Your slice thickness is exactly what it sounds like - how thick, in millimeters, your slices are. This is also called the through-plane resolution of your voxels - voxels are often thicker between slices than within a slice. Sometimes you'll leave a gap between slices; this is called the "skip" distance and isn't factored into your slice thickness.

small-volume correction (SVC)
*****************************
If you have a pre-existing hypothesis about a particular region in the brain - an anatomical or functional ROI from another study, say - then you might want to search within only that region for activation. This helps avoid the multiple-comparison problem for thresholding; instead of correcting your threshold for the tens of thousands of voxels in the whole brain, you can say you're only looking within a small region and correct for only the hundreds or thousands of tests within a much smaller region. This is called small-volume correction. It's available in SPM through the results interface's S.V.C. button. This button is also used sometimes to merely save a cluster or region as a functional ROI in SPM, rather than actually looking at the corrected statistics. See `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_ for more on thresholding.

smoothing
*********
A spatial preprocessing_ step in which your functional images are blurred slightly. Each voxel's intensity is replaced with a weighted average of its own intensity and some voxels around it; this is accomplished by convolving a Gaussian function - the `Smoothing kernel`_ - with the intensity at each voxel. The amount of blurring is determined by the size of the kernel. Smoothing can greatly increase your `Signal-to-Noise Ratio (SNR)`_, as well as increase the chance of getting group activations (by increasing the size and hence overlap of functional regions) and validating the assumptions of `Gaussian random field`_ theory if you're doing that sort of `Family-wise error correction (FWE)`_. The downside of smoothing is, well, it makes your data blurrier. This is a problem if you're trying to decide whether one voxel or its neighbor is active, or if you're worried about smearing activation across anatomical or functional boundaries in the brain. It effectively reduces the resolution of your images. `Smoothing FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#smoothing>`_ has tons more on why to smooth and why not to smooth.

smoothing kernel
****************
A generally Gaussian function which is convolved with voxel intensities in a given functional image during smoothing_. The "size" of the kernal is the FWHM (full-width half-maximum) measurement of the Gaussian function. Common kernel sizes for fMRI range between 2 and 12 mm, depending on what you're looking for. See `Smoothing FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#smoothing>`_ for more on choosing a kernel size.

spatial frequency
*****************
Like any other signal, images can be analyzed in terms of their frequency. A gross simplification might be looking at the image intensities of neighboring voxels as a timecourse, and finding the frequencies of the waveforms contained within. In real life, finding spatial frequency is a little trickier, but the idea is the same. Low spatial frequency equals slow change in intensity; areas with low spatial frequency in an image are largely homogeneous, smooth, and less-varying. High spatial frequency equals fast change in intensity; areas of high spatial frequency in an image are often edges, or choppy patterns. `k-space`_ is a way to view images in terms of their spatial frequency.

spatial preprocessing
*********************
See preprocessing_; this term refers specifically to spatial transformations done before analysis, like normalization_, smoothing_, `slice timing`_ correction or realignment_, and excluding temporal manipulations like `high-pass filter`_ or `pre-whitening`_.

spatial smoothing
*****************
A measure of `spatial frequency`_. Spatial smoothness just measure the amount of low-spatial-frequency information in an image or a local region of an image. This is a way of quantifying how smoothly an image varies across the whole volume or a small chunk of it. Images have to have a relatively high spatial smoothness to satisfy the assumptions of `Gaussian random field`_ theory and be eligible for Gaussian-random-field `Family-wise error correction (FWE)`_. Increasing their spatial smoothness can be accomplished with, of all things, smoothing_. Crazy. See `Smoothing FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#smoothing>`_ and `P threshold FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#p-threshold>`_ for the relationship between smoothness and thresholding.

spiral imaging
**************
A particular `pulse sequence`_ in which `k-space`_ is sampled in a spiraling trajectory, rather than in discrete lines. Spiral imaging avoids some of the common artifact_ than can plague other sequences like `Echo-planar Imaging (EPI)`_: geometric distortions, ghosting, or radical displacement. Spiral artifacts tend to be simply blurring of greater and lesser degree. Some spiral sequences can be more susceptible to dropout_, but spiral in-out sequences seem to recover a great deal of signal from all parts of the brain. See `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for a bit more on spiral sequences.

spiral-in, spiral-out, spiral in-out, spiralio
**********************************************
Different variations of spiral pulse sequences. In spiral-in, `k-space`_ is sampled in an inward-spiraling trajectory during the TR; in spiral-out, `k-space`_ is sampled in an outward-spiraling trajectory. Spiral in-out (also called spiralio) sequences do both, sampling k-space on an inwards spiral followed by an outwards spiral during the same TR and averaging the two images together. Spiral in-out sequences in particular do an excellent job at avoiding dropout_ in many areas of the brain traditionally thought to be difficult to image due to dropout. Check out `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for more.

SPM (Statistical Parametric Mappin)
***********************************
A software package for neuroimaging analysis, written in MATLAB_ and distributed freely. Probably one of the most widely-used package worldwide, currently. Has an easy-to-learn interface combined with some of the most sophisticated statistical modeling available. See `SPM in a Nutshell FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#spm-in-a-nutshell>`_ for a more detailed summary of what SPM is. For everything else, see `SPM's main homepage <http://www.fil.ion.ucl.ac.uk/spm/>`_ and the `SPM Mailinglist <https://www.jiscmail.ac.uk/cgi-bin/webadmin?A0=spm>`_.

stimulus-correlated motion (SCM)
********************************
Head motion during an experiment is a big enough problem to start with. But random head motion can be dealt with by realignment_ and including your motion parametes in your design matrix, to eliminate any signal correlated with head motion. So why doesn't everyone just do that? Because if your subject moved their head in correlation with your task paradigm, removing motion-correlated signal will also remove task-correlated signal - which is what you're looking for. So stimulus-correlated motion is a big problem because it prevents you from regressing out motion-related activity. Evaluating your SCM should be a priority for anyone who includes motion parameters in their design matrix, particularly if you don't use a bite bar or if you have an emotionally-intense paradigm. Check out `Realignment FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#realignment>`_ for more.

structural equation modeling (SEM)
**********************************
A statistical method for analyzing `functional connectivity`_. Structural equation modeling (SEM) allows you to start with a set of `Region of Interest (ROI)`_ and figure out what the connection strengths between them are, via a model-fitting process. It can't be used to determine the directionality of connection, but it can do a good job describing which connections are strong and which are weak, which can be crucial in ruling out certain theoretical constructs. See `Connectivity FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#connectivity>`_ for lots more on this.

surface mapping
***************
The cortex, where much of the brain's processing takes place, could be flattened out into a flat sheet. But in the head, it's all crinkled up into sulci and gyri. If you ignore the folds of the brain and simply analyze it like it's all one homogenous shape - as traditional voxel-based analysis do - then you may well miss important principles of how activation is organized, and you might even miss real activations in general. Surface mapping techniques are related to inflation_ and flattening_ techniques, and surface mapping is in fact a necessary prerequisite for those. Surface mapping simply starts with a high-quality anatomical scan, and builds a three-dimensional model of the folds and curves of the brain, which is then linked to particular voxels in the functional analysis. This allows the activation from the functional images to be mapped not just to a particular voxel, but to a particular point on the surface of the cortex. This surface can then be manipulated and visualized in far more interesting ways than simple voxel-based pictures allow.

susceptibility
**************
Also called magnetic susceptibility. Used to describe regions where magnetic fields are generally more distorted, chopped up, and subject to dropout_, due to the tissue characteristics of a region. Usually, regions of high susceptibility (try typing that five times fast) are near tissue/air interfaces, or interfaces between two different types of tissue, where the magnetic differences between the two materials causes distortions in the local field. High-susceptibility regions traditionally include the orbitofrontal cortex, medial temporal lobe, and many subcortical structures. Spiral in-out imaging has shown good promise at dealing with susceptibility-induced dropout. See `Scanning FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#scanning>`_ for more.


T
=

tal2mni
*******
A script written by Matthew Brett (check the internet for tal2mni.m or mni2tal.m), which aims to convert a set of XYZ coordinates from a given point in the Talairach_ atlas brain into the same anatomical point in the Montreal Neurological Institute (MNI) standard template brain. The Talairach_ brain, which is used as the normalization_ template for AFNI, BrainVoyager, and other programs, differs slightly from the MNI brain in several ways, particularly in the inferior parts of the brain. In order to use facilities like the `Talairach Daemon`_ or other Talairach-coordinate lookups to make ROIs for normalized SPM results, or in order to report Talairach_ data in MNI coordinates, it's necessary to convert the Talairach_ coordinates into MNI space with this script. It's not a perfect mapping, but it's widely used. See `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ and `Normalization FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#normalization>`_ for more.

Talairach
*********
In 1988, Talairach and Tournoux published a widely-cited paper created a common reference coordinate system for use in the human brain. The paper set forth axes labels and directions, an origin at the anterior commissure, and anatomical and cytoarchitectonic labeling for many individual coordinate points within the brain. The coordinate system is based on one reference brain they dissected, sometimes referred to as the Talairach brain. The coordinate system has been widely adopted, and many algorithms have sprung up to normalize arbitrary brains to the Talairach reference shape. Coordinates in the reference system are said to be in Talairach space, and the full listing of coordinates and their anatomical locations is called the Talairach atlas. (Tournoux pretty much got the short end of this whole stick.) Although the coordinate system has been widely used and has proven very valuable for standing reporting of results, it has drawbacks: the Talairach brain itself is a fairly unrepresentative single subject (and differs significantly from a more average template brain - see tal2mni_), it ignores left-right hemispheric differences as only one hemisphere was labeled, and there are no MRI pictures available of it to be directly comparable. Some programs, like `SPM (Statistical Parametric Mappin)`_, have avoided using the Talairach brain for normalization, but Talairach labeling is pretty much inescapable at this point. Check out `ROI FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#roi>`_ for a little more on all this, as well as `Normalization FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#normalization>`_.

Talairach Daemon
****************
A very nice software package hosted by UT-San Antonio and developed by Lancaster et. al, the Talairach Daemon takes in a set of coordinates in Talairach_ space and spits out a set of anatomical labels for each point - hemisphere, anatomical area, brodmann area, tissue type - based on the Talairach_ atlas. This allows you, in an automated fashion, to label your results in a common space with many other researchers.

task-correlated motion
**********************
See `stimulus-correlated motion (SCM)`_.

temporal derivative
*******************
Derivative of a function with respect to time. In SPM, the temporal derivative of the `canonical HRF`_ looks something like the canonical but can be used as a `basis function`_, to model a degree of uncertainty as to the exact onset of the HRF. See `HRF FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#hrf>`_ for more.

temporal filtering
******************
A filter applied in the temporal domain to some signal to help cut noise. Temporal filters knock out some frequencies in a given signal while allowing others to pass through; some types include `high-pass filter`_, `low-pass filter`_, and `band-pass filter`_. In fMRI, applying some temporal filtering is a terrifically good idea, because noise is heavily concentrated in some parts of the frequency spectrum. See `Temporal Filtering FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#temporal-filtering>`_ for more.

Tesla
*****
The Tesla is the standard international (or metric system, if you must) unit of magnetic flux density. It's abbreviated simply as T. It measures, in a nutshell, the strength of a standing magnetic field at a given point. It's named after Nikola Tesla, the engineer who discovered the rotating magnetic field back in the 19th century. The strength of an MRI scanner is measured in Tesla. Most scanners in current use for humans are rated as 3T; human scanners up to 7T can be found around. For comparison, the Earth's standing magnetic field is around 2.5 * 10e-5 T.

time-locked averaging
*********************
A technique in signal processing for signals where some repeating signal is corrupted by random noise. If you know the timepoints in the timeseries when the signal starts and can choose a window of time following the start to look at - say, 30 seconds - then you could take the 30-second chunk following each signal onset and average all those 30-second chunks together. If you have five signal onsets, then you have 5 windows; you average the first timepoint in each window together (all 5 of them), then the second timepoint in each window together (all 5 of those), then the third timepoint, etc. This creates an average time window - the average response following a signal onset. If the noise is roughly random, it should average to zero, and you'll get a clearer picture of your signal than from any individual response. The resulting `peristimulus timecourse`_ is called "time-locked" because it always describes a given time following the onsets - it's locked in time to the condition's onsets. This technique has long been used in EEG, and with the advent of a `event-related design`_, it began to be used in fMRI as well. The technique may not be appropriate for `rapid event-related designs`_; when the window following an onset overlaps the onset of other signals, the final timecourse can be muddled by other signals.

timecourse, timeseries
**********************
A list of numbers that are taken to represented some measurement sampled over time. Each point in the timeseries represents a specific point in time; neighboring points represent neighboring moments, later points represent later points in time, etc. Many scientific domains deal with timeseries data, and so a good deal of research has been done on how to deal with any peculiar characteristics they might have - autocorrelation_, etc. In fMRI, the most common timeseries would be the series of measurements from a specific voxel across all the functional images - that repeated measurement represents a series of samples over time in (we hope) one unique point in the brain.


U
=

unwarping
*********
A preprocessing_ technique which attempts to eliminate some of the residual effects of head motion after realignment. The method attempts to estimate a map of the inhomogeneities in the magnetic field and thus map regions of high susceptibility_, and calculate how those regions might have distorted the data around them, once the head motion parameters are known. Unfortunately, this method is currently (and probably will always be) available only for `Echo-planar Imaging (EPI)`_ functional data, not spiral, due to the models of geometric distortion used. See `Realignment FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#realignment>`_ for a bit more.


V
=

variable ISI
************
Stands for variable inter-stimulus interval. A type of experiment in which a varying amount of time separates the beginning of all stimuli - trials can be all the same length or all different, but the onsets of stimuli aren't all the same length of time apart. variable ISI studies most often have ISIs that are randomized within certain extremes, not just arbitrarily variable. Generally only a `event-related design`_ are variable ISI, although there's no reason why you couldn't have a limited-variability-ISI `block design`_ experiment. variable ISI event-related experiments, though, are much better than `fixed ISI`_ experiments at both efficiency_ and power_, especially as the ISI increases. In general, several empirical studies have shown that for event-related designs, `variable ISI`_ is the way to go. For block designs, the difference is fairly insignificant, and variable ISI can make the design less powerful, depending on how it's used. See `Jitter FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#jitter>`_ for more on the difference between fixed and variable.

voxels
******
One "dot" in a 3-D picture. Like "pixel" for 2-D pictures, but it's three-dimensional. Voxels have a given size, usually a few millimeters in any direction (although they can be isotropic_ or anisotropic_). Their size is specified in millimeters generally, like 2x2x3.5; the third dimension is generally the through-plane size or `slice thickness`_. In a given brain, you'll often have tens of thousands of voxels, even if you haven't resampled your voxels to be smaller during preprocessing_. Voxels are specified on a coordinate system that's different than the millimeter coordinate system; millimeters coordinates have their origin in the middle of the image (and so can be negative), whereas voxel coordinates start counting in one corner of the image and are always positive.

Voxel-based Morphometry (VBM)
*****************************
A type of analysis which doesn't look at functional images, but instead looks at the differences between subjects' anatomy. Anatomical images are segmented into different tissue types, and the measurements generally looked at are the total volume of gray matter (or white matter or CSF) in a given anatomical structure. This type of analysis is about the form, or morphometry of the brain, and it's based not on the surface of the brain or any dissection of it but on arbitrarily-sampled Voxels_ - hence the name. See `Segmentation FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#segmentation>`_ for more.


W
=

white noise
***********
Noise which is random and independent from measurement to measurement. In other words, it is equally strong in all frequencies. White noise is nice because it tends to average to zero, which enables the use of many simple smoothing_ techniques to get rid of it, although it tends to defeat filtering techniques. It's in contrast to colored noise, which has some correlation from timepoint to timepoint. fMRI noise tends to be pretty white in the spatial domain (with some exceptions) and severely colored in the temporal domain. See `Smoothing FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#smoothing>`_ and `Temporal Filtering FAQ <http://miykael.github.io/nipype-beginner-s-guide/faq.html#temporal-filtering>`_ for a little more.

whitening
*********
See `pre-whitening`_.

Workflow
********
Workflows are the core elements of Nipype and can also be called pipelines. Workflows consists of Nodes, MapNodes and other Workflows and define the sequential order data processing and other algorithms should be executed by. For more see this `beginner's guide introduction section <http://miykael.github.io/nipype-beginner-s-guide/nipype.html#workflow-engine>`_.


X
=


Y
=


Z
=


Numbers
=======

1.5T, 3T, 4T, 7T (etc.)
***********************
Ratings of different strengths of MRI scanners. T is the abbreviation for Tesla_, the international standard unit for magnetic flux density.
