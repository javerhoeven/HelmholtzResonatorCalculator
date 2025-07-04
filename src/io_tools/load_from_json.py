import json
from calculation import Simulation

def load_from_json(file_path) -> Simulation:
    """Load Simulation from JSON file.

    Args:
        file_path (str): file path to the JSON file.

    Returns:
        Simulation: Simulation object with loaded data.
    """

    with open(file_path, 'r') as file:
        data = json.load(file)

    return Simulation.from_dict(data)
