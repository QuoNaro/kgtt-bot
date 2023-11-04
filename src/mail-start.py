from kgtt_bot.schedule import ScheduleMailing
from config import config
if __name__ == '__main__':
    ScheduleMailing(config['token'],database=config['db-path'],reload_time= config['table-reload-time']).start()