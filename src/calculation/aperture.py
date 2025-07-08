from traits.api import HasTraits, Enum, Range, Float, Bool, TraitError
from traitsui.api import View, Item, Group
import numpy as np
from numpy import pi

class Aperture(HasTraits):
    form = Enum('tube', 'slit')

    length = Range(0.001, 0.5)  # must be positive
    radius = Range(0.005, 1.0, value=None, allow_none=True)  # only for 'tube'
    width = Range(0.001, 0.5, value=None, allow_none=True)  # only for 'slit'
    height = Range(0.001, 0.5, value=None, allow_none=True)  # only for 'slit'
    amount = Range(1, 100, 1)

    inner_ending = Enum('open', 'flange') # default = 'open'
    outer_ending = Enum('flange', 'open') # default = 'flange' because it is on the outer wall

    additional_dampening = Bool(False)
    xi = Float(None, allow_none=True)  # required, if additional_dampening=True

    # --- Berechnete Attribute ---
    area = Float
    inner_end_correction = Float
    outer_end_correction = Float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_logical_dependencies()
        self._compute_area_and_corrections()

    def _validate_logical_dependencies(self):
        # Formabhängige Pflichtfelder
        if self.form == 'tube':
            if self.radius is None:
                raise TraitError("Radius required if form='tube'.")
        elif self.form == 'slit':
            if self.width is None or self.height is None:
                raise TraitError("form='slit' requires width and height.")

        # damping vs. xi
        if self.additional_dampening and self.xi is None:
            raise TraitError("xi required if additional_dampening=True.")

    def _compute_area_and_corrections(self):
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
            # Optional: set radius as "virtual circle radius"
            self.radius = 0.5 * self.width
            
    def get_tube_correction(self, ending):
        if ending == 'open':
            return 0.6 * self.radius
        elif ending == 'flange':
            return 0.85 * self.radius
        else:
            raise ValueError("Invalid ending. Choose 'open' or 'flange'. ")

    
    def get_slit_end_correction(self, x : float, y : float) -> float:
        """
        Calculates the end correction after the 
        equation given in Mechel's "Formulas of Acoustics", p. 319 

        Args:
            x (float): width of slit
            y (float): height of slit
        """
        # lower value needs to be a
        if x < y:
            a = 0.5 * x
            b = 0.5 * y
        else:
            a = 0.5 * y
            b = 0.5 * x

        beta = a/b
        delta_l_a =  2/(3*pi) * (beta + (1- (1+beta**2)**(3/2)) / beta**2 ) + (2/pi) * (1/beta * np.log(beta+np.sqrt(1+beta**2)) + np.log(1/beta*(1+np.sqrt(1+beta**2))))
        delta_l = delta_l_a * a
        return delta_l


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
            base.update({
                'radius': self.radius
            })
        elif self.form == 'slit':
            base.update({
                'width': self.width,
                'height': self.height
            })

        return base

    
    @classmethod
    def from_dict(cls, data):
        """Creates an Aperture instance from a dictionary"""
        return cls(
            form=data['form'],
            length=data['length'],
            radius=data['radius'],
            inner_ending=data.get('inner_ending', 'open'),
            outer_ending=data.get('outer_ending', 'flange'),
            additional_dampening=data.get('additional_dampening', False),
            xi=data.get('xi', None),
            amount=data.get('amount', 1),
            width=data.get('width', None),
            height=data.get('height', None)
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