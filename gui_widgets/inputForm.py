from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QDoubleSpinBox, QComboBox, QFileDialog, QMessageBox)

# --- InputForm ---
class InputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.combo_shape = QComboBox(); self.combo_shape.addItems(["Zylinder", "Quader"])
        self.combo_shape.currentTextChanged.connect(self.update_inputs)
        self.layout.addWidget(QLabel("Geometrie:")); self.layout.addWidget(self.combo_shape)

        # Geometrie-Felder
        # Zylinder
        self.spin_r = QDoubleSpinBox(); self.spin_r.setPrefix("r="); self.spin_r.setValue(0.1); self.spin_r.setSuffix("m")
        self.spin_h = QDoubleSpinBox(); self.spin_h.setPrefix("h="); self.spin_h.setValue(0.2); self.spin_h.setSuffix("m")

        # Quader 
        self.spin_l = QDoubleSpinBox(); self.spin_l.setPrefix("l="); self.spin_l.setValue(0.2); self.spin_l.setSuffix("m")
        self.spin_b = QDoubleSpinBox(); self.spin_b.setPrefix("b="); self.spin_b.setValue(0.1); self.spin_b.setSuffix("m")
        self.spin_t = QDoubleSpinBox(); self.spin_t.setPrefix("h="); self.spin_t.setValue(0.05); self.spin_t.setSuffix("m")

        # Öffnungen
        self.combo_opening = QComboBox(); self.combo_opening.addItems(["Rund", "Schlitz"])
        self.combo_opening.currentTextChanged.connect(self.update_opening)
        self.spin_n = QDoubleSpinBox(); self.spin_n.setPrefix("n="); self.spin_n.setValue(1); self.spin_n.setDecimals(0)
        self.spin_L = QDoubleSpinBox(); self.spin_L.setPrefix("L="); self.spin_L.setValue(0.02)
        self.spin_r_open = QDoubleSpinBox(); self.spin_r_open.setPrefix("r_open="); self.spin_r_open.setValue(0.005)
        self.spin_b_slit = QDoubleSpinBox(); self.spin_b_slit.setPrefix("b_slit="); self.spin_b_slit.setValue(0.01)
        self.spin_l_slit = QDoubleSpinBox(); self.spin_l_slit.setPrefix("l_slit="); self.spin_l_slit.setValue(0.05)

        # Bedingungen
        # Temperatur
        self.spin_T = QDoubleSpinBox()
        self.spin_T.setPrefix("T=")
        self.spin_T.setValue(20)
        self.spin_T.setSuffix("°C")
        self.spin_T.setMinimum(-273.15)
        self.spin_T.setDecimals(2)
        
        # Luftfeuchtigkeit
        self.spin_H = QDoubleSpinBox()
        self.spin_H.setPrefix("H=")
        self.spin_H.setValue(50)
        self.spin_H.setSuffix("%")
        self.spin_H.setRange(0.0, 100.0)
        self.spin_H.setDecimals(2)

        self.widgets = [self.spin_r, self.spin_h, self.spin_l, self.spin_b, self.spin_t,
                        self.combo_opening, self.spin_n, self.spin_L, self.spin_r_open,
                        self.spin_b_slit, self.spin_l_slit, self.spin_T, self.spin_H]
        for w in self.widgets: self.layout.addWidget(w)
        self.setLayout(self.layout)
        self.layout.addStretch()
        self.update_inputs("Zylinder")
        self.update_opening("Rund")

    def update_inputs(self, shape):
        for w in [self.spin_r, self.spin_h, self.spin_l, self.spin_b, self.spin_t]:
            w.setVisible(False)
        if shape == "Zylinder":
            self.spin_r.setVisible(True); self.spin_h.setVisible(True)
        else:
            self.spin_l.setVisible(True); self.spin_b.setVisible(True); self.spin_t.setVisible(True)

    def update_opening(self, shape):
        for w in [self.spin_r_open, self.spin_b_slit, self.spin_l_slit]:
            w.setVisible(False)
        if shape == "Rund":
            self.spin_r_open.setVisible(True)
        else:
            self.spin_b_slit.setVisible(True); self.spin_l_slit.setVisible(True)

    def get_inputs(self):
        dims = {}
        
        if self.combo_shape.currentText() == "Zylinder":
            dims = {'r': self.spin_r.value(), 'h': self.spin_h.value()}
        else:
            dims = {'l': self.spin_l.value(), 'b': self.spin_b.value(), 'h': self.spin_t.value()}
        
        dims.update({'L': self.spin_L.value(), 'r_open': self.spin_r_open.value(),
                     'b_slit': self.spin_b_slit.value(), 'l_slit': self.spin_l_slit.value()})
        
        return (self.combo_shape.currentText(), dims, int(self.spin_n.value()),
                self.combo_opening.currentText(), self.spin_T.value(), self.spin_H.value())
