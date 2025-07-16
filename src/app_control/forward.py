from calculation import Aperture, Geometry, Medium, Resonator, SimulationParameters, Simulation 
from io_tools import save_to_json

def forward(parameters : dict):
    """    
    calculates the absorbtion area and resonance frequency based on parameters provided by the GUI


    Args:
        parameters (dict): all required parameters. can be handed over from GUI or CLI
    """

    # Geometry parameters
    form = parameters['geometry']['shape']
    
    # for cuboid
    x = parameters['geometry'].get('l', None)
    y = parameters['geometry'].get('b', None)
    z = parameters['geometry'].get('h', None)

    # for cylinder
    radius = parameters['geometry'].get('radius', None)
    height = parameters['geometry'].get('height', None)
    # create Geometry instance
    geom = Geometry(form=form, x=x, y=y, z=z, radius=radius, height=height)

    # create Resonator instance
    resonator = Resonator(geom, parameters['aperture'])

    # specify simulation parameters
    temp = parameters['conditions']['temperature']
    rel_humidity = parameters['conditions']['humidity']

    medium = Medium(temperature_celsius=temp, rel_humidity=rel_humidity)
    sim_params = SimulationParameters(medium=medium, values_per_octave=500)

    # run simulation 
    simulation = Simulation(resonator=resonator, sim_params=sim_params)
    simulation.calc_all()
    return simulation
