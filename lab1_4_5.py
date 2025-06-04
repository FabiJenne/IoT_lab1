import time
import serial
import sys
import random
import csv

from PyQt5.QtCore import Qt, QTimer, QDateTime, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_4_5_ui import Ui_Form

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

ser = serial.Serial(
    port='COM8',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)


class SensorData:
    def __init__(self, serial_connection):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.serial = serial_connection

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def update(self):
        line = self.serial.readline().decode().strip()
        values = line.split(",")
        self._x = float(values[0])
        self._y = float(values[1])
        self._z = float(values[2])
        # self._x, self._y, self._z = line.split(",")

class Lab1(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mybuttonfunction = self.on_off
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.setWindowTitle("arduino_sensors")
        self.status = 0
        self.timestamps = []
        self.timestamps_xas = []
        self.x = []
        self.y = []
        self.z = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.plot_data)
        self.ui.MplWidget.canvas.axes.set_ylim(0, 2)  # set lim y-as at 0-10

        self.data = SensorData(ser)

    def plot_data(self):
        # self.x.append(self.x[-1] + 1)
        # self.y.append(random.randrange(10))
        self.data.update()
        self.x.append(self.data.x)
        self.y.append(self.data.y)
        self.z.append(self.data.z)

        time = QDateTime.currentDateTime().toMSecsSinceEpoch()/1000
        self.timestamps.append(time)

        if len(self.timestamps) > 1:
            self.timestamps_xas.append(self.timestamps[-1] - self.timestamps[0])
        else:
            self.timestamps_xas.append(0)
        
        print(f"timestamp: {self.timestamps[-1]}") 
        print(f"x: {self.data.x}, y: {self.data.y}, z: {self.data.z}")

        if len(self.x) > 20:
            self.x = self.x[-20:]
            self.y = self.y[-20:]
            self.z = self.z[-20:]
            self.timestamps_xas = self.timestamps_xas[-20:]
        
        self.ui.MplWidget.canvas.axes.clear()
        # self.ui.MplWidget.canvas.axes.plot(self.x, self.y, 'r', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(self.timestamps_xas, self.x, 'r', label='x', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(self.timestamps_xas, self.y, 'g', label='y', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(self.timestamps_xas, self.z, 'b', label='z', linewidth=0.5)
        self.ui.MplWidget.canvas.draw()

    def on_off(self):
        if self.status:
            ser.write("off".encode())
            self.timer.stop()
            # print(ser.readline().decode())
            time.sleep(1)
            self.status = 0
        else:
            ser.write("on".encode())
            self.timer.start(100)  # every 100msec execute self.plot.data
            self.plot_data()
            # print(ser.readline().decode())
            # time.sleep(1)
            self.status = 1

    def save_to_file(self):
        self.name
        QFileDialog.Save


if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    # sensor_data = SensorData()
    # sensor_data.getting_data()
    # value = sensor_data.getting_data()
    # print(value)
    sys.exit(app.exec_())
