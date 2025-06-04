# ddfacet-dft-fft-g2g-tutorials

**User Tutorials for DDFacet, DFT, FFT, and Grid-to-Grid Pipelines**

This repository provides a set of Markdown-based tutorials designed to help users run and understand radio astronomy processing pipelines involving DDFacet, DFT, FFT, and Grid-to-Grid (G2G) transformations. The actual pipelines are pre-packaged in Singularity containers.

---

## Purpose

These tutorials aim to:

* Guide users in executing complex radio astronomy workflows,
* Demonstrate usage patterns for DDFacet, DFT, FFT, and G2G tools,
* Serve as hands-on documentation for container-based pipeline execution.

---

## Getting Started

1. **Install Singularity (Apptainer)** on your system:

   ```bash
   sudo apt install singularity-container
   ```

2. **Open and follow the Markdown tutorials**, which provide step-by-step instructions to run the containers and execute each processing stage.

---

## ❓ FAQ

**Q: Can I use my own data?**
A: Absolutely! Just make sure the input formats match those expected by the pipelines (e.g., CASA Measurement Sets for DDFacet).

**Q: Do I need to modify the containers?**
A: No. All pipelines are fully contained within Singularity images. You only need to mount your data and follow the provided commands.

---

## Contact  

For questions or feedback, please contact:  
- [Ophélie Renaud](mailto:ophelie.renaud@ens-paris-saclay.fr)

