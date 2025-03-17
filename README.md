# 2025-CarDreamer-Project

## Technical Updates:
  - CarDreamer(v3) model deployed on local machine using Windows Ubuntu
  - Check the following steps to complete the deployment


### How to Deploy CarDreamer Model in Windows System:
Since the CarDreamer model was initially created and tested based on Linux OS; The CarDreamer model has a limited capability of adapting Linux OS.

#### Here we provide an alternative solution for Windows OS users; here is the procedure for deploying CarDreamer V3 on Windows Os:
  1. Download Windows Unbuntu
    a. https://apps.microsoft.com/detail/9PDXGNCFSCZV?hl=en-us&gl=US&ocid=pdpshare
  2. Install Conda and setup the conda environment by following the CarDreamer Setup tutorial, refer to the following page:
    a. https://github.com/ucd-dare/CarDreamer?tab=readme-ov-file
    b. https://github.com/ucd-dare/CarDreamer/tree/master/dreamerv3
  3. Make sure to use the 1.24.3 version of Numpy; Run the following command to check & install 1.24.3 numpy
    a.  python3.8 -m pip install numpy==1.24.3
  4. If jax is incompatible with your numpy, run the following command:
    a. pip install "jax<0.5.0" "jaxlib<0.5.0" numpy==1.24.3
  5. Download the Carla for Linux, version 0.9.15
     a. https://github.com/carla-simulator/carla/releases
     b. unzip the carla to your workspace
  6. Make sure the CarlaUE4.sh is executable by running the following command:
    a. chmod +x /correct/path/to/CarlaUE4.sh
  7. For setup of the environment variable, use the following command to find the path:
    a. find ~/CARDREAMER/ -name "CarlaUE4.sh"
    b. export CARLA_ROOT="</path/to/carla>"
    c. export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla":${PYTHONPATH}
  9. Go to the following page to download the Hugging Face checkpoint:
     https://huggingface.co/ucd-dare/CarDreamer/tree/main
     
### Steps to Run the Cascaded CarDreamer AI Model
1. Make sure you have access to Carla 9.15 and Cardreamer v3 by following the procedure above.
2. Clone the right checkpoint linked in the CarDreamre Project GitHub page.
3. Clone this repository; a Linux system is recommended.
4. Find the CarDreamer directory, replace the eval_dm3.sh file with the same eval_dm3.sh offered in this project the eval_dm3.sh contains important configuration and setup, so make sure to use the right one.
5. In your CarDreamer folder, find the common.yaml file, change to map to Town03.
6. Open a terminal and run the Carla simulator.
7. Move the checkpoint to the logdir file in your CarDreamer folder. Make sure to follow the convention for the four_lane example, which already exists in the logdir folder.
8. Open a terminal, activate the cardreamer conda environment, then run the command: python cardreamer_project.py
9. The cascaded CarDreamer AI should start to run now.
10. The program will prompt you to enter start and end points for the ego vehicle.
11. Depend on the complexity and map topology, the drive path will be consists with several takeovers, left turns, and right turns. Each of these artifacts corresponds to a CarDreamer task.

    
## Important Notice: 
1. Make sure the right version of CARLA is installed, the latest version does not work very well. 
2. Download the hugging face checkpoints at the CarDreamer GitHub main page. Use the correct path to the checkpoint.
