[![CI](https://github.com/amosproj/amos-ss2021-neural-network-enablement/actions/workflows/main.yml/badge.svg?event=pull_request_target)](https://github.com/amosproj/amos-ss2021-neural-network-enablement/actions/workflows/main.yml)

# Neural Network Enablement (AMOS SS 2021)

<p align="center">
<a href="https://github.com/amosproj/amos-ss2021-neural-network-enablement">
    <img src="Deliverables/2021-04-21%20Logo.PNG" alt="Logo" width="412" height="139">
  </a>
</p>

**Industry Partner:** 
Heiko Schick, Huawei Germany

**Project Description:**
The goal of the project is to transfer existing neural networks onto Huawei provided hardware (Atlas 200 DK System) and software and to turn the use of those neural networks into a (web service mediated) service.

    The service shall: 
    ● Allow the upload and display of input and output images
    ● The application of the neural network to the images
    
    The neural networks:
    ● Have to be transferred, configured, and possibly trained
    ● Onto dedicated hardware attached to a student workstation

The main function of the neural network allows for colorization of black & white images, but other functions might be added.

**Setting up and running the webservice**
- Run the script `Webservice/scripts/setup.sh` to set up the environment initially.
- Run the script `Webservice/scripts/run.sh` to start the service.

**Project Constraints:**
Core technologies: Python, Python frameworks, and Linux
Team language: English
Needed resources: The Atlas 200DK System 
