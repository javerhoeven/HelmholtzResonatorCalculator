from calculation import Aperture, Geometry, Medium, Resonator, SimulationParameters, Simulation 
import numpy as np
def compare_results():
    """This function compares results for the resonance frequency to the online calculators given in the SRS
    """

    geom = []
    ap = []
    sim_params = SimulationParameters(Medium(20, 0.6))

    # Lautsprechershop
    geom.append(Geometry('cuboid', x=1.2, y=.3, z=.3))
    ap.append(Aperture('tube', 0.14, 0.05))

    results = {
        'Lautsprechershop' : 31.5
    }

    
    for _geom, _ap in zip(geom, ap):
        _sim = Simulation(Resonator(_geom, _ap), sim_params)
        _sim.resonance_frequency()



if __name__ == '__main__':
    """
    Create a demo absorber
    """

    # generate resonator
    geom = Geometry('cuboid', x=.5, y=.3, z=.2)
    geom = Geometry('cuboid', x=1., y=.6, z=.4)

    ap = Aperture('tube', 0.05, 0.02)
    # ap = Aperture('tube', 0.05, 0.02, additional_dampening=True, xi=12)
    # ap = Aperture('slit', 0.01, 0.5, width=0.02, height=0.5)
    resonator = Resonator(geom, ap)

    # specify simulation parameters
    temp = 20
    rel_humidity = 0.6

    medium = Medium(temp, rel_humidity)
    sim_params = SimulationParameters(medium, values_per_octave=100)

    # run simulation
    simulation = Simulation(resonator=resonator, sim_params=sim_params)
    simulation.plot_absorbtion_area()
    print(simulation.resonance_frequency())
    # simulation.plot_volume()


