from calculation import *
from scipy.optimize import minimize
import numpy as np
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
    freq_range = [f_target*0.01, f_target*10] # automatically set frequency range
    sim_params = SimulationParameters(medium, freq_range=freq_range, values_per_octave=500) 
    sim = Simulation(res, sim_params)

    # Simulate and extract results
    f_res, peak_area, q_factor = sim.resonance_frequency(), sim.peak_absorbtion_area, sim.calc_q_factor()
    
    try:
        # Penalize deviation from target f_res and Q
        penalty = 100 * abs(f_res - f_target) + 50 * abs(q_factor - q_target)
    except TypeError:
        return np.inf  # If Q factor is None, return a large penalty
    
    return -peak_area + penalty


def inverse(f_target, q_target):
    # Initial guess for [x, y, z, radius, length, xi] in meters
    x0 = [0.3, 0.3, 0.3, 0.02, 0.05, 20]

    # Bounds: [(min, max), ...] per parameter
    bounds = [
        (0.1, 1.0),  # x
        (0.1, 1.0),  # y
        (0.1, 1.0),  # z
        (0.005, 0.1),  # aperture radius
        (0.01, 0.3),   # aperture length
        (1, 5000)
    ]

    best_result = None
    num_trials = 500

    # try multiple initial guesses
    fail_count = 0
    for _ in range(num_trials):
        # Random initial guess within bounds
        x0 = np.array([np.random.uniform(low, high) for (low, high) in bounds])

        try:
            res = minimize(
                objective,
                x0,
                args=(f_target, q_target),
                method='SLSQP',
                bounds=bounds,
                options={'maxiter': 100, 'disp': False}
            )

            if res.success:
                if best_result is None or res.fun < best_result.fun:
                    best_result = res
                else:
                    fail_count += 1

        except Exception as e:
            print(f"Optimization failed at one start: {e}")
    print(f"{fail_count} of {num_trials} inital guesses failed")
    # Result
    x, y, z, radius, length, xi = best_result.x

    # reapply simulation
    medium = Medium()
    freq_range = [f_target*0.01, f_target*100] # automatically set frequency range
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

    # plotting the result
    sim.plot_absorbtion_area()