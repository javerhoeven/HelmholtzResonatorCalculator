from simulation import Simulation
from geometry import Geometry
from aperture import Aperture
from simulation_parameters import SimulationParameters
from simulation import Simulation
from resonator import Resonator
from medium import Medium


if __name__ == '__main__':
    """
    Create a demo absorber
    """

    # generate resonator
    l = .5
    b = .3
    h = .2
    form = 'cuboid'

    geom = Geometry(form, x=l, y=b, z=h)
    ap = Aperture('tube', 0.1, 0.02)
    # ap = Aperture('slit', 0.01, 0.5, width=0.02, height=0.5)
    resonator = Resonator(geom, ap)

    # specify simulation parameters
    temp = 20
    rel_humidity = 0.6

    medium = Medium(temp, rel_humidity=rel_humidity)
    sim_params = SimulationParameters(medium, values_per_octave=200)

    # run simulation
    simulation = Simulation(resonator=resonator, sim_params=sim_params)
    simulation.plot_absorbtion_area()




