from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QComboBox, QGroupBox, QFormLayout, QMessageBox
)
from traits.api import HasTraits, Enum, Range, Float, Bool, TraitError
from calculation.aperture import Aperture

class InputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()

        # === 1. GEOMETRIE ===
        self.group_geometry = QGroupBox("Geometry")
        geo_layout = QFormLayout()

        self.combo_shape = QComboBox()
        self.combo_shape.addItems(["Cylinder", "Cuboid"])
        self.combo_shape.setToolTip("Select the shape of the resonator: cylindrical or cuboid.")
        self.combo_shape.currentTextChanged.connect(self.update_inputs)
        geo_layout.addRow("Form:", self.combo_shape)


        self.spin_r = QDoubleSpinBox(); self.spin_r.setPrefix("r="); self.spin_r.setValue(0.1); self.spin_r.setSuffix("m")
        self.spin_h = QDoubleSpinBox(); self.spin_h.setPrefix("h="); self.spin_h.setValue(0.2); self.spin_h.setSuffix("m")
        self.spin_l = QDoubleSpinBox(); self.spin_l.setPrefix("l="); self.spin_l.setValue(0.2); self.spin_l.setSuffix("m")
        self.spin_b = QDoubleSpinBox(); self.spin_b.setPrefix("b="); self.spin_b.setValue(0.1); self.spin_b.setSuffix("m")
        self.spin_t = QDoubleSpinBox(); self.spin_t.setPrefix("h="); self.spin_t.setValue(0.05); self.spin_t.setSuffix("m")
        # Tool-Tipps:
        self.spin_r.setToolTip("Radius of the cylindrical resonator [m].")
        self.spin_h.setToolTip("Height of the cylindrical resonator [m].")
        self.spin_l.setToolTip("Length of the cuboid resonator [m].")
        self.spin_b.setToolTip("Width of the cuboid resonator [m].")
        self.spin_t.setToolTip("Height (or thickness) of the cuboid resonator [m].")

        geo_layout.addRow(self.spin_r)
        geo_layout.addRow(self.spin_h)
        geo_layout.addRow(self.spin_l)
        geo_layout.addRow(self.spin_b)
        geo_layout.addRow(self.spin_t)
        self.group_geometry.setLayout(geo_layout)
        self.main_layout.addWidget(self.group_geometry)

        # === 2. ÖFFNUNG ===
        self.group_opening = QGroupBox("Aperture Properties")
        opening_layout = QFormLayout()

        self.combo_aperture_form = self.add_enum_combobox("Aperture form:", "form", opening_layout)
        self.combo_aperture_form.currentTextChanged.connect(self.update_opening)    

        self.spin_n = QDoubleSpinBox(); self.spin_n.setPrefix("n="); self.spin_n.setValue(1); self.spin_n.setDecimals(0)
        self.spin_L = QDoubleSpinBox(); self.spin_L.setPrefix("L="); self.spin_L.setValue(0.02); self.spin_L.setSuffix("m")
        self.spin_r_open = QDoubleSpinBox(); self.spin_r_open.setPrefix("r_open="); self.spin_r_open.setValue(0.005); self.spin_r_open.setSuffix("m")
        self.spin_b_slit = QDoubleSpinBox(); self.spin_b_slit.setPrefix("b_slit="); self.spin_b_slit.setValue(0.01); self.spin_b_slit.setSuffix("m")
        self.spin_l_slit = QDoubleSpinBox(); self.spin_l_slit.setPrefix("l_slit="); self.spin_l_slit.setValue(0.05); self.spin_l_slit.setSuffix("m")
        # Tool-Tipps:
        self.combo_aperture_form.setToolTip("Geometric form of the aperture used in acoustic calculations (e.g. 'tube', 'slit').")
        self.spin_n.setToolTip("Number of openings in the resonator wall.")
        self.spin_L.setToolTip("Physical length of the aperture, often equal to the wall thickness [m].")
        self.spin_r_open.setToolTip("Radius of the circular aperture [m].")
        self.spin_b_slit.setToolTip("Width of the slit aperture [m].")
        self.spin_l_slit.setToolTip("Length of the slit aperture [m].")

        opening_layout.addRow(self.spin_n)
        opening_layout.addRow(self.spin_L)
        opening_layout.addRow(self.spin_r_open)
        opening_layout.addRow(self.spin_b_slit)
        opening_layout.addRow(self.spin_l_slit)
        self.group_opening.setLayout(opening_layout)
        self.main_layout.addWidget(self.group_opening)

        # === 3. ENDEN ===
        self.group_endings = QGroupBox("Boundary Configuration")
        endings_layout = QFormLayout()
        self.combo_inner_ending = self.add_enum_combobox("Inner End:", "inner_ending", endings_layout)
        self.combo_outer_ending = self.add_enum_combobox("Outer End:", "outer_ending", endings_layout)
        # Tool-Tipps:
        self.combo_inner_ending.setToolTip("Type of inner boundary of the aperture (e.g. open or flanged).")
        self.combo_outer_ending.setToolTip("Type of outer boundary of the aperture (e.g. open or flanged).")

        self.group_endings.setLayout(endings_layout)
        self.main_layout.addWidget(self.group_endings)

        # === 4. BEDINGUNGEN ===
        self.group_conditions = QGroupBox("Environmental Conditions")
        cond_layout = QFormLayout()

        self.spin_T = QDoubleSpinBox()
        self.spin_T.setPrefix("T="); self.spin_T.setValue(20); self.spin_T.setSuffix("°C")
        self.spin_T.setMinimum(-273.15); self.spin_T.setDecimals(2)

        self.spin_H = QDoubleSpinBox()
        self.spin_H.setPrefix("H="); self.spin_H.setValue(50); self.spin_H.setSuffix("%")
        self.spin_H.setRange(0.0, 100.0); self.spin_H.setDecimals(2)
        # Tool-Tipps:
        self.spin_T.setToolTip("Ambient temperature [°C].")
        self.spin_H.setToolTip("Relative humidity [%].")

        cond_layout.addRow(self.spin_T)
        cond_layout.addRow(self.spin_H)
        self.group_conditions.setLayout(cond_layout)
        self.main_layout.addWidget(self.group_conditions)

        self.setLayout(self.main_layout)
        self.update_inputs("Cylinder")
        self.update_opening("tube")

    def add_enum_combobox(self, label: str, trait_name: str, layout):
        combo = QComboBox()
        values = Aperture().trait(trait_name).handler.values
        combo.addItems(values)
        layout.addRow(label, combo)
        return combo

    def update_inputs(self, shape):
        for w in [self.spin_r, self.spin_h, self.spin_l, self.spin_b, self.spin_t]:
            w.setVisible(False)
        if shape == "Cylinder":
            self.spin_r.setVisible(True); self.spin_h.setVisible(True)
        else:
            self.spin_l.setVisible(True); self.spin_b.setVisible(True); self.spin_t.setVisible(True)

    def update_opening(self, shape):
        for w in [self.spin_r_open, self.spin_b_slit, self.spin_l_slit]:
            w.setVisible(False)
        if shape == "tube":
            self.spin_r_open.setVisible(True)
        else:
            self.spin_b_slit.setVisible(True); self.spin_l_slit.setVisible(True)

    def get_inputs(self):
        # --- Geometry ---
        if self.combo_shape.currentText() == "Cylinder":
            geometry = {
                'shape': 'cylinder',
                'r': self.spin_r.value(),
                'h': self.spin_h.value()
            }
        else:
            geometry = {
                'shape': 'cuboid',
                'l': self.spin_l.value(),
                'b': self.spin_b.value(),
                'h': self.spin_t.value()
            }

        # --- Aperture ---
        form = self.combo_aperture_form.currentText()
        aperture_kwargs = {
            'form': form,
            'amount': int(self.spin_n.value()),
            'length': self.spin_L.value(),
            'inner_ending': self.combo_inner_ending.currentText(),
            'outer_ending': self.combo_outer_ending.currentText()
        }

        if form == 'tube':
            aperture_kwargs['radius'] = self.spin_r_open.value()
        elif form == 'slit':
            aperture_kwargs['width'] = self.spin_b_slit.value()
            aperture_kwargs['height'] = self.spin_l_slit.value()

        # --- Environmental Conditions ---
        conditions = {
            'temperature': self.spin_T.value(),
            'humidity': self.spin_H.value()
        }

        # Optional: Aperture-Objekt mit Traits validieren
        try:
            aperture = Aperture(**aperture_kwargs)
        except TraitError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid aperture configuration:\n{e}")
            return None

        return {
            'geometry': geometry,
            'aperture': aperture,
            'conditions': conditions
        }

