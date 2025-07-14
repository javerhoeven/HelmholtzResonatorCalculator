from PyQt6.QtWidgets import QMessageBox
from gui_widgets.inputForm import InputForm
from gui_widgets.resultView import ResultView
from app_control import forward


# --- Controller ---
class GUIController:
    """
    Controller class connecting the InputForm and ResultView components.

    It handles the coordination between GUI inputs and backend simulation logic,
    and updates the result view based on calculated data.
    """

    def __init__(self, input_form: InputForm, result_view: ResultView) -> None:
        """
        Initialize the GUIController.

        Args:
            input_form (InputForm): Widget for collecting user inputs.
            result_view (ResultView): Widget for displaying calculated results.
        
        Returns:
            None
        """

        self.input_form = input_form; self.result_view = result_view


    def calculate_and_show(self) -> None:
        """
        Run the simulation using input parameters and update the result view.

        This method:
        - Retrieves parameters from the input form
        - Runs the simulation via the `forward()` function
        - Extracts results (resonance frequency, Q-factor, absorption area)
        - Passes result data to the result view for plotting and display

        On failure, a critical QMessageBox is shown.

        Args:
            None

        Returns:
            None
        """

        try:
            params = self.input_form.get_inputs()

            # create simulation
            sim = forward(params)
            self.simulation = sim
            
            # Extract results
            f_res = sim.f_resonance                     # Peak
            q_factor = sim.q_factor                     # Q-Factor
            a_max = sim.peak_absorbtion_area            # Max Absorption Area
            
            data = {"Frequency [Hz]" : sim.sim_params.frequencies,
                    "Absorption Area" : sim.absorbtion_area,
                    "Impedance Friction" : sim.z_friction,
                    "Impedance Porous" : sim.z_porous,
                    "Impedance Radiation" : sim.z_radiation,
                    "Impedance Stiff Mass" : sim.z_stiff_mass}

            # Update the GUI with simulation results
            self.result_view.show_results(f_res, data, q_factor, a_max)
            
        
        except Exception as e:
            QMessageBox.critical(None, "Fehler", str(e))