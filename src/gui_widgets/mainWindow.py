from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox)
from math import pi

from gui_widgets.inputForm import InputForm
from gui_widgets.resultView import ResultView

from io_tools.save_to_json import save_to_json


# --- MainWindow ---
class MainWindow(QMainWindow):
    """
    Main application window for the Helmholtz-Resonator Tool.

    This class assembles the main GUI components including the input form,
    result view, and control buttons for simulation and export functionality.
    """

    def __init__(self) -> None:
        """
        Initialize the main window and set up the GUI layout.

        Components:
        - InputForm: widget for user-defined parameters.
        - ResultView: widget for displaying plots and calculated results.
        - GUIController: handles the business logic and calculations.
        
        Args:
            None

        Returns:
            None
        """

        from gui_widgets.GUIController import GUIController

         
        super().__init__()
        self.setWindowTitle("Helmholtz-Resonator Tool")

        self.input_form = InputForm()
        self.result_view = ResultView()
        self.input_form.result_view = self.result_view  # <--- Direkter Zugriff
        self.controller = GUIController(self.input_form, self.result_view)
        
        self.button_calc = QPushButton("Calculate")
        self.button_calc.clicked.connect(self.on_calculate)
        
        self.button_export = QPushButton("Export Results (JSON)")
        self.button_export.clicked.connect(self.on_export_json)
        
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


    def on_calculate(self) -> None: 
        """
        Trigger the calculation and plotting of results.

        This method uses the controller to process input data and
        update the ResultView accordingly.

        Args:
            None

        Returns:
            None
        """

        self.data = self.controller.calculate_and_show()


    def on_export_json(self) -> None:
        """
        Open a file dialog to export the simulation results as a JSON file.

        If no simulation has been run yet, a warning message is shown.
        
        Args:
            None

        Returns:
            None
        """

        path, _ = QFileDialog.getSaveFileName(self, "Save Simulation", "", "JSON Files (*.json)")
        if not path:
            return

        try:
            # Stelle sicher, dass du auf ein gültiges Simulation-Objekt zugreifst
            simulation = getattr(self.controller, "simulation", None)  # oder self.data, falls dort gespeichert
            if simulation is None:
                QMessageBox.warning(self, "Export Error", "No simulation data available.")
                return

            save_to_json(simulation, path)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export simulation:\n{e}")

