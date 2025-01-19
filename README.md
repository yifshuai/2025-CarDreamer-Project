# 2025-CarDreamer-Project

Technical Updates:
  - CarDreamer(v3) model deployed on local machine using Windows Ubuntu
  - Check the following steps to complete the deployment


How to Deploy CarDreamer Model in Windows System:
Since the CarDreamer model was initially created and tested based on Linux OS; The CarDreamer model has a limited capability of adapting Linux OS.

Here we provide an alternative solution for Windows OS users; here is the procedure for deploying CarDreamer V3 on Windows Os:
  1. Download Windows Unbuntu
    a. https://apps.microsoft.com/detail/9PDXGNCFSCZV?hl=en-us&gl=US&ocid=pdpshare
  2. Install Conda and setup the conda environment by following the CarDreamer Setup tutorial, refer to the following page:
    a. https://github.com/ucd-dare/CarDreamer?tab=readme-ov-file
    b. https://github.com/ucd-dare/CarDreamer/tree/master/dreamerv3
  3. Make sure to use the 1.24.3 version of Numpy; Run the following command to check & install 1.24.3 numpy
    a.  python3.8 -m pip install numpy==1.24.3
  4. If jax is incompatible with your numpy, run the following command:
    a. pip install "jax<0.5.0" "jaxlib<0.5.0" numpy==1.24.3
  5. Make sure the CarlaUnreal.sh is executable by running the following command:
    a. chmod +x /correct/path/to/CarlaUnreal.sh
  6. For setup of the environment variable use the following command to find the path:
    a. find ~/CARDREAMER/ -name "CarlaUnreal.sh"
    b. export CARLA_ROOT="</path/to/carla>"
    c. export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla":${PYTHONPATH}
