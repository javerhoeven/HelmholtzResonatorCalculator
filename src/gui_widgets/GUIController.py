from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QDoubleSpinBox, QComboBox, QFileDialog, QMessageBox)

from app_control import forward
import numpy as np

## hier muss das entsprechende modul importiert werden, 
# welches die input parameter verarbeitet
# from HelmholtzModel import HelmholtzModel

# --- Controller ---
class GUIController:
    def __init__(self, input_form, result_view):
        self.input_form = input_form; self.result_view = result_view
    def calculate_and_show(self):
        try:
            # get simulation parameters from input form
            params = self.input_form.get_inputs()

            # create simulation
            sim = forward(params)
            # get data to display
            f_res = sim.f_resonance                     # Peak
            q_factor = sim.q_factor                     # Q-Factor
            a_max = sim.peak_absorbtion_area            # Max Absorption Area
            
            data = {"Frequency [Hz]" : sim.sim_params.frequencies,
                    "Absorption Area" : sim.absorbtion_area,
                    "Impedance Friction" : sim.z_friction,
                    "Impedance Porous" : sim.z_porous,
                    "Impedance Radiation" : sim.z_radiation,
                    "Impedance Stiff Mass" : sim.z_stiff_mass}



            # hier wird auf die Rückgabeparameter der Berechnung zugegriffen um diese dann ans ResultView zu schicken
            # 
            #f0, data = model.results()
            self.result_view.show_results(f_res, data, q_factor, a_max)
            
            
        
        except Exception as e:
            QMessageBox.critical(None, "Fehler", str(e))