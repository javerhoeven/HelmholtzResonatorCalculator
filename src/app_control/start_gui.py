import sys
from PyQt6.QtWidgets import  QApplication
# from gui_widgets.main_window import MainWindow

def start_gui():
    app = QApplication(sys.argv)
    # TODO: fix
    # win = MainWindow()
    # win.show()
    sys.exit(app.exec())