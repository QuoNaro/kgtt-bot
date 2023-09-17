import threading
import time

import vk_api
import vk_api.exceptions

from loguru import logger
from types import GeneratorType
from config import config,global_dir
from bot.utils.schedule import write_json,read_json,get_global_dictionary,TableParser,get_text
from tiny_vk.database import Database
from tiny_vk.utils import user_message


def get_vk_name(token : str,id):
  vk = vk_api.VkApi(token=token)
  user = vk.method("users.get", {"user_ids": id})
  fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
  return fullname
  
logger.add(f"{global_dir}/logs/schedule.log", level='INFO',format="<{level}> {time} - {message}", rotation="10MB", compression="zip")

class ScheduleMailing:
  
  def __init__(self) -> None:
    self.reload_time : int =  config['table-reload-time']
    

  def generator(self) -> GeneratorType:
    """Генерирует json объекты (старый и новый)"""
    while True:
      tp = TableParser('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')
      old : dict = read_json(f'{global_dir}/{config["json-path"]}')
      new : dict = get_global_dictionary(tp)
      yield (old,new)
      time.sleep(self.reload_time)

  def message_with_schedule(self) -> threading.Thread:
    try:
      text = get_text(self.new[self.group]).splitlines()
      text[0] = f'{text[0]} [Рассылка]'
      text = '\n'.join(text)
      user_message(config['token'],self.id,text)
    except vk_api.exceptions.ApiError as e:
      logger.exception(f"Ошибка доступа для {self.id} : {e}")

  def mailing(self):
    for user_id,group in self.database.get_mailing_ids('mail'):
      self.id = user_id
      self.group = group.lower()
      
      try:
        assert self.old[self.group] == self.new[self.group]
          
      except AssertionError:
        # Запускаем поток для отправки рассылки пользователю
        threading.Thread(target=self.message_with_schedule).start()
      except KeyError as ke:
        
        logger.info(f"Группа {self.group} для {self.id}({get_vk_name(config['token'],self.id)}) не найдена! Пропуск!\n{ke}")
      except Exception:
        pass

  def on(self):
    for old,new in self.generator():
      self.database = Database(f'{global_dir}/{config["db-path"]}','Users')
      self.old, self.new = old,new

      # Рассылка всем пользователям , подписавшимся на рассылку
      self.mailing()
      # Обновляем json
      write_json(f'{global_dir}/{config["json-path"]}', self.new)
      logger.info(f"Файл-расписание {global_dir}/{config['json-path']} обновлен!")
      