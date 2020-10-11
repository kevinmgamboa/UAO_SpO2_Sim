"""
UAO SpO2 Simulator GUI - No Hardware Required !
-------------------------------------
Created on Thu Dec 21 12:07:49 2017
by the author: Kevin Machado Gamboa
Contact: ing.kevin@hotmail.com
Modified on Sun Oct 11 10:29:39 2020
------------------------------------
REFERENCES: 
    [1] Development of a Low-Cost Pulse Oximeter Simulator for Educational Purposes
    https://github.com/kevinmgamboa/UAO_SpO2_Sim
    [2] Sebastian Sepulveda - plot data from a function in real time 
    https://github.com/ssepulveda/RTGraph/tree/oldRTGraph
"""
# -----------------------------------------------------------------------------
#                             Libraries Needed
# -----------------------------------------------------------------------------
import sys
import numpy as np
from time import time
import scipy.io as sio
#import PCF8591v2 as ADC
from collections import deque
from multiprocessing import Queue
# Librery for the management of Qt v5. UI platform
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
# -----------------------------------------------------------------------------
#                              GUI Development
# -----------------------------------------------------------------------------
# @brief Buffer size for the data (number of points in the plot)
N_SAMPLES = 100
# @brief Update time of the plot, in ms
PLOT_UPDATE_TIME = 1
# @brief Point to update in each redraw
PLOT_UPDATE_POINTS = -1

class mainWindow(QMainWindow):
    def __init__(self):
        #Inicia el objeto QMainWindow
        QMainWindow.__init__(self)
        # Loads an .ui file & configure UI
        loadUi("mainWindowPPG.ui",self)
        self.setupUI()   
        # Shared variables, initial values
        self.queue = Queue(N_SAMPLES)
        self.dataR = deque([], maxlen=N_SAMPLES)
        self.dataIR = deque([], maxlen=N_SAMPLES)
        self.TIME = deque([], maxlen=N_SAMPLES)

        self._timer_plot = None
        self.plot_colors = ['#0072bd', '#d95319', '#bd0000']
        # Spo2 signal initial parameters
        self.timestamp = 0.0
        self.ampR = 0.4      # amplitud for Red signal
        self.ampIR = 0.270      # amplitud for InfraRed signal
        self.minR = 1.45   # Desplacement from zero for Red signal
        self.minIR = 1.45   # Desplacement from zero for Red signal

        self._configure_plot()
        # UI connectors
        self.HRsl.valueChanged.connect(self.spo2sl_change)
        self.spo2sl.valueChanged.connect(self.spo2sl_change)        
        # Configurations
        
        self._enable_ui(True)        
        self._configure_timers()
        self.buttons()
        self._initial(self.ampR, self.ampIR)
        self.spo2sl_change()
