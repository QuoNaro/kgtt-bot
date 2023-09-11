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
def init_systemd(env):
    unit_names = ('kgttbot','schedule_mailing')
    parrent_path = Path(__file__).parent.cwd()
    for name in unit_names:
        unit_content = f'''
[Unit]
Description = KGTT Bot module

[Service]
ExecStart = {env} {parrent_path}/start_{name}.py
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


@modules.command
@click.option('--env', prompt = "Интерпретатор",help = "Путь до интерпретатора python")
def init_supervisor(env):
    
    #Установка supervisor
    subprocess.call(['sudo', 'pip', 'install', 'supervisor'])
    unit_names = ('kgttbot','schedule_mailing')
    parrent_path = Path(__file__).parent.cwd()
    for name in unit_names:
        unit_content = f'''
        [program:{name}]
        command={env} {parrent_path}/start_{name}.py
        autostart=true
        autorestart=true'''
        # Запись в папку
        with open(f'{parrent_path}/{name}.conf', 'w') as unit_file:
            unit_file.write(unit_content)   
    
        # Перемещение в папку процессов supervisor
        supervisor_dir = '/etc/supervisor/conf.d/'
        subprocess.call(['sudo','mv',f'{parrent_path}/{name}.conf',supervisor_dir])
        
    # Перезагрузка демонов
    subprocess.call(['sudo', 'supervisorctl', 'daemon-reload'])


