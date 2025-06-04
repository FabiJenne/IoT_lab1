import time
import serial
import sys

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


class Lab1(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mybuttonfunction = self.on_off
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.setWindowTitle("arduino_sensors")
        self.status = 0
        self.timer = QTimer(self)

    def on_off(self):
        if self.status:
            ser.write("off".encode())
            self.timer.stop()
            print(ser.readline().decode())
            time.sleep(1)
            self.status = 0
        else:
            ser.write("on".encode())
            self.timer.start(100)  # every 100msec execute self.plot.data
            print(ser.readline().decode())
            time.sleep(1)
            self.status = 1


if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    sys.exit(app.exec_())