## -----------------------------------
##    SpO2 Parameters & Plotting
## -----------------------------------        
    def ppg_parameters(self, minR, ampR, minIR, ampIR, t, HR):
        """
        Store the function of two signals - e.g PPG Red and Infrared channel signals
        We can also put here a sine, cosine, etc.
        """
        f= HR * (1/60)
        # Spo2 Red signal function
        self.sR= minR + ampR * (0.5*np.sin(2*np.pi*t*f) + 0.22*np.sin(2*np.pi*t*2*f+40))
        # Spo2 InfraRed signal function
        self.sIR= minIR + ampIR * (0.5*np.sin(2*np.pi*t*f) + 0.22*np.sin(2*np.pi*t*2*f+40))
        
        return self.sR, self.sIR

    def spo2sl_change(self):
        """
        Change the value of the SpO2 when movind the slider.
        It also have the list of SpO2 values vs the R value
        """
        spo2value = self.spo2sl.value()
        self.showSpo2.setText(str(spo2value))
        
        spO2 = [100,99,98,97,96,95,94,93,92,91,90,89,88,87,86,85,84,83,82,81,80,79,78,77,76,75,
                74,73,72,71,70,69,68,67,66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,51,50]
        
        R = [0.50,0.55,0.60,0.64,0.66,0.70,0.71,0.72,0.73,0.75,0.76,0.77,0.78,0.80,0.81,0.82,0.83,
             0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.00,
             1.01,1.00,1.05,1.11,1.12,1.16,1.19,1.25,1.27,1.32,1.33,1.35,1.39,1.43,1.47,1.52,1.50]
        
        Ri = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        Ri[spO2.index(spo2value)] = R[spO2.index(spo2value)]

        # R-IR values & SpO2
        rR = [0.3,0.4,0.4,0.4,0.4,0.3,0.3,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.5,0.4,0.4,0.4,
              0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4] 
        
        IR = [1.0,0.9,0.7,1.0,0.9,0.7,0.7,0.6,0.6,0.58,0.57,0.54,0.52,0.5,0.5,0.48,0.47,0.46,0.45,0.445,
              0.44,0.43,0.42,0.39,0.4,0.39,0.38,0.38,0.37,0.35,0.36,0.35,0.35,0.34,0.34,0.34,0.33,0.32,0.32,
              0.31,0.3,0.3,0.3,0.29,0.29,0.28,0.28,0.27,0.27,0.26,0.25]

        self.ampR = rR[spO2.index(spo2value)]
        self.ampIR = IR[spO2.index(spo2value)]
        
        self.showR.setText(str(round(self.ampR/self.ampIR,2)))
        self.showRac.setText(str(round(self.ampR,2)))
        self.showIRac.setText(str(round(self.ampIR,2)))
        self.showDC.setText(str(round(self.minR,2)))

        self._initial(self.ampR, self.ampIR)

        self._Rplt.clear()
        self._Rplt.plot(x=list(R), y=list(spO2), pen=self.plot_colors[0])
        self._Rplt.plot(x=list(Ri), y=list(spO2), pen=self.plot_colors[0],  symbolBrush=(255,0,0))

    def _initial(self, ampR, ampIR):
        """
        contain the initial figure in the UI
        """
        HR = self.HRsl.value()
        self.showHR.setText(str(HR))
        
        t=np.linspace(0.2,0.8,100);
        sR,sIR = self.ppg_parameters(self.minR, ampR, self.minIR, ampIR, t, 200)
        
        datos=sio.loadmat('curvesHB');
        X=datos['x'];
        
        x_HBo2=X[0]
        HBo2=X[1]
        x_oxyHB=X[2]
        oxyHB=X[3]
        spo2value = self.spo2sl.value()
        HBx = np.linspace((700-spo2value),1000,100)
        HBy = X[5]
        # 1 naranja
        # 2 rojo
        self._plt.clear()
        self._plt.plot(x=list(t)[-PLOT_UPDATE_POINTS:], y=list(sR)[-PLOT_UPDATE_POINTS:], pen=self.plot_colors[1])
        self._plt.plot(x=list(t)[-PLOT_UPDATE_POINTS:], y=list(sIR)[-PLOT_UPDATE_POINTS:], pen=self.plot_colors[0])
        
        self._Rplt_2.clear()
        self._Rplt_2.plot(x=list(x_HBo2), y=list(HBo2), pen=self.plot_colors[0])
        self._Rplt_2.plot(x=list(x_oxyHB), y=list(oxyHB), pen=self.plot_colors[0])
        self._Rplt_2.plot(x=list(HBx), y=list(HBy), pen=self.plot_colors[1])
        
    def _update_plot(self):
        """
        Updates and redraws the graphics in the plot.
        """
        # Geting heart rate
        HR = float(self.HRsl.value())
        # generates the time
        self.tPPG = time() - self.timestamp
        self.sR, self.sIR = self.ppg_parameters(self.minR, self.ampR, self.minIR, self.ampIR, self.tPPG, HR)

        # store data into variables 
        self.TIME.append(self.tPPG)
        self.dataR.append(self.sR)
        self.dataIR.append(self.sIR)

        # Draw new data
        self._plt_2.clear()
        self._plt_2.plot(x=list(self.TIME)[-PLOT_UPDATE_POINTS:], y=list(self.dataR)[-PLOT_UPDATE_POINTS:], pen=self.plot_colors[1])
        self._plt_2.plot(x=list(self.TIME)[-PLOT_UPDATE_POINTS:], y=list(self.dataIR)[-PLOT_UPDATE_POINTS:], pen=self.plot_colors[0])
