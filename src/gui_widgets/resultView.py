from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel,  QComboBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np


# --- ResultView ---
class ResultView(QWidget):
    """
    Visual component for displaying the simulation results in the GUI.

    This widget includes:
    - Dropdowns to control the X and Y axes of the plot
    - A Matplotlib plot with toolbar
    - Labels showing computed quantities such as resonance frequency, Q-factor,
      peak absorption area, and impedance components.
    """

    def __init__(self):
        """
        Initialize the result display view and set up layout, widgets, and event handling.
        
        Args:
            None

        Returns:
            None
        """

        super().__init__()
        layout = QVBoxLayout()


        # Axis selection dropdowns
        self.combo_x = QComboBox()
        self.combo_x.addItems(["Frequency [Hz]"])
        self.combo_y = QComboBox()
        self.combo_y.addItems(["Absorption Area", "Impedance Friction", "Impedance Porous",
                              "Impedance Radiation", "Impedance Stiff Mass"])


        layout.addWidget(QLabel("X-Axis:"))
        layout.addWidget(self.combo_x)
        layout.addWidget(QLabel("Y-Axis:"))
        layout.addWidget(self.combo_y)

        # Matplotlib canvas and toolbar
        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # Result labels
        self.label_f0 = QLabel("Resonance Frequency: - Hz")
        self.label_q = QLabel("Q Factor: -")
        self.label_amax = QLabel("Max Absorption Area: - m²")
        self.label_friction = QLabel("Friction: - Pa·s/m")
        self.label_porous = QLabel("Porous: - Pa·s/m")

        self.label_f0.setToolTip("Frequency at which resonance occurs (Hz).")
        self.label_q.setToolTip("Quality factor – sharpness of the resonance peak.")
        self.label_amax.setToolTip("Maximum effective absorption area (m²).")
        self.label_friction.setToolTip("Frictional impedance: Resistance due to air viscosity inside the aperture.")
        self.label_porous.setToolTip("Porous impedance: Acoustic resistance caused by porous material effects at the boundary.")
        
        result_layout = QHBoxLayout()
        result_layout.addWidget(self.label_f0)
        result_layout.addWidget(self.label_q)
        result_layout.addWidget(self.label_amax)
        result_layout.addWidget(self.label_friction)
        result_layout.addWidget(self.label_porous)

        layout.addLayout(result_layout)
        self.setLayout(layout)

        # Connect dropdowns to dynamic plot update
        self.combo_x.currentTextChanged.connect(self.update_plot)
        self.combo_y.currentTextChanged.connect(self.update_plot)

        # Internal state
        self._data = {}
        self._f0 = None
        self._q = None
        self._a_max = None


    def show_results(self, f0: float, data: dict, q_factor: float = None, a_max: float = None) -> None:
        
        """Update the plot and display numerical results.

        Args:
            f0 (float): Resonance frequency in Hz
            data (dict): Dict with 'x' and 'y' arrays (based on dropdown selection)
            q_factor (float | None): Optional Q-factor
            a_max (float | None): Optional maximum absorption area [m²]
        
        Returns:
            None
        """
        from matplotlib.ticker import LogLocator, FuncFormatter

        # Update labels
        self.label_f0.setText(f"Resonance Frequency: {f0:.2f} Hz")
        self.label_q.setText(f"Q Factor: {q_factor:.2f}" if q_factor is not None else "Q Factor: -")
        self.label_amax.setText(f"Peak Absorption Area: {a_max:.4f} m²" if a_max is not None else "Peak Absorption Area: - m²")
        self.label_friction.setText(f"Friction: {max(data.get('Impedance Friction')):.2f} [Pa·s/m]")
        self.label_porous.setText(f"Porous: {data.get('Impedance Porous'):.2f} [Pa·s/m]")

        # Plot
        x = data.get(self.combo_x.currentText(), [])
        y = data.get(self.combo_y.currentText(), [])
        
        self.ax.clear()
        if np.iscomplexobj(y):
            self.ax.plot(x, np.real(y), label=f"RE({self.combo_y.currentText()}) vs {self.combo_x.currentText()}")
            self.ax.plot(x, np.imag(y), label=f"IMAG({self.combo_y.currentText()}) vs {self.combo_x.currentText()}")
        
        elif np.isscalar(y):
            self.ax.plot(x, np.full_like(x, y), label = f"{self.combo_y.currentText()} vs {self.combo_x.currentText()}")

        else:
            self.ax.plot(x, y, label=f"{self.combo_y.currentText()} vs {self.combo_x.currentText()}")
        
        self.ax.set_xlim(f0 /5, f0 *5)
        self.ax.set_xscale('log')

        # make pretty labels
        self.ax.set_xlabel(self.combo_x.currentText())
        self.ax.set_ylabel(self.combo_y.currentText())
        self.ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1, 2, 5))) # 1, 2, 5
        self.ax.xaxis.set_minor_locator(LogLocator(base=10, subs=range(1, 10)))
        self.ax.xaxis.set_major_formatter(
            FuncFormatter(lambda x, _:
                        f'{x/1000:.0f} k' if x >= 1000 else f'{x:.0f}'))
        
        self.ax.grid(which='major', ls='--', lw=.6)
        self.ax.grid(which='minor', ls=':',  lw=.3)
        self.ax.legend()
        self.canvas.draw()

        
        # Save state for dynamic updates
        self._data = data
        self._f0 = f0
        self._q = q_factor
        self._a_max = a_max

    def update_plot(self) -> None:
        """
        Re-render the plot when axis selections change.

        Only works if results have already been shown at least once.
        
        Args:
            None

        Returns:
            None
        """
        if not self._data or self._f0 is None:
            return  # noch nichts zum Anzeigen
        self.show_results(self._f0, self._data, self._q, self._a_max)
