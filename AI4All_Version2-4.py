from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMainWindow, QLabel, QApplication, QTextEdit
# from PyQt5.QtOpenGL import QGLWidget
import sys
# import subprocess
import os
import psutil
import time
import pyautogui
import requests
from bs4 import BeautifulSoup
import socket

import sys
import time
import json
from PyQt5 import QtWidgets, QtCore

import pywinauto.keyboard as keyboard



class WorkerThread(QtCore.QObject):
    def __init__(self, func, school_id, start_function, download_handler, closeProgramXYZ, resetUiState):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.connect((socket.gethostname(), 1242))
        self.s.connect(("127.0.0.1", 1242))
        # self.s.sendall(b"Hello")
        self.msg = ''
        self.func = func

        self.is_obj_on_heat_bed = False

        self.printed_count = 0
        self.now_command = ''
        self.last_command = ''

        self.count_previous_command = 0
        self.previous_commands = []

        self.school_id = school_id
        self.is_fetch = True
        self.startFunction = start_function
        self.download3DModel = download_handler
        self.closeProgramXYZ = closeProgramXYZ
        self.resetUiState = resetUiState
        self.last_time = time.time()

    def setFetchStatus(self, status):
        self.is_fetch = status

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            self.last_command = self.now_command
            self.now_command = self.msg

            # Long running task ...
            # self.signalExample.emit("leet", 1337)
            
            self.msg = self.s.recv(1024)
            # .decode("utf-8") # รับค่า
            print(f"---{self.msg}---")
            # self.func(99,'white','TRUE')          
            # if self.msg == b'\x00':
            #     self.func(12, 'red', 'Waiting')
            # elif self.msg == b'Initialization':
            #     self.func(12, 'lightgreen', 'Initialization')
            if self.msg == b'Busy':
                self.func(2, 'yellow', 'Printer Busy')
            elif self.msg == b'Ready':
                self.func(2, 'lightgreen', 'Printer Ready')
            elif self.msg == b'Pre-heat Extruder':
                self.printed_count = 0 # Reset count
                self.func(3, 'lightgreen', 'Pre-heat Extrude')
                self.closeProgramXYZ()
                self.setFetchStatus(status=True)
            elif self.msg == b'Printing':
                self.func(4, 'lightgreen', 'Printing')
                self.printed_count += 1
            elif self.msg == b'Store Extruder':
                self.func(5, 'lightgreen', 'Store Extrude')
            elif self.msg == b'Object On Heat Bed': # Waiting user to press OK on Printer
                self.func(6, 'lightgreen', 'Object On Heat Bed')
                self.is_obj_on_heat_bed = True
            elif self.msg == b'\x00':
                pass

            time_pass = time.time() - self.last_time
            
            if self.printed_count == 0:
                if self.is_fetch and self.msg == b'Ready' and time_pass > 3:        
                    
                    print("Fetching")

                    response = requests.get('http://tele3dprinting.com/2019/process.php?api=list')
                    # response = requests.get(self.serverAddressList.text())
                    response = response.json()

                    self.last_time = time.time()

                    for obj in response:
                        if obj['school_id'] == self.school_id.text():
                            self.is_fetch = False

                            # Don't forget to reset self.is_fetch state !!! When print finish !!
                            save_path = self.download3DModel(file_id=obj['file_id'], file_name=obj['file'])
                            # self.printed_count += 1
                            self.startFunction(is_worker_handle=True, save_path=save_path) # Status Printing is here

            else: # != 0
                print("----> Else")
                # if self.last_command == b'Object On Heat Bed':
                if self.is_obj_on_heat_bed:
                    print(f"----> Obj on heat bed, {self.is_fetch=}, {self.msg=}")
                    self.resetUiState()
                    self.is_fetch = True
                    if self.is_fetch and self.msg == b'Ready':  
                        print("Fetching")

                        response = requests.get('http://tele3dprinting.com/2019/process.php?api=list')
                        # response = requests.get(self.serverAddressList.text())
                        response = response.json()

                        print(f"----> {response=}")

                        self.last_time = time.time()

                        for obj in response:
                            if obj['school_id'] == self.school_id.text():
                                self.is_fetch = False
                                self.is_obj_on_heat_bed = False

                                # Don't forget to reset self.is_fetch state !!! When print finish !!
                                save_path = self.download3DModel(file_id=obj['file_id'], file_name=obj['file'])
                                # self.printed_count += 1
                                self.startFunction(is_worker_handle=True, save_path=save_path, is_first_time=False)      
                    
            # if self.msg == b'Pre-heat Extruder':
            #     self.closeProgramXYZ()

            
            


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()


        with open('CONFIG.json', 'r') as file:
            self.DEFAULT_CONFIG = json.load(file)


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

        self.sc_id = self.findChild(QLineEdit, 'lineEdit_2')
        self.sc_id.setText(self.DEFAULT_CONFIG['SCHOOL_ID'])

        self.status1 = self.findChild(QLabel, 'label_12')  # download3DModel
        self.status2 = self.findChild(QLabel, 'label_13')  # เปิดโปรแกรม
        self.status3 = self.findChild(QLabel, 'label_14')
        self.status4 = self.findChild(QLabel, 'label_15')
        self.status5 = self.findChild(QLabel, 'label_16')
        self.status6 = self.findChild(QLabel, 'label_17')
        self.status7 = self.findChild(QLabel, 'label_18')
        self.status8 = self.findChild(QLabel, 'label_19')
        self.status9 = self.findChild(QLabel, 'label_20')
        self.status10 = self.findChild(QLabel, 'label_21')
        self.status11 = self.findChild(QLabel, 'label_22')
        self.status12 = self.findChild(QLabel, 'label_23')

        self.resetUiState()

        self.backEndWorker = self.findChild(QLabel,'label_3')
        self.backEndState = self.findChild(QLabel,'label_4')
        self.fileState = self.findChild(QLabel,'label_5')
        self.printerStatus = self.findChild(QLabel,'label_6')
        self.fileName = self.findChild(QLabel,'label_8')

        self.show()

        ''' ---------------------- Thread ----------------------- '''
        self.worker = WorkerThread(self.testUpdateUI, self.sc_id, self.startButtonPressed, self.download3DModel, self.closeProgramXYZ, self.resetUiState)
        self.workerThread = QtCore.QThread()
        # Init worker run() at startup (optional)
        self.workerThread.started.connect(self.worker.run)
        # self.worker.signalExample.connect(self.signalExample)  # Connect your signals/slots
        # Move the Worker object to the Thread object
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()

    def resetUiState(self):
        self.status1.setStyleSheet("background-color: white")
        self.status1.setText("Waiting...")
        self.status1.setToolTip('This is a tooltip message.')

        self.status2.setStyleSheet("background-color: white")
        self.status2.setText("Waiting...")
        self.status2.setToolTip('This is a tooltip message.')

        self.status3.setStyleSheet("background-color: white")
        self.status3.setText("Waiting...")
        self.status3.setToolTip('This is a tooltip message.')

        self.status4.setStyleSheet("background-color: white")
        self.status4.setText("Waiting...")
        self.status4.setToolTip('This is a tooltip message.')

        self.status5.setStyleSheet("background-color: white")
        self.status5.setText("Waiting...")
        self.status5.setToolTip('This is a tooltip message.')

        self.status6.setStyleSheet("background-color: white")
        self.status6.setText("Waiting...")
        self.status6.setToolTip('This is a tooltip message.')

        self.status7.setStyleSheet("background-color: white")
        self.status7.setText("Waiting...")
        self.status7.setToolTip('This is a tooltip message.')

        self.status8.setStyleSheet("background-color: white")
        self.status8.setText("Waiting...")
        self.status8.setToolTip('This is a tooltip message.')

        self.status9.setStyleSheet("background-color: white")
        self.status9.setText("Waiting...")
        self.status9.setToolTip('This is a tooltip message.')

        self.status10.setStyleSheet("background-color: white")
        self.status10.setText("Waiting...")
        self.status10.setToolTip('This is a tooltip message.')

        self.status11.setStyleSheet("background-color: white")
        self.status11.setText("Waiting...")
        self.status11.setToolTip('This is a tooltip message.')

        self.status12.setStyleSheet("background-color: white")
        self.status12.setText("Waiting...")
        self.status12.setToolTip('This is a tooltip message.')


    def testUpdateUI(self, status_number, color, text):
        text = str(text)
        print(status_number, color, text)
        if status_number == 2:
            self.status2.setStyleSheet("background-color: " + color)
            self.status2.setText(text)
            self.printerStatus.setText(text)
        elif status_number == 3:
            self.status3.setStyleSheet("background-color: " + color)
            self.status3.setText(text)
            self.printerStatus.setText(text)
        elif status_number == 4:
            self.status4.setStyleSheet("background-color: " + color)
            self.status4.setText(text)
            self.printerStatus.setText(text)
        elif status_number == 5:
            self.status5.setStyleSheet("background-color: " + color)
            self.status5.setText(text)
            self.printerStatus.setText(text)
        elif status_number == 6:
            self.status6.setStyleSheet("background-color: " + color)
            self.status6.setText(text)
            self.printerStatus.setText(text)
        elif status_number == 7:
            self.status7.setStyleSheet("background-color: " + color)
            self.status7.setText(text)
        elif status_number == 99:
            self.backEndWorker.setText(text)

    def closeProgramXYZ(self):
        # if "XYZPrint.exe" in (p.name() for p in psutil.process_iter()):
        os.system("TASKKILL /F /IM XYZPrint.exe")
        self.resetUiState()

    def openProgramXYZ(self):
        # subprocess.call(["C:\\Program Files\\XYZprint\\XYZprint.exe"])
        os.startfile("C:\\Program Files\\XYZprint\\XYZprint.exe")

    def download3DModel(self, file_id, file_name):  # .3w
        print("Downloading 3D Model")

        desktop_path = os.path.expanduser("~/Desktop")  # Find desktop path
        directory_path = desktop_path+"/3DTeleprint"

        try:
            if not os.path.exists(directory_path):  # Check is path alive?
                self.backEndState.setText('Check is path alive?')
                os.makedirs(directory_path)  # Create folder
                self.backEndState.setText('Create folder')
        except OSError:
            print('Error: Creating directory. ' + directory_path)
            self.backEndState.setText('Error: Creating directory.')


        self.fileName.setText(file_name)

        # download_url = 'http://tele3dprinting.com/2019/process.php?api=stl.read&file_id=' + file_id
        download_url = self.serverAddressID.text() + file_id
        self.logTextEdit.append(download_url)
        r = requests.get(download_url, allow_redirects=True)
        save_path = directory_path+'/'+file_name
        self.logTextEdit.append(save_path)
        with open(save_path, 'wb') as file:
            file.write(r.content)

        # return save_path
        # "%userprofile%" = Get username of this PC
        return os.path.join(os.path.expandvars("%userprofile%"), "Desktop", "3DTeleprint", file_name)
        # C:\Users\Lookpeach\Desktop\3DTeleprint\2020-10-14 16-09-58 (2) (Cube_test.stl).0.stl

    def checkImageExisting(self, state_click_image_url, timeout=5):
        found_location = None
        last = time.time()
        while found_location == None and time.time()-last < timeout:
            # found_location = pyautogui.locateOnScreen(state_click_image_url, confidence= .8)
            found_location = pyautogui.locateOnScreen(state_click_image_url)

            if found_location:
                return True
                # buttonx, buttony = pyautogui.center(found_location)
                # pyautogui.click(buttonx, buttony)

    def checkImageExisting_2(self, state_click_image_url, timeout=5, click=False):
        found_location = None
        last = time.time()
        while found_location == None and time.time()-last < timeout:
            # found_location = pyautogui.locateOnScreen(state_click_image_url, confidence= .8)
            found_location = pyautogui.locateOnScreen(state_click_image_url)

            if found_location:
                if click:
                    buttonx, buttony = pyautogui.center(found_location)
                    pyautogui.click(buttonx, buttony)
                return True
            

    def emulateFunction(self, state_click_image_url):
        found_location = None
        while found_location == None:
            # found_location = pyautogui.locateOnScreen(state_click_image_url, confidence=0.8)
            # found_location = pyautogui.locateOnScreen(state_click_image_url)
            found_location = pyautogui.locateOnScreen(state_click_image_url, grayscale=True)

            if found_location:
                buttonx, buttony = pyautogui.center(found_location)
                pyautogui.click(buttonx, buttony)

    def mouseEmulation(self, file_path):
        time.sleep(15)
        self.checkImageExisting_2('ImageRecognition/1-Close-Login.PNG', click=True)
        self.checkImageExisting_2('ImageRecognition/2-Import-file.PNG', click=True)
        self.checkImageExisting_2('ImageRecognition/3-Open-file.PNG', click=True)
        print(f"---> File Path : {file_path}")
        # time.sleep(2)
        pyautogui.write(file_path)
        # pyautogui.typewrite(file_path)
        # keyboard.send_keys(file_path)
        time.sleep(2)
        self.emulateFunction('ImageRecognition/4-OK-open-file.PNG')
        is_found_error = self.checkImageExisting_2('ImageRecognition/4-OK-open-file.PNG', click=True) # เปลี่ยนรูปด้วย
        if is_found_error:
            is_found_error = self.checkImageExisting_2('ImageRecognition/4-2-OK-open-file.PNG', click=True) # เปลี่ยนรูปด้วย
            # is_found_error
        # pyautogui.press('enter')
        self.fileState.setText('Import to XYZ.')

        is_found_error = self.checkImageExisting('ImageErrorCase/SettingInstalledMaterial-Cut.png') # เปลี่ยนรูปด้วย
        if is_found_error:
            os.system('shutdown /r /t 0')

        # is_found_error = self.checkImageExisting('ImageErrorCase/CannotRenderFile-Cut.png', timeout=5) # เปลี่ยนรูปด้วย
        # if is_found_error:
        #     os.system('shutdown /r /t 0')
        
        is_found_error = self.checkImageExisting('ImageErrorCase/ObjectSmall-Cut.png', timeout=5) # เปลี่ยนรูปด้วย
        if is_found_error:
            self.emulateFunction('ImageRecognition/4-1-No.PNG')

        is_found_error = self.checkImageExisting('ImageErrorCase/FileError-Cut.png', timeout=5) # เปลี่ยนรูปด้วย
        if is_found_error:
            self.emulateFunction('ImageErrorCase/OkFileError-Cut.PNG')
            self.emulateFunction('ImageRecognition/1-Close-Login.PNG')
            self.emulateFunction('ImageRecognition/2-Import-file.PNG')
            self.emulateFunction('ImageRecognition/3-Open-file.PNG')
            is_found_error = self.checkImageExisting('ImageErrorCase/CannotRenderFile-Cut.png', timeout=5) # เปลี่ยนรูปด้วย
            if is_found_error:
                os.system('shutdown /r /t 0')

        self.worker.s.sendall(b'st:0:st')
        # time.sleep(10)
        self.emulateFunction('ImageRecognition/5-Print.PNG')

        is_found_error = self.checkImageExisting('ImageErrorCase/SettingInstalledMaterial-Cut.png', timeout=5) # เปลี่ยนรูปด้วย
        if is_found_error:
            self.emulateFunction('ImageRecognition/5-Print.PNG')

        is_found_error = self.checkImageExisting('ImageErrorCase/NoPrinter-Cut.png', timeout=5) # เปลี่ยนรูปด้วย
        if is_found_error:
            os.system('shutdown /r /t 0')

        is_found_error = self.checkImageExisting('ImageErrorCase/PrinterBusy-Cut.png', timeout=5) # เปลี่ยนรูปด้วย
        if is_found_error:
            os.system('shutdown /r /t 0')

    def startButtonPressed(self, is_worker_handle=False, save_path='', is_first_time=True):
        # This is executed when the button is pressed
        print('-----------printButtonPressed------------')
        self.logTextEdit.append("START")
        self.worker.s.sendall(b"st:0:st")

        ready_status = self.status2.text()
        print(f"ready_status={ready_status}")
        if ready_status == "Printer Ready" or not is_first_time:
            if is_worker_handle:
                save_path = save_path
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
                self.mouseEmulation(save_path)

                # self.worker.setFetchStatus(status=True) # Reset fetch status
        else:
            pass

    def stopButtonPressed(self):
        # This is executed when the button is pressed
        # self.worker.s.send(b'\x01')
        self.logTextEdit.append("STOP")
        self.worker.s.sendall(b'st:2:st')
        print('STOP')

    def resetButtonPressed(self):
        # This is executed when the button is pressed
        self.logTextEdit.append("RESET")
        print('RESET')


app = QApplication(sys.argv)
window = Ui()
app.exec_()
