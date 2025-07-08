from calculation import Simulation, SimulationParameters, Aperture, Geometry, Resonator, Medium
from scipy.optimize import minimize
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed


class Optimizer:
    """
    This class optimizes the geometry and aperture to achieve a target resonance frequency and Q factor.

    """

    def __init__(self, f_target, q_target):
        """
        Initialize the optimizer with target frequency and Q factor.

        Args:
            f_target (float): Target resonance frequency.
            q_target (float): Target Q factor.
        """
        self.f_target = f_target
        self.q_target = q_target

        self.best_results = []
        self.best_result = None

        self.bounds = [[]]

    # function to optimize
    def objective(self, vars):
        """This function is called by the optimizer to evaluate a Helmholtz simulation for the given parameters and returns a penalty for the deviation from the target resonance frequency and Q factor.

        Args:
            vars (list): geometry and aperture parameters in the order [x, y, z, radius, length, xi].
          

        Returns:
            float: penalized peak value of the simulation result, where a lower value is better.
        """
        x, y, z, radius, length, xi = vars

        f_target = self.f_target
        q_target = self.q_target

        # Create geometry and aperture
        geom = Geometry(form='cuboid', x=x, y=y, z=z)
        ap = Aperture(form='tube', radius=radius, length=length, additional_dampening=True, xi=xi)
        res = Resonator(geom, ap)

        # Define medium and simulation
        medium = Medium()
        freq_range = (f_target*0.001, f_target*10) # automatically set frequency range
        sim_params = SimulationParameters(medium=medium, freq_range=freq_range, values_per_octave=300) 
        sim = Simulation(res, sim_params)

        # Simulate and extract results
        f_res, peak_area = sim.calc_resonance_frequency_and_peak_area()
        q_factor = sim.calc_q_factor()
        
        try:
            # Penalize deviation from target f_res and Q
            f_weight = 1000 # weight of penalty
            f_penalty = np.abs(np.log10(f_res / f_target)) * f_weight

            q_weight = 500
            q_penalty = np.abs(np.log10(q_factor / q_target)) * q_weight
            
        except TypeError:
            return np.inf  # If Q factor is None, return a large penalty
        
        return -peak_area + f_penalty + q_penalty
    
    def run_single_optimization(self, x0):
        """tries to optimize the target parameters within the objective function

        Args:
            x0 (np.array): initial parameters
            bounds (list): value boundaries for each parameter
            f_target (float): target frequency
            q_target (float): target q-factor

        Returns:
            np.array: optimal parameters, None when optimization failed
        """
        try:
            res = minimize(
                self.objective,
                x0,
                method='SLSQP',
                bounds=self.bounds,
                options={'maxiter' : 100, 'disp' : False}
            )
            return res
        except Exception as e:
            return None
        
    def generate_initial_set(self):
        """Uses f_R approximation function to generate a set of plausible initial values. 

        """
        c = 343 # assume for approximation
        coeff = c / (2*np.pi)

        solve_for = np.random.choice(['x', 'y', 'z', 'radius', 'length'])

        x, y, z, radius, length, xi = [np.random.uniform(low, high) for (low, high) in self.bounds]
        xi = 50 # assume a fixed value for xi

        V = x*y*z
        S = np.pi*radius**2

        try:
            if solve_for == 'x':
                x = S / (y * z * length * (coeff / self.f_target)**2)
                x = np.clip(x, self.bounds[0][0], self.bounds[0][1])

            elif solve_for == 'y':
                y = S / (x * z * length * (coeff / self.f_target)**2)
                y = np.clip(y, self.bounds[1][0], self.bounds[1][1])

            elif solve_for == 'z':
                z = S / (x * y * length * (coeff / self.f_target)**2)
                z = np.clip(z, self.bounds[2][0], self.bounds[2][1])

            elif solve_for == 'radius':
                S = V * length * (coeff / self.f_target)**2
                radius = np.sqrt(S / np.pi)
                radius = np.clip(radius, self.bounds[3][0], self.bounds[3][1]) 
            elif solve_for == 'length':
                length = S / (V * (coeff / self.f_target)**2)
                length = np.clip(length, self.bounds[4][0], self.bounds[4][1])
        
        except Exception as e:
            print(f"Failed to solve for {solve_for}: {e}")
            return None 
        
        return [x, y, z, radius, length, xi]
    
    def search_optimal(self):
        """Call this function to start the optimization process. It will try to find the optimal geometry and aperture parameters that achieve the target resonance frequency and Q factor.

        """

        # TODO: adjust according to Tobis 
        # Bounds: [(min, max), ...] per parameter
        self.bounds = [
            (0.1, 1.0),  # x
            (0.1, 1.0),  # y
            (0.1, 1.0),  # z
            (0.01, 0.1),  # aperture radius
            (0.01, 0.3),   # aperture length
            (1, 5000)
        ]
        # initial_bounds = bounds.copy()
        # initial_bounds[-1] = [1, 1000]


        results = []
        num_trials = 200
        # create initial guesses, half informed, half random         
        initial_guesses = [self.generate_initial_set() for _ in range(num_trials//2)] # generate estimations for good results
        initial_guesses.extend([list([np.random.uniform(low, high) for (low, high) in self.bounds]) for _ in range(num_trials//2)]) # append completely random guesses

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.run_single_optimization, x0) for x0 in initial_guesses]

            for future in as_completed(futures):
                res = future.result()
                if res and res.success:
                    results.append(res)


        num_fails = num_trials - len(results)

        self.best_results = sorted(results, key=lambda r: r.fun)
        self.best_result = self.best_results[0]

        
        print(f"{num_fails} of {num_trials} inital guesses failed")
        
        # Result
        self.display_results(self.best_result)


    def display_results(self, result):
        """Displays the best result found by the optimizer. Prints out relevant information. 

        Args:
            best_result (_type_): best result found
            f_target (): target frequency
            q_target (_type_): target q-factor
        """
        x, y, z, radius, length, xi = result.x

        # reapply simulation
        medium = Medium()
        # freq_range = (self.f_target*0.001, self.f_target*100) # automatically set frequency range
        freq_range = (20, 1000)
        sim = Simulation(
            Resonator(Geometry(form='cuboid', x=x, y=y, z=z), 
                        Aperture(form='tube', radius=radius, length=length, additional_dampening=True, xi=xi)),
            SimulationParameters(medium=medium, freq_range=freq_range, values_per_octave=1000) 
        )

        (f_res, peak_area), q_factor = sim.calc_resonance_frequency_and_peak_area(),  sim.calc_q_factor()

        print("Optimal dimensions and aperture:")
        print(f"x={x:.3f} m, y={y:.3f} m, z={z:.3f} m")
        print(f"Aperture radius={radius:.3f} m, aperture length={length:.3f} m, damping with xi={xi:.3f}")
        print(f"Peak absorption at f_res = {f_res:.3f} Hz (target: {self.f_target}): {peak_area:.3f} m²")
        print(f"achieved Q-Factor: {q_factor:.3f} (target: {self.q_target})")
        print(f"achieved optimization value: {result.fun:.3f}")
        print(f"freq vector has {len(sim.sim_params.frequencies)} values")

        # plotting the result
        sim.plot_absorbtion_area()
