from numpy import pi
import numpy as np
class Aperture():
    # TODO: use kwargs for all except form
    def __init__(self, 
                form : str,
                length : float,
                radius : float,
                inner_ending : str = 'open',
                outer_ending : str = 'flange',  # because it is on the outer wall
                additional_dampening : bool = False,
                xi : float = None,
                amount : int = 1,
                width : float = None, # in case of slit
                height : float = None, # in case of slit
                ):
        """Configures the aperture specs

        Args:
            form (str): can be 'round' or 'slit'. currently only 'round' supported
            length (float): length of the aperture
            radius (float): radius of the aperture (assuming it is round)
            inner_ending (str, optional): can be flange or open. Defaults to 'open'.
            outer_ending (str, optional): can be flange or open. Defaults to 'open'.
            additional_dampening (bool, optional): If additional dampening material is used in the aperture. Defaults to False.
            xi (float, optional): length-specific flow resistance of the dampening material . Defaults to None.
            amount (int, optional): number of apertures. all apertures must have same sizes. Defaults to 1.
        """
        self.form = form
        self.length = length
        self.radius = radius
        self.inner_ending = inner_ending
        self.outer_ending = outer_ending
        self.additional_dampening = additional_dampening
        self.amount = amount
        self.xi = xi

        if form == 'slit':
            # TODO: check if all values are available
            self.area = width*height*amount
            self.radius = np.sqrt(self.area/pi)
            
            end_correction = self.get_slit_end_correction(width, height)
            self.inner_end_correction = end_correction
            self.outer_end_correction = end_correction

        elif form == 'tube':
            self.area = pi * self.radius**2 * amount

            self.inner_end_correction = self.get_tube_correction(self.inner_ending)
            self.outer_end_correction = self.get_tube_correction(self.outer_ending)

        else:
            raise ValueError("Invalid form. Choose 'round' or 'slit'. ")
          

    def get_tube_correction(self, ending):
        if ending == 'open':
            return 0.6 * self.radius
        elif ending == 'flange':
            return 0.85 * self.radius
        else:
            raise ValueError("Invalid ending. Choose 'open' or 'flange'. ")

    
    def get_slit_end_correction(self, x : float, y : float) -> float:
        """Calculates the end correction after the 
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
