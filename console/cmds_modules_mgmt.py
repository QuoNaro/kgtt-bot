import click
from pathlib import Path
import subprocess
from console.main import cli

    
@cli.group
def modules():
    """Управление модулями бота"""
    pass

@modules.command
@click.option('--env', prompt = "Интерпретатор",help = "Путь до интерпретатора python")
def init(env):
    unit_names = ('kgttbot','schedule_mailing')
    parrent_path = Path(__file__).parent.cwd()
    for name in unit_names:
        unit_content = f'''
[Unit]
Description = KGTT Bot module

[Service]
ExecStart = {env} {parrent_path}/{name}.py
Restart = always

[Install]
WantedBy = multi-user.target
    '''
        # Запись на в папку
        with open(f'{parrent_path}/{name}.service', 'w') as unit_file:
            unit_file.write(unit_content)   
    
        # Перемещение в unit-сервисы
        unit_dir = '/etc/systemd/system/'
        subprocess.call(['sudo','mv',f'{parrent_path}/{name}.service',unit_dir])
        
    # Перезагрузка демонов
    subprocess.call(['sudo', 'systemctl', 'daemon-reload'])

@modules.command()
@click.option('--schedule_mailing',is_flag = True)
@click.option('--bot',is_flag = True)
def enable(schedule_mailing,bot):
    if schedule_mailing:
        subprocess.call(['sudo', 'systemctl','enable','schedule_mailing.service'])
    
    if bot:
        subprocess.call(['sudo', 'systemctl','enable','kgttbot.service'])
    
@modules.command()
@click.option('--schedule_mailing',is_flag = True)
@click.option('--bot',is_flag = True)
def disable(schedule_mailing,bot):
    if schedule_mailing:
        subprocess.call(['sudo', 'systemctl','disable','schedule_mailing.service'])
    
    if bot:
        subprocess.call(['sudo', 'systemctl','disable','kgttbot.service'])
    
@modules.command()
@click.option('--schedule_mailing',is_flag = True)
@click.option('--bot',is_flag = True)
def start(schedule_mailing,bot):
    if schedule_mailing:
        subprocess.call(['sudo', 'systemctl','start','schedule_mailing.service'])
    
    if bot:
        subprocess.call(['sudo', 'systemctl','start','kgttbot.service'])

@modules.command()
@click.option('--schedule_mailing',is_flag = True)
@click.option('--bot',is_flag = True)
def restart(schedule_mailing,bot):
    if schedule_mailing:
        subprocess.call(['sudo', 'systemctl','restart','schedule_mailing.service'])
    
    if bot:
        subprocess.call(['sudo', 'systemctl','restart','kgttbot.service'])

@modules.command()
@click.option('--schedule_mailing',is_flag = True)
@click.option('--bot',is_flag = True)
def stop(schedule_mailing,bot):
    if schedule_mailing:
        subprocess.call(['sudo', 'systemctl','stop','schedule_mailing.service'])
    
    if bot:
        subprocess.call(['sudo', 'systemctl','stop','kgttbot.service'])
