#!python
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon
from utils import find_claro
 
def about_DAGMC():
    """
    Provides the about box
    """

    claro = find_claro()

    about_box = QMessageBox(claro)
    about_box.setWindowTitle("About DAGMC toolbar")
    about_box.setText("The DAGMC toolbar provides tools to enhance the DAGMC workflow.\n\n" \
    "This tool is provided under an MIT license. See the provided license file for details.")
    about_box.setIconPixmap(QIcon('../icons/svalinn.png').pixmap(32, 32)) 
    
    about_box.exec_()


if __name__ == "__coreformcubit__":
    about_DAGMC()
