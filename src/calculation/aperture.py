from traits.api import HasTraits, Enum, Range, Float, Bool, TraitError, Union
from traitsui.api import View, Item, Group
import numpy as np
from numpy import pi

class Aperture(HasTraits):
    """
    Models the aperture of a Helmholtz resonator, either as a tube or a slit.

    Attributes:
        form (str): Shape of the aperture ('tube' or 'slit').
        length (float): Length of the aperture.
        radius (float): Radius for 'tube' form.
        width (float): Width for 'slit' form.
        height (float): Height for 'slit' form.
        amount (int): Number of apertures.
        inner_ending (str): Boundary condition inside ('open' or 'flange').
        outer_ending (str): Boundary condition outside ('open' or 'flange').
        additional_dampening (bool): Whether porous damping is used.
        xi (float): Damping coefficient (required if damping enabled).

        area (float): Computed cross-sectional area.
        inner_end_correction (float): End correction at inner boundary.
        outer_end_correction (float): End correction at outer boundary.
    """

    form = Enum('tube', 'slit')
    length = Range(0.001, 0.5)
    radius = Range(0.005, 1.0, value=None, allow_none=True)
    width = Range(0.001, 0.5, value=None, allow_none=True)
    height = Range(0.001, 0.5, value=None, allow_none=True)
    amount = Range(1, 100, 1)
    inner_ending = Enum('open', 'flange')
    outer_ending = Enum('flange', 'open')
    additional_dampening = Bool(False)
    xi = Union(None, Float)

    area = Float
    inner_end_correction = Float
    outer_end_correction = Float

    def __init__(self, **kwargs):
        """Initialize and validate aperture configuration."""
        super().__init__(**kwargs)
        self._validate_logical_dependencies()
        self._compute_area_and_corrections()

    def _validate_logical_dependencies(self):
        """Validates consistency of traits based on form and dampening."""
        if self.form == 'tube' and self.radius is None:
            raise TraitError("Radius required if form='tube'.")
        elif self.form == 'slit' and (self.width is None or self.height is None):
            raise TraitError("form='slit' requires width and height.")

        if self.additional_dampening and self.xi is None:
            raise TraitError("xi required if additional_dampening=True.")

    def _compute_area_and_corrections(self):
        """Computes the aperture area and end corrections."""
        if self.form == 'tube':
            self.area = pi * self.radius**2 * self.amount
            self.inner_end_correction = self.get_tube_correction(self.inner_ending)
            self.outer_end_correction = self.get_tube_correction(self.outer_ending)

        elif self.form == 'slit':
            self.area = self.width * self.height * self.amount
            self.radius = np.sqrt(self.area / pi)
            correction = self.get_slit_end_correction(self.width, self.height)
            self.inner_end_correction = correction
            self.outer_end_correction = correction
            self.radius = 0.5 * self.width

    def get_tube_correction(self, ending):
        """Returns the empirical end correction for a tube end.

        Args:
            ending (str): 'open' or 'flange'.

        Returns:
            float: End correction length.
        """
        if ending == 'open':
            return 0.6 * self.radius
        elif ending == 'flange':
            return 0.85 * self.radius
        else:
            raise ValueError("Invalid ending. Choose 'open' or 'flange'. ")

    def get_slit_end_correction(self, x: float, y: float) -> float:
        """
        Calculates end correction for slits using Mechel's formulation.

        Args:
            x (float): Width of slit.
            y (float): Height of slit.

        Returns:
            float: End correction length.
        """
        if x < y:
            a, b = 0.5 * x, 0.5 * y
        else:
            a, b = 0.5 * y, 0.5 * x

        beta = a / b
        delta_l_a = 2 / (3 * pi) * (beta + (1 - (1 + beta**2)**(3/2)) / beta**2)
        delta_l_a += (2 / pi) * (1 / beta * np.log(beta + np.sqrt(1 + beta**2)) + np.log(1 / beta * (1 + np.sqrt(1 + beta**2))))
        return delta_l_a * a

    def to_dict(self):
        """Returns the aperture as a dictionary, including only relevant fields based on form."""
        base = {
            'form': self.form,
            'length': self.length,
            'amount': self.amount,
            'inner_ending': self.inner_ending,
            'outer_ending': self.outer_ending,
            'additional_dampening': self.additional_dampening,
            'xi': self.xi if self.additional_dampening else None,
            'area': self.area,
            'inner_end_correction': self.inner_end_correction,
            'outer_end_correction': self.outer_end_correction
        }

        if self.form == 'tube':
            base.update({'radius': self.radius})
        elif self.form == 'slit':
            base.update({'width': self.width, 'height': self.height})

        return base

    @classmethod
    def from_dict(cls, data):
        """Creates an Aperture instance from a dictionary."""
        return cls(
            form=data['form'],
            length=data['length'],
            radius=data.get('radius'),
            inner_ending=data.get('inner_ending', 'open'),
            outer_ending=data.get('outer_ending', 'flange'),
            additional_dampening=data.get('additional_dampening', False),
            xi=data.get('xi'),
            amount=data.get('amount', 1),
            width=data.get('width'),
            height=data.get('height')
        )

    # TraitsUI View
    traits_view = View(
        Group(
            Item('form', label="Form der Öffnung"),
            Item('length', label="Länge (m)"),
            Item('radius', label="Radius (m)", enabled_when='form == "tube"'),
            Item('width', label="Breite (m)", enabled_when='form == "slit"'),
            Item('height', label="Höhe (m)", enabled_when='form == "slit"'),
            Item('amount', label="Anzahl Öffnungen"),
        ),
        title="Aperture",
        buttons=['OK', 'Cancel'],
        resizable=True
    )

# Beispiel GUI starten
if __name__ == "__main__":
    aperture = Aperture(form='tube', length=0.1, radius=0.02, amount=1)
    aperture.configure_traits()
