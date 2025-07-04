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
            params = self.input_form.get_inputs()
            print(params)

            # create simulation
            sim = forward(params)
            # get data to display
            frequencies = sim.sim_params.frequencies    # x-Axis
            absorbtion_area = sim.absorbtion_area       # y-Axis
            z_friction = sim.z_friction                 # y-Axis
            z_porous = np.full_like(frequencies, sim.z_porous)                   # y-Axis
            z_radiation = sim.z_radiation                  # y-Axis
            z_stiff_mass = sim.z_stiff_mass                 # y-Axis
            f_res = sim.f_resonance                     # Peak
            q_factor = sim.q_factor                     # Q-Factor
            a_max = sim.peak_absorbtion_area                           # Max Absorption Area
            
            data = {"Frequency [Hz]" : frequencies,
                    "Absorption Area" : absorbtion_area,
                    "Impedance Friction" : z_friction,
                    "Impedance Porous" : z_porous,
                    "Impedance Radiation" : z_radiation,
                    "Impedance Stiff Mass" : z_stiff_mass}



            # hier wird auf die Rückgabeparameter der Berechnung zugegriffen um diese dann ans ResultView zu schicken
            # 
            #f0, data = model.results()
            self.result_view.show_results(f_res, data, q_factor, a_max)
            
            
        
        except Exception as e:
            QMessageBox.critical(None, "Fehler", str(e))