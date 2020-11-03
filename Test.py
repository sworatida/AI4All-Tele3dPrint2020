from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMainWindow, QLabel, QApplication, QTextEdit
# from PyQt5.QtOpenGL import QGLWidget
import sys
# import subprocess
import os
import time
import pyautogui
import requests
from bs4 import BeautifulSoup
import socket

import sys
import time
from PyQt5 import QtWidgets, QtCore



class WorkerThread(QtCore.QObject):
    def __init__(self, func):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), 1242))
        self.msg = ''
        self.func = func

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            # Long running task ...
            # self.signalExample.emit("leet", 1337)

            self.msg = self.s.recv(1024)
            # .decode("utf-8") # รับค่า
            print(f"---{self.msg}---")
            # if self.msg == b'\x00':
            #     self.func(12, 'red', 'Waiting')
            # elif self.msg == b'Initialization':
            #     self.func(12, 'lightgreen', 'Initialization')
            if self.msg == b'Busy':
                self.func(2, 'yellow', 'Printer Busy')
            elif self.msg == b'Ready':
                self.func(2, 'lightgreen', 'Printer Ready')
            elif self.msg == b'Pre-heat Extruder':
                self.func(3, 'lightgreen', 'Pre-heat Extrude')
            elif self.msg == b'Printing':
                self.func(4, 'lightgreen', 'Printing')
            elif self.msg == b'Store Extruder':
                self.func(5, 'lightgreen', 'Store Extrude')
            elif self.msg == b'Object On Heat Bed':
                self.func(6, 'lightgreen', 'Object On Heat Bed')
            elif self.msg == b'\x00':
                pass
            else:
                self.func(7, 'lightgreen', 'Temp is '+str(ord(self.msg)))


# class Server(QtCore.QObject):
#     def __init__(self):
#         super().__init__()
#         HOST = socket.gethostname()  # Standard loopback interface address (localhost)
#         # Port to listen on (non-privileged ports are > 1023)
#         PORT = 1243

#         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.s.bind((HOST, PORT))
#         self.s.listen()
#         self.conn, addr = self.s.accept()

#     @QtCore.pyqtSlot()
#     def run(self):
#         while True:
#             pass

