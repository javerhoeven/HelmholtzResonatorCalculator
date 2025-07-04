import json
from calculation import Simulation
def save_to_json(simulation: Simulation, file_path: str) -> None:
    """Save Simulation to JSON file.

    Args:
        simulation (Simulation): Simulation object to save.
        file_path (str): file path to save the JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(simulation.to_dict(), file, indent=4)