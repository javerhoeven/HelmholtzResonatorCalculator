from calculation import *


examples = {
    '01' : Resonator(
        Geometry('cuboid', x=0.5, y=0.3, z=0.2),
        Aperture('tube', 0.1, 0.05, additional_dampening=True, xi=50)),
    '02' : Resonator(
        Geometry('cuboid', x=1.0, y=0.6, z=0.4),
        Aperture('tube', 0.1, 0.05, additional_dampening=True, xi=12)),
    '03' : Resonator(
        Geometry('cuboid', x=0.8, y=0.5, z=0.3),
        Aperture('slit', 0.01, 0.5, width=0.02, height=0.5)),
    '04' : Resonator(
        Geometry('cylinder', radius=0.1, height=0.2),
        Aperture('tube', 0.05, 0.02, additional_dampening=True, xi=12)),
    '05' : Resonator(
        Geometry('cylinder', radius=0.15, height=0.25),
        Aperture('tube', 0.07, 0.03, additional_dampening=True, xi=20)),
    '06' : Resonator(
        Geometry('cuboid', x=0.6, y=0.4, z=0.3),
        Aperture('slit', 0.02, 0.6, width=0.03, height=0.6)),
    '07' : Resonator(
        Geometry('cylinder', radius=0.12, height=0.18),
        Aperture('tube', 0.06, 0.025, additional_dampening=True, xi=15)),
    '08' : Resonator(
        Geometry('cuboid', x=0.7, y=0.5, z=0.4),
        Aperture('slit', 0.015, 0.5, width=0.025, height=0.5)),
    '09' : Resonator(
        Geometry('cylinder', radius=0.08, height=0.22),
        Aperture('tube', 0.04, 0.02, additional_dampening=True, xi=10)),
    
}


def load_example(example : str) -> Simulation:
    """Load one of the examples and create a Simulation object with default simulation parameters.

    Args:
        example (str): Number of the example to load, e.g. '01', '02', etc.

    Returns:
        Simulation: Simulation object
    """

    resonator = examples.get(example)

    # Default Simulation Parameters
    medium = Medium()
    sim_params = SimulationParameters(medium=medium, values_per_octave=200)

    # create simulation object
    simulation = Simulation(resonator, sim_params)
    return simulation