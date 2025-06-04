import time
import serial
import sys


from datetime import datetime
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_ui import Ui_Form

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)


class SensorData:
    def __init__(self):
        self._x = []
        self._y = []
        self._z = []
        self._timestamps = []
        self._start_time = datetime.now()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def timestamps(self):
        return self._timestamps

    def update(self):
        line = ser.readline().decode().strip()
        if line:
            values = line.split(",")
            self._timestamps.append((datetime.now() -
                                     self._start_time).total_seconds())
            self._x.append(float(values[0]))
            self._y.append(float(values[1]))
            self._z.append(float(values[2]))


class Lab1(QMainWindow):
    def __init__(self, *args):
        print("ik start")
        QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mybuttonfunction = self.on_off
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.setWindowTitle("arduino_sensors")
        self.status = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.plot_data)
        self.ui.MplWidget.canvas.axes.set_ylim(0, 2)  # set lim y-as at 0-10
        self.data = SensorData()

    def plot_data(self):
        self.data.update()
        x = self.data.x[-20:]
        y = self.data.y[-20:]
        z = self.data.z[-20:]
        timestamps = self.data.timestamps[-20:]

        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(timestamps, x, 'r', label='x', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(timestamps, y, 'g', label='y', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(timestamps, z, 'b', label='z', linewidth=0.5)
        self.ui.MplWidget.canvas.draw()

    def on_off(self):
        if self.status:
            print("On")
            self.timer.stop()
            time.sleep(1)
            self.status = 0
        else:
            self.timer.start(100)  # every 100msec execute self.plot.data
            self.plot_data()
            self.status = 1


if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    # sensor_data = SensorData()
    # sensor_data.getting_data()
    # value = sensor_data.getting_data()
    # print(value)
    sys.exit(app.exec_())
