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
        self.z_friction : np.array
        self.k = self.sim_params.omega / self.sim_params.medium.c
        self.absorbtion_area : np.array = None
        self.absorbtion_area_diffuse : np.array = None
        self.max_absorbtion_area : np.array = None

        
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
        k = self.k 
        r = ap.radius
        rho = self.sim_params.medium.density
        v = self.sim_params.medium.kinematic_viscosity
        f = self.sim_params.frequencies
        l_ap = ap.length
        S = ap.area
        # TODO: move this test to a separate validation test
        limit = np.argwhere(k*r < 0.5)[-1, -1] 
        print(f"k*r << 1 (k*r < 0.1) condition is met until {f[limit]} Hz.")
        print("Adjusting z_friction according to the condition. ")

        z_friction = 8 * v * rho / r**2 * l_ap / S
        z_friction_arr = np.full_like(f, z_friction)
        z_friction_arr[limit+1:] = 0 # set to zero for frequencies above kr<0.1
        self.z_friction = z_friction_arr
        

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

        # TODO: fix that logic --> should be two separate attributes for theta and diffuse
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
    
    def calc_max_absorbtion_area(self, plot : bool = True):
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

        if self.absorbtion_area is None:
            self.calc_absorbtion_area()

        plt.semilogx(self.sim_params.frequencies, self.absorbtion_area)
        # plt.axvline(self.resonance_frequency(), linestyle=':')
        plt.grid()
        plt.title("Absorbtion area of Helmholtz Resonator")
        plt.ylabel(f"Absorbtion area / m$^2$")
        plt.xlabel("Frequency / Hz")
        plt.show()

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