import click
import warnings
from app_control import optimizer, start_gui


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
@click.option('--freq', type=float, help="Target frequency where maximum absorbtion is desired.")
@click.option('--q_factor', type=float, help="Target Q-Factor (Bandwidth)")
def optimize(freq, q_factor):
    """
    Run optimization
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
    click.echo("Running optimizer...")
    optimizer(freq, q_factor)


if __name__ == "__main__":
    cli()