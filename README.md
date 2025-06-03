# DDFacet tutorial for beginner
This documentation gives a brief overview of how to use DDFacet to input a LOFAR-type measurementSet and output reconstructed images. 

## Biblio 
:page_facing_up: [DDFacet](https://arxiv.org/pdf/1712.02078) *C. Tasse, B. Hugo, M. Mirmont, O. Smirnov, M. Atemkeng, L. Bester, M.J. Hardcastle4, R. Lakhoo, S. Perkins and T. Shimwel «Multi-core multi-node parallelization of the radio interferometric imaging pipeline DDFacet»*

:page_facing_up: [DDFacet parallel](https://arxiv.org/pdf/1712.02078) *N. Monnier, D. Guibert, C. Tasse, N. Gac, F. Orieux, E. Raffin, O. M. Smirnov, B. V. Hugo «Faceting for direction-dependent spectral deconvolution»*

## Requirements
- Download ddfacet singularity image: `ddf_dev_np1.22.4.sif` [NAS - vaader](https://nasext-vaader.insa-rennes.fr/ietr-vaader/)
- Download parset example: `Template.parset` [NAS - vaader](https://nasext-vaader.insa-rennes.fr/ietr-vaader/)
- Having a measurementSet (i.e. **\*.ms** ==> set of folders)
- (option) Download the script that facilitates reading **\*.fits** (based on the ds9 tool): `dsm.py` [NAS - vaader](https://nasext-vaader.insa-rennes.fr/ietr-vaader/)

## Preliminary step

- Run the following commands to install dependencies and prepare your working environment:
```bash
# install singularity
sudo apt update
sudo apt install singularity-container -y

# Install DS9 viewer (for FITS files)
sudo apt install saods9

# Create a writable folder for data
sudo mkdir -p /media/tasse/data
sudo chown -R $USER /media/tasse

```

- Once everything is ready, you can start DDFacet inside the container: 
    - Single architecture node (multicore I gess usage):
    ```bash
    # run the singularity environment
    singularity shell -B/home -B/media/tasse/data ./ddf_dev_np1.22.4.sif
    ```
    - Multi architecture node
    ```bash
    # run the singularity environment
    mpirun -np 2 singularity exec -B/home -B/media/tasse/data ./ddf_dev_np1.22.4.sif [DDFacet command directly]
    ```    
    
This will drop you into a shell where you can run `DDF.py` with your `.parset` file and `.ms` input.

## DDF command

<details>
    <summary style="cursor: pointer; color: #007bff;"> Click here to reveal the section </summary>
.

 This comes from `DDF.py -h`.   
    
```    
Usage: DDF.py [parset file] <options>

Questions and suggestions: cyril.tasse@obspm.fr

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Visibility data options:
    --Data-MS=MS(s)     Single MS name, or list of comma-separated MSs, or
                        name of *.txt file listing MSs.   Note that each MS
                        may also be specified as a glob pattern (e.g. *.MS),
                        and may be suffixed with "//Dx" and/or "//Fy" to
                        select specific DATA_DESC_ID and FIELD_IDs in the MS.
                        "x" and "y" can take the form of a single number, a
                        Pythonic range (e.g. "0:16"), an inclusive range
                        ("0~15"), or "*" to select all. E.g.
                        "foo.MS//D*//F0:2" selects all DDIDs, and fields 0 and
                        1 from foo.MS. If D and/or F is not specified,
                        --Selection-Field and --Selection-DDID is used as the
                        default. (default: )
    --Data-ColName=COLUMN
                        MS column to image (default: CORRECTED_DATA)
    --Data-ChunkHours=N
                        Process data in chunks of <=N hours. Use 0 for no
                        chunking. (default: 0.0)
    --Data-Sort=0|1     if True, data will be resorted by baseline-time order
                        internally. This usually speeds up processing.
                        (default: False)

  Predict:
    --Predict-ColName=COLUMN
                        MS column to write predict to. Can be empty to
                        disable. (default: none)
    --Predict-MaskSquare=IMAGE
                        Use this field if you want to predict (in/out)side a
                        square region. Syntax is (MaskOutSide,NpixInside). For
                        example setting (0,1000) will predict the outer
                        (1000x1000) square only (default: none)
    --Predict-FromImage=IMAGE
                        In --Image-Mode=Predict, will predict data from this
                        image, rather than --Data-InitDicoModel (default:
                        none)
    --Predict-InitDicoModel=FILENAME
                        Resume deconvolution from given DicoModel (default:
                        none)
    --Predict-Overwrite=0|1
                        Allow overwriting of predict column (default: True)

  Data selection options:
    --Selection-Field=FIELD
                        default FIELD_ID to read, if not specified in --Data-
                        MS. (default: 0)
    --Selection-DDID=DDID
                        default DATA_DESC_ID to read, if not specified in
                        --Data-MS. (default: 0)
    --Selection-TaQL=TaQL
                        additional TaQL selection string (default: )
    --Selection-ChanStart=N
                        First channel (default: 0)
    --Selection-ChanEnd=N
                        Last channel+1, -1 means up and including last
                        channel. (default: -1)
    --Selection-ChanStep=N
                        Channel stepping (default: 1)
    --Selection-FlagAnts=ANT,...
                        List of antennas to be flagged, e.g. "RS,CS017LBA"
                        (default: )
    --Selection-UVRangeKm=KM_MIN,KM_MAX
                        Select baseline range (default: [0, 2000])
    --Selection-TimeRange=SELECTION_TIMERANGE
                        Select time range (two comma separated values)
                        containing UTC start and end times in ISO8601
                        (default: )
    --Selection-TimeRangeFromStartMin=SELECTION_TIMERANGEFROMSTARTMIN
                        In minutes before start of obs. (default: )
    --Selection-DistMaxToCore=KM
                        Select antennas by specifying a maximum distance to
                        core (default: )
    --Selection-AutoFlagNyquist=SELECTION_AUTOFLAGNYQUIST
                        flag those baselines that are not properly sampled
                        (default: 0)

  Options for input and output image names:
    --Output-Mode=Dirty|Clean|Predict|PSF
                        What to do. (default: Clean)
    --Output-Clobber=0|1
                        Allow overwriting of existing parset and images (can't
                        be specified via parset!) (default: False)
    --Output-Name=BASENAME
                        Base name of output images (default: image)
    --Output-ShiftFacetsFile=OUTPUT_SHIFTFACETSFILE
                        Astrometric correction per facet, when Image-
                        Mode=RestoreAndShift (default: none)
    --Output-RestoringBeam=OUTPUT_RESTORINGBEAM
                         (default: none)
    --Output-Also=CODES
                        Save also these images (i.e. adds to the default set
                        of --Output-Images) (default: )
    --Output-Cubes=CODES
                        Also save cube versions for these images (only MmRrIi
                        codes recognized) (default: )
    --Output-Images=OUTPUT_IMAGES
                        Combination of letter codes indicating what images to
                        save.  Uppercase for intrinsic flux scale [D]irty,
                        [M]odel, [C]onvolved model, [R]esiduals, restored
                        [I]mage; Lowercase for apparent flux scale  [d]irty,
                        [m]odel, [c]onvolved model, [r]esiduals, restored
                        [i]mage; Other images: [P]SF, [N]orm, [n]orm facets,
                        [S] flux scale, [A]lpha (spectral index), [X] mixed-
                        scale (intrinsic model, apparent residuals, i.e.
                        Cyrils original output), [o] intermediate mOdels
                        (Model_i), [e] intermediate rEsiduals (Residual_i),
                        [k] intermediate masK image, [z] intermediate auto
                        mask-related noiZe image, [g] intermediate dirty
                        images (only if [Debugging]
                        SaveIntermediateDirtyImages is enabled). [F] intrinsic
                        MFS restored image [f] apparent MFS restored image Use
                        "all" to save all. (default: DdPAMRIikemz)
    --Output-StokesResidues=OUTPUT_STOKESRESIDUES
                        After cleaning Stokes I, output specified residues if
                        [r] or [R] is specified in option Output-Images. Note
                        that the imager does not perform deconvolution on any
                        Stokes products other than I - it only outputs
                        residues. (default: I)

  SPIMaps:
    --SPIMaps-AlphaThreshold=N
                        Multiple of the RMS in final residual which determines
                        threshold for fitting alpha map. (default: 15)

  General imager settings:
    --Image-NPix=NPIX   Image size. (default: 5000)
    --Image-Cell=ARCSEC
                        Cell size. (default: 5.0)
    --Image-PhaseCenterRADEC=RA,DEC
                        Use non-default phase centre. If "align" is used, all
                        MSs will be rephased to the phase centre of the first
                        MS. Otherwise, specify [HH:MM:SS,DD:MM:SS] direction.
                        If empty, no rephasing is done. (default: none)
    --Image-SidelobeSearchWindow=NPIX
                        Size of PSF subwindow (centred around the main lobe)
                        to search for the highest sidelobe when fitting the
                        PSF size. (default: 200)

  Spacial tessellation settings:
    --Facets-NFacets=N  Number of facets to use. (default: 3)
    --Facets-CatNodes=FACETS_CATNODES
                         (default: none)
    --Facets-DiamMax=DEG
                        Max facet size, for tessellations. Larger facets will
                        be broken up. (default: 180.0)
    --Facets-DiamMin=DEG
                        Min facet size, for tessellations. Smaller facets will
                        be merged. (default: 0.0)
    --Facets-MixingWidth=FACETS_MIXINGWIDTH
                        Sigma of the gaussian (in pixels) being used to mix
                        the facets on their edges (default: 10)
    --Facets-PSFOversize=X
                        For cleaning, use oversize PSF relative to size of
                        facet. (default: 1.0)
    --Facets-PSFFacets=N
                        Number of PSF facets to make. 0: same as NFacets (one
                        PSF per facet) 1: one PSF for entire field. (default:
                        0)
    --Facets-Padding=FACTOR
                        Facet padding factor. (default: 1.7)
    --Facets-Circumcision=N
                        Set to non-0 to override NPixMin computation in
                        FacetsToIm(). Debugging option, really. (default: 0)
    --Facets-FluxPaddingAppModel=FACETS_FLUXPADDINGAPPMODEL
                        For flux-dependent facet-padding, the apparant model
                        image (or cube) (default: none)
    --Facets-FluxPaddingScale=FACETS_FLUXPADDINGSCALE
                        The factor applied to the --Facets-Padding for the
                        facet with the highest flux (default: 2.0)
    --Facets-SkipTh=FACETS_SKIPTH
                        Skip gridding/degridding if the mean Jones power is
                        lower than this level (useful in mosaicing mode)
                        (default: 0.0)

  Data and imaging weight settings:
    --Weight-ColName=COLUMN
                        Read data weights from specified column. Use
                        WEIGHT_SPECTRUM or WEIGHT, more rarely IMAGING_WEIGHT.
                        You can also specify a list of columns like using
                        --Weight-ColName=[WEIGHT_SPECTRUM,IMAGING_WEIGHT]
                        (default: WEIGHT_SPECTRUM)
    --Weight-Mode=Natural|Uniform|Robust|Briggs
                        Image weighting. (default: Briggs)
    --Weight-MFS=0|1    If True, MFS uniform/Briggs weighting is used (all
                        channels binned onto one uv grid). If 0, binning is
                        per-band. (default: True)
    --Weight-Robust=R   Briggs robustness parameter, from -2 to 2. (default:
                        0.0)
    --Weight-SuperUniform=X
                        Super/subuniform weighting: FoV for weighting purposes
                        is taken as X*Image_Size (default: 1.0)
    --Weight-OutColName=COLUMN
                        Save the internally computed weights into this column
                        (default: none)
    --Weight-EnableSigmoidTaper=WEIGHT_ENABLESIGMOIDTAPER
                        Toggles sigmoid tapering type:bool (default: 0)
    --Weight-SigmoidTaperInnerCutoff=WEIGHT_SIGMOIDTAPERINNERCUTOFF
                        Inner taper cutoff in uvwavelengths type:float
                        (default: 0.0)
    --Weight-SigmoidTaperOuterCutoff=WEIGHT_SIGMOIDTAPEROUTERCUTOFF
                        Outer taper cutoff in uvwavelengths type:float
                        (default: 0.0)
    --Weight-SigmoidTaperInnerRolloffStrength=WEIGHT_SIGMOIDTAPERINNERROLLOFFSTRENGTH
                        Rolloff strength on inner taper if enabled. 1.0 is
                        essentially a boxcar, 0.0 means very long rolloffs
                        type:float (default: 0.5)
    --Weight-SigmoidTaperOuterRolloffStrength=WEIGHT_SIGMOIDTAPEROUTERROLLOFFSTRENGTH
                        Rolloff strength on outer taper if enabled. 1.0 is
                        essentially a boxcar, 0.0 means very long rolloffs
                        type:float (default: 0.5)

  Low level parameters related to the forward and backward image to visibility spaces transforms:
    --RIME-Precision=S|D
                        Single or double precision gridding. DEPRECATED?
                        (default: S)
    --RIME-PolMode=I|IQ|IU|IV|IQU|IQUV
                        Polarization mode. (default: I)
    --RIME-FullMTilde=RIME_FULLMTILDE
                        Uee the full MTilde as described in the paper to do
                        the image plane correction type:bool (default: False)
    --RIME-FFTMachine=RIME_FFTMACHINE
                         (default: FFTW)
    --RIME-ForwardMode=BDA-degrid|Classic|Montblanc
                        Forward predict mode. (default: BDA-degrid)
    --RIME-BackwardMode=BDA-grid|Classic
                        Backward mode. (default: BDA-grid)
    --RIME-DecorrMode=RIME_DECORRMODE
                        decorrelation mode (default: )
    --RIME-DecorrLocation=Center|Edge
                        where decorrelation is estimated (default: Edge)

  Imager convolution function settings:
    --CF-OverS=N        Oversampling factor. (default: 11)
    --CF-Support=N      CF support size. (default: 7)
    --CF-Nw=PLANES      Number of w-planes. Setting this to 1 enables AIPS
                        style faceting. (default: 100)
    --CF-wmax=METERS    Maximum w coordinate. Visibilities with larger w will
                        not be gridded. If 0, no maximum is imposed. (default:
                        0.0)

  Compression settings (baseline-dependent averaging [BDA] and sparsification):
    --Comp-GridDecorr=X
                        Maximum BDA decorrelation factor (gridding) (default:
                        0.02)
    --Comp-GridFoV=Full|Facet
                        FoV over which decorrelation factor is computed
                        (gridding) (default: Facet)
    --Comp-DegridDecorr=X
                        Maximum BDA decorrelation factor (degridding)
                        (default: 0.02)
    --Comp-DegridFoV=Full|Facet
                        FoV over which decorrelation factor is computed
                        (degridding) (default: Facet)
    --Comp-Sparsification=N1,N2,...
                        apply sparsification compression to initial major
                        cycles. Sparsification refers to throwing away random
                        visibilities. Supply a list of factors: e.g. 100,30,10
                        would mean only 1/100 of the data is used for the
                        first major cycle, 1/30 for the second, 1/10 for the
                        third, and full data for the fourth cycle onwards.
                        This can substantially accelerate deconvolution of
                        deep observations, since, in these regimes, very
                        little sensitivity is required for model construction
                        in the initial cycles. (default: 0)
    --Comp-BDAMode=1|2  BDA block computation mode. 1 for Cyril's old mode, 2
                        for Oleg's new mode. 2 is faster but see issue #319.
                        (default: 1)
    --Comp-BDAJones=COMP_BDAJONES
                        If disabled, gridders and degridders will apply a
                        Jones terms per visibility. If 'grid', gridder will
                        apply them per BDA block, if 'both' so will the
                        degridder. This is faster but possibly less accurate,
                        if you have rapidly evolving Jones terms. (default: 0)

  Parallelization options:
    --Parallel-NCPU=N   Number of CPUs to use in parallel mode. 0: use all
                        available. 1: disable parallelism. (default: 0)
    --Parallel-Affinity=PARALLEL_AFFINITY
                        pin processes to cores. -1/1/2 determines stepping
                        used in selecting cores. Alternatively specifies a
                        list of length NCPU. Alternatively "disable" to
                        disable affinity settings Alternatively "enable_ht"
                        uses stepping of 1 (equivalent to
                        Parallel.Affinity=1), will use all vthreads - the
                        obvious exception is if HT is disabled at BIOS level
                        Alternatively "disable_ht" autodetects the NUMA layout
                        of the chip for Debian-based systems and dont use both
                        vthreads per core Use 1 if unsure. (default: 1)
    --Parallel-MainProcessAffinity=PARALLEL_MAINPROCESSAFFINITY
                        this should be set to a core that is not used by
                        forked processes, this option is ignored when using
                        option "disable or disable_ht" for Parallel.Affinity
                        (default: 0)
    --Parallel-MotherNode=PARALLEL_MOTHERNODE
                         (default: localhost)

  Cache management options:
    --Cache-Reset=0|1   Reset all caches (including PSF and dirty image)
                        (default: False)
    --Cache-Jones=reset|auto
                        Reset cached Jones (default: auto)
    --Cache-SmoothBeam=reset|auto|force
                        Reset cached smooth beam (default: auto)
    --Cache-Weight=reset|auto
                        Reset cached weight (default: auto)
    --Cache-PSF=off|reset|auto|force
                        Cache PSF data. (default: auto)
    --Cache-Dirty=off|reset|auto|forcedirty|forceresidual
                        Cache dirty image data. (default: auto)
    --Cache-VisData=off|auto|force
                        Cache visibility data and flags at runtime. (default:
                        auto)
    --Cache-LastResidual=0|1
                        Cache last residual data (at end of last minor cycle)
                        (default: True)
    --Cache-Dir=CACHE_DIR
                        Directory to store caches in. Default is to keep cache
                        next to the MS, but this can cause performance issues
                        with e.g. NFS volumes. If you have fast local storage,
                        point to it. %metavar:DIR (default: )
    --Cache-DirWisdomFFTW=CACHE_DIRWISDOMFFTW
                        Directory in which to store the FFTW wisdom files
                        (default: ~/.fftw_wisdom)
    --Cache-ResetWisdom=0|1
                        Reset Wisdom file (default: False)
    --Cache-CF=0|1      Cache convolution functions. With many CPUs, may be
                        faster to recompute. (default: True)
    --Cache-HMP=0|1     Cache HMP basis functions. With many CPUs, may be
                        faster to recompute. (default: False)

  Apply E-Jones (beam) during imaging:
    --Beam-Model=None|LOFAR|FITS|GMRT|ATCA
                        Beam model to use. (default: none)
    --Beam-At=facet|tessel
                        when DDESolutions are enabled, compute beam per facet,
                        or per larger solution tessel (default: facet)
    --Beam-PhasedArrayMode=A|AE
                        PhasedArrayMode beam mode. (default: AE)
    --Beam-NBand=N      Number of channels over which same beam value is used.
                        0 means use every channel. (default: 0)
    --Beam-CenterNorm=0|1
                        Normalize beam so that its amplitude at the centre is
                        1. (default: False)
    --Beam-Smooth=BEAM_SMOOTH
                        Compute the interpolated smooth beam (default: False)
    --Beam-SmoothNPix=BEAM_SMOOTHNPIX
                        Number of pixels the beam is evaluated and smoothed
                        (default: 11)
    --Beam-SmoothInterpMode=BEAM_SMOOTHINTERPMODE
                        Linear/Log (default: Linear)
    --Beam-FITSFile=BEAM_FITSFILE
                        Beam FITS file pattern. A beam pattern consists of
                        eight FITS files, i.e. a real and imaginary part for
                        each of the four Jones terms. The following
                        substitutions are performed to form up the eight
                        filenames: $(corr) or $(xy) is replaced by the Jones
                        element label (e.g. "xx" or "rr"), $(reim) is replaced
                        by "re" or "im", $(realimag) is replaced by "real" or
                        "imag". Uppercase variables are replaced by uppercase
                        values, e.g. $(REIM) by "RE" pr "IM". Use "unity" if
                        you want to apply a unity matrix for the E term (e.g.
                        only want to do visibility derotations). Correlation
                        labels (XY or RL) are determined by reading the MS,
                        but may be overridden by the FITSFeed option. To use a
                        heterogeneous mix of beams you have to first type
                        specialize the antennas using a json configuration of
                        the following format: {'lband': { 'patterns': {
                        'cmd::default': ['$(stype)_$(corr)_$(reim).fits',...],
                        }, 'define-stationtypes': { 'cmd::default': 'meerkat',
                        'ska000': 'ska' } }, ... } This will substitute
                        'meerkat' for all antennas but ska000, with
                        'meerkat_$(corr)_$(reim).fits' whereas beams for
                        ska000 will be loaded from 'ska_$(corr)_$(reim).fits'
                        in this example. The station name may be specified as
                        regex by adding a '~' infront of the pattern to match,
                        e.g '~ska[0-9]{3}': 'ska' will assgign all the 'ska'
                        type to all matching names such as ska000, ska001,
                        ..., skaNNN. Each station type in the pattern section
                        may specify a list of patterns for different frequency
                        ranges. Multiple keyed dictionaries such as this may
                        be specified within one file. They will be treated as
                        chained configurations, adding more patterns and
                        station-types to the first such block. Warning: Once a
                        station is type-specialized the type applies to
                        **ALL** chained blocks! Blocks from more than one
                        config file can be loaded by comma separation, e.g. '
                        --Beam-FITSFile conf1.json,conf2.json,...', however no
                        block may define multiple types for any station. If
                        patterns for a particular station type already exists
                        more patterns are just appended to the existing list.
                        Warning: where multiple patterns specify the same
                        frequency range the first such pattern closest to the
                        MS SPW frequency coverage will be loaded. If no
                        configuration file is provided the pattern may not
                        contain $(stype) -- station independence is assumed.
                        This is the same as specifing the following config:
                        {'lband': { 'patterns': { 'cmd::default':
                        ['$(corr)_$(reim).fits',...], }, 'define-
                        stationtypes': { 'cmd::default': 'cmd::default' } }
                        (default: beam_$(corr)_$(reim).fits)
    --Beam-FITSFeed=None|xy|XY|rl|RL
                        If set, overrides correlation labels given by the
                        measurement set. (default: none)
    --Beam-FITSFeedSwap=0|1
                        swap feed patterns (X to Y and R to L) (default:
                        False)
    --Beam-DtBeamMin=MIN
                        change in minutes on which the beam is re-evaluated
                        (default: 5.0)
    --Beam-FITSParAngleIncDeg=DEG
                        increment in PA in degrees at which the beam is to be
                        re-evaluated (on top of DtBeamMin) (default: 5.0)
    --Beam-FITSLAxis=AXIS
                        L axis of FITS file. Minus sign indicates reverse
                        coordinate convention. (default: -X)
    --Beam-FITSMAxis=AXIS
                        M axis of FITS file. Minus sign indicates reverse
                        coordinate convention. (default: Y)
    --Beam-FITSVerbosity=LEVEL
                        set to >0 to have verbose output from FITS
                        interpolator classes. (default: 0)
    --Beam-FITSFrame=BEAM_FITSFRAME
                        coordinate frame for FITS beams. Currently, alt-az,
                        equatorial and zenith mounts are supported. (default:
                        altaz)
    --Beam-FeedAngle=BEAM_FEEDANGLE
                        offset feed angle to add to parallactic angle
                        (default: 0.0)
    --Beam-ApplyPJones=BEAM_APPLYPJONES
                        derotate visibility data (only when FITS beam is
                        active and also time sampled). If you have equatorial
                        mounts this is not what you should be doing! (default:
                        0)
    --Beam-FlipVisibilityHands=BEAM_FLIPVISIBILITYHANDS
                        apply anti-diagonal matrix if FITS beam is enabled
                        effectively swapping X and Y or R and L and their
                        respective hands (default: 0)

  Multifrequency imaging options:
    --Freq-BandMHz=MHz  Gridding cube frequency step. If 0, --Freq-NBand is
                        used instead. (default: 0.0)
    --Freq-FMinMHz=MHz  Gridding cube frequency Min. If 0, is ignored.
                        (default: 0.0)
    --Freq-FMaxMHz=MHz  Gridding cube frequency Max. If 0, is ignored.
                        (default: 0.0)
    --Freq-DegridBandMHz=MHz
                        Degridding cube frequency step. If 0, --Freq-
                        NDegridBand is used instead. (default: 0.0)
    --Freq-NBand=N      Number of image bands for gridding. (default: 1)
    --Freq-NDegridBand=N
                        Number of image bands for degridding. 0 means degrid
                        each channel. (default: 0)

  Apply DDE solutions during imaging (@cyriltasse please document this section):
    --DDESolutions-DDSols=DDESOLUTIONS_DDSOLS
                        Name of the DDE solution file (default: )
    --DDESolutions-SolsDir=DDESOLUTIONS_SOLSDIR
                        Name of the directry of the DDE Solutions which
                        contains
                        <SolsDir>/<MSNames>/killMS.<SolsName>.sols.npz
                        (default: none)
    --DDESolutions-GlobalNorm=DDESOLUTIONS_GLOBALNORM
                        Option to normalise the Jones matrices (options:
                        MeanAbs, MeanAbsAnt, BLBased or SumBLBased). See code
                        for more detail (default: none)
    --DDESolutions-JonesNormList=DDESOLUTIONS_JONESNORMLIST
                        Deprecated? (default: AP)
    --DDESolutions-JonesMode=Scalar|Diag|Full
                         (default: Full)
    --DDESolutions-DDModeGrid=DDESOLUTIONS_DDMODEGRID
                        In the gridding step, apply Jones matrices Amplitude
                        (A) or Phase (P) or Amplitude&Phase (AP) (default: AP)
    --DDESolutions-DDModeDeGrid=DDESOLUTIONS_DDMODEDEGRID
                        In the degridding step, apply Jones matrices Amplitude
                        (A) or Phase (P) or Amplitude&Phase (AP) (default: AP)
    --DDESolutions-ScaleAmpGrid=DDESOLUTIONS_SCALEAMPGRID
                        Deprecated? (default: 0)
    --DDESolutions-ScaleAmpDeGrid=DDESOLUTIONS_SCALEAMPDEGRID
                        Deprecated? (default: 0)
    --DDESolutions-CalibErr=DDESOLUTIONS_CALIBERR
                        Deprecated? (default: 10.0)
    --DDESolutions-Type=Krigging|Nearest
                        Deprecated? (default: Nearest)
    --DDESolutions-Scale=DEG
                        Deprecated? (default: 1.0)
    --DDESolutions-gamma=DDESOLUTIONS_GAMMA
                        Deprecated? (default: 4.0)
    --DDESolutions-RestoreSub=DDESOLUTIONS_RESTORESUB
                        Deprecated? (default: False)
    --DDESolutions-ReWeightSNR=DDESOLUTIONS_REWEIGHTSNR
                        Deprecated? (default: 0.0)

  Apply pointing offsets to beam during DFT predict. Requires Montblanc in --RIME-ForwardMode.:
    --PointingSolutions-PointingSolsCSV=POINTINGSOLUTIONS_POINTINGSOLSCSV
                        Filename of CSV containing time-variable pointing
                        solutions. None initializes all antenna pointing
                        offsets to 0, 0 (default: none)
    --PointingSolutions-InterpolationMode=LERP
                        Interpolation mode (default: LERP)

  Common deconvolution options. Not all of these apply to all deconvolution modes:
    --Deconv-Mode=HMP|Hogbom|SSD|WSCMS
                        Deconvolution algorithm. (default: HMP)
    --Deconv-MaxMajorMaxMajorIter=N
                        Max number of major cycles. (default: 20)
    --Deconv-MaxMinorIter=N
                        Max number of (overall) minor cycle iterations (HMP,
                        Hogbom). (default: 20000)
    --Deconv-AllowNegative=0|1
                        Allow negative components (HMP, Hogbom). (default:
                        True)
    --Deconv-Gain=GAIN  Loop gain (HMP, Hogbom). (default: 0.1)
    --Deconv-FluxThreshold=Jy
                        Absolute flux threshold at which deconvolution is
                        stopped  (HMP, Hogbom, SSD). (default: 0.0)
    --Deconv-CycleFactor=X
                        Cycle factor: used to set a minor cycle stopping
                        threshold based on PSF sidelobe level  (HMP, Hogbom).
                        Use 0 to disable, otherwise 2.5 is a reasonable value,
                        but may lead to very shallow minor cycle. (default:
                        0.0)
    --Deconv-RMSFactor=X
                        Set minor cycle stopping threshold to X*{residual RMS
                        at start of major cycle}  (HMP, Hogbom, SSD).
                        (default: 0.0)
    --Deconv-PeakFactor=X
                        Set minor cycle stopping threshold to X*{peak residual
                        at start of major cycle}  (HMP, Hogbom, SSD).
                        (default: 0.15)
    --Deconv-PrevPeakFactor=X
                        Set minor cycle stopping threshold to X*{peak residual
                        at end of previous major cycle} (HMP). (default: 0.0)
    --Deconv-NumRMSSamples=N
                        How many samples to draw for RMS computation. Use 0 to
                        use all pixels (most precise). (default: 10000)
    --Deconv-ApproximatePSF=SF
                        when --Comp-Sparsification is on, use approximate
                        (i.e. central facet) PSF for cleaning while operating
                        above the given sparsification factor (SF). This
                        speeds up HMP reinitialization in major cycles. A
                        value of 1-10 is sensible. Set to 0 to always use
                        precise per-facet PSF. (default: 0)
    --Deconv-PSFBox=BOX
                        determines the size of the PSF subtraction box used in
                        CLEAN-style deconvolution (if appropriate). Use "auto"
                        (or "sidelobe") for a Clark-CLEAN-style box taken out
                        to a certain sidelobe (faster). Use "full" to subtract
                        the full PSF, Hogbom-style (more accurate, can also
                        combine with --Image-PSFOversize for maximum
                        accuracy). Use an integer number to set an explicit
                        box radius, in pixels. (HMP) (default: auto)

  Masking options. The logic being Mask_{i+1} = ExternalMask | ResidualMask | Mask_{i}:
    --Mask-External=FILENAME
                        External clean mask image (FITS format). (default:
                        none)
    --Mask-Auto=MASK_AUTO
                        Do automatic masking (default: False)
    --Mask-AutoRMSFactor=MASK_AUTORMSFACTOR
                        RMS Factor for automasking HMP (default: 3)
    --Mask-SigTh=MASK_SIGTH
                        set Threshold (in sigma) for automatic masking
                        (default: 10)
    --Mask-FluxImageType=MASK_FLUXIMAGETYPE
                        If Auto enabled, does the cut of SigTh either on the
                        ModelConv or the Restored (default: ModelConv)

  When using a noise map to HMP or to mask:
    --Noise-MinStats=NOISE_MINSTATS
                        The parameters to compute the noise-map-based mask for
                        step i+1 from the residual image at step i. Should be
                        [box_size,box_step] (default: [60, 2])
    --Noise-BrutalHMP=NOISE_BRUTALHMP
                        If noise map is computed, this option enabled, it
                        first computes an image plane deconvolution with a
                        high gain value, and compute the noise-map-based mask
                        using the brutal-restored image (default: True)

  Hybrid Matching Pursuit (aka multiscale/multifrequency) mode deconvolution options:
    --HMP-Alpha=MIN,MAX,N
                        List of alphas to fit. (default: [-1.0, 1.0, 11])
    --HMP-Scales=LIST   List of scales to use. (default: [0])
    --HMP-Ratios=HMP_RATIOS
                        @cyriltasse please document (default: [''])
    --HMP-NTheta=N      Number of PA steps to use. (default: 6)
    --HMP-SolverMode=PI|NNLS
                        Solver mode: pseudoinverse, or non-negative least
                        squares. (default: PI)
    --HMP-AllowResidIncrease=FACTOR
                        Allow the maximum residual to increase by at most this
                        much relative to the lowest residual, before bailing
                        out due to divergence. (default: 0.1)
    --HMP-MajorStallThreshold=X
                        Major cycle stall threshold. If the residual at the
                        beginning of a major cycle is above X*residual at the
                        beginning of the previous major cycle, then we
                        consider the deconvolution stalled and bail out.
                        (default: 0.8)
    --HMP-Taper=HMP_TAPER
                        Weighting taper size for HMP fit. If 0, determined
                        automatically. (default: 0)
    --HMP-Support=HMP_SUPPORT
                        Basis function support size. If 0, determined
                        automatically. (default: 0)
    --HMP-PeakWeightImage=HMP_PEAKWEIGHTIMAGE
                        weigh the peak finding by given image (default: none)
    --HMP-Kappa=HMP_KAPPA
                        Regularization parameter. If stddev of per-alpha
                        solutions exceeds the maximum solution amplitude
                        divided by Kappa, forces a fully-regularized solution.
                        Use 0 for no such regularization. (default: 0.0)
    --HMP-OuterSpaceTh=HMP_OUTERSPACETH
                         (default: 2.0)
    --HMP-FractionRandomPeak=HMP_FRACTIONRANDOMPEAK
                         (default: none)

  Hogbom:
    --Hogbom-PolyFitOrder=HOGBOM_POLYFITORDER
                        polynomial order for frequency fitting (default: 4)
    --Hogbom-LinearPeakfinding=Joint|Separate
                        Perform EVPA-preserving (complex-valued) polarization
                        CLEAN (Pratley-Johnston-Hollitt) or separate Q and U
                        cleaning. (default: Joint)

  WSCMS:
    --WSCMS-NumFreqBasisFuncs=WSCMS_NUMFREQBASISFUNCS
                        number of basis functions to use for the fit to the
                        frequency axis (default: 4)
    --WSCMS-MultiScale=WSCMS_MULTISCALE
                        whether to use multi-scale or not (recommended to use
                        Hogbom if not using multi-scale) (default: True)
    --WSCMS-MultiScaleBias=WSCMS_MULTISCALEBIAS
                        scale bias parameter (smaller values give more weight
                        to larger scales) (default: 0.55)
    --WSCMS-ScaleBasis=WSCMS_SCALEBASIS
                        the kind of scale kernels to use (only Gauss available
                        for now) (default: Gauss)
    --WSCMS-Scales=WSCMS_SCALES
                        Scale sizes in pixels/FWHM eg. [0, 4, 8, 16] (if None
                        determined automatically) (default: none)
    --WSCMS-MaxScale=WSCMS_MAXSCALE
                        The maximum extent of the scale functions in pixels
                        (default: 250)
    --WSCMS-NSubMinorIter=WSCMS_NSUBMINORITER
                        Number of iterations for the sub minor loop (default:
                        250)
    --WSCMS-SubMinorPeakFact=WSCMS_SUBMINORPEAKFACT
                        Peak factor of sub minor loop (default: 0.85)
    --WSCMS-MinorStallThreshold=WSCMS_MINORSTALLTHRESHOLD
                        if the peak in the minor cycle decreases by less than
                        this fraction it has stalled and we go back to the
                        major cycle (default: 1e-07)
    --WSCMS-MinorDivergenceFactor=WSCMS_MINORDIVERGENCEFACTOR
                        if the peak flux increases by more than this fraction
                        between minor cycles then it has diverged and we go
                        back to a major cycle (default: 1.3)
    --WSCMS-AutoMask=WSCMS_AUTOMASK
                        whether to use scale dependent auto-masking (default:
                        True)
    --WSCMS-AutoMaskThreshold=WSCMS_AUTOMASKTHRESHOLD
                        Threshold at which the scale dependent mask should be
                        fixed. (default: none)
    --WSCMS-AutoMaskRMSFactor=WSCMS_AUTOMASKRMSFACTOR
                        Default multiple of RMS at which to start AutoMasking
                        in case no (default: 3)
    --WSCMS-CacheSize=WSCMS_CACHESIZE
                        the number of items to keep in the cache dict before
                        spilling over to disk (default: 3)
    --WSCMS-Padding=WSCMS_PADDING
                        padding in the minor cycle. Can often be much smaller
                        than facet padding (default: 1.2)

  Montblanc settings (for --Image-PredictMode=Montblanc):
    --Montblanc-TensorflowServerTarget=URL
                        URL for the TensorflowServer, e.g.
                        grpc://tensorflow.server.com:8888/ (default: )
    --Montblanc-LogFile=FILENAME
                        None to dump as Output-Name.montblanc.log, otherwise
                        user-specified filename (default: none)
    --Montblanc-MemoryBudget=MONTBLANC_MEMORYBUDGET
                        Predictor memory budget in GiB (default: 4.0)
    --Montblanc-LogLevel=NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL
                        Log level to write to console, rest of the messages
                        goes to log file (default: WARNING)
    --Montblanc-SolverDType=single|double
                        Data type used in solver, (default: double)
    --Montblanc-DriverVersion=tf
                        Backend to use, (default: tf)

  SSD deconvolution mode settings:
    --SSDClean-Parallel=0|1
                        Enable parallel mode. (default: True)
    --SSDClean-IslandDeconvMode=SSDCLEAN_ISLANDDECONVMODE
                        Moresane, GA, Sasir, ... (default: GA)
    --SSDClean-SSDSolvePars=SSDCLEAN_SSDSOLVEPARS
                         (default: ['S', 'Alpha'])
    --SSDClean-SSDCostFunc=SSDCLEAN_SSDCOSTFUNC
                         (default: ['Chi2', 'MinFlux'])
    --SSDClean-BICFactor=SSDCLEAN_BICFACTOR
                         (default: 0.0)
    --SSDClean-ArtifactRobust=SSDCLEAN_ARTIFACTROBUST
                         (default: False)
    --SSDClean-ConvFFTSwitch=SSDCLEAN_CONVFFTSWITCH
                         (default: 1000)
    --SSDClean-NEnlargePars=SSDCLEAN_NENLARGEPARS
                         (default: 0)
    --SSDClean-NEnlargeData=SSDCLEAN_NENLARGEDATA
                         (default: 2)
    --SSDClean-RestoreMetroSwitch=SSDCLEAN_RESTOREMETROSWITCH
                         (default: 0)
    --SSDClean-MinMaxGroupDistance=SSDCLEAN_MINMAXGROUPDISTANCE
                         (default: [10, 50])
    --SSDClean-MaxIslandSize=SSDCLEAN_MAXISLANDSIZE
                         (default: 0)
    --SSDClean-InitType=SSDCLEAN_INITTYPE
                         (default: HMP)

  SSD2 deconvolution mode settings:
    --SSD2-PolyFreqOrder=SSD2_POLYFREQORDER
                        Add Polyi to --SSDClean-SSDSolvePars. (default: 2)
    --SSD2-SolvePars=SSD2_SOLVEPARS
                         (default: ['Poly'])
    --SSD2-InitType=SSD2_INITTYPE
                         (default: ['HMP', 'MultiSlice:Orieux'])
    --SSD2-ConvexifyIslands=SSD2_CONVEXIFYISLANDS
                         (default: 1)
    --SSD2-NLastCyclesDeconvAll=SSD2_NLASTCYCLESDECONVALL
                        This parameter sets how many of the last cycles will
                        deconvolve all islands. If set to 0, SSD2 will use
                        --Deconv-CycleFactor, --Deconv-PeakFactor, --Deconv-
                        RMSFactor to determine threshold above which islands
                        are reestimated. If set to 2, in the last 2 major
                        cycle all islands are estimated. If -1: Always deconv
                        all islands regardless of the cycle number (default:
                        1)

  MultiSliceDeconv:
    --MultiSliceDeconv-Type=MULTISLICEDECONV_TYPE
                        MORESANE, Orieux, etc (default: MORESANE)
    --MultiSliceDeconv-PolyFitOrder=MULTISLICEDECONV_POLYFITORDER
                         (default: 2)

  GAClean:
    --GAClean-NSourceKin=GACLEAN_NSOURCEKIN
                         (default: 50)
    --GAClean-NMaxGen=GACLEAN_NMAXGEN
                         (default: 50)
    --GAClean-MinSizeInit=GACLEAN_MINSIZEINIT
                         (default: 10)
    --GAClean-AlphaInitHMP=GACLEAN_ALPHAINITHMP
                         (default: [-4.0, 1.0, 6])
    --GAClean-ScalesInitHMP=GACLEAN_SCALESINITHMP
                         (default: [0, 1, 2, 4, 8, 16, 24, 32])
    --GAClean-GainInitHMP=GACLEAN_GAININITHMP
                         (default: 0.1)
    --GAClean-RatiosInitHMP=GACLEAN_RATIOSINITHMP
                         (default: [''])
    --GAClean-NThetaInitHMP=GACLEAN_NTHETAINITHMP
                         (default: 4)
    --GAClean-MaxMinorIterInitHMP=GACLEAN_MAXMINORITERINITHMP
                         (default: 10000)
    --GAClean-AllowNegativeInitHMP=GACLEAN_ALLOWNEGATIVEINITHMP
                         (default: False)
    --GAClean-RMSFactorInitHMP=GACLEAN_RMSFACTORINITHMP
                         (default: 3.0)
    --GAClean-ParallelInitHMP=0|1
                        run island init in parallel. Serial mode may reduce
                        RAM pressure, and could be useful for debugging.
                        (default: True)
    --GAClean-NCPU=GACLEAN_NCPU
                        number of cores to use for parallel fitness
                        calculations (in large-island mode). Default of 0
                        means use as many as specified by --Parallel-NCPU. If
                        you find yourself running out of memory here, you
                        might want to specify a small number of cores for this
                        step. (default: 0)

  PyMoresane internal options:
    --MORESANE-NMajorIter=MORESANE_NMAJORITER
                        Maximum number of iterations allowed in the major
                        loop. Exit condition. (default: 200)
    --MORESANE-NMinorIter=MORESANE_NMINORITER
                        Maximum number of iterations allowed in the minor
                        loop. Serves as an exit condition when the SNR is does
                        not reach a maximum. (default: 200)
    --MORESANE-Gain=MORESANE_GAIN
                        Loop gain for the deconvolution. (default: 0.1)
    --MORESANE-ForcePositive=MORESANE_FORCEPOSITIVE
                        Boolean specifier for whether or not a model must be
                        strictly positive. (default: True)
    --MORESANE-SigmaCutLevel=MORESANE_SIGMACUTLEVEL
                        Number of sigma at which thresholding is to be
                        performed. (default: 1)

  Options related to logging:
    --Log-Memory=0|1    log memory use (default: False)
    --Log-Boring=0|1    disable progress bars and other pretty console output
                        (default: False)
    --Log-Append=0|1    append to log file if it exists (default truncates)
                        (default: False)

  Debugging options for the discerning masochist:
    --Debug-PauseWorkers=0|1
                        Pauses worker processes upon launch (with SIGSTOP).
                        Useful to attach gdb to workers. (default: False)
    --Debug-FacetPhaseShift=L,M
                        Shift in facet coordinates in arcseconds for l and m
                        (this phase steers the sky over the image plane).
                        (default: [0.0, 0.0])
    --Debug-PrintMinorCycleRMS=0|1
                        Compute and print RMS in minor cycle iterations.
                        (default: False)
    --Debug-DumpCleanSolutions=DEBUG_DUMPCLEANSOLUTIONS
                        Dump intermediate minor cycle solutions to a file. Use
                        0 or 1, or give an explicit list of things to dump
                        (default: 0)
    --Debug-DumpCleanPostageStamps=X,Y,R
                        Also dump postage stamps when cleaning within a radius
                        R of X,Y. Implies --Debug-DumpCleanSolutions.
                        (default: )
    --Debug-CleanStallThreshold=DEBUG_CLEANSTALLTHRESHOLD
                        Throw an exception when a fitted CLEAN component is
                        below this threshold in flux. Useful for debugging.
                        (default: 0.0)
    --Debug-MemoryGreedy=0|1
                        Enable memory-greedy mode. Retain certain shared
                        arrays in RAM as long as possible. (default: True)
    --Debug-APPVerbose=DEBUG_APPVERBOSE
                        Verbosity level for multiprocessing. (default: 0)
    --Debug-Pdb=never|always|auto
                        Invoke pdb on unexpected error conditions (rather than
                        exit).  If set to 'auto', then invoke pdb only if
                        --Log-Boring is 0. (default: auto)

  Miscellaneous options:
    --Misc-RandomSeed=N
                        seed random number generator with explicit seed, if
                        given. Useful for reproducibility of the random-based
                        optimizations (sparsification, etc.). (default: none)
    --Misc-ConserveMemory=MISC_CONSERVEMEMORY
                        if true, tries to minimize memory use at possible
                        expense of runtime. (default: 0)
    --Misc-IgnoreDeprecationMarking=0|1
                        if true, tries to run deprecated modes.  Currently
                        this means that deconvolution machines are reset and
                        reinitialized each major cycle. (default: False)
```
                            
                            
</details>
                            
                          

## Example 
                            
### Single node (multicore) Execution
                            
#### Default imaging (dirty map)

```bash
DDF.py Template.parset \
    --Data-MS 0000.MS \
    --Output-Name default/test \
    --Data-ColName DATA
```
                            
###### Output: 
The command will generate two FITS files in the `default` folder:
* `test.dirty.fits`: The raw, uncalibrated image.
* `test.dirty.corr.fits`: The calibrated image (if calibration is applied).
                            
###### Displaying the results:
`python dsm.py default/test.dirty.fits`
or if you don't mind about calibration: `ds9 *.fits -lock frame wcs -zoom to fit`
                                                     
![ds9](https://hackmd.io/_uploads/rk9bjCEkex.png)
> :bulb: Color map suggestion in DS9: Color > `inferno`                            
#### Degridding
To generate model visibilities from an input image (useful for subtraction or calibration):
- copy a `test.dirty.fits` file in the right location. 
    

```
DDF.py Template.parset \
    --Data-MS 0000.MS \ 
    --Output-Name predict/test \ 
    --Output-Mode Predict \ 
    --Predict-ColName DDF_PREDICT  \
    --Predict-FromImage predict/test.dirty.fits
```
    
###### Output: 
The command will generate two FITS files in the `default` folder:
* `test.cube.model.fits`: Spectral cube model

The command will also store the predicted visibilities in the column `DDF_PREDICT` of `0000.MS`


> :bulb: If the input image (`.fits`) only contains a single frequency channel and the MS has multiple channels, DDFacet will replicate the image across the spectral axis to create a matching cube.


                            
#### Clean
When you observe the sky with a radio telescope, you don't get a perfect image right away. What you get is a dirty image — it contains real sources, but also lots of artifacts from the instrument's point spread function (PSF). The Clean mode helps remove these artifacts and reconstruct a clearer, more realistic image of the sky. Use this mode when you want to visualize a usable sky image or create accurate sky models for calibration or source subtraction.
  
```
DDF.py Template.parset \
  --Data-MS 0000.MS \
  --Output-Name clean/test \
  --Output-Mode Clean \
  --Deconv-Mode HMP \
  --Freq-NBand 3 \
  --Freq-NDegridBand 1 \
  --Mask-Auto True \
  --Mask-SigTh 15 \
  --Mask-AutoRMSFactor 3 \
  --Deconv-MaxMajorIter 1 \
  --Deconv-MaxMinorIter 5
```
###### Output: 
The command will generate two FITS files in the `clean` folder:
* `test.alfa.fits`: Weight map showing confidence per pixel in the model.
* `test.app.model.fits`: The reconstructed model of the sky (just the detected sources).
* `test.app.restored.fits`: The final clean image: model + residual smoothed with the PSF.
* `test.brutalModelConv01.fits`: Raw versions of model images (for advanced use/debugging).
* `test.brutalRestored01.fits`: Raw versions of restored images (for advanced use/debugging).
* `test.mask01.fits`: Mask used to guide automatic cleaning (based on signal thresholds).
* `test.noise01.fits`: Noise estimation map of the image.
* `test.residual01.fits`: What’s left after subtracting the model from the dirty image.
    
    
![Screenshot from 2025-04-23 11-43-11](https://hackmd.io/_uploads/Hk_9PVLkgg.png)

    
|Deconv-Mode | Speed | Resources | Use When…|
| -------- | -------- | -------- | -------- |
|HMP (Harmonic Matching Pursuit)| 🟢 Fast | 🟢 Light | You want quick results and decent cleaning, good default.|
Hogbom | 🟡 Medium | 🟡 Medium | Classic CLEAN, for point sources.
SSD (Steepest-Descent Deconvolution)| 🔴 Very Slow | 🔴 Heavy | Gradient-based deconv, avoid unless you really need precise large-scale structures.
WSCMS (Weighted Source Component Model Subtaction) | 🔴 Very Slow | 🔴 Heavy | Advanced method for complex sky models, but slow and memory-hungry.
    
    
### Multinode Execution
#### Requirements
- Multinode & multicore cluster
- Dowload python casacore: `pip install python-casacore`
- Having a distributed MeasuremenSet or download the script to split yours [here](https://github.com/Ophelie-Renaud/ddfacet-dft-fft-g2g-tutorials). Usage: 
    ```python
    python split_ms_tool.py /path/to/my.ms output_prefix --criterion field --n_splits 3
    ```
    *where `criterion field` ∈ [`time` (default: split by observation time), `scan` (split by scan number, continuous observation sequence), `field` (split by field/source ID), `spw` (split by spectral window (frequency), `channel` (split each spectral channel into a separate MS)], `n_splits` by default limited to your MS criterion field* .


    

#### Default imaging (dirty map)
Change the measurementSets names with your distributed measuremenSets names.
```
mpirun -np 2 singularity exec -B /home -B /media/tasse/data \
./ddf_dev_np1.22.4.sif DDF.py Template.parset \
--Data-MS 0000.MS,0000.MS \
--Output-Name default/test \
--Data-ColName DATA
```

#### Degridding    
```
mpirun -np 2 singularity exec -B /home -B /media/tasse/data \
./ddf_dev_np1.22.4.sif DDF.py Template.parset \
--Data-MS 0000.MS,0000.MS \
--Output-Name predict/test \ 
--Output-Mode Predict \ 
--Predict-ColName DDF_PREDICT \
--Predict-FromImage predict/test.dirty.fits
```    

#### Clean


<p align="center">
  <img src="https://hackmd.io/_uploads/rytkVN2Glx.png" alt="Figure DDFacet" width="400"/>
  <br>
  <em>The following command enables the reconstruction of a distributed MeasurementSet across a multi-node architecture, based on the work by N. Monnier et al: <a href="https://hal.science/hal-03729202/document">DDFacet parallel</a>.</em>
</p>



```
mpirun -np 2 singularity exec -B /home -B /media/tasse/data \
./ddf_dev_np1.22.4.sif DDF.py Template.parset \
--Data-MS 0000.MS,0000.MS \
--Output-Name clean/test \
--Output-Mode Clean \
--Deconv-Mode HMP \
--Freq-NBand 3 \
--Freq-NDegridBand 1 \
--Mask-Auto True \
--Mask-SigTh 15 \
--Mask-AutoRMSFactor 3 \
--Deconv-MaxMajorIter 1 \
--Deconv-MaxMinorIter 5
```


## Note
:warning: *This tutorial has been tested from the `SB155.rebin.ms` mesuremenSet obtained from NenuFAR via nancep.* 
We still need to figure out the proper way to build a multi-frequency image cube (i.e., one image per frequency channel or subband). Contributions and ideas are welcome!
                           