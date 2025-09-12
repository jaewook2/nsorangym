# nsorangym

## Introduction
This project is carried out under the **parent project**  
“Development of RAN Intelligent Controller for O-RAN Intelligence (RS-2023-00225468)”  
and funded as a **sub-project entrusted by ETRI**, titled  
*“Research on Intelligent Control Method for Energy Efficient 5G RAN”*.

## Background
This project is copied from **“A Gymnasium Environment for ns-O-RAN”**,  
and has been modified based on the following software components:

- **e2sim** ([link](https://github.com/wineslab/ns-o-ran-e2-sim))  
- **ns3-oran-mmwave** ([link](https://github.com/wineslab/ns-o-ran-ns3-mmwave))  
- **ns-o-ran** ([link](https://github.com/o-ran-sc/sim-ns3-o-ran-e2))  
- **ns-o-ran-gym** ([link](https://github.com/wineslab/ns-o-ran-gym))  

## Related Repositories
From the above projects, we copied and modified them for our objectives and published them under our GitHub repositories:

- **e2sim**: [https://github.com/jaewook2/nsorangym_e2sim](https://github.com/jaewook2/nsorangym_e2sim)  
- **ns3-oran-mmwave**: [https://github.com/jaewook2/nsorangym_mmwave](https://github.com/jaewook2/nsorangym_mmwave)  
- **ns-o-ran**: [https://github.com/jaewook2/nsorangym_nsoran](https://github.com/jaewook2/nsorangym_nsoran)  
- **ns-o-ran-gym**: [https://github.com/jaewook2/nsorangym_gym](https://github.com/jaewook2/nsorangym_gym)  


## Installation

You can install and run **nsorangym** in two ways:

- **A. Using Docker (recommended)**
- **B. Installing on the host machine**
### A. Using Docker (recommended)

#### 1) Build the image
```bash
# Clone nsorangym (this repo)
git clone https://github.com/jaewook2/nsorangym.git
cd nsorangym

# Build Docker image
docker build -t nsorangym:latest
```
#### 2) Run the container
```bash
# Basic run (CPU)
docker run --rm -it \
  --name nsorangym \
  -v $PWD:/workspace/nsorangym \
  nsorangym:latest /bin/bash

## GPU (optional)
docker run --rm -it \
  --gpus all \
  --name nsorangym \
  -v $PWD:/workspace/nsorangym \
  nsorangym:latest /bin/bash

#Example RUN
cd nsorangym_gym/
