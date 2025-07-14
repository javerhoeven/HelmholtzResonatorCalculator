# Entire code with proper indentation
code = """
import matplotlib.pyplot as plt
import numpy as np
# from .simulation_parameters import SimulationParameters
# from .resonator import Resonator

class Simulation:
    \"\"\"
    A class to simulate the acoustic behavior of a Helmholtz resonator.

    This class models all relevant physical impedances (porous damping, 
    radiation, stiffness/mass, friction) and computes the resulting 
    absorption area, resonance frequency, and quality factor.
    \"\"\"

    def __init__(self, resonator, sim_params):
        \"\"\"
        Initializes the simulation with a resonator and simulation parameters.
        \"\"\"
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
        self.calc_absorbtion_area()
        self.calc_resonance_frequency_and_peak_area()
        self.calc_q_factor()

    def calc_z_porous(self):
        ap = self.resonator.aperture
        if ap.additional_dampening:
            S = ap.area
            l_ap = ap.length
            xi = ap.xi
            self.z_porous = xi * l_ap / S
        else:
            self.z_porous = 0
        return self.z_porous

    def calc_z_radiation(self):
        ap = self.resonator.aperture
        med = self.sim_params.medium
        rho = med.density
        c = med.c
        r = ap.radius
        k = self.sim_params.k
        f = self.sim_params.frequencies
        delta_l_out = ap.outer_end_correction

        limit = np.argwhere(k * r < 0.5)[-1]
        if ap.outer_ending == 'open':
            self.z_radiation = rho * c * (k**2 * r**2 / (4 * np.pi) + 1j * k * delta_l_out)
        elif ap.outer_ending == 'flange':
            self.z_radiation = rho * c * (k**2 * r**2 / (2 * np.pi) + 1j * k * delta_l_out)
        else:
            raise ValueError("Invalid outer ending. Choose 'open' or 'flange'.")
        return self.z_radiation

    def calc_z_friction(self):
        ap = self.resonator.aperture
        k = self.k 
        r = ap.radius
        rho = self.sim_params.medium.density
        v = self.sim_params.medium.kinematic_viscosity
        f = self.sim_params.frequencies
        l_ap = ap.length
        S = ap.area

        limit = np.argwhere(k * r < 0.2)[-1, -1]
        z_friction = 8 * v * rho / r**2 * l_ap / S
        z_friction_arr = np.full_like(f, z_friction)
        z_friction_arr[limit + 1:] = 0
        self.z_friction = z_friction_arr
        return z_friction_arr

    def calc_absorbtion_area(self):
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

        if not diffuse:
            self.absorbtion_area = np.real(z_reso) / (np.abs(z_reso + z_rad)**2) * (2 * rho * c / np.cos(theta))
        else:
            self.absorbtion_area = 2 * (np.real(z_reso) / (np.abs(z_reso + z_rad)**2) * (2 * rho * c / np.cos(0)))
        return self.absorbtion_area

    def calc_resonance_frequency_and_peak_area(self):
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()
        peak_idx = np.argmax(self.absorbtion_area)
        self.peak_absorbtion_area = self.absorbtion_area[peak_idx]
        f_res = self.sim_params.frequencies[peak_idx]
        self.f_resonance = f_res
        return f_res, self.peak_absorbtion_area

    def calc_q_factor(self):
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()

        curve = self.absorbtion_area
        freqs = self.sim_params.frequencies
        peak_idx = np.argmax(curve)
        f_res = freqs[peak_idx]
        peak = curve[peak_idx]

        half_peak = peak / 2
        diff = curve - half_peak
        sign_change_idc = np.where(np.diff(np.sign(diff)))[0]
        try:
            i1 = sign_change_idc[0]
            i2 = sign_change_idc[1]
        except IndexError:
            return None

        x0, x1 = freqs[i1], freqs[i1 + 1]
        y0, y1 = diff[i1], diff[i1 + 1]
        f1 = x0 - y0 * (x1 - x0) / (y1 - y0)

        x0, x1 = freqs[i2], freqs[i2 + 1]
        y0, y1 = diff[i2], diff[i2 + 1]
        f2 = x0 - y0 * (x1 - x0) / (y1 - y0)

        bandwidth = f2 - f1
        q_factor = f_res / bandwidth

        self.f_q_low = f1
        self.f_q_high = f2
        self.q_factor = q_factor
        return q_factor

    def calc_max_absorbtion_area(self, plot=True):
        max_absorbtion_area = self.sim_params._lambda**2 / (2 * np.pi)
        self.max_absorbtion_area = max_absorbtion_area
        if plot:
            plt.semilogx(self.sim_params.frequencies, max_absorbtion_area, linestyle=':')
            plt.grid()
            plt.title("maximum absorbtion area")
            plt.show()

    def plot_absorbtion_area(self):
        from matplotlib.ticker import MultipleLocator
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()
        if self.q_factor is None or self.f_q_low is None or self.f_q_high is None:
            self.calc_q_factor()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.semilogx(self.sim_params.frequencies, self.absorbtion_area)
        ax.axvline(self.f_q_low, linestyle=':')
        ax.axvline(self.f_q_high, linestyle=':')
        custom_ticks = list(range(20, 101, 10)) + list(range(200, 501, 100))
        ax.set_xticks(custom_ticks)
        ax.grid(True, which='both', linestyle='--')
        ax.set_ylabel("Absorbtion area / m$^2$")
        ax.set_xlabel("Frequency / Hz")
        plt.title("Absorbtion area of Helmholtz Resonator")
        return ax

    def to_dict(self):
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
            "q_factor": self.q_factor,
        }

    @classmethod
    def from_dict(cls, data):
        resonator = Resonator.from_dict(data['resonator'])
        sim_params = SimulationParameters.from_dict(data['simulation_parameters'])
        sim = cls(resonator=resonator, sim_params=sim_params)
        sim.z_porous = data.get('z_porous', 0.0) 
        if data['z_radiation_real'] is None or data['z_radiation_imag'] is None:
            sim.z_radiation = None
        else:
            sim.z_radiation = np.array(data['z_radiation_real']) + 1j * np.array(data['z_radiation_imag'])
        if data['z_stiff_mass_real'] is None or data['z_stiff_mass_imag'] is None:
            sim.z_stiff_mass = None
        else:
            sim.z_stiff_mass = np.array(data['z_stiff_mass_real']) + 1j * np.array(data['z_stiff_mass_imag'])
        sim.z_friction = np.array(data.get('z_friction')) if data.get('z_friction') is not None else None
        sim.absorbtion_area = np.array(data.get('absorbtion_area')) if data['absorbtion_area'] is not None else None
        sim.max_absorbtion_area = np.array(data.get('max_absorbtion_area')) if data['max_absorbtion_area'] is not None else None
        sim.q_factor = data.get('q_factor', None)
        return sim

    def plot_volume(self, center=(0, 0, 0), color='cyan', alpha=0.6, edge_color='black'):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        form = self.resonator.geometry.form
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        if form == 'cylinder':
            print("printing cylinders is not yet available!")
        elif form == 'cuboid':
            geom = self.resonator.geometry
            hx = geom.x / 2
            hy = geom.y / 2
            hz = geom.z / 2
            x_c, y_c, z_c = center
            vertices = np.array([
                [x_c - hx, y_c - hy, z_c - hz],
                [x_c + hx, y_c - hy, z_c - hz],
                [x_c + hx, y_c + hy, z_c - hz],
                [x_c - hx, y_c + hy, z_c - hz],
                [x_c - hx, y_c - hy, z_c + hz],
                [x_c + hx, y_c - hy, z_c + hz],
                [x_c + hx, y_c + hy, z_c + hz],
                [x_c - hx, y_c + hy, z_c + hz]
            ])
            faces = [
                [vertices[0], vertices[1], vertices[2], vertices[3]],
                [vertices[4], vertices[5], vertices[6], vertices[7]],
                [vertices[0], vertices[1], vertices[5], vertices[4]],
                [vertices[2], vertices[3], vertices[7], vertices[6]],
                [vertices[0], vertices[3], vertices[7], vertices[4]],
                [vertices[1], vertices[2], vertices[6], vertices[5]]
            ]
            ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors=edge_color, alpha=alpha))
            ax.set_xlim([x_c - geom.x, x_c + geom.x])
            ax.set_ylim([y_c - geom.y, y_c + geom.y])
            ax.set_zlim([z_c - geom.z, z_c + geom.z])
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_zlabel('Z-axis')
            plt.show()
"""

from ace_tools import display_dataframe_to_user
code[:1000]  # just a preview of the code content

