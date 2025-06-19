from calculation import *
from scipy.optimize import minimize
import numpy as np
"""
This function optimizes the geometry and aperture to achieve a target resonance frequency and Q factor.

"""
# TODO: make this into class
last_peak = {}
# Example wrapper function to optimize
def objective(vars, f_target, q_target):
    x, y, z, radius, length, xi = vars

    # Create geometry and aperture
    geom = Geometry('cuboid', x=x, y=y, z=z)
    ap = Aperture('tube', radius=radius, length=length, additional_dampening=True, xi=xi)
    res = Resonator(geom, ap)

    # Define medium and simulation
    medium = Medium()
    sim_params = SimulationParameters(medium, values_per_octave=200)
    sim = Simulation(res, sim_params)

    # Simulate and extract results
    f_res, peak_area, q_factor = sim.resonance_frequency(), sim.peak_absorbtion_area, sim.calc_q_factor()
    
    try:
        # Penalize deviation from target f_res and Q
        penalty = 100 * abs(f_res - f_target) + 10 * abs(q_factor - q_target)
    except TypeError:
        return np.inf  # If Q factor is None, return a large penalty
    
    last_peak['peak'] = peak_area
    return -peak_area + penalty


def inverse(f_target, q_target):
    # Initial guess for [x, y, z, radius, length, xi] in meters
    x0 = [0.3, 0.3, 0.3, 0.02, 0.05, 20]

    # Bounds: [(min, max), ...] per parameter
    bounds = [
        (0.1, 1.0),  # x
        (0.1, 1.0),  # y
        (0.1, 1.0),  # z
        (0.005, 0.05),  # aperture radius
        (0.01, 0.2),   # aperture length
        (1, 5000)
    ]

    res = minimize(
        objective,
        x0,
        args=(f_target, q_target),
        method='SLSQP',
        bounds=bounds,
        options={'maxiter': 100, 'disp': True}
    )

    # Result
    x, y, z, radius, length, xi = res.x
    peak_abs = last_peak.get('peak', None)

    print("Optimal dimensions and aperture:")
    print(f"x={x:.3f} m, y={y:.3f} m, z={z:.3f} m")
    print(f"Aperture radius={radius:.3f} m, aperture length={length:.3f} m, damping with xi={xi:.3f}")
    print(f"Peak absorption at f_res = {f_target} Hz: {peak_abs:.3f} m²")

    # plotting the result
    if res.success:
        Simulation(
            Resonator(Geometry('cuboid', x=x, y=y, z=z), 
                      Aperture('tube', radius=radius, length=length, additional_dampening=True, xi=xi)),
            SimulationParameters(Medium(), values_per_octave=200)
        ).plot_absorbtion_area()