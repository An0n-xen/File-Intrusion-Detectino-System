# Import PyQt5 dep
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QProgressBar, QLabel, QMessageBox, QListWidget,QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import Qt

# Import other dep
import sys ,os
import hashlib, threading
import time ,json

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()

        uic.loadUi('UI_files/main.ui',self)
        self.rootpath = os.getcwd()
        self.safe_path = os.getcwd() + '\Safe'
        os.chdir(self.safe_path)
        self.threadoff = 0

        # Add Button
        self.button_add = self.findChild(QPushButton, 'Add_btn')
        self.button_add.clicked.connect(self.addfunc)

        # Remove Button
        self.botton_remove = self.findChild(QPushButton, 'Remove_btn')
        self.botton_remove.clicked.connect(self.removefun)

        # Check Button
        self.botton_check = self.findChild(QPushButton, 'Check_btn')
        self.botton_check.clicked.connect(self.checkfunc)

        # Reset Button
        self.botton_set = self.findChild(QPushButton, 'Set_btn')
        self.botton_set.clicked.connect(self.setfunc)

        # Monitor Button
        self.botton_monitor = self.findChild(QPushButton, 'Monitor_btn')
        self.botton_monitor.clicked.connect(self.mon_thread)

        # Mointor off Button
        self.botton_monitoroff = self.findChild(QPushButton, 'Monitoroff_btn')
        self.botton_monitoroff.clicked.connect(self.monitoroff)

        # Setting up progress bar
        self.progressbar = self.findChild(QProgressBar, 'progress')
        self.progressbar.setRange(0, 100)

        # Setting up label
        self.info_label = self.findChild(QLabel,'Info_label')
        self.info_label.setText('')

        # Setting up list view of file check
        self.list_view = self.findChild(QListWidget, 'Checklist')
        self.item_in_list = []

        # Setting up list view for intrusion
        self.list_view_intru = self.findChild(QListWidget, 'mon_mode')

        self.show()

    def messagebox(self,message,activate):

        if activate == 'warning':
            msg = QMessageBox()
            msg.setWindowTitle('Warning')
            msg.setText(message)
            msg.setIcon(QMessageBox.Warning)

            exe = msg.exec_()

        if activate == 'set':
            msg = QMessageBox()
            msg.setWindowTitle('System Set')
            msg.setText(message)
            msg.setIcon(QMessageBox.Information)

            exe = msg.exec_()

    def addfunc(self):
        fpath, _ = QFileDialog.getOpenFileName(self, "Select file", 'C:')
        
        try:
            with open(fpath,'rb') as file:
                content = file.read()

            # Taking file name
            fname = fpath.split("/")[-1]
        except:
            message = 'Please select file'
            self.messagebox(message,'warning')
        # Recreating file in Safe folder
        try:
            with open(fname, 'wb') as file:
                file.write(content)

            self.progressbar.setValue(100)
            self.info_label.setText('Complete..')
        except:
            pass

        t1 = threading.Thread(target=self.complete)
        t1.start()    

    def complete(self):
        time.sleep(0.5)
        self.progressbar.setValue(0)
        time.sleep(0.9)
        self.info_label.setText('')
        
    def removefun(self):
        fpath, _ = QFileDialog.getOpenFileName(self, "Select file", '')

        try:
            os.remove(fpath)
            self.progressbar.setValue(100)
            self.info_label.setText('Complete')

        except:
            message = 'Please select file'
            self.messagebox(message,'warning')
            
        t2 = threading.Thread(target=self.complete)
        t2.start()
        
    def checkfunc(self):
        file_list = os.listdir()

        # Checking adds
        for i in range(len(file_list)):
            if file_list[i] not in self.item_in_list:
                self.list_view.addItem(file_list[i])
                self.item_in_list.append(self.list_view.item(i).text())
        
            else:
                pass       

        # Check removes
        for item in self.item_in_list:
            if item not in file_list:
                index = self.item_in_list.index(item)
                self.list_view.takeItem(index)
                self.item_in_list.pop(index)
    
    def mon_thread(self):
        self.stop_thread = False
        self.mon_t = threading.Thread(target=self.monitor, args=(lambda : self.stop_thread,))
        self.mon_t.start()
        
    def monitor(self,mode):

        def intrude(type,info):
            if type == '001':
                print('File intergrity breach')
                error_code = 'Breach code:' + ' ' + type
                self.list_view_intru.addItem(error_code)
                
            elif type == '002':
                print('File intergrity breach')
                error_code = 'Breach code:' + ' ' + type
                self.list_view_intru.addItem(error_code)

            elif type == '003':
                print('File intergrity breach')
                error_code = 'Breach code:' + ' ' + type
                self.list_view_intru.addItem(error_code)

            elif type == '004':
                print('File intergrity breach')
                error_code = 'Breach code:' + ' ' + type
                self.list_view_intru.addItem(error_code)

        ## Reading json files
        json_path = self.rootpath + '/data.json'

        with open(json_path, 'r') as file:
            data = json.load(file)
        
        while True:

            ## Count Files
            file_num = len(os.listdir()) 
            valid_file_num = data['numfile']
            
            if file_num == valid_file_num:
                pass

            else:
                info = f'File number: ({file_num}) does not match on in database:({valid_file_num})'
                intrude('001', info)

            ## Check Filename and extensions
            file_name_extension = os.listdir(self.safe_path)

            filename_list = []
            extension_list = []

            valid_filename_list = data['fnames']
            valid_fileextension_list = data['fextension']

            
            # Extracting filename and extension
            for ex in file_name_extension:
                filename = os.path.splitext(ex)[0]
                extension = os.path.splitext(ex)[1]

                filename_list.append(filename)
                extension_list.append(extension)

            for i in range(file_num):
                if filename_list[i] not in  valid_filename_list:
                    type = '002'
                    info = 'Filenames Doesnt Match'
                    intrude(type,info)

                elif extension_list[i] not in valid_fileextension_list[i]:
                    type = '003'
                    info = 'File extensionn doesnt match'
                    intrude(type,info)
                
            ## Check File hashes
            hasher = hashlib.sha256()
            valid_hashlist = data['hashlist']
            hashlist = []

            for item in file_name_extension:
                filepath = self.safe_path + '/' + item
                
                with open(filepath, 'rb') as file:
                    buf = file.read()
                    hasher.update(buf)
                
                hashlist.append(hasher.hexdigest())

            for i in range(file_num):
                if hashlist[i] not in valid_hashlist:
                    type = '004'
                    info = ''
                    intrude(type, info)

            if mode():
                break

            time.sleep(5)

    def monitoroff(self):
        self.stop_thread = True
        self.mon_t.join()

    def setfunc(self):
        ## Data
        DATA = {}

        ## Count Files 
        files = os.listdir()
        filenum = len(files)

        # Storing Data
        DATA['numfile'] = filenum

        ## Check Filename and extensions
        filename_list = []
        extension_list = []
        for ex in files:
            filename = os.path.splitext(ex)[0]
            extension = os.path.splitext(ex)[1]

            filename_list.append(filename)
            extension_list.append(extension)

        # Storing Data
        DATA['fnames'] = filename_list
        DATA['fextension'] = extension_list

        ## Check File hashes
        hasher = hashlib.sha256()
        hashlist = []

        for item in files:
            filepath = self.safe_path + '/' + item
            
            with open(filepath, 'rb') as file:
                buf = file.read()
                hasher.update(buf)
            
            hashlist.append(hasher.hexdigest())

        # Storing data
        DATA['hashlist'] = hashlist
        
        ## Storing Data to json
        json_path = self.rootpath + '/data.json'
        
        with open(json_path,'w') as file:
            json.dump(DATA, file)

        message = "System has been Set"
        self.messagebox(message,'set')  

        t3 = threading.Thread(target=self.complete)
        t3.start()

def initialize():                  
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()


