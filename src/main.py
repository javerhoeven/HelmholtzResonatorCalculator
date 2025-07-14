from app_control import forward, optimizer, start_gui
from io_tools import load_from_json, save_to_json, export_cad
from io_tools.examples import load_example, examples


# --- Hauptprogramm ---
if __name__ == '__main__':

    # start_gui()
    optimizer(300, 10)
