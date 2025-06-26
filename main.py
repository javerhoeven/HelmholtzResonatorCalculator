from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QDoubleSpinBox, QComboBox, QFileDialog, QMessageBox)

from gui_widgets.inputForm import InputForm
from gui_widgets.resultView import ResultView
from gui_widgets.GUIController import GUIController


from app_control import forward, search_optimal
from io_tools import load_from_json
from io_tools.examples import load_example, examples


# --- MainWindow ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helmholtz-Resonator Tool")
        self.input_form = InputForm()
        self.result_view = ResultView()
        self.controller = GUIController(self.input_form, self.result_view)
        
        self.button_calc = QPushButton("Berechnen / Plot")
        self.button_calc.clicked.connect(self.on_calculate)
        
        self.button_export = QPushButton("Export CSV")
        self.button_export.clicked.connect(self.on_export)
        
        layout = QHBoxLayout()
        layout.addWidget(self.input_form)
        layout.addWidget(self.result_view)
        
        right = QVBoxLayout()
        right.addLayout(layout)
        right.addWidget(self.button_calc)
        right.addWidget(self.button_export)
        
        central = QWidget()
        central.setLayout(right)
        self.setCentralWidget(central)


    def on_calculate(self): 
        self.data = self.controller.calculate_and_show()

    def on_export(self):
        if hasattr(self, "data"):
            path, _ = QFileDialog.getSaveFileName(self, "Speichern", "", "CSV Files (*.csv)")
            if path: self.result_view.export_csv(self.data, path)

# --- Hauptprogramm ---
if __name__ == '__main__':
    # import sys 
    # app = QApplication(sys.argv) 
    # win = MainWindow()
    # win.show()
    # sys.exit(app.exec())
    # for example in examples:
    #    print(f"Running example {example}")
    #    simulation = load_example(example)
    #    simulation.plot_absorbtion_area()
    #    simulation.calc_q_factor()


    
    search_optimal(20, 1)