from app_control import forward, optimizer, start_gui
from io_tools import load_from_json, save_to_json, export_cad
from io_tools.examples import load_example, examples


# --- Hauptprogramm ---
if __name__ == '__main__':
    """
    This main function is for debugging purposes only. 
    The entry point for the command line interface (CLI) is in helmholtz_resonator_calculator.py.
    """

    start_gui()
    #optimizer(300, 5)
