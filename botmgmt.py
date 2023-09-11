import os
from console.main import cli
from console.cmd_make_config import make_config
from config import config_abspath,global_dir

if os.path.exists(config_abspath):
    from config import config
    from console.cmd_init import init
    from console.cmds_bot_utils import *
    from console.cmds_modules_mgmt import *

    if os.path.exists(f'{global_dir}/{config["db-path"]}'):
        from console.cmds_db import *




if __name__ == '__main__':
    cli()
    

