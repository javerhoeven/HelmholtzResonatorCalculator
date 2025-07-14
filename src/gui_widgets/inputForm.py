from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFileDialog, QPushButton, QDoubleSpinBox, QComboBox, QGroupBox, QFormLayout, QMessageBox, QCheckBox
)
from traits.api import TraitError
from calculation.aperture import Aperture
from io_tools.load_from_json import load_from_json

class InputForm(QWidget):
    """
    User interface component for inputting resonator configuration parameters.

    This form includes user inputs for:
    - Geometry (cylinder or cuboid)
    - Aperture (form, amount, dimensions, damping)
    - Boundary conditions (inner/outer endings)
    - Environmental conditions (temperature, humidity)
    - Loading configuration files (JSON)

    Attributes:
        result_view (ResultView): Reference to the result view for accessing selected axes.
    """

    def __init__(self) -> None:
        """
        Initialize the input form with all required widgets, tooltips, default values,
        layout logic, and initial visibility for geometry and aperture configuration.
        
        Args:
            None

        Returns:
            None
        """

        super().__init__()
        self.main_layout = QVBoxLayout()

        # === 1. GEOMETRY ===
        self.group_geometry = QGroupBox("Geometry")
        geo_layout = QFormLayout()

        self.combo_shape = QComboBox()
        self.combo_shape.addItems(["Cylinder", "Cuboid"])
        self.combo_shape.setToolTip("Select the shape of the resonator: cylindrical or cuboid.")
        self.combo_shape.currentTextChanged.connect(self.update_inputs)
        geo_layout.addRow("Form:", self.combo_shape)


        self.spin_r = QDoubleSpinBox(); self.spin_r.setPrefix("r = "); self.spin_r.setValue(0.1); self.spin_r.setSuffix(" m"); self.spin_r.setRange(0, 1e6)
        self.spin_h = QDoubleSpinBox(); self.spin_h.setPrefix("h = "); self.spin_h.setValue(0.2); self.spin_h.setSuffix(" m"); self.spin_h.setRange(0, 1e6)
        self.spin_l = QDoubleSpinBox(); self.spin_l.setPrefix("l = "); self.spin_l.setValue(0.2); self.spin_l.setSuffix(" m"); self.spin_l.setRange(0, 1e6)
        self.spin_b = QDoubleSpinBox(); self.spin_b.setPrefix("b = "); self.spin_b.setValue(0.1); self.spin_b.setSuffix(" m"); self.spin_b.setRange(0, 1e6)
        self.spin_t = QDoubleSpinBox(); self.spin_t.setPrefix("h = "); self.spin_t.setValue(0.05); self.spin_t.setSuffix(" m"); self.spin_t.setRange(0, 1e6)
        # Tool-Tipps:
        self.spin_r.setToolTip("Radius of the cylindrical resonator (m).")
        self.spin_h.setToolTip("Height of the cylindrical resonator (m).")
        self.spin_l.setToolTip("Length of the cuboid resonator (m).")
        self.spin_b.setToolTip("Width of the cuboid resonator (m).")
        self.spin_t.setToolTip("Height (or thickness) of the cuboid resonator (m).")

        geo_layout.addRow(self.spin_r)
        geo_layout.addRow(self.spin_h)
        geo_layout.addRow(self.spin_l)
        geo_layout.addRow(self.spin_b)
        geo_layout.addRow(self.spin_t)
        self.group_geometry.setLayout(geo_layout)
        self.main_layout.addWidget(self.group_geometry)

        # === 2. Aperture ===
        self.group_opening = QGroupBox("Aperture Properties")
        opening_layout = QFormLayout()

        self.add_damping_cb = QCheckBox("additional damping")
        self.spin_xi = QDoubleSpinBox(); self.spin_xi.setPrefix("xi = "); self.spin_xi.setValue(0); self.spin_xi.setSuffix(" Pa·s/m"); self.spin_xi.setRange(0, 1e6)
        self.spin_xi.setDisabled(True)
        self.add_damping_cb.stateChanged.connect(self.toggle_damping_input)

        opening_layout.addRow(self.add_damping_cb)
        opening_layout.addRow(self.spin_xi)


        self.combo_aperture_form = self.add_enum_combobox("Aperture form:", "form", opening_layout)
        self.combo_aperture_form.currentTextChanged.connect(self.update_opening)    

        self.spin_n = QDoubleSpinBox(); self.spin_n.setPrefix("n = "); self.spin_n.setValue(1); self.spin_n.setDecimals(0); self.spin_n.setRange(0, 1e6)
        self.spin_L = QDoubleSpinBox(); self.spin_L.setPrefix("L = "); self.spin_L.setValue(0.02); self.spin_L.setSuffix(" m"); self.spin_L.setRange(0, 1e6)
        self.spin_r_open = QDoubleSpinBox(); self.spin_r_open.setPrefix("r_open = "); self.spin_r_open.setValue(0.005); self.spin_r_open.setSuffix(" m"); self.spin_r_open.setRange(0, 1e6)
        self.spin_b_slit = QDoubleSpinBox(); self.spin_b_slit.setPrefix("b_slit = "); self.spin_b_slit.setValue(0.01); self.spin_b_slit.setSuffix(" m"); self.spin_b_slit.setRange(0, 1e6)
        self.spin_l_slit = QDoubleSpinBox(); self.spin_l_slit.setPrefix("l_slit = "); self.spin_l_slit.setValue(0.05); self.spin_l_slit.setSuffix(" m"); self.spin_l_slit.setRange(0, 1e6)
        # Tool-Tipps:
        self.add_damping_cb.setToolTip("Enable additional acoustic damping in the aperture.")
        self.spin_xi.setToolTip("Damping coefficient xi (Pa·s/m). Only used if additional damping is active.")
        self.combo_aperture_form.setToolTip("Geometric form of the aperture used in acoustic calculations (e.g. 'tube', 'slit').")
        self.spin_n.setToolTip("Number of openings in the resonator wall.")
        self.spin_L.setToolTip("Physical length of the aperture, often equal to the wall thickness (m).")
        self.spin_r_open.setToolTip("Radius of the circular aperture (m).")
        self.spin_b_slit.setToolTip("Width of the slit aperture (m).")
        self.spin_l_slit.setToolTip("Length of the slit aperture (m).")

        opening_layout.addRow(self.spin_n)
        opening_layout.addRow(self.spin_L)
        opening_layout.addRow(self.spin_r_open)
        opening_layout.addRow(self.spin_b_slit)
        opening_layout.addRow(self.spin_l_slit)
        self.group_opening.setLayout(opening_layout)
        self.main_layout.addWidget(self.group_opening)

        # === 3. ENDING ===
        self.group_endings = QGroupBox("Boundary Configuration")
        endings_layout = QFormLayout()
        self.combo_inner_ending = self.add_enum_combobox("Inner End:", "inner_ending", endings_layout)
        self.combo_outer_ending = self.add_enum_combobox("Outer End:", "outer_ending", endings_layout)
        # Tool-Tipps:
        self.combo_inner_ending.setToolTip("Type of inner boundary of the aperture (e.g. open or flanged).")
        self.combo_outer_ending.setToolTip("Type of outer boundary of the aperture (e.g. open or flanged).")

        self.group_endings.setLayout(endings_layout)
        self.main_layout.addWidget(self.group_endings)

        # === 4. ENVIRONMENTAL CONDITIONS ===
        self.group_conditions = QGroupBox("Environmental Conditions")
        cond_layout = QFormLayout()

        self.spin_T = QDoubleSpinBox()
        self.spin_T.setPrefix("T = "); self.spin_T.setValue(20); self.spin_T.setSuffix(" °C")
        self.spin_T.setMinimum(-273.15); self.spin_T.setMaximum(1e6); self.spin_T.setDecimals(2)

        self.spin_H = QDoubleSpinBox()
        self.spin_H.setPrefix("H = "); self.spin_H.setValue(50); self.spin_H.setSuffix(" %")
        self.spin_H.setRange(0.0, 100.0); self.spin_H.setDecimals(2)
        # Tool-Tipps:
        self.spin_T.setToolTip("Ambient temperature (°C).")
        self.spin_H.setToolTip("Relative humidity (%).")

        cond_layout.addRow(self.spin_T)
        cond_layout.addRow(self.spin_H)
        self.group_conditions.setLayout(cond_layout)
        self.main_layout.addWidget(self.group_conditions)

        # === 5. Load Configurations JSON Format ===
        self.button_load_json = QPushButton("Load Configuration (JSON)")
        self.button_load_json.clicked.connect(self.load_from_json_file)
        self.main_layout.addWidget(self.button_load_json)

        self.setLayout(self.main_layout)
        self.update_inputs("Cylinder")
        self.update_opening("tube")


    def toggle_damping_input(self, state: int) -> None:
        """
        Enable or disable the damping coefficient input based on the checkbox state.

        Args:
            state (int): Qt.Checked (2) oder Qt.Unchecked (0)

        Returns:
            None
        """

        self.spin_xi.setEnabled(state == 2)  # 2 = Qt.Checked

    def add_enum_combobox(self, label: str, trait_name: str, layout) -> QComboBox:
        """
        Create a QComboBox filled with enum values from a given trait.

        Args:
            label (str): Label shown next to the combobox.
            trait_name (str): Name of the trait to extract enum values from.
            layout (QFormLayout): Layout to which the row will be added.

        Returns:
            QComboBox: The created and populated combobox.
        """

        combo = QComboBox()
        values = Aperture().trait(trait_name).handler.values
        combo.addItems(values)
        layout.addRow(label, combo)
        return combo

    def update_inputs(self, shape: str) -> None:
        """
        Show or hide input fields depending on selected geometry shape.

        Args:
            shape (str): The selected shape ('Cylinder' or 'Cuboid').
        Returns:
            None
        """

        for w in [self.spin_r, self.spin_h, self.spin_l, self.spin_b, self.spin_t]:
            w.setVisible(False)
        if shape == "Cylinder":
            self.spin_r.setVisible(True); self.spin_h.setVisible(True)
        else:
            self.spin_l.setVisible(True); self.spin_b.setVisible(True); self.spin_t.setVisible(True)

    def update_opening(self, shape: str) -> None:
        """
        Show or hide aperture dimension inputs depending on aperture type.

        Args:
            shape (str): The selected aperture form ('tube' or 'slit').
        Returns:
            None
        """
        for w in [self.spin_r_open, self.spin_b_slit, self.spin_l_slit]:
            w.setVisible(False)
        if shape == "tube":
            self.spin_r_open.setVisible(True)
        else:
            self.spin_b_slit.setVisible(True); self.spin_l_slit.setVisible(True)

    def get_inputs(self) -> dict | None:
        """
        Collect and validate all user inputs to build the simulation input dictionary.

        Args:
            None

        Returns:
            dict | None: A dictionary with geometry, aperture, environmental, and plot parameters,
                         or None if input validation failed.
        """
        # --- Geometry ---
        if self.combo_shape.currentText() == "Cylinder":
            geometry = {
                'shape': 'cylinder',
                'radius': self.spin_r.value(),
                'height': self.spin_h.value()
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

        aperture_kwargs['additional_dampening'] = self.add_damping_cb.isChecked()

        # Nur setzen, wenn aktiviert
        if self.add_damping_cb.isChecked():
            aperture_kwargs['xi'] = self.spin_xi.value()



        # --- Environmental Conditions ---
        conditions = {
            'temperature': self.spin_T.value(),
            'humidity': self.spin_H.value() / 100 # Umwandlung von Prozent in Dezimal
        }

        # --- Plot Settings ---
        plot_settings = {
            'x_axis': self.result_view.combo_x.currentText(),
            'y_axis': self.result_view.combo_y.currentText()
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
            'conditions': conditions,
            'plot': plot_settings
        }


    def load_from_json_file(self) -> None:
        """
        Load simulation parameters from a JSON file and update all form fields accordingly.
        Args:
            None

        Returns:
            None
        """
        path, _ = QFileDialog.getOpenFileName(self, "Load JSON", "", "JSON Files (*.json)")
        if not path:
            return

        try:
            simulation = load_from_json(path)
            resonator = simulation.resonator
            aperture = resonator.aperture
            geometry = resonator.geometry
            medium = simulation.sim_params.medium

            # --- Geometry ---
            if geometry.form == 'cylinder':
                self.combo_shape.setCurrentText("Cylinder")
                self.spin_r.setValue(geometry.radius)
                self.spin_h.setValue(geometry.height)
            elif geometry.form == 'cuboid':
                self.combo_shape.setCurrentText("Cuboid")
                self.spin_l.setValue(geometry.x)
                self.spin_b.setValue(geometry.y)
                self.spin_t.setValue(geometry.z)

            # --- Aperture ---
            self.combo_aperture_form.setCurrentText(aperture.form)
            self.spin_n.setValue(aperture.amount)
            self.spin_L.setValue(aperture.length)
            self.combo_inner_ending.setCurrentText(aperture.inner_ending)
            self.combo_outer_ending.setCurrentText(aperture.outer_ending)

            if aperture.form == "tube":
                self.spin_r_open.setValue(aperture.radius)
            elif aperture.form == "slit":
                self.spin_b_slit.setValue(aperture.width)
                self.spin_l_slit.setValue(aperture.height)

            # --- Additional Damping ---
            self.add_damping_cb.setChecked(aperture.additional_dampening)
            self.spin_xi.setEnabled(aperture.additional_dampening)
            if aperture.additional_dampening:
                self.spin_xi.setValue(aperture.xi)

            # --- Conditions ---
            self.spin_T.setValue(medium.temperature_celsius)
            self.spin_H.setValue(medium.rel_humidity * 100)
            
           

            QMessageBox.information(self, "Success", "Settings loaded successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load settings:\n{e}")
