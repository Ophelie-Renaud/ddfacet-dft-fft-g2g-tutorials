# DFT/FFT/G2G tutorial for beginner
This documentation gives a brief overview of how to use basic imaging pipelines (DFT/FFT/G2G) to input a nenuFAR-type measurementSet and output reconstructed images. 

## Biblio 
:page_facing_up: [G2G](https://arxiv.org/pdf/1712.02078) *N. Monnier, F. Orieux, N. Gac, C. Tasse, E. Raffin, D. Guibert «Fast Grid to Grid Interpolation for Radio Interferometric Imaging»*

:page_facing_up: [Generic imaging pipeline](https://hal.science/hal-04361151/file/paper_dasip24_5_wang_updated-2.pdf): *S. Wang, N. Gac, H. Miomandre, J.-F. Nezan, K. Desnos, F. Orieux « An Initial Framework for Prototyping Radio-Interferometric Imaging Pipelines»*.

## Requirements
- Download pipelines singularity image: `sdp_pipeline.sif` [GitHub](https://github.com/Ophelie-Renaud/simsdp-generic-imaging-pipeline/tree/main/param_code)
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

```

- Once everything is ready, you can start imaging pipelines inside the container: 
```bash
# run the singularity environment
singularity run sdp_pipeline.sif <dft/fft/g2g> <NUM_VIS> <GRID_SIZE> <NUM_MINOR_CYCLE> <NUM_NODES> <MS_PATH>
```

## Note
:warning: *This tutorial is in progress.*