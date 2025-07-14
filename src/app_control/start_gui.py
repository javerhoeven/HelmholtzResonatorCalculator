from PyQt6.QtWidgets import  QApplication
from gui_widgets.mainWindow import MainWindow

def start_gui():
    import sys 
    app = QApplication(sys.argv) 
    win = MainWindow()
    win.show()
    sys.exit(app.exec())