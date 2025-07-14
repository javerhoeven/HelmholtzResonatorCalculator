import matplotlib.pyplot as plt
import numpy as np
from .simulation_parameters import SimulationParameters
from .resonator import Resonator

class Simulation():
    
 


    """
    Represents a full simulation of a Helmholtz resonator.

    This class performs acoustic simulations in relationship to geometric and physical properties, 
    including calculation of impedances, absorption behavior, resonance frequency, and Q-factor.

    Attributes:
        resonator (Resonator): The Helmholtz resonator configuration.
        sim_params (SimulationParameters): Frequency and medium parameters.
        z_porous (float): Additional impedance from porous damping.
        z_radiation (np.array): Radiation impedance across frequency range.
        z_stiff_mass (np.array): Stiffness and mass impedance.
        z_friction (np.array): Viscous (friction) impedance.
        k (np.array): Wavenumber.
        absorbtion_area (np.array): Resulting absorption area vs. frequency.
        absorbtion_area_diffuse (np.array): Not used currently.
        max_absorbtion_area (np.array): Theoretical maximum absorption area.
        q_factor (float): Calculated Q-factor.
        f_q_low (float): Lower -3 dB frequency point.
        f_q_high (float): Upper -3 dB frequency point.
        f_resonance (float): Calculated resonance frequency.
        peak_absorbtion_area (float): Max absorption at resonance.
    """

    def __init__(self, resonator: Resonator, sim_params: SimulationParameters):
        """
        Initialize a Simulation instance.

        Args:
            resonator (Resonator): The Helmholtz resonator object.
            sim_params (SimulationParameters): Frequency & medium configuration.
        """
        self.resonator = resonator
        self.sim_params = sim_params

        self.z_porous = None
        self.z_radiation = None
        self.z_stiff_mass = None
        self.z_friction = None
        self.k = self.sim_params.omega / self.sim_params.medium.c
        self.absorbtion_area = None
        self.absorbtion_area_diffuse = None
        self.max_absorbtion_area = None
        self.q_factor = None
        self.f_q_low = None
        self.f_q_high = None
        self.f_resonance = None
        self.peak_absorbtion_area = None

    def calc_all(self):
        """
        Convenience method to calculate absorption area, resonance frequency, and Q-factor in one step.
        """
        self.calc_absorbtion_area()
        self.calc_resonance_frequency_and_peak_area()
        self.calc_q_factor()

    def calc_z_porous(self) -> float:
        """
        Calculates the real-valued porous impedance for additional dampening.

        Returns:
            float: Porous impedance if enabled; 0 otherwise.
        """
        ap = self.resonator.aperture
        if ap.additional_dampening:
            S = ap.area
            l_ap = ap.length
            xi = ap.xi
            self.z_porous = xi * l_ap / S
        else:
            self.z_porous = 0
        return self.z_porous

    def calc_z_radiation(self) -> np.array:
        """
        Calculates the complex radiation impedance over frequency.

        Returns:
            np.array: Radiation impedance vector.
        """
        ap = self.resonator.aperture
        med = self.sim_params.medium
        rho = med.density
        c = med.c
        r = ap.radius
        k = self.sim_params.k
        delta_l_out = ap.outer_end_correction

        if ap.outer_ending == 'open':
            self.z_radiation = rho * c * (k**2 * r**2 / (4*np.pi) + 1j * k * delta_l_out)
        elif ap.outer_ending == 'flange':
            self.z_radiation = rho * c * (k**2 * r**2 / (2*np.pi) + 1j * k * delta_l_out)
        else:
            raise ValueError("Invalid outer ending. Choose 'open' or 'flange'.")
        return self.z_radiation

    def calc_z_stiff_mass(self) -> np.array:
        """
        Calculates the impedance contribution from stiffness and mass.

        Returns:
            np.array: Complex impedance vector.
        """
        ap = self.resonator.aperture
        rho = self.sim_params.medium.density
        c = self.sim_params.medium.c
        S = ap.area
        omega = self.sim_params.omega
        volume = self.resonator.geometry.volume
        l_ap = ap.length
        delta_l_total = ap.inner_end_correction + ap.outer_end_correction

        self.z_stiff_mass = rho * c**2 / (1j*omega*volume) + 1j*omega*rho*(l_ap + delta_l_total) / S
        return self.z_stiff_mass

    def calc_z_friction(self) -> np.array:
        """
        Calculates the real-valued friction impedance from viscosity.

        Returns:
            np.array: Friction impedance vector.
        """
        ap = self.resonator.aperture
        k = self.k
        r = ap.radius
        rho = self.sim_params.medium.density
        v = self.sim_params.medium.kinematic_viscosity
        f = self.sim_params.frequencies
        l_ap = ap.length
        S = ap.area

        limit = np.argwhere(k * r < 0.2)[-1, -1]
        z_friction_val = 8 * v * rho / r**2 * l_ap / S
        self.z_friction = np.full_like(f, z_friction_val)
        self.z_friction[limit+1:] = 0
        return self.z_friction

    def calc_absorbtion_area(self) -> np.array:
        """
        Computes the absorption area as a function of frequency.

        Returns:
            np.array: Absorption area vector.
        """
        self.calc_z_porous()
        self.calc_z_radiation()
        self.calc_z_stiff_mass()
        self.calc_z_friction()

        z_total = self.z_friction + self.z_porous + self.z_stiff_mass
        z_rad = self.z_radiation

        rho = self.sim_params.medium.density
        c = self.sim_params.medium.c
        theta = self.sim_params.angle_of_incidence

        if self.sim_params.assume_diffuse:
            self.absorbtion_area = 2 * (np.real(z_total) / np.abs(z_total + z_rad)**2) * (2 * rho * c)
        else:
            self.absorbtion_area = np.real(z_total) / np.abs(z_total + z_rad)**2 * (2 * rho * c / np.cos(theta))

        return self.absorbtion_area

    def calc_resonance_frequency_and_peak_area(self) -> float:
        """
        Determines the resonance frequency and peak absorption value.

        Returns:
            float: Resonance frequency.
        """
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()

        peak_idx = np.argmax(self.absorbtion_area)
        self.peak_absorbtion_area = self.absorbtion_area[peak_idx]
        self.f_resonance = self.sim_params.frequencies[peak_idx]
        return (self.f_resonance, self.peak_absorbtion_area)

    def calc_q_factor(self) -> float:
        """
        Calculates the Q factor from the -3 dB bandwidth.

        Returns:
            float: Quality factor (Q).
        """
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()

        curve = self.absorbtion_area
        freqs = self.sim_params.frequencies
        peak_idx = np.argmax(curve)
        f_res = freqs[peak_idx]
        peak = curve[peak_idx]
        half_peak = peak / 2

        diff = curve - half_peak
        idx = np.where(np.diff(np.sign(diff)))[0]

        try:
            i1, i2 = idx[0], idx[1]
        except IndexError:
            return None

        # Linear interpolation to find -3dB points
        f1 = freqs[i1] - diff[i1] * (freqs[i1+1] - freqs[i1]) / (diff[i1+1] - diff[i1])
        f2 = freqs[i2] - diff[i2] * (freqs[i2+1] - freqs[i2]) / (diff[i2+1] - diff[i2])

        self.f_q_low = f1
        self.f_q_high = f2
        self.q_factor = f_res / (f2 - f1)
        return self.q_factor

    def calc_max_absorbtion_area(self, plot: bool = True):
        """
        Calculates the theoretical maximum absorption area.

        Args:
            plot (bool): Whether to plot the curve.
        """
        self.max_absorbtion_area = self.sim_params.wavelength**2 / (2 * np.pi)
        if plot:
            plt.semilogx(self.sim_params.frequencies, self.max_absorbtion_area, linestyle=':')
            plt.grid()
            plt.title("Maximum Absorption Area")
            plt.show()

    def plot_absorbtion_area(self, ion: bool = False):
        """
        Plots the absorption area across the frequency range.

        Args:
            ion (bool): Whether to enable interactive plotting.
        """
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()
        if self.q_factor is None:
            self.calc_q_factor()

        if ion:
            plt.ion()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.semilogx(self.sim_params.frequencies, self.absorbtion_area)
        ax.axvline(self.f_q_low, linestyle=':')
        ax.axvline(self.f_q_high, linestyle=':')
        ax.set_title("Absorption Area of Helmholtz Resonator")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absorption Area (m²)")
        ax.grid(True, which='both', linestyle='--')
        plt.show()

    def to_dict(self):
        """
        Serializes the simulation and results into a dictionary.

        Returns:
            dict: Serialized simulation data.
        """
        return {
            "resonator": self.resonator.to_dict(),
            "simulation_parameters": self.sim_params.to_dict(),
            "z_porous": self.z_porous,
            "z_radiation_real": np.real(self.z_radiation).tolist() if self.z_radiation is not None else None,
            "z_radiation_imag": np.imag(self.z_radiation).tolist() if self.z_radiation is not None else None,
            "z_stiff_mass_real": np.real(self.z_stiff_mass).tolist() if self.z_stiff_mass is not None else None,
            "z_stiff_mass_imag": np.imag(self.z_stiff_mass).tolist() if self.z_stiff_mass is not None else None,
            "z_friction": self.z_friction.tolist() if self.z_friction is not None else None,
            "absorbtion_area": self.absorbtion_area.tolist() if self.absorbtion_area is not None else None,
            "max_absorbtion_area": self.max_absorbtion_area.tolist() if self.max_absorbtion_area is not None else None,
            "q_factor": self.q_factor
        }

    @classmethod
    def from_dict(cls, data):
        """
        Reconstructs a Simulation instance from dictionary data.

        Args:
            data (dict): Serialized simulation data.

        Returns:
            Simulation: Restored simulation instance.
        """
        resonator = Resonator.from_dict(data['resonator'])
        sim_params = SimulationParameters.from_dict(data['simulation_parameters'])

        sim = cls(resonator=resonator, sim_params=sim_params)
        sim.z_porous = data.get('z_porous')

        zr_real = data.get('z_radiation_real')
        zr_imag = data.get('z_radiation_imag')
        if zr_real and zr_imag:
            sim.z_radiation = np.array(zr_real) + 1j * np.array(zr_imag)

        zs_real = data.get('z_stiff_mass_real')
        zs_imag = data.get('z_stiff_mass_imag')
        if zs_real and zs_imag:
            sim.z_stiff_mass = np.array(zs_real) + 1j * np.array(zs_imag)

        sim.z_friction = np.array(data.get('z_friction')) if data.get('z_friction') else None
        sim.absorbtion_area = np.array(data.get('absorbtion_area')) if data.get('absorbtion_area') else None
        sim.max_absorbtion_area = np.array(data.get('max_absorbtion_area')) if data.get('max_absorbtion_area') else None
        sim.q_factor = data.get('q_factor')
        return sim
