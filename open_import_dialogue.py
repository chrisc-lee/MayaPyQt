from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

# Get the main Maya window
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    
class OpenImportDialogue(QtWidgets.QDialog):
    # constructor
    def __init__(self, parent=maya_main_window()):
        super(OpenImportDialogue, self).__init__(parent)
        self.setWindowTitle("Open/Import/Reference")
        self.setMinimumSize(300, 80)
        
        # call these functions to instantiate widgets in window (along with layouts and connections for widgets)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    # create widgets
    def create_widgets(self):
        pass
    # create layouts for widgets
    def create_layouts(self):
        pass
    # create connects for signals to slots
    def create_connections(self):
        pass

# main function of script        
if __name__ == "__main__":
    try:
        open_import_dialogue.close()
        open_import_dialogue.deleteLater()
    except:
        pass
    open_import_dialogue = OpenImportDialogue();
    open_import_dialogue.show()