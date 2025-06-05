import time
import serial
import sys
import statistics as stats

from datetime import datetime
from PyQt5.QtCore import Qt, QTimer, QDateTime, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_ui import Ui_Form

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


class SensorData(QThread):
    data_updated = pyqtSignal()
    def __init__(self):
        super().__init__(parent=None)
        self._x = []
        self._y = []
        self._z = []
        self._timestamps = []
        self._start_time = datetime.now()
        self._running = False

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

    def run(self):
        self._running = True
        while self._running:
            line = ser.readline().decode().strip()
            if line:
                values = line.split(",")
                self._timestamps.append((datetime.now() -
                                        self._start_time).total_seconds())
                self._x.append(float(values[0]))
                self._y.append(float(values[1]))
                self._z.append(float(values[2]))
                self.data_updated.emit()

    def calc_mean(self):
        self.mean_x = sum(self._x) / len(self._x)
        self.mean_y = sum(self._y) / len(self._y)
        self.mean_z = sum(self._z) / len(self._z)
        print(f"Mean: x:{self.mean_x}, y:{self.mean_y}, z:{self.mean_z}")
    
    def calc_std(self):
        self.std_x = stats.stdev(self._x)
        self.std_y = stats.stdev(self._y)
        self.std_z = stats.stdev(self._z)
        print(f"Std via stat: x:{self.std_x:.4f}, y:{self.std_y:.4f}, z:{self.std_z:.4f}")


class Lab1(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        self.last_pause_index = 0
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mybuttonfunction = self.on_off
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.setWindowTitle("arduino_sensors")
        self.status = 0
        self.ui.MplWidget.canvas.axes.set_ylim(0, 2)  # set lim y-as at 0-10
        self.data = SensorData()
        self.data.data_updated.connect(self.plot_data)
        self.data.start()

    def plot_data(self):
        if not self.status:
            return
        start = self.last_pause_index
        x = self.data.x[start:]
        y = self.data.y[start:]
        z = self.data.z[start:]
        timestamps = self.data.timestamps[start:]

        x = x[-20:]
        y = y[-20:]
        z = z[-20:]
        timestamps = timestamps[-20:]

        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(timestamps, x, 'r', label='x', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(timestamps, y, 'g', label='y', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(timestamps, z, 'b', label='z', linewidth=0.5)
        self.ui.MplWidget.canvas.draw()

    def on_off(self):
        if self.status:
            self.status = 0
            self.last_pause_index = len(self.data.timestamps)
            self.ui.pushButton.setText("Start")
            self.ui.pushButton.setStyleSheet("")
            self.data.calc_mean()
            self.data.calc_std()
        else:
            self.plot_data()
            self.status = 1
            self.ui.pushButton.setText("Stop")
            self.ui.pushButton.setStyleSheet("background-color : red")


if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    # sensor_data = SensorData()
    # sensor_data.getting_data()
    # value = sensor_data.getting_data()
    # print(value)
    sys.exit(app.exec_())
