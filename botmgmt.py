import os
import toml
from console.main import cli
from console.cmd_make_config import make_config
if os.path.exists('config.toml'):
    from console.cmd_init import init
    from console.cmds_bot_utils import *
    from console.cmds_modules_mgmt import *
    
    with open('config.toml','r') as tml:
        config = toml.load(tml)
    
    if os.path.exists(config['db-path']):
        from console.cmds_db import *




if __name__ == '__main__':
    cli()
    

