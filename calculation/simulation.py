import matplotlib.pyplot as plt
import numpy as np
from .simulation_parameters import SimulationParameters
from .resonator import Resonator

class Simulation():
    def __init__(self,
                 resonator : Resonator,
                 sim_params : SimulationParameters):
        self.resonator = resonator
        self.sim_params = sim_params

        self.z_porous : float
        self.z_radiation : np.array
        self.z_stiff_mass : np.array
        self.z_friction : float
        self.k = self.sim_params.omega / self.sim_params.medium.c
        self.absorbtion_area : np.array = None

        
    def calc_z_porous(self):
        """
        calculates the real, frequency-invariant porous absorbtion 
        in case additional dampening material is used
        """
        # TODO: delete additional_dampening bool, just check if xi is none
        ap = self.resonator.aperture
        if ap.additional_dampening == True:
            S = ap.area
            l_ap = ap.length
            xi = ap.xi
            self.z_porous = xi * l_ap / S
        else:
            self.z_porous = 0
            # TODO: raise Error without crashing the program
            # raise ValueError("Dampening is not enabled.")

    def calc_z_radiation(self):
        """
        calculates complex, frequency-dependant acoustic radiation impedance ("Schallstrahlungsimpedanz")
        """
        
        ap = self.resonator.aperture
        med = self.sim_params.medium
        rho = med.density
        c = med.c
        r = ap.radius
        k = self.sim_params.k
        f = self.sim_params.frequencies
        delta_l_out = ap.outer_end_correction

        # check if requirement for equation is met
        limit = np.argwhere(k*r < 0.5)[-1]
        # TODO: move this test to beginning of simulation to immediately truncate all freq-related vectors
        print(f"k*r < 0.5 condition is met until {f[limit]} Hz.")

        if ap.outer_ending == 'open':
            self.z_radiation = rho * c * (k**2 * r**2 / (4*np.pi) + 1j * k * delta_l_out)
        elif ap.outer_ending == 'flange':
            self.z_radiation = rho * c * (k**2 * r**2 / (2*np.pi) + 1j * k * delta_l_out)
        else:
            raise ValueError("Invalid outer ending. Choose 'open' or 'flange'.")
        
    def calc_z_stiff_mass(self):
        """
        calculates impedance based on acoustic stiffness and mass.
        becomes zero at resonance frequency

        """

        ap = self.resonator.aperture
        rho = self.sim_params.medium.density
        c = self.sim_params.medium.c
        S = ap.area
        omega = self.sim_params.omega
        volume = self.resonator.geometry.volume
        l_ap = ap.length
        delta_l_in_out = ap.inner_end_correction + ap.outer_end_correction
      
        self.z_stiff_mass = rho * c**2 / (1j*omega*volume) + 1j*omega*rho*(l_ap+delta_l_in_out) / S

    def calc_z_friction(self):
        """
        calculate the real-valued viscosity loss
        """        
        ap = self.resonator.aperture
        # TODO: what if no radius is given (slit)? can i just use area / pi instead of r**2?
        r = ap.radius
        rho = self.sim_params.medium.density
        v = self.sim_params.medium.kinematic_viscosity
        l_ap = ap.length
        S = ap.area

        z_friction = 8 * v * rho / r**2 * l_ap / S
        # TODO: add Z_porous here?
        self.z_friction = z_friction
        

    def calc_absorbtion_area(self):
        """
        calculates the absorbtion area over a frequency vector
        """

        self.calc_z_porous()
        self.calc_z_radiation()
        self.calc_z_stiff_mass()
        self.calc_z_friction()

        z_reso = self.z_friction + self.z_porous + self.z_stiff_mass
        z_rad = self.z_radiation

        rho = self.sim_params.medium.density
        c = self.sim_params.medium.c
        theta = self.sim_params.angle_of_incidence

        diffuse = self.sim_params.assume_diffuse

        if diffuse is False:
            # for specific angle of incidence theta
            self.absorbtion_area = np.real(z_reso) / (np.abs(z_reso + z_rad)**2) * (2*rho*c / np.cos(theta))

        else:
            # for diffuse sound 
            self.absorbtion_area = 2 * (np.real(z_reso) / (np.abs(z_reso + z_rad)**2) * (2*rho*c / np.cos(0)))

    def resonance_frequency(self) -> float:
        """returns the resonance frequency
        calculated as maximum of the absorbtion area

        Returns:
            float: resonance frequency
        """
        # check if absorbtion area exists
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()
        
        f_res = self.sim_params.frequencies[np.argmax(self.absorbtion_area)]
        print(f'Resonance Frequency at {f_res}')
        return f_res
    def plot_absorbtion_area(self):
        """
        Plots the absorbtion area over the frequency
        """
        # TODO: make it look nice

        if self.absorbtion_area is None:
            self.calc_absorbtion_area()
        plt.semilogx(self.sim_params.frequencies, self.absorbtion_area)
        plt.grid()
        plt.title("Absorbtion area of Helmholtz Resonator")
        plt.show()