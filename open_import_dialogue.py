from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds

# Get the main Maya window
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    
class OpenImportDialogue(QtWidgets.QDialog):
    
    # File filters for file selection window
    FILE_FILTERS = "Maya (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
    
    selected_filter = "Maya (*.ma *.mb)"
    
    # For creating an instance of module in production environment
    dialog_instance = None
    
    @classmethod
    def show_dialog(cls):
        if not cls.dialog_instance:
            cls.dialog_instance = OpenImportDialogue()
        cls.dialog_instance.show()
        if cls.dialog_instance.isHidden():
            cls.dialog_instance.show()
        else:
            cls.dialog_instance.raise_()
            cls.dialog_instance.activateWindow()
    
    # Constructor
    def __init__(self, parent=maya_main_window()):
        super(OpenImportDialogue, self).__init__(parent)
        self.setWindowTitle("Open/Import/Reference")
        self.setMinimumSize(300, 80)
        
        # Call these functions to instantiate widgets in window (along with layouts and connections for widgets)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    # Create widgets
    def create_widgets(self):
        self.file_lineedit = QtWidgets.QLineEdit()
        self.select_file_path_button = QtWidgets.QPushButton()
        self.select_file_path_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.select_file_path_button.setToolTip("Select File")
        
        self.open_radiobtn = QtWidgets.QRadioButton("Open")
        self.open_radiobtn.setChecked(True) # set default checked
        self.import_radiobtn = QtWidgets.QRadioButton("Import")
        self.ref_radiobtn = QtWidgets.QRadioButton("Reference")
        
        self.force_check_box =  QtWidgets.QCheckBox("Force")
        
        self.apply_button = QtWidgets.QPushButton("Apply")
        self.close_button = QtWidgets.QPushButton("Close")
        
    # Create layouts for widgets
    def create_layouts(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.file_lineedit)
        file_path_layout.addWidget(self.select_file_path_button)
        
        # Part of the same parent so this set of radio buttons only has one checked at a time
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
    
    # Create connections for signals to slots
    def create_connections(self):
        self.select_file_path_button.clicked.connect(self.show_file_select_dialogue)
        self.open_radiobtn.toggled.connect(self.update_force_visibility)
        
        self.apply_button.clicked.connect(self.load_file)
        self.close_button.clicked.connect(self.close)
    
    # Load file into Maya
    def load_file(self):
        file_path = self.file_lineedit.text()
        
        # Check if file_path is not empty
        if not file_path:
            om.MGlobal.displayError("No file path was selected.")
            return
        
        # Check if file_path exists
        file_info = QtCore.QFileInfo(file_path)
        
        if not file_info.exists():
            om.MGlobal.displayError("File does not exist: {0}".format(file_path))
            return
        
        # Check which radio button was selected
        if self.open_radiobtn.isChecked():
            self.open_file(file_path)
        elif self.import_radiobtn.isChecked():
            self.import_file(file_path)
        else:
            self.reference_file(file_path)
    # Open file
    def open_file(self, file_path):
        force = self.force_check_box.isChecked()
        # If unsaved changes confirm first with user
        if not force and cmds.file(q=True, modified=True):
            result = QtWidgets.QMessageBox.question(self, "Modified", "Current scene has unsaved changes. Continue?")
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                force = True
            else:
                return
        cmds.file(file_path, open=True, ignoreVersion=True, force=force)
    
    # Import file
    def import_file(self, file_path):
        cmds.file(file_path, i=True, ignoreVersion=True)
    # Reference file
    def reference_file(self, file_path):
        cmds.file(file_path, reference=True, ignoreVersion=True)
    
    # Toggle force check box visibility
    def update_force_visibility(self, checked):
        self.force_check_box.setVisible(checked)
    
    # Show file select dialogue box
    def show_file_select_dialogue(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        if file_path:
            self.file_lineedit.setText(file_path)

# Main function of script for development testing        
if __name__ == "__main__":
    try:
        open_import_dialogue.close()
        open_import_dialogue.deleteLater()
    except:
        pass
    open_import_dialogue = OpenImportDialogue();
    open_import_dialogue.show()