## -----------------------------------
##      Window Configuration
## -----------------------------------    
    def _configure_plot(self):
        """
        Configures specific elements of the PyQtGraph plots.
        """
        self.plt.setBackground(background=None)
        self.plt.setAntialiasing(True)
        self._plt = self.plt.addPlot(row=1, col=1)
        self._plt.setLabel('bottom', "Tiempo", "s")
        self._plt.setLabel('left', "Amplitud", "Volt")
        self._plt.showGrid(x=False, y=True)
        
        self.plt_2.setBackground(background=None)
        self.plt_2.setAntialiasing(True)
        self._plt_2 = self.plt_2.addPlot(row=1, col=1)
        self._plt_2.setLabel('bottom', "Tiempo", "s")
        self._plt_2.setLabel('left', "Amplitud", "Volt")
        self._plt_2.showGrid(x=False, y=False)
        
        self.Rplt.setBackground(background=None)
        self.Rplt.setAntialiasing(True)
        self._Rplt = self.Rplt.addPlot(row=1, col=1)
        self._Rplt.setLabel('bottom', "R-value")
        self._Rplt.setLabel('left', "%SpO2")
        self._Rplt.showGrid(x=False, y=True)
        
        self.Rplt_2.setBackground(background=None)
        self.Rplt_2.setAntialiasing(True)
        self._Rplt_2 = self.Rplt_2.addPlot(row=1, col=1)
        self._Rplt_2.setLabel('bottom', "Longitud de Onda", "*nm")
        self._Rplt_2.setLabel('left', "Absorbancia")
        self._Rplt_2.showGrid(x=False, y=True)

    def setupUI(self):
        """
       Configures everything regarding the UI
        """
        # Defult Heart Rate configuration
        self.HRsl.setMaximum(250)
        self.HRsl.setMinimum(50)
        self.HRsl.setValue(80)
        self.HRsl.setTickPosition(QSlider.TicksBelow)
        self.HRsl.setTickInterval(1)
        # Defult SpO2 configuration
        self.spo2sl.setMaximum(100)
        self.spo2sl.setMinimum(50)
        self.spo2sl.setValue(100)
        self.spo2sl.setTickPosition(QSlider.TicksBelow)
        self.spo2sl.setTickInterval(1)
            
    def _enable_ui(self, enabled):
        """
        Enable touching the buttons in the UI
        """
        self.startButton.setEnabled(enabled)
        self.spo2sl.setEnabled(enabled)
        self.HRsl.setEnabled(enabled)
        self.showSpo2.setEnabled(enabled)
        self.stopButton.setEnabled(not enabled)

    def buttons(self):
        """
        Configures the connections between signals and UI elements.
        """
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
    
    def start(self):
        """
        This function works when the start button is clicked
        It generates a t0 time and activates the Qt timer which connects to update_plot
        :return:
        """
        self.stop()
        self._plt_2.clear()
        self._enable_ui(False)
        self.timestamp= time()
        self._timer_plot.start(PLOT_UPDATE_TIME)
        
    def stop(self):
        """
        This function works when the stop button is clicked
        it stop the timer and resets the buffers
        """
        self._initial(self.ampR, self.ampIR)
        self._enable_ui(True)
        self._timer_plot.stop()  
        self.reset_buffers()    
        
    def _configure_timers(self):
        """
        Configures specific elements of the QTimers.
        :return:
        """
        self._timer_plot = QtCore.QTimer(self) # gives _timer_plot the attribute of QtCore.QTimer
        self._timer_plot.timeout.connect(self._update_plot)  # connects with _update_plot method
        
    def reset_buffers(self):
        """
        Clear everything into the vectors that have the signals
        """
        self.dataR.clear()
        self.dataIR.clear()
        self.TIME.clear()        
# -----------------------------------------------------------------------------
#                             App Execution
# -----------------------------------------------------------------------------        
# Instance to start an application in windows
app = QApplication(sys.argv)
# debemos crear un objeto para la clase creada arriba
_mainWindow = mainWindow()
# Creating an object for the class created above
_mainWindow.show()
# Running application
app.exec_()