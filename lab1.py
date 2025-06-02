import time
import serial
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
from lab1_ui import Ui_Form


class Lab1(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mybuttonfunction = aan_uit
        self.ui.pushButton.clicked.connect(self.mybuttonfunction)
        self.setWindowTitle("arduino_sensors")


ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

status = 0


def aan_uit():
    global status
    if status:
        ser.write("off".encode())
        print(ser.readline().decode())
        time.sleep(.1)
        status = 0
    else:
        ser.write("on".encode())
        print(ser.readline().decode())
        time.sleep(1)
        status = 1

""" while 1:
    user_input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()

    elif user_input == "on":
        ser.write("on".encode())
        print(ser.readline().decode())
        time.sleep(.1)

    elif user_input == "off":
        ser.write("off".encode())
        print(ser.readline().decode())
        time.sleep(.1)
    else:
        print("Invalid command")
        time.sleep(.1) """

if __name__ == "__main__":
    app = QApplication([])
    form = Lab1()
    form.show()
    sys.exit(app.exec_())