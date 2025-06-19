from app_control import forward
from io_tools import load_from_json


if __name__ == '__main__':
   
    # forward({})

    sim = load_from_json('simulation_result.json')
    sim.plot_absorbtion_area()

