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
        self.file_lineedit = QtWidgets.QLineEdit()
        self.select_file_path_button = QtWidgets.QPushButton("...")
        
        self.open_radiobtn = QtWidgets.QRadioButton("Open")
        self.open_radiobtn.setChecked(True) # set default checked
        self.import_radiobtn = QtWidgets.QRadioButton("Import")
        self.ref_radiobtn = QtWidgets.QRadioButton("Reference")
        
        self.force_check_box =  QtWidgets.QCheckBox("Force")
        
        self.apply_button = QtWidgets.QPushButton("Apply")
        self.close_button = QtWidgets.QPushButton("Close")
        
    # create layouts for widgets
    def create_layouts(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.file_lineedit)
        file_path_layout.addWidget(self.select_file_path_button)
        
        # part of the same parent so this set of radio buttons only has one checked at a time
        radio_button_layout = QtWidgets.QHBoxLayout()
        radio_button_layout.addWidget(self.open_radiobtn)
        radio_button_layout.addWidget(self.import_radiobtn)
        radio_button_layout.addWidget(self.ref_radiobtn)
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.close_button)
        
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("File: ", file_path_layout)
        form_layout.addRow("", radio_button_layout)
        form_layout.addRow("", self.force_check_box)
        form_layout.addRow("", button_layout)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
    
    # create connections for signals to slots
    def create_connections(self):
        self.select_file_path_button.clicked.connect(self.show_file_select_dialogue)
        self.open_radiobtn.toggled.connect(self.update_force_visibility)
        
        self.apply_button.clicked.connect(self.load_file)
        self.close_button.clicked.connect(self.close)
    
    # load file into Maya
    def load_file(self):
        pass
    
    # toggle force check box visibility
    def update_force_visibility(self, checked):
        pass
    
    # show file select dialogue box
    def show_file_select_dialogue(self):
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