import threading
import time

import vk_api
import vk_api.exceptions

from loguru import logger
from types import GeneratorType
from config import config
from bot.utils.schedule import write_json,read_json,get_global_dictionary,TableParser,get_text
from tiny_vk.database import Database
from tiny_vk.utils import user_message



logger.add(f"logs/schedule.log", level='INFO',format="<{level}> {time} - {message}", rotation="10MB", compression="zip")

class ScheduleMailing:
  
  def __init__(self) -> None:
    self.reload_time : int =  config['table-reload-time']
    self.database = Database(config['db-path'],'Users')
    self.tableparser = TableParser('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')

  def listener(self) -> GeneratorType:
    
    def get_old() -> dict:
      try:
        return read_json(config['json-path'])
      except Exception:
        return {}

    def get_new() -> dict:
      try:
        return get_global_dictionary(self.tableparser)
      except Exception:
        return {}

    while True:
      old : dict = get_old()
      new : dict = get_new()
      yield (old,new)
      time.sleep(self.reload_time)

  @staticmethod
  def thread_runner(user_id : int, group : str , new_json_file : dict):
    try:
      text = "[Изменения в расписании]\n"+get_text(new_json_file[group])
      user_message(config['token'],user_id,text)
    except vk_api.exceptions.ApiError as e:
      logger.exception(f"Ошибка доступа для {user_id} : {e}")

  def start(self):
    for old_json,new_json in self.listener():
      
      for user_id,group in self.database.get_mailing_ids('mail'):
        try:
          assert old_json[group] == new_json[group]
          
        except KeyError:
          logger.info(f"Группа {group} для {user_id} не найдена! Пропуск!")
          continue
        
        except AssertionError:
          threading.Thread(target=self.thread_runner,args=[user_id,group,new_json]).start()
        
        except Exception:
          continue
          
      write_json(config['json-path'], new_json)
      logger.info("Файл-расписание обновлен!")
      