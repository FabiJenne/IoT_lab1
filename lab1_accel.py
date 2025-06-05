import serial
import sys
import csv
import statistics as stat

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
        self._running = False
        self._x = []
        self._y = []
        self._z = []
        self.mean_x = 0
        self.mean_y = 0
        self.mean_z = 0
        self.std_x = 0
        self.std_y = 0
        self.std_z = 0
        self._timestamps = []
        self._start_time = datetime.now

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

    @property
    def start_time(self):
        return self.start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    def run(self):
        self._running = True
        ser.reset_input_buffer()
        line = ser.readline().decode().strip()
        if line:
            values = line.split(",")
            if len(values) != 3:
                return
            self._timestamps.append((datetime.now() -
                                    self._start_time).total_seconds())
            self._x.append(float(values[0]))
            self._y.append(float(values[1]))
            self._z.append(float(values[2]))
            self.calc_mean()
            self.calc_std()
            self.data_updated.emit()

    def calc_mean(self):
        if self.x and self.y and self.z:
            self.mean_x = round(sum(self.x) / len(self.x), 3)
            self.mean_y = round(sum(self.y) / len(self.y), 3)
            self.mean_z = round(sum(self.z) / len(self.z), 3)

    def calc_std(self):
        if len(self.x) and len(self.y) and len(self.z) > 2:
            self.std_x = round(stat.stdev(self._x), 3)
            self.std_y = round(stat.stdev(self._y), 3)
            self.std_z = round(stat.stdev(self._z), 3)


class Lab1(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        self.last_pause_index = 0
        self.ui = Ui_Form()
        self.data = SensorData()
        self.ui.setupUi(self)
        self.mybuttonfunction = self.on_off
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.ui.pushButton_2.clicked.connect(self.to_file)
        self.setWindowTitle("arduino_sensors")
        self.status = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_func)
        self.data.data_updated.connect(self.plot_data)
        self.ui.MplWidget.canvas.axes.set_ylim(0, 2)  # set lim y-as at 0-10

    def timer_func(self):
        self.data.start()

    def plot_data(self):
        if not self.status:
            return
        start = self.last_pause_index
        x = self.data.x[start:]
        y = self.data.y[start:]
        z = self.data.z[start:]
        timestamps = self.data.timestamps[start:]

        spinBox = self.ui.spinBox.value()
        if spinBox and spinBox < timestamps[-1] - timestamps[0]:
            self.on_off()

        x = x[-20:]
        y = y[-20:]
        z = z[-20:]
        timestamps = timestamps[-20:]

        self.ui.label.setText(f"mean: {self.data.all_mean}")
        self.ui.label_2.setText(f"std: {self.data.all_std}")

        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(timestamps, x, 'r', label='x', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(timestamps, y, 'g', label='y', linewidth=0.5)
        self.ui.MplWidget.canvas.axes.plot(timestamps, z, 'b', label='z', linewidth=0.5)
        self.ui.MplWidget.canvas.draw()

    def on_off(self):
        if self.status:
            self.timer.stop()
            self.data.terminate()
            self.status = 0
            self.last_pause_index = len(self.data.timestamps)
            self.ui.pushButton.setText("Start")
            self.ui.pushButton.setStyleSheet("")
        else:
            self.data.start_time = datetime.now()
            self.timer.start(self.ui.spinBox_2.value())
            self.plot_data()
            self.status = 1
            self.ui.pushButton.setText("Stop")
            self.ui.pushButton.setStyleSheet("background-color : red;" +
                                             "color : white; border: none;" +
                                             "border-radius: 5px;")

    def to_file(self):
        all_data = zip(self.data.timestamps, self.data.x, self.data.y, self.data.z)
        with open("data.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'X', 'Y', 'Z'])
            for row in all_data:
                writer.writerow(row)


def print_threads():
    import threading
    print("Actieve threads:")
    for t in threading.enumerate():
        print(t)


if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    # sensor_data = SensorData()
    # sensor_data.getting_data()
    # value = sensor_data.getting_data()
    # print(value)
    sys.exit(app.exec_())
