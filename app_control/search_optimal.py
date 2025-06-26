from calculation import *
from scipy.optimize import minimize
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

"""
This function optimizes the geometry and aperture to achieve a target resonance frequency and Q factor.

"""
# TODO: make this into class

# wrapper function to optimize
def objective(vars, f_target, q_target):
    x, y, z, radius, length, xi = vars

    # Create geometry and aperture
    geom = Geometry('cuboid', x=x, y=y, z=z)
    ap = Aperture('tube', radius=radius, length=length, additional_dampening=True, xi=xi)
    res = Resonator(geom, ap)

    # Define medium and simulation
    medium = Medium()
    freq_range = [f_target*0.001, f_target*10] # automatically set frequency range
    sim_params = SimulationParameters(medium, freq_range=freq_range, values_per_octave=300) 
    sim = Simulation(res, sim_params)

    # Simulate and extract results
    f_res, peak_area, q_factor = sim.resonance_frequency(), sim.peak_absorbtion_area, sim.calc_q_factor()
    
    try:
        # Penalize deviation from target f_res and Q
        penalty = 100 * abs(f_res - f_target) + 50 * abs(q_factor - q_target)
    except TypeError:
        return np.inf  # If Q factor is None, return a large penalty
    
    return -peak_area + penalty

def run_single_optimization(x0, bounds, f_target, q_target):
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
            objective,
            x0,
            args=(f_target, q_target),
            method='SLSQP',
            bounds=bounds,
            options={'maxiter' : 100, 'disp' : False}
        )
        return res
    except Exception as e:
        return None


def generate_initial_set(f_target, bounds):
    """Uses f_R approximation function to generate a set of plausible initial values. 

    Args:
        f_target (float): target resonance frequency
        bounds (list): boundaries for initial guesses
    """
    c = 343 # TODO: get this from somewhere
    coeff = c / (2*np.pi)

    solve_for = np.random.choice(['x', 'y', 'z', 'radius', 'length'])

    x, y, z, radius, length, xi = [np.random.uniform(low, high) for (low, high) in bounds]
    xi = 500 # TODO

    V = x*y*z
    S = np.pi*radius**2

    try:
        if solve_for == 'x':
            x = S / (y * z * length * (coeff / f_target)**2)
            x = np.clip(x, bounds[0][0], bounds[0][1])

        elif solve_for == 'y':
            y = S / (x * z * length * (coeff / f_target)**2)
            y = np.clip(y, bounds[1][0], bounds[1][1])

        elif solve_for == 'z':
            z = S / (x * y * length * (coeff / f_target)**2)
            z = np.clip(z, bounds[2][0], bounds[2][1])

        elif solve_for == 'radius':
            S = V * length * (coeff / f_target)**2
            radius = np.sqrt(S / np.pi)
            radius = np.clip(radius, bounds[3][0], bounds[3][1]) 
        elif solve_for == 'length':
            length = S / (V * (coeff / f_target)**2)
            length = np.clip(length, bounds[4][0], bounds[4][1])
    
    except Exception as e:
        print(f"Failed to solve for {solve_for}: {e}")
        return None 
    
    return [x, y, z, radius, length, xi]
    
    

def search_optimal(f_target, q_target):

    # Bounds: [(min, max), ...] per parameter
    bounds = [
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
    num_trials = 1000
    
    # initial_guesses = [np.array([np.random.uniform(low, high) for (low, high) in initial_bounds]) for _ in range(num_trials)]
         
    initial_guesses = [generate_initial_set(f_target, bounds) for _ in range(num_trials//2)] # generate estimations for good results
    initial_guesses.extend([list([np.random.uniform(low, high) for (low, high) in bounds]) for _ in range(num_trials//2)]) # append completely random guesses

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_single_optimization, x0, bounds, f_target, q_target) for x0 in initial_guesses]

        for future in as_completed(futures):
            res = future.result()
            if res and res.success:
                results.append(res)


    num_fails = num_trials - len(results)

    sorted_results = sorted(results, key=lambda r: r.fun)
    best_result = sorted_results[0]

    
    print(f"{num_fails} of {num_trials} inital guesses failed")
    
    
    
    # Result
    x, y, z, radius, length, xi = best_result.x

    # reapply simulation
    medium = Medium()
    freq_range = [f_target*0.001, f_target*100] # automatically set frequency range
    sim = Simulation(
        Resonator(Geometry('cuboid', x=x, y=y, z=z), 
                    Aperture('tube', radius=radius, length=length, additional_dampening=True, xi=xi)),
        SimulationParameters(medium, freq_range=freq_range, values_per_octave=500) 
    )
    f_res, peak_area, q_factor = sim.resonance_frequency(), sim.peak_absorbtion_area, sim.calc_q_factor()

    print("Optimal dimensions and aperture:")
    print(f"x={x:.3f} m, y={y:.3f} m, z={z:.3f} m")
    print(f"Aperture radius={radius:.3f} m, aperture length={length:.3f} m, damping with xi={xi:.3f}")
    print(f"Peak absorption at f_res = {f_res:.3f} Hz (target: {f_target}): {peak_area:.3f} m²")
    print(f"achieved Q-Factor: {q_factor:.3f} (target: {q_target})")
    print(f"achieved optimization value: {best_result.fun:.3f}")
    print(f"freq vector has {len(sim.sim_params.frequencies)} values")

    # plotting the result
    sim.plot_absorbtion_area()