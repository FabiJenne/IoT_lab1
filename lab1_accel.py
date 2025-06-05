import time
import serial
import sys
import csv
import statistics as stat

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
    port='COM8',
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

    def calc_mean(self):
        self.mean_x = sum(self._x) / len(self._x)
        self.mean_y = sum(self._y) / len(self._y)
        self.mean_z = sum(self._z) / len(self._z)
        self.all_mean = {self.mean_x, self.mean_y, self.mean_z}
    
    def calc_std(self):
        self.std_x = stat.stdev(self._x)
        self.std_y = stat.stdev(self._y)
        self.std_z = stat.stdev(self._z)
        self.all_std = {self.std_x, self.std_y, self.std_z}


class Lab1(QMainWindow):
    def __init__(self, *args):
        print("ik start")
        QMainWindow.__init__(self)
        self.last_pause_index = 0
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mybuttonfunction = self.on_off
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.ui.pushButton_2.clicked.connect(self.to_file)
        self.setWindowTitle("arduino_sensors")
        self.status = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.plot_data)
        self.ui.MplWidget.canvas.axes.set_ylim(0, 2)  # set lim y-as at 0-10
        self.data = SensorData()


    def plot_data(self):
        self.data.update()
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
            print("On")
            self.timer.stop()
            time.sleep(1)
            self.status = 0
            self.last_pause_index = len(self.data.timestamps)
            self.ui.pushButton.setText("Form", "Stop")
        else:
            self.timer.start(100)  # every 100msec execute self.plot.data
            self.plot_data()
            self.status = 1
            self.data.calc_mean()
            self.data.calc_std()
            self.ui.label.setText(f"mean: x={self.data.mean_x:.2f}, y={self.data.mean_y:.2f}, z={self.data.mean_z:.2f}")
            self.ui.label_2.setText(f"std: x={self.data.std_x:.2f}, y={self.data.std_y:.2f}, z={self.data.std_z:.2f}")
            self.ui.pushButton.setText("Form", "Start")

    def to_file(self):
        all_data = zip(self.data.timestamps, self.data.x, self.data.y, self.data.z)
        with open("data.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'X', 'Y', 'Z'])
            for row in all_data:
                writer.writerow(row)
        # with open("data.csv", 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writecol(self.data.timestamps)
        #     writer.writerow(self.data.x)
        #     writer.writerow(self.data.y)
        #     writer.writerow(self.data.z)
           

if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    # sensor_data = SensorData()
    # sensor_data.getting_data()
    # value = sensor_data.getting_data()
    # print(value)
    sys.exit(app.exec_())
