from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QDoubleSpinBox, QComboBox, QFileDialog, QMessageBox)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import csv


# --- ResultView ---
class ResultView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label_f0 = QLabel("Resonanzfrequenz: - Hz")
        self.canvas = FigureCanvas(Figure()); self.ax = self.canvas.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.combo_x = QComboBox(); self.combo_x.addItems(["Frequenz [Hz]", "Temperatur [°C]"])
        self.combo_y = QComboBox(); self.combo_y.addItems(["Absorptionsgrad", "Impedanz", "Schallgeschwindigkeit"])

        layout.addWidget(QLabel("X-Achse:")); layout.addWidget(self.combo_x)
        layout.addWidget(QLabel("Y-Achse:")); layout.addWidget(self.combo_y)
        layout.addWidget(self.toolbar); layout.addWidget(self.canvas); layout.addWidget(self.label_f0)
        
        self.setLayout(layout)

    def show_results(self, f0, data):
        self.label_f0.setText(f"Resonanzfrequenz: {f0:.2f} Hz")
        x = data.get(self.combo_x.currentText(), []); y = data.get(self.combo_y.currentText(), [])
        self.ax.clear(); self.ax.plot(x, y, label=f"{self.combo_y.currentText()} vs {self.combo_x.currentText()}")
        self.ax.set_xlabel(self.combo_x.currentText()); self.ax.set_ylabel(self.combo_y.currentText())
        self.ax.grid(); self.ax.legend(); self.canvas.draw()
        
    def export_csv(self, data, path):
        with open(path, "w", newline="") as f: writer = csv.writer(f)
        x_key, y_key = self.combo_x.currentText(), self.combo_y.currentText()
        writer.writerow([x_key, y_key]); [writer.writerow([x, y]) for x, y in zip(data[x_key], data[y_key])]
