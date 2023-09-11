import os
import toml

global_dir = os.path.dirname(__file__)
config_abspath = f'{global_dir}/config.toml'
if os.path.exists(config_abspath):
    with open(config_abspath,'r') as tml:
        config = toml.load(tml)
