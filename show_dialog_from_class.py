# Python won't reimport packages/modules so Maya needs to be closed and reopened for any changes to take effect. 
# This is good for a production environment only since code will not change there. 

# For a development environment we can run script directly from main function or we can use reload(<module_name>) function
# to reload packages/modules. Reload can introduce some issues though so beware.

from open_import_dialogue import OpenImportDialogue

OpenImportDialogue.show_dialog()