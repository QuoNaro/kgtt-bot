import click
import os
from console.main import cli


@cli.command
def update():
    """Обновить программу"""
    os.system('git fetch')
    os.system('python install-requirements.py')

            


    