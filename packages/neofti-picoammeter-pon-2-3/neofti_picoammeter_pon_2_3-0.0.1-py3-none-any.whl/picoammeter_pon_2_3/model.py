#Project module
from picoammeter_pon_2_3.ui.mainWindow import MainWindow, ModeInterface as MImainWindow
from picoammeter_pon_2_3 import modbusRTUOverTCP, outputData, dataHandler
from picoammeter_pon_2_3.ui.dialogConfig import DialogConfig
#Third party module
from PyQt6 import QtWidgets, QtCore
import numpy as np
#Python module
import logging
from datetime import datetime
from pathlib import Path
import os


log = logging.getLogger()

class Model(QtCore.QObject):
    def __init__(self,parent=None):
        log.debug("Model is initting")
        super().__init__(parent=parent)
        self.__initView__()
        self.__initSignal__()
        self.timer = QtCore.QTimer(parent=parent)
        self.__parent = parent
        self.timer.timeout.connect(self.doTimer)
        self.elapsedTimer = QtCore.QElapsedTimer()
        self.__initValueData__()
        self.connected = False
    def __del__(self):
        self.handlerConnection.disconnect()
    def __initValueData__(self):
        self.x = list()
        self.data = list()
        self.measuredData = list()
        self.cycle = 0
        self.integralCh1 = 0
        self.integralCh2 = 0
        self.integralCh3 = 0
    def __initView__(self):
        self.__mainWindow = MainWindow()
        self.__mainWindow.setPathSaveFolder(str(Path.home()))
        self.__mainWindow.show()
    def __initSignal__(self):
        self.__mainWindow.startSignal.connect(self.start)
        self.__mainWindow.stopSignal.connect(self.stop)
        self.__mainWindow.writeTimeGateSignal.connect(self.writeTimeGate)
        self.__mainWindow.openDialogConfigSignal.connect(self.openDialogConfig)
        self.__mainWindow.typeShowedDataChanged.connect(self.updateTypeShowData)
        self.__mainWindow.clearDataSignal.connect(self.clearData)
    def clearData(self):
        self.__initValueData__()
        self.elapsedTimer.restart()
    def updateTimeGate(self):
        timeGate = self.handlerConnection.readRegisters(50,1)
        self.__mainWindow.setTimeGate(timeGate[0])
    def updateTypeShowData(self):
        self.typeShowedDataIsChanged = True
    def start(self):
        #os.system("/etc/init.d/networking restart")
        log.debug("Start measure")
        self.elapsedTimer.start()
        self.timer.setInterval(100)
        #self.handler.disconnect()
        if not self.connected:
            self.__mainWindow.showMessage("Error connecting to device")
            self.__mainWindow.setMode(MImainWindow.DEFAULT)
            return 
        '''self.handler = modbusRTUOverTCP.Handler("192.168.127.100", 4001, 1)
        if not self.handler.connect():
            self.__mainWindow.showMessage("Error connecting to device")
            self.__mainWindow.setMode(MImainWindow.DEFAULT)
            self.handler.disconnect()
            return '''
        self.__mainWindow.getChart().clearData()
        self.__initValueData__()
        if self.__mainWindow.checkBoxWrite.isChecked():
            self.outputData = outputData.WriterCSV("{0}{1}{2}".format(self.__mainWindow.getPathSaveFolder(),os.path.sep,"{0}_Picoammeter Pon 2_3 Data.csv".format(datetime.now().strftime("%Y-%m-%d %H:%M"))))
            self.outputData.open()
        self.writting = self.__mainWindow.checkBoxWrite.isChecked()
        self.typeShowedDataIsChanged = False
        self.typeShowedData = "Fluence"
        self.updateTimeGate()
        self.timer.start()
    def doTimer(self):
        readedRegisters = self.handlerConnection.readRegisters(0,4)
        #readedRegisters = (1,np.random.rand()*500,np.random.rand()*500,np.random.rand()*500)
        if readedRegisters[0] != 1: 
            return
        self.x.append(self.elapsedTimer.elapsed()/1000)
        self.data.append(readedRegisters[1:4])

        if self.typeShowedDataIsChanged:
            self.measuredData = dataHandler.getColoumbsByVoltages(self.data) 
            if self.__mainWindow.typeDataShow == "Fluence":
                self.measuredData = dataHandler.getFluencesByCoulombs(self.measuredData, self.__mainWindow.getChargeNumber())
            self.integralCh1 = np.sum(self.measuredData[:0])
            self.integralCh2 = np.sum(self.measuredData[:1])
            self.integralCh3 = np.sum(self.measuredData[:2])
            self.typeShowedDataIsChanged = False
        else:
            newItem = dataHandler.getCoulombByVoltage(readedRegisters[1:4])
            if self.__mainWindow.typeDataShow == "Fluence":
                newItem = dataHandler.getFluenceByCoulomb(newItem, self.__mainWindow.getChargeNumber()) 
            self.measuredData.append(newItem)
            self.integralCh1 = self.integralCh1 + newItem[0]
            self.integralCh2 = self.integralCh2 + newItem[1]
            self.integralCh3 = self.integralCh3 + newItem[2]

        self.cycle = self.cycle + 1
        #self.integralCh1 = self.integralCh1 + self.measuredData[-1][0]
        #self.integralCh2 = self.integralCh2 + self.measuredData[-1][1]
        #self.integralCh3 = self.integralCh3 + self.measuredData[-1][2]

        if self.writting:
            self.outputData.writeLine("{0};{1};{2};{3}".format(self.x[-1],readedRegisters[1],readedRegisters[2],readedRegisters[3]))


        self.__mainWindow.setDataChart(
            self.x,
            self.measuredData)
        self.__mainWindow.setCycleAndIntegralData(self.cycle,self.integralCh1, self.integralCh2, self.integralCh3)
    def stop(self):
        self.timer.stop()
        log.debug("Stop measure")
        if self.writting:
            self.outputData.close()
            del self.outputData
        #self.handlerConnection.disconnect()
    def writeTimeGate(self,value:int):
        if value<10 or value>200:
            self.__mainWindow.showMessage("Invalid value Time Gate")
            return
        self.handlerConnection.writeRegister(50, (value))
    def openDialogConfig(self):
        dialog = DialogConfig(self.__mainWindow)
        dialog.exec()
        if (dialog.result()==1):
            self.handlerConnection = dialog.getHandlerConnection()
            self.connected = True
            self.__mainWindow.pushButtonStartStopRun.setEnabled(True)

