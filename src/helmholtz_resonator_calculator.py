import click
import warnings
from app_control import optimizer, start_gui
from io_tools import save_to_json


@click.group()
def cli():
    """
    Main CLI entry point of the project
    """
    pass

@cli.command()
def gui():
    """
    Starts the graphical user interface 
    """
    start_gui()


@cli.command()
@click.argument('freq', type=float)
@click.argument('q_factor', type=float)
@click.option('--save', type=str, help="If a path (string) is given, the results will be saved as a .json file.")
def optimize(freq, q_factor, save):
    """
    Run optimization
    """

    
        
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        click.echo("Running optimizer...")
        best_sim = optimizer(freq, q_factor)

    # check string
    if save:
        if save.endswith(".json"):
            print("Valid path provided!")
        else:
            print("Please make sure the file extension '.json' is part of your output path. ")
        save_to_json(best_sim, save)

    print(f"Successfully saved simulation object to {save}!")
    print("="*50)

    


if __name__ == "__main__":
    cli()