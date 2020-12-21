"""Command line frontend"""

import click
from alembic.config import CommandLine

from example_blog import __version__
from example_blog.config import settings
from example_blog.server import Server


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-V', '--version', is_flag=True, help='Show version and exit.')
def main(ctx, version):
    if version:
        click.echo(__version__)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option('-h', '--host', show_default=True, help=f'Host IP. Default: {settings.HOST}')
@click.option('-p', '--port', show_default=True, help=f'Port. Default: {settings.PORT}')
@click.option('--level', help='Log level')
@click.option('--file', help='logfile')
def server(host, port, level, file):
    """Command pass config, if not None, it will pass settings, override config file."""
    kwargs = {
        'LOGLEVEL': level,
        'LOGFILE': file,
        'HOST': host,
        'PORT': port,
    }
    for name, value in kwargs.items():
        if value:
            settings.set(name, value)

    Server().run()


if __name__ == '__main__':
    main()
