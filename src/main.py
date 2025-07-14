from PyQt6.QtWidgets import (QApplication)
from gui_widgets.mainWindow import MainWindow


from app_control import forward, optimizer
from io_tools import load_from_json, save_to_json, export_cad
from io_tools.examples import load_example, examples


# --- Hauptprogramm ---
if __name__ == '__main__':
    import sys 
    app = QApplication(sys.argv) 
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

    # for example in examples:
    #    print(f"Running example {example}")
    #    simulation = load_example(example)
    #    simulation.plot_absorbtion_area()
    #    simulation.calc_q_factor()


    
    # with warnings.catch_warnings():
    #     warnings.simplefilter("ignore", category=RuntimeWarning)
    #     save = 'TESTESTEST.json'
    #     best_sim = optimizer(200, 10)
    #     save_to_json(best_sim, save)

    # sim = load_example('01')
    # save_to_json(sim, 'example_01.json')
    # sim2 = load_from_json('example_01.json')
    # sim2.plot_absorbtion_area()
    # export_cad(sim2, 'example_01.stl')

    #pass