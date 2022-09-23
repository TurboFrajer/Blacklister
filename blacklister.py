from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys,requests, json
from netaddr import *
from datetime import datetime

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI.ui', self) # Load the .ui file 


        self.show() # Show the GUI

        self.input1 = self.findChild(QtWidgets.QLineEdit, 'input')
        self.input2 = self.findChild(QtWidgets.QLineEdit, 'input_2')

        self.textB = self.findChild(QtWidgets.QTextEdit, 'displayField')

        self.prase1 = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.menubar = self.findChild(QtWidgets.QMenuBar)

        self.bl = QtWidgets.QAction("Blacklisty", self) 
        self.menubar.addAction(self.bl)

        self.ib = QtWidgets.QAction("Interní blokování",self) 
        self.menubar.addAction(self.ib)

        self.bl.triggered.connect(self.showblack)
        self.ib.triggered.connect(self.showintern)

        self.button1 = self.findChild(QtWidgets.QPushButton, "blackbutton")
        self.button2 = self.findChild(QtWidgets.QPushButton, "internbutton")

        self.button1.clicked.connect(self.showblack)
        self.button2.clicked.connect(self.showintern)

        self.blackfinder = self.findChild(QtWidgets.QPushButton, "blackfinder")
        self.blackfinder.clicked.connect(self.blacksearch)


        self.internfinder = self.findChild(QtWidgets.QPushButton, "internfinder")
        self.internfinder.clicked.connect(self.internsearch)
        self.display1 = self.findChild(QtWidgets.QTextEdit, "display1")
        self.display2 = self.findChild(QtWidgets.QTextEdit, "display2")
        self.display3 = self.findChild(QtWidgets.QTextEdit, "display3")
        self.display4 = self.findChild(QtWidgets.QTextEdit, "display4")
        self.display5 = self.findChild(QtWidgets.QTextEdit, "display5")
        self.display6 = self.findChild(QtWidgets.QTextEdit, "display6")
        self.display7 = self.findChild(QtWidgets.QTextEdit, "display7")
        self.display8 = self.findChild(QtWidgets.QTextEdit, "display8")
        self.display9 = self.findChild(QtWidgets.QTextEdit, "display9")
        self.display10 = self.findChild(QtWidgets.QTextEdit, "display10")
        self.display11 = self.findChild(QtWidgets.QTextEdit, "display11")
        self.display12 = self.findChild(QtWidgets.QTextEdit, "display12")
        self.display13 = self.findChild(QtWidgets.QTextEdit, "display13")
        self.display14 = self.findChild(QtWidgets.QTextEdit, "display14")
        self.display15 = self.findChild(QtWidgets.QTextEdit, "display15")
        self.display16 = self.findChild(QtWidgets.QTextEdit, "display16")
        self.display17 = self.findChild(QtWidgets.QTextEdit, "display17")
        self.displayStatus = self.findChild(QtWidgets.QTextEdit, "displayStatus")
        self.displayStatus.setStyleSheet("font-size:24px; border:2px solid black")


    def showblack(self):
        self.prase1.setCurrentIndex(1)
                          
    def showintern(self):
        self.prase1.setCurrentIndex(2)

    def blacksearch(self):
        url4 = requests.get("enter blacklist  IPv4 URL") # !!!!!!!! NEED URL!!!!!!!
        url6 = requests.get("enter blacklist IPv6 URL") # !!!!!!!! NEED URL!!!!!!!
        url4.encoding = "utf-8"
        url6.encoding = "utf-8"
        text = url4.text + url6.text
        info = text.splitlines()
        found = [z.split()[0] for z in info]



        for x in range(len(found)):
            try:
                IPNetwork(self.input1.text()) == True

            except:
                print("Není IP adresa nebo rozsah.")
                self.textB.clear()
                self.textB.insertPlainText("Není IP adresa nebo rozsah.")
                break
            
            if IPNetwork(self.input1.text()) in IPNetwork(found[x]):        
                for y in range(len(info)):
                    if found[x] in info[y]:
                        tim = info[y].split()
                        print(f"Adresa {tim[0]} je blacklisted.")
                        self.textB.clear()
                        self.textB.insertPlainText(f"Adresa {tim[0]} je blacklisted.")
                        if tim[1] == "0":
                            print("Perma blacklisted.")
                            self.textB.insertPlainText("\nPerma blacklisted.")
                            duvoda = " ".join(tim[2:])
                            print(f"Důvod: {duvoda}")
                            self.textB.insertPlainText(f"\nDůvod: {duvoda}")
                            
                        elif tim[1].isnumeric() == True and tim[2].isnumeric() == True:
                            print(f"Blacklisted od: {datetime.fromtimestamp(int(tim[2]))}")
                            self.textB.insertPlainText(f"\nBlacklisted od: {datetime.fromtimestamp(int(tim[2]))}")
                            bando = int(tim[1])+int(tim[2])
                            print(f"Blacklisted do: {datetime.fromtimestamp(bando)}")
                            self.textB.insertPlainText(f"\nBlacklisted do: {datetime.fromtimestamp(bando)}")
                            duvodb = " ".join(tim[3:])
                            print(f"Důvod: {duvodb}")                            
                            self.textB.insertPlainText(f"\nDůvod: {duvodb}")                           
                            
                        else:
                            print(info[y])
                            self.textB.insertPlainText(info[y])                         
                            break
                break
        else:
            print("Není blacklisted.")
            self.textB.clear()
            self.textB.insertPlainText("Není blacklisted.")

    def internsearch(self):
        try: 
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            url = "enter internal URL" # !!!!!! enter internal URL !!!!!!!!
            r = requests.post(url, data=f"data={{\"action\": \"search\",\"ip\":\"{self.input2.text().strip()}\"}}",headers=headers )

            parsed = json.loads(r.text)
            devices = parsed["devices"]
            listing = list(devices) 

            #1
            self.display1.clear()
            self.display1.insertPlainText("ID:" + listing[0]["identificator"])
            self.display1.insertPlainText("\nHostname:" + listing[0]["hostname"])
            self.display1.insertPlainText("\nStatus:" + listing[0]["status"])

            if listing[0]["status"] == "0":
                self.display1.setStyleSheet("background-color:green;color:white")
            else:
                self.display1.setStyleSheet("background-color:red;color:white")

            #2
            self.display2.clear()
            self.display2.insertPlainText("ID:" + listing[1]["identificator"])
            self.display2.insertPlainText("\nHostname:" + listing[1]["hostname"])
            self.display2.insertPlainText("\nStatus:" + listing[1]["status"])

            if listing[1]["status"] == "0":
                self.display2.setStyleSheet("background-color:green;color:white")
            else:
                self.display2.setStyleSheet("background-color:red;color:white")

            #3
            self.display3.clear()
            self.display3.insertPlainText("ID:" + listing[2]["identificator"])
            self.display3.insertPlainText("\nHostname:" + listing[2]["hostname"])
            self.display3.insertPlainText("\nStatus:" + listing[2]["status"])

            if listing[2]["status"] == "0":
                self.display3.setStyleSheet("background-color:green;color:white")
            else:
                self.display3.setStyleSheet("background-color:red;color:white")

            #4
            self.display4.clear()
            self.display4.insertPlainText("ID:" + listing[3]["identificator"])
            self.display4.insertPlainText("\nHostname:" + listing[3]["hostname"])
            self.display4.insertPlainText("\nStatus:" + listing[3]["status"])

            if listing[3]["status"] == "0":
                self.display4.setStyleSheet("background-color:green;color:white")
            else:
                self.display4.setStyleSheet("background-color:red;color:white")
                
            #5
            self.display5.clear()
            self.display5.insertPlainText("ID:" + listing[4]["identificator"])
            self.display5.insertPlainText("\nStatus:" + listing[4]["status"])

            if listing[4]["status"] == "0":
                self.display5.setStyleSheet("background-color:green;color:white")
            else:
                self.display5.setStyleSheet("background-color:red;color:white")

            #6
            self.display6.clear()
            self.display6.insertPlainText("ID:" + listing[5]["identificator"])
            self.display6.insertPlainText("\nStatus:" + listing[5]["status"])

            if listing[5]["status"] == "0":
                self.display6.setStyleSheet("background-color:green;color:white")
            else:
                self.display6.setStyleSheet("background-color:red;color:white")

            #7
            self.display7.clear()
            self.display7.insertPlainText("ID:" + listing[6]["identificator"])
            self.display7.insertPlainText("\nStatus:" + listing[6]["status"])

            if listing[6]["status"] == "0":
                self.display7.setStyleSheet("background-color:green;color:white")
            else:
                self.display7.setStyleSheet("background-color:red;color:white")

            #8
            self.display8.clear()
            self.display8.insertPlainText("ID:" + listing[7]["identificator"])
            self.display8.insertPlainText("\nStatus:" + listing[7]["status"])

            if listing[7]["status"] == "0":
                self.display8.setStyleSheet("background-color:green;color:white")
            else:
                self.display8.setStyleSheet("background-color:red;color:white")

            #9
            self.display9.clear()
            self.display9.insertPlainText("ID:" + listing[8]["identificator"])
            self.display9.insertPlainText("\nStatus:" + listing[8]["status"])

            if listing[8]["status"] == "0":
                self.display9.setStyleSheet("background-color:green;color:white")
            else:
                self.display9.setStyleSheet("background-color:red;color:white")

            #10
            self.display10.clear()
            self.display10.insertPlainText("ID:" + listing[9]["identificator"])
            self.display10.insertPlainText("\nStatus:" + listing[9]["status"])

            if listing[9]["status"] == "0":
                self.display10.setStyleSheet("background-color:green;color:white")
            else:
                self.display10.setStyleSheet("background-color:red;color:white")
            
            #11
            self.display11.clear()
            self.display11.insertPlainText("ID:" + listing[10]["identificator"])
            self.display11.insertPlainText("\nStatus:" + listing[10]["status"])

            if listing[10]["status"] == "0":
                self.display11.setStyleSheet("background-color:green;color:white")
            else:
                self.display11.setStyleSheet("background-color:red;color:white")

            #12
            self.display12.clear()
            self.display12.insertPlainText("ID:" + listing[11]["identificator"])
            self.display12.insertPlainText("\nStatus:" + listing[11]["status"])

            if listing[11]["status"] == "0":
                self.display12.setStyleSheet("background-color:green;color:white")
            else:
                self.display12.setStyleSheet("background-color:red;color:white")

            #13
            self.display13.clear()
            self.display13.insertPlainText("ID:" + listing[12]["identificator"])
            self.display13.insertPlainText("\nStatus:" + listing[12]["status"])

            if listing[12]["status"] == "0":
                self.display13.setStyleSheet("background-color:green;color:white")
            else:
                self.display13.setStyleSheet("background-color:red;color:white")
                
            #14
            self.display14.clear()
            self.display14.insertPlainText("ID:" + listing[13]["identificator"])
            self.display14.insertPlainText("\nStatus:" + listing[13]["status"])

            if listing[13]["status"] == "0":
                self.display14.setStyleSheet("background-color:green;color:white")
            else:
                self.display14.setStyleSheet("background-color:red;color:white")
            
            #15
            self.display15.clear()
            self.display15.insertPlainText("ID:" + listing[14]["identificator"])
            self.display15.insertPlainText("\nStatus:" + listing[14]["status"])

            if listing[14]["status"] == "0":
                self.display15.setStyleSheet("background-color:green;color:white")
            else:
                self.display15.setStyleSheet("background-color:red;color:white")

            #16
            self.display16.clear()
            self.display16.insertPlainText("ID:" + listing[15]["identificator"])
            self.display16.insertPlainText("\nStatus:" + listing[15]["status"])

            if listing[15]["status"] == "0":
                self.display16.setStyleSheet("background-color:green;color:white")
            else:
                self.display16.setStyleSheet("background-color:red;color:white")

            #17
            self.display17.clear()
            self.display17.insertPlainText("ID:" + listing[16]["identificator"])
            self.display17.insertPlainText("\nStatus:" + listing[16]["status"])

            if listing[16]["status"] == "0":
                self.display17.setStyleSheet("background-color:green;color:white")
            else:
                self.display17.setStyleSheet("background-color:red;color:white")

            #Status
            self.displayStatus.clear()
            self.displayStatus.insertPlainText(f"{self.input2.text().strip()} otestována.")

        except:
            self.displayStatus.clear()
            self.displayStatus.insertPlainText("Není IP adresa nebo rozsah")
            
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application

