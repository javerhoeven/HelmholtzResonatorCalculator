from numpy import pi
class Aperture():
    def __init__(self, 
                form : str,
                length : float,
                radius : float,
                inner_ending : str = 'open',
                outer_ending : str = 'open',
                additional_dampening : bool = False,
                xi : float = None,
                amount : int = 1
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
        # TODO: does not do anything currently
        self.form = form
        self.length = length
        self.radius = radius
        self.inner_ending = inner_ending
        self.outer_ending = outer_ending
        self.additional_dampening = additional_dampening
        self.amount = amount
        self.xi = xi
        # TODO: add slits
        self.area = pi * self.radius**2 * amount
