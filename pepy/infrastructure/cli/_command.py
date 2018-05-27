import click

from pepy.application.command import ImportDownloadsFile
from pepy.infrastructure import container


@click.group()
def cli():
    pass


@cli.command('import:downloads_file')
@click.option('--file', prompt=True, help='CSV file to import')
def import_downloads_file_action(file: str):
    click.echo('Importing file')
    with open(file, 'r') as file_content:
        cmd = ImportDownloadsFile(file_content)
        container.command_bus.publish(cmd)
