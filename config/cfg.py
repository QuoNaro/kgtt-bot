import os
import dotenv
current_dir = os.path.abspath(f'{__file__}/../..')
database_abs_path = f'{current_dir}/kgtt.db'

dotenv.load_dotenv(dotenv_path=f'{current_dir}/config/.env')
token = os.getenv("TOKEN")

event_reload_time = 2
tableid = ''

