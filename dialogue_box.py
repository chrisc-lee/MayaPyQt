from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


# Get the main Maya window
def mayaMainWindow():
    mainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindowPtr), QtWidgets.QWidget)

# creating own signal for QLineEdit    
class MyLineEdit(QtWidgets.QLineEdit):
    enter_pressed = QtCore.Signal(str)
    
    def keyPressEvent(self, e):
        super(MyLineEdit, self).keyPressEvent(e)
        
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit("Enter Key Pressed")
        elif e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit("Return Key Pressed")

class TestDialogue(QtWidgets.QDialog):
    # constructor (make parent the Maya main window so exists in Maya window and doesn't create a new window outside Maya window)
    def __init__(self, parent=mayaMainWindow()):
        super(TestDialogue, self).__init__(parent)
        self.setWindowTitle("Test Dialogue")
        self.setMinimumWidth(200)
        # The help button is disabled by default in Maya 2022
        #self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        # call these functions to instantiate widgets in window (along with layouts and connections for widgets)
        self.createWidgets()
        self.createLayouts()
        self.createConnections()
        
    def createWidgets(self):
        # combo box (drop down box)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(["ComboBoxItem 1", "ComboBoxItem 2", "ComboBoxItem 3", "ComboBoxItem 4"])
        # Line edit (text field)
        self.linedit = MyLineEdit()
        # Check Box
        self.checkbox1 = QtWidgets.QCheckBox() 
        self.checkbox2 = QtWidgets.QCheckBox()
        # Buttons
        self.okBtn = QtWidgets.QPushButton("OK")
        self.cancelBtn = QtWidgets.QPushButton("Cancel")
             
    def createLayouts(self):
        # Form Layout
        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow("ComboBox: ", self.combobox)
        formLayout.addRow("Name: ", self.linedit)
        formLayout.addRow("Hidden: ", self.checkbox1)
        formLayout.addRow("Lock: ", self.checkbox2)
        # Horizontal Box Layout
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.okBtn)
        buttonLayout.addWidget(self.cancelBtn)
        # Vertical Box Layout for main layout (to hold other layouts)
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
    
    # create connections for signals to slots
    def createConnections(self):
        self.linedit.enter_pressed.connect(self.on_enter_pressed)
        self.checkbox1.toggled.connect(self.printIsHidden)
        self.combobox.activated.connect(self.on_activated_int)
        self.combobox.activated[str].connect(self.on_activated_str) #[str] to indicate which function to call using decorator
        self.cancelBtn.clicked.connect(self.close)
    
    # slots for different widgets    
    def on_enter_pressed(self, text):
        print(text)
    
    # decorators for "function overloading" (since python doesn't do python overloading)
    @QtCore.Slot(int)
    def on_activated_int(self, index):
        print("ComboBox Index: {0}".format(index))
    
    @QtCore.Slot(str)
    def on_activated_str(self, text):
        print("ComboBox Text: {0}".format(text))
        
    def printHelloName(self, name):
        #name = self.linedit.text()
        print("Hello {0}!".format(name))
    
    def printIsHidden(self, checked):
        #isHidden = self.checkbox1.isChecked()
        if checked:
            print("Object is hidden")
        else:
            print("Object is visible")

# main function of script        
if __name__ == "__main__":
    try:
        testDialogue.close()
        testDialogue.deleteLater()
    except:
        pass
    testDialogue = TestDialogue();
    testDialogue.show()