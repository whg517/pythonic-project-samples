"""Command line"""
import click
from click import Context

from file2mongo import __version__
from file2mongo.config import settings
from file2mongo.exceptions import BaseError
from file2mongo.log import init_log
from file2mongo.transform import file_to_mongo


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    '-V',
    '--version',
    is_flag=True,
    help='Show version and exit.'
)  # If it's true, it will override `settings.VERBOSE`
@click.option('-v', '--verbose', is_flag=True, help='Show more info.')
@click.option(
    '--debug',
    is_flag=True,
    help='Enable debug.'
)  # If it's true, it will override `settings.DEBUG`
def main(ctx: Context, version: str, verbose: bool, debug: bool):
    """Main commands"""
    if version:
        click.echo(__version__)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    else:
        if verbose:
            settings.set('VERBOSE', True)
        if debug:
            settings.set('DEBUG', True)


@main.command()
def run():
    """Run command"""
    init_log()
    try:
        file_to_mongo()
    except BaseError as ex:
        click.echo(ex, err=True)
