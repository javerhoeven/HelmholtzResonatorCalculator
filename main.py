from app_control import forward
from io_tools import load_from_json
from io_tools.examples import load_example, examples


if __name__ == '__main__':
   
   for example in examples:
       print(f"Running example {example}")
       simulation = load_example(example)
       simulation.plot_absorbtion_area()
       simulation.calc_q_factor()
    #    simulation.calc_max_absorbtion_area(plot=True)
