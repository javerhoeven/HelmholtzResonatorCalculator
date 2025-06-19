from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QDoubleSpinBox, QComboBox, QFileDialog, QMessageBox)

## hier muss das entsprechende modul importiert werden, 
# welches die input parameter verarbeitet
# from HelmholtzModel import HelmholtzModel

# --- Controller ---
class GUIController:
    def __init__(self, input_form, result_view):
        self.input_form = input_form; self.result_view = result_view
    def calculate_and_show(self):
        try:
            params = self.input_form.get_inputs()
            print(params)

            ##hier wird auf das Helmholtzmodel zugegriffen
            #model = HelmholtzModel(*params)


            # hier wird auf die Rückgabeparameter der Berechnung zugegriffen um diese dann ans ResultView zu schicken
            # 
            #f0, data = model.results()
            #self.result_view.show_results(f0, data)
            
            #return data
        
        except Exception as e:
            QMessageBox.critical(None, "Fehler", str(e))