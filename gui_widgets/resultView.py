from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel,  QComboBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import csv


# --- ResultView ---
class ResultView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()


        # Plot + Steuerung
        self.combo_x = QComboBox()
        self.combo_x.addItems(["Frequency [Hz]"])
        self.combo_y = QComboBox()
        self.combo_y.addItems(["Absorption Coefficient", "Impedance"])

        layout.addWidget(QLabel("X-Axis:"))
        layout.addWidget(self.combo_x)
        layout.addWidget(QLabel("Y-Axis:"))
        layout.addWidget(self.combo_y)

        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # --- Ergebnis-Labels: f0, Q, Amax ---
        self.label_f0 = QLabel("Resonance Frequency: - Hz")
        self.label_q = QLabel("Q Factor: -")
        self.label_amax = QLabel("Max Absorption Area: - m²")

        self.label_f0.setToolTip("Frequency at which resonance occurs (Hz).")
        self.label_q.setToolTip("Quality factor – sharpness of the resonance peak.")
        self.label_amax.setToolTip("Maximum effective absorption area (m²).")

        result_layout = QHBoxLayout()
        result_layout.addWidget(self.label_f0)
        result_layout.addWidget(self.label_q)
        result_layout.addWidget(self.label_amax)

        layout.addLayout(result_layout)
        self.setLayout(layout)

    def show_results(self, f0, data, q_factor=None, a_max=None):
        """Update the plot and display numerical results.

        Args:
            f0 (float): Resonance frequency in Hz
            data (dict): Dict with 'x' and 'y' arrays (based on dropdown selection)
            q_factor (float | None): Optional Q-factor
            a_max (float | None): Optional maximum absorption area [m²]
        """
        # Update labels
        self.label_f0.setText(f"Resonance Frequency: {f0:.2f} Hz")
        self.label_q.setText(f"Q Factor: {q_factor:.2f}" if q_factor is not None else "Q Factor: -")
        self.label_amax.setText(f"Max Absorption Area: {a_max:.4f} m²" if a_max is not None else "Max Absorption Area: - m²")

        # Plot
        x = data.get(self.combo_x.currentText(), [])
        y = data.get(self.combo_y.currentText(), [])
        self.ax.clear()
        self.ax.plot(x, y, label=f"{self.combo_y.currentText()} vs {self.combo_x.currentText()}")
        self.ax.set_xlabel(self.combo_x.currentText())
        self.ax.set_ylabel(self.combo_y.currentText())
        self.ax.grid()
        self.ax.legend()
        self.canvas.draw()

    def export_csv(self, data, path):
        x_key = self.combo_x.currentText()
        y_key = self.combo_y.currentText()
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([x_key, y_key])
            for x, y in zip(data[x_key], data[y_key]):
                writer.writerow([x, y])

