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

        self.z_porous : float = None
        self.z_radiation : np.array = None
        self.z_stiff_mass : np.array = None
        self.z_friction : np.array = None
        self.k = self.sim_params.omega / self.sim_params.medium.c
        self.absorbtion_area : np.array = None
        self.absorbtion_area_diffuse : np.array = None
        self.max_absorbtion_area : np.array = None
        self.q_factor : float = None
        self.f_q_low : float = None
        self.f_q_high : float = None
        self.f_resonance : float = None
        self.peak_absorbtion_area : float = None

    def calc_all(self):
        """
        Calculates all relevant simulation attributes: absorbtion area, resonance frequency, peak_absorbtion_area, Q-factor
        """
        self.calc_absorbtion_area()
        self.calc_resonance_frequency_and_peak_area()
        self.calc_q_factor()
        

        
    def calc_z_porous(self) -> float:
        """
        calculates the real, frequency-invariant porous absorbtion 
        in case additional dampening material is used
        """
        ap = self.resonator.aperture
        if ap.additional_dampening == True:
            S = ap.area
            l_ap = ap.length
            xi = ap.xi
            self.z_porous = xi * l_ap / S
            return self.z_porous
        else:
            self.z_porous = 0
            # TODO: raise Error without crashing the program
            # raise ValueError("Dampening is not enabled.")

    def calc_z_radiation(self) -> np.array:
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
        # print(f"k*r < 0.5 condition is met until {f[limit]} Hz.")

        if ap.outer_ending == 'open':
            self.z_radiation = rho * c * (k**2 * r**2 / (4*np.pi) + 1j * k * delta_l_out)
            return self.z_radiation
        elif ap.outer_ending == 'flange':
            self.z_radiation = rho * c * (k**2 * r**2 / (2*np.pi) + 1j * k * delta_l_out)
            return self.z_radiation
        else:
            raise ValueError("Invalid outer ending. Choose 'open' or 'flange'.")
        
    def calc_z_stiff_mass(self) -> np.array:
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
      
        z_stiff_mass = rho * c**2 / (1j*omega*volume) + 1j*omega*rho*(l_ap+delta_l_in_out) / S
        self.z_stiff_mass = z_stiff_mass
        return z_stiff_mass

    def calc_z_friction(self) -> np.array:
        """
        calculate the real-valued viscosity loss
        """   
        ap = self.resonator.aperture
        k = self.k 
        r = ap.radius
        rho = self.sim_params.medium.density
        v = self.sim_params.medium.kinematic_viscosity
        f = self.sim_params.frequencies
        l_ap = ap.length
        S = ap.area
        # TODO: move this test to a separate validation test
        limit = np.argwhere(k*r < 0.2)[-1, -1] 
        # print(f"k*r << 1 (k*r < 0.2) condition is met until {f[limit]} Hz.")
        # print("Adjusting z_friction according to the condition. ")

        z_friction = 8 * v * rho / r**2 * l_ap / S
        z_friction_arr = np.full_like(f, z_friction)
        z_friction_arr[limit+1:] = 0 # set to zero for frequencies above kr<0.2
        self.z_friction = z_friction_arr
        return z_friction_arr
        

    def calc_absorbtion_area(self) -> np.array:
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

        # TODO: fix that logic --> should be two separate attributes for theta and diffuse
        if diffuse is False:
            # for specific angle of incidence theta
            self.absorbtion_area = np.real(z_reso) / (np.abs(z_reso + z_rad)**2) * (2*rho*c / np.cos(theta))
        else:
        
            # for diffuse sound 
            self.absorbtion_area = 2 * (np.real(z_reso) / (np.abs(z_reso + z_rad)**2) * (2*rho*c / np.cos(0)))

        return self.absorbtion_area

    def calc_resonance_frequency_and_peak_area(self) -> float:
        """returns the resonance frequency
        calculated as maximum of the absorbtion area

        Returns:
            float: resonance frequency
        """
        # check if absorbtion area exists
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()
        
        peak_idx = np.argmax(self.absorbtion_area)
        self.peak_absorbtion_area = self.absorbtion_area[peak_idx]
        f_res = self.sim_params.frequencies[peak_idx]
        self.f_resonance = f_res
        # print(f'Resonance Frequency at {f_res:.3f}')
        return (f_res, self.peak_absorbtion_area)
    
    def calc_q_factor(self) -> float:
        """
        calculates absorbtion area's Q factor

        Returns:
            float: Q-Factor
        """

        # check if absorbtion area exists
        if self.absorbtion_area is None:
            self.calc_absorbtion_area()

        curve = self.absorbtion_area
        freqs = self.sim_params.frequencies
        peak_idx = np.argmax(curve)
        f_res = freqs[peak_idx]
        peak = curve[peak_idx]

        half_peak = peak / 2
        # even with with resolution interpolation is needed
        diff = curve - half_peak
        sign_change_idc = np.where(np.diff(np.sign(diff)))[0]
        try:
            i1 = sign_change_idc[0]
            i2 = sign_change_idc[1]
        except IndexError:
            # print("-3 dB point out of frequency range. Cannot calculate Q factor.")
            return None

        # f1
        x0, x1 = freqs[i1], freqs[i1+1]
        y0, y1 = diff[i1], diff[i1+1]
        f1 = x0 - y0 * (x1 - x0) / (y1 - y0) # linear interpolation

        # f2
        x0, x1 = freqs[i2], freqs[i2+1]
        y0, y1 = diff[i2], diff[i2+1]
        f2 = x0 - y0 * (x1 - x0) / (y1 - y0) # linear interpolation

        bandwidth = f2-f1
        q_factor = f_res / bandwidth

        self.f_q_low = f1
        self.f_q_high = f2
        self.q_factor = q_factor
        return q_factor

    
    def calc_max_absorbtion_area(self, plot : bool = True):
        """
        calculates to theoretically maximum possible absorbtion area

        Args:
            plot (bool, optional): decides if the curve is plotted. Defaults to True.
        """
        max_absorbtion_area = self.sim_params._lambda**2/(2*np.pi)
        self.max_absorbtion_area = max_absorbtion_area
        if plot:
            plt.semilogx(self.sim_params.frequencies, max_absorbtion_area, linestyle=':')
            plt.grid()
            plt.title("maximum absorbtion area")
            plt.show()

    def plot_absorbtion_area(self):
        """
        Plots the absorbtion area over the frequency
        """
        from matplotlib.ticker import MultipleLocator

        if self.absorbtion_area is None:
            self.calc_absorbtion_area()
        if self.q_factor is None or self.f_q_low is None or self.f_q_high is None:
            self.calc_q_factor()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.semilogx(self.sim_params.frequencies, self.absorbtion_area)
        ax.axvline(self.f_q_low, linestyle=':') # -3 dB point left
        ax.axvline(self.f_q_high, linestyle=':') # -3 dB point right
        # xticks = list(range(20, 101, 10)) + list(range(200, 1001, 100))
        # ax.set_xticks(xticks)
        plt.title("Absorbtion area of Helmholtz Resonator")
        ax.set_ylabel(f"Absorbtion area / m$^2$")
        ax.set_xlabel("Frequency / Hz")

        # ticks
        # Define custom tick locations at 20, 30, ..., 100, 200, ...
        custom_ticks = list(range(20, 101, 10)) + list(range(200, 501, 100))
        ax.set_xticks(custom_ticks)

        # Format ticks as plain numbers
        # from matplotlib.ticker import ScalarFormatter
        # ax.get_xaxis().set_major_formatter(ScalarFormatter())
        # ax.tick_params(axis='x', which='major', labelrotation=45)

        # Enable grid on both major and minor ticks
        ax.grid(True, which='both', linestyle='--')
        return ax

    def to_dict(self):
        """Convert the simulation results to a dictionary representation."""
   
        # self.calc_all()
        return {
            "resonator": self.resonator.to_dict(),
            "simulation_parameters": self.sim_params.to_dict(),
            
            # Impedances
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
        """Creates a Simulation instance from a dictionary"""
        resonator = Resonator.from_dict(data['resonator'])
        sim_params = SimulationParameters.from_dict(data['simulation_parameters'])
        
        sim = cls(resonator=resonator, sim_params=sim_params)
        sim.z_porous = data.get('z_porous', 0.0) 

        # for complex impedances, check if real and imaginary parts are present
        if data['z_radiation_real'] is None or data['z_radiation_imag'] is None:
            sim.z_radiation = None
        else:
            sim.z_radiation = np.array(data.get('z_radiation_real', None)) + 1j * np.array(data.get('z_radiation_imag', None))

        if data['z_stiff_mass_real'] is None or data['z_stiff_mass_imag'] is None:
            sim.z_stiff_mass = None
        else:
            sim.z_stiff_mass = np.array(data.get('z_stiff_mass_real', None)) + 1j * np.array(data.get('z_stiff_mass_imag', None))

        sim.z_friction = data.get('z_friction', None)
        sim.absorbtion_area = np.array(data.get('absorbtion_area')) if data['absorbtion_area'] is not None else None

        sim.max_absorbtion_area = np.array(data.get('max_absorbtion_area')) if data['max_absorbtion_area'] is not None else None
        sim.q_factor = data.get('q_factor', None)

        return sim

    def plot_volume(self, center=(0, 0, 0), color='cyan', alpha=0.6, edge_color='black'):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        """
        plots the volume and the front face with the aperture
        """
        form = self.resonator.geometry.form

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        if form == 'cylinder':
            print("printing cylinders is not yet available!")
            pass

            
        elif form == 'cuboid':

            geom = self.resonator.geometry
            # Calculate half lengths for easier vertex definition
            hx = geom.x / 2
            hy = geom.y / 2
            hz = geom.z / 2

            # Define the 8 vertices of the cuboid relative to its center
            x_c, y_c, z_c = center
            vertices = np.array([
                [x_c - hx, y_c - hy, z_c - hz],  # 0
                [x_c + hx, y_c - hy, z_c - hz],  # 1
                [x_c + hx, y_c + hy, z_c - hz],  # 2
                [x_c - hx, y_c + hy, z_c - hz],  # 3
                [x_c - hx, y_c - hy, z_c + hz],  # 4
                [x_c + hx, y_c - hy, z_c + hz],  # 5
                [x_c + hx, y_c + hy, z_c + hz],  # 6
                [x_c - hx, y_c + hy, z_c + hz]   # 7
            ])

            # Define the 6 faces of the cuboid using vertex indices
            faces = [
                [vertices[0], vertices[1], vertices[2], vertices[3]], # Bottom face
                [vertices[4], vertices[5], vertices[6], vertices[7]], # Top face
                [vertices[0], vertices[1], vertices[5], vertices[4]], # Front face
                [vertices[2], vertices[3], vertices[7], vertices[6]], # Back face
                [vertices[0], vertices[3], vertices[7], vertices[4]], # Left face
                [vertices[1], vertices[2], vertices[6], vertices[5]]  # Right face
            ]

            ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors=edge_color, alpha=alpha))
            
            # Set limits for the axes
            ax.set_xlim([x_c - geom.x, x_c + geom.x])
            ax.set_ylim([y_c - geom.y, y_c + geom.y])
            ax.set_zlim([z_c - geom.z, z_c + geom.z])
            
            # Add labels
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_zlabel('Z-axis')

            # # Define Apertures
            # ap = self.resonator.aperture
            # if ap.form == 'tube':


            #     ap_pos = (x_c + hx, y_c, z_c) # shift x coordinate

            #     phi = np.linspace(0, 2*np.pi, 100)
            #     r = ap.radius
            #     x = np.full_like(phi, ap_pos[0])
            #     y = r * np.cos(phi) + ap_pos[1]
            #     z = r * np.sin(phi) + ap_pos[2]

            #     ax.plot(x, y, z, linewidth=1, color=edge_color)


                
            # else:
            #     print("currently, only tubes can be drawn!")

            
            plt.show()