#         # with self.conn:
#         #     print('Connected by', addr)
#         #     while True:
#         #         time.sleep(0.7)
#         #         self.conn.sendall(x)
#         #         data = self.conn.recv(1024)
#         #         # if not data:
#         #         #     break


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ProgramSetXYZ.ui', self)

        self.setWindowTitle("Tele3DPrint - FIBO - KMUTT")

        self.startButton = self.findChild(
            QPushButton, 'pushButton_3')  # Find the button
        self.startButton.setToolTip(
            'This is a tooltip message.')  # Edit tooltip here
        # Remember to pass the definition/method, not the return value!
        self.startButton.clicked.connect(self.startButtonPressed)

        self.serverAddressList = self.findChild(QLineEdit, 'lineEdit')
        # print(f"-----> {self.serverAddressList.text()}")
        self.serverAddressList.setToolTip(
            'This is a tooltip message.')  # Edit tooltip here
        self.serverAddressID = self.findChild(QLineEdit, 'lineEdit_3')
        self.serverAddressID.setToolTip(
            'This is a tooltip message.')  # Edit tooltip here

        self.stopButton = self.findChild(QPushButton, 'pushButton_2')
        self.stopButton.setToolTip(
            'This is a tooltip message.')  # Edit tooltip here
        self.stopButton.clicked.connect(self.stopButtonPressed)

        self.resetButton = self.findChild(QPushButton, 'pushButton')
        self.resetButton.setToolTip(
            'This is a tooltip message.')  # Edit tooltip here
        self.resetButton.clicked.connect(self.resetButtonPressed)

        self.logTextEdit = self.findChild(QTextEdit, 'logText')
        self.logTextEdit.setToolTip(
            'This is a tooltip message.')  # Edit tooltip here
        self.logTextEdit.clear()  # Delete all string in QTextEdit
        # self.logTextEdit.append('asdasd') # Add new string to QTextEdot

        # self.messages.append(f'Running Program..')
        # self.logTextEdit.setText("\n".join(self.messages))

        self.status1 = self.findChild(QLabel, 'label_12')  # download3DModel
        self.status1.setStyleSheet("background-color: white")
        self.status1.setText("Waiting...")
        self.status1.setToolTip('This is a tooltip message.')

        self.status2 = self.findChild(QLabel, 'label_13')  # เปิดโปรแกรม
        self.status2.setStyleSheet("background-color: white")
        self.status2.setText("Waiting...")
        self.status2.setToolTip('This is a tooltip message.')

        self.status3 = self.findChild(QLabel, 'label_14')
        self.status3.setStyleSheet("background-color: white")
        self.status3.setText("Waiting...")
        self.status3.setToolTip('This is a tooltip message.')

        self.status4 = self.findChild(QLabel, 'label_15')
        self.status4.setStyleSheet("background-color: white")
        self.status4.setText("Waiting...")
        self.status4.setToolTip('This is a tooltip message.')

        self.status5 = self.findChild(QLabel, 'label_16')
        self.status5.setStyleSheet("background-color: white")
        self.status5.setText("Waiting...")
        self.status5.setToolTip('This is a tooltip message.')

        self.status6 = self.findChild(QLabel, 'label_17')
        self.status6.setStyleSheet("background-color: white")
        self.status6.setText("Waiting...")
        self.status6.setToolTip('This is a tooltip message.')

        self.status7 = self.findChild(QLabel, 'label_18')
        self.status7.setStyleSheet("background-color: white")
        self.status7.setText("Waiting...")
        self.status7.setToolTip('This is a tooltip message.')

        self.status8 = self.findChild(QLabel, 'label_19')
        self.status8.setStyleSheet("background-color: white")
        self.status8.setText("Waiting...")
        self.status8.setToolTip('This is a tooltip message.')

        self.status9 = self.findChild(QLabel, 'label_20')
        self.status9.setStyleSheet("background-color: white")
        self.status9.setText("Waiting...")
        self.status9.setToolTip('This is a tooltip message.')

        self.status10 = self.findChild(QLabel, 'label_21')
        self.status10.setStyleSheet("background-color: white")
        self.status10.setText("Waiting...")
        self.status10.setToolTip('This is a tooltip message.')

        self.status11 = self.findChild(QLabel, 'label_22')
        self.status11.setStyleSheet("background-color: white")
        self.status11.setText("Waiting...")
        self.status11.setToolTip('This is a tooltip message.')

        self.status12 = self.findChild(QLabel, 'label_23')
        self.status12.setStyleSheet("background-color: white")
        self.status12.setText("Waiting...")
        self.status12.setToolTip('This is a tooltip message.')


        self.show()

        ''' ---------------------- Thread ----------------------- '''
        self.worker = WorkerThread(self.testUpdateUI)
        self.workerThread = QtCore.QThread()
        # Init worker run() at startup (optional)
        self.workerThread.started.connect(self.worker.run)
        # self.worker.signalExample.connect(self.signalExample)  # Connect your signals/slots
        # Move the Worker object to the Thread object
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()

        ''' ---------------------- Server ----------------------- '''
        # self.worker_server = Server()
        # self.workerThread_2 = QtCore.QThread()
        # # Init worker run() at startup (optional)
        # self.workerThread_2.started.connect(self.worker_server.run)
        # # self.worker.signalExample.connect(self.signalExample)  # Connect your signals/slots
        # # Move the Worker object to the Thread object
        # self.worker_server.moveToThread(self.workerThread_2)
        # self.workerThread_2.start()

    def testUpdateUI(self, status_number, color, text):
        # self.status12.setStyleSheet("background-color: lightgreen")
        # self.status12.setText("Waiting...")
        text = str(text)
        print(status_number, color, text)
        if status_number == 2:
            self.status2.setStyleSheet("background-color: " + color)
            self.status2.setText(text)
        elif status_number == 3:
            self.status3.setStyleSheet("background-color: " + color)
            self.status3.setText(text)
        elif status_number == 4:
            self.status4.setStyleSheet("background-color: " + color)
            self.status4.setText(text)
        elif status_number == 5:
            self.status5.setStyleSheet("background-color: " + color)
            self.status5.setText(text)
        elif status_number == 6:
            self.status6.setStyleSheet("background-color: " + color)
            self.status6.setText(text)
        elif status_number == 7:
            self.status7.setStyleSheet("background-color: " + color)
            self.status7.setText(text)

    def openProgramXYZ(self):
        # subprocess.call(["C:\\Program Files\\XYZprint\\XYZprint.exe"])
        os.startfile("C:\\Program Files\\XYZprint\\XYZprint.exe")

    def download3DModel(self):  # .3w
        print("Downloading 3D Model")

        desktop_path = os.path.expanduser("~/Desktop")  # Find desktop path
        directory_path = desktop_path+"/3DTeleprint"

        try:
            if not os.path.exists(directory_path):  # Check is path alive?
                os.makedirs(directory_path)  # Create folder
        except OSError:
            print('Error: Creating directory. ' + directory_path)

        # response = requests.get('http://tele3dprinting.com/2019/process.php?api=list')
        response = requests.get(self.serverAddressList.text())
        if response.content == b'<ol></ol>':  # If don't have file to download
            return

        soup = BeautifulSoup(response.content)
        data = soup.find_all('a')

        splited_text = data[0].text.split('#')

        file_id = splited_text[0]
        file_name = splited_text[1]  # .split(' ')[-1]

        # download_url = 'http://tele3dprinting.com/2019/process.php?api=stl.read&file_id=' + file_id
        download_url = self.serverAddressID.text() + file_id
        r = requests.get(download_url, allow_redirects=True)
        save_path = directory_path+'/'+file_name
        with open(save_path, 'wb') as file:
            file.write(r.content)

        # return save_path
        # "%userprofile%" = Get username of this PC
        return os.path.join(os.path.expandvars("%userprofile%"), "Desktop", "3DTeleprint", file_name)
        # C:\Users\Lookpeach\Desktop\3DTeleprint\2020-10-14 16-09-58 (2) (Cube_test.stl).0.stl

        # self.updateGL()
        # time.sleep(3)

    def emulateFunction(self, state_click_image_url):
        found_location = None
        while found_location == None:
            found_location = pyautogui.locateOnScreen(state_click_image_url, confidence=.9)

            if found_location:
                buttonx, buttony = pyautogui.center(found_location)
                pyautogui.click(buttonx, buttony)

    def mouseEmulation(self, file_path):
        self.emulateFunction('ImageRecognition/1-Close-Login.PNG')
        self.emulateFunction('ImageRecognition/2-Import-file.PNG')
        self.emulateFunction('ImageRecognition/3-Open-file.PNG')
        pyautogui.write(file_path)
        pyautogui.press('enter')

        self.worker.s.send(b'\x02')
        time.sleep(3)

        self.emulateFunction('ImageRecognition/5-Print.PNG')

    # def startSocketServer(self):
    #     HOST = socket.gethostname()  # Standard loopback interface address (localhost)
    #     PORT = 1243        # Port to listen on (non-privileged ports are > 1023)

    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.bind((HOST, PORT))
    #         s.listen()
    #         conn, addr = s.accept()
    #         with conn:
    #             print('Connected by', addr)
    #             # while True:
    #                 # conn.sendall(b'0')
    #             conn.sendall(b'\x00')
    #             # data = conn.recv(1024)
    #             # if not data:
    #             #     break

    def startButtonPressed(self):
        # This is executed when the button is pressed
        # print('printButtonPressed')
        self.logTextEdit.append("START")
        self.worker.s.send(b'\x00') # ส่งค่า 0 กลับไปที่ Server
        # self.startSocketServer()


        ready_status = self.status2.text()
        print(f"ready_status={ready_status}")
        if ready_status == "Printer Ready":
            save_path = self.download3DModel()
            print(f"save_path = {save_path}")
            # save_path = '"C:\\Users\\Lookpeach\\Desktop\\3DTeleprint\\2020-10-14 16-09-58 (2) (Cube_test.stl).0.stl"'
            if save_path == None:
                self.status1.setStyleSheet("background-color: red")
                self.status1.setText("No file to download.")
                self.logTextEdit.append("No file to download.")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
                self.logTextEdit.append("-")
            else:
                self.logTextEdit.append("Download Model Complete.")
                self.status1.setStyleSheet("background-color: lightgreen")
                self.status1.setText("Download Model Complete.")

                self.logTextEdit.append("Open Program XYZ.")
                self.openProgramXYZ()
                print('Server Address List is:' +
                      self.serverAddressList.text())
                print('Server Address ID Model is:' +
                      self.serverAddressID.text())
                save_path = self.download3DModel()
                self.mouseEmulation(save_path)
        else:
            pass

    def stopButtonPressed(self):
        # This is executed when the button is pressed
        self.worker.s.send(b'\x01')
        print('STOP')

    def resetButtonPressed(self):
        # This is executed when the button is pressed
        print('RESET')


app = QApplication(sys.argv)
window = Ui()
app.exec_()
