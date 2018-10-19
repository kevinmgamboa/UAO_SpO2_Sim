# Introduction
The Open Source graphical user interface (GUI) for a SpO2 simulator, named as UAO_SpO2_Sim, it's a project that was born in 2017 in the Research Group in Biomedical Engineering, GBIO, at the Autonomous University of the West (Universidad Autónoma de Occidente), in Cali Colombia.

This project contains software and hardware. You will find in this Github just the coding related to the software developed or the GUI. A quick view of the software results will be available in an article that will be soon publish in the IEEExplore by the name "Development of a low-cost pulse oximeter simulator for educational purposes". The results in detail, containing also the hardware, will be available for the public in general in the online repository of Universidad Autonoma de Occidente, Cali, Colombia, by the name "DESARROLLO E IMPLEMENTACIÓN DE UN SIMULADOR DE PULSIOXIMETRÍA PARA USO ACADÉMICO". The link of the repository is:

* http://red.uao.edu.co/

## Software Requirements

The quickest way requires to have installed Spyder 3.2.4 (or a higher version) and Qt Designer 5.2.1 (or a higher version).
Secondly, we need to ensure that we have installed the next python libraries (especially the first two, given that the rest are installed with spyder):

* pyqtgraph
* PyQt5
* multiprocessing
* scipy
* collections
* numpy
* sys
* time

## Files Description
* "mainWindowPPG.py" contains the main code of the GUI
* "mainWindowPPG.ui" contains the GUI developed in the software Qt. 
* "UAOspo2sim.py" contains the main code but to be run with the Rpi 3 B+ and the ADC PCF8591
* "curvesHB.mat" contains a matrix in which each row is a vector that displays a curve. This is use for some graphical effects. 

## Summary of the main idea of the GUI 
Understanding the Pulse Oximetry technique requires the a set of knowledge, including:
- light absorption phenomenon of two beams with wavelength between 640 nm and 950 nm in hemoglobin Hb & oxyhemoglobin HbO2.
- The generation of red and infrared photoplethysmographic signals components after passing through the skin bed as a finger.
- The comprehension of ratio and AC and DC components of these red and infrared photoplethysmographic signals.
- The calculation of SpO2 (%) in function of ratio

With this GUI we intend to visually include these set of knowledge within the interface. This fact makes the operator of the simulation to visualize this figures regarding the pulse oximeter techniques anytime he/she operates the simulator.

## GUI preview
Once everything gets installed you will display a GUI as the picture bellow:
![interfaz](https://user-images.githubusercontent.com/15948497/47217427-37407780-d3a0-11e8-9995-735536e6769b.jpg)
