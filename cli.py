"""
A commandline wrapper around the core code which performs multi-file backups.
"""


import sys
import click
from core import template_config, read_config, validate_user_input, backup_files


@click.group()
def cli():
    """
    Run a multi-backup, copying multiple files to a list of directories.
    """
    pass

@click.command()
@click.option("--config", default="./config.json", help="JSON configuration file")
def template(config):
    """
    Generate a template JSON configuration file. This file will contain a list
    of source files to be backed up to a list of destination directories.

    The template file can be modified with actual information that can be acted
    upon.

    Args:
        config_file_name: Name for the newly generated template JSON configuration file
    """
    template_config(config)
    sys.exit(0)

@click.command()
@click.option("--config", default="./config.json", help="JSON configuration file")
def backup(config):
    """
    Given a configuration file with files and directories, backup the files to the directories.

    Args:
        config: Optional configuration file, defaults to `config.json`
    """
    click.echo("Starting backup")
    valid, cfg = read_config(config)
    if not valid:
        click.echo("Invalid configuration file {}".format(config))
        sys.exit(1)
    valid, errors = validate_user_input(cfg["sources"], cfg["destinations"])
    if not valid:
        for error in errors:
            click.echo(error)
        sys.exit(1)
    backup_files(cfg["sources"], cfg["destinations"])
    click.echo("Backup complete")
    sys.exit(0)

cli.add_command(template)
cli.add_command(backup)
