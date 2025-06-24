from calculation import Aperture, Geometry, Medium, Resonator, SimulationParameters, Simulation 
from io_tools import save_to_json

def forward(parameters : dict):
    """    
    calculates the absorbtion area and resonance frequency based on given parameters


    Args:
        parameters (dict): all required parameters. can be handed over from GUI or CLI
    """

    
    # TODO: replace all dummy / example values with GUI data, as soo as it's here

    # generate resonator
    geom = Geometry('cuboid', x=.5, y=.3, z=.2)
    # geom = Geometry('cuboid', x=1., y=.6, z=.4)

    ap = Aperture('tube', 0.1, 0.05, additional_dampening=True, xi=50)
    # ap = Aperture('tube', 0.05, 0.02, additional_dampening=True, xi=12)
    # ap = Aperture('slit', 0.01, 0.5, width=0.02, height=0.5)
    resonator = Resonator(geom, ap)

    # specify simulation parameters
    temp = 20
    rel_humidity = 0.6

    medium = Medium(temp, rel_humidity)
    sim_params = SimulationParameters(medium, values_per_octave=200)

    # run simulation
    simulation = Simulation(resonator=resonator, sim_params=sim_params)
    simulation.plot_absorbtion_area()
    # print(simulation.resonance_frequency())
    # simulation.calc_max_absorbtion_area(plot=True)
    simulation.calc_q_factor()
    # save_to_json(simulation, 'simulation_result.json')
    
