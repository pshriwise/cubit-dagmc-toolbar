#!python
from PySide6.QtWidgets import QApplication, QDockWidget, QMessageBox

def get_qapp():
    return QApplication.instance()

# I'm not sure why findChild doesn't work
def find_claro():
    qApp = get_qapp()
    widgets = qApp.topLevelWidgets()
    for w in widgets:
        if "Claro" in w.objectName() and type(w).__name__ == 'QMainWindow':
            return w
    return None

def ErrorWindow(error_msg):
    claro = find_claro()
    msg = QMessageBox(claro)
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(error_msg)
    msg.setWindowTitle("Error")
    msg.exec_()

if __name__ == "__coreformcubit__":
    qApp = qApp = get_qapp()
    claro = find_claro()
    ccp = claro.findChild(QDockWidget, "CubitCommandPanel")
    ccl = claro.findChild(QDockWidget, "ClaroCommandWindow")
