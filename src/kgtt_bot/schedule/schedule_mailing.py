import threading
import time
import sqlite3 as sql
import json

import vk_api
import vk_api.exceptions

from kgtt_bot.schedule import TableParser,get_text,Group
from kgtt_bot.vk import user_message


class ScheduleMailing:
  
  def __init__(self, __token : str, database : str, reload_time : int = 60) -> None:
    self.reload_time : int =  reload_time
    self.db = sql.connect(database)
    self.__token = __token
  
  def FillStudGroups(self,schedule : dict):
    self.db.cursor().execute("DELETE FROM StudGroups;")
    for key,value in schedule.items():
      self.db.cursor().execute("REPLACE INTO StudGroups (StudGroup, Schedule) VALUES (?,?)",(key,str(value)))
    self.db.commit()
  
  @staticmethod
  def get_new_json(tableparser : TableParser) -> dict[str,dict]:
    gd = {}
    for group in tableparser.get_groups():
      try:
        group_key = group.upper().replace('-','')
        gd[group_key] = Group(tableparser,group).get_dictionary()
      except Exception:
        gd[group_key] = None
    return gd

  def get_old_json(self,tableparser : TableParser) -> dict[str,dict]:
    gd = {}
    for group in tableparser.get_groups():
      try:
        group = group.upper().replace('-','')
        request = self.db.cursor().execute(f"""SELECT json(Schedule) 
                                      FROM StudGroups 
                                      WHERE StudGroup = '{group}';""").fetchone()[0]
        gd[group] = json.loads(request)
      except Exception:
        gd[group] = None
    return gd

  def get_dictionaries(self) -> tuple[dict]:
    """
Собирает словари\n
:param old: Собирает словарь из базы данных (Таблица - StudGroups)    
:param new: Собирает данные из Google Table техникума
    
    
    """
    while True:
      tp = TableParser('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')
      old : dict = self.get_old_json(tp)
      new : dict = self.get_new_json(tp)
      yield (old,new)
      time.sleep(self.reload_time)

  def message_with_schedule(self) -> None:
    try:
      text = get_text(self.new[self.group]).splitlines()
      text[0] = f'{text[0]} [Рассылка]'
      text = '\n'.join(text)
      user_message(self.__token, self.id,text)
    except vk_api.exceptions.ApiError:
      print('Ошибка отправки сообщения')

  def mailing(self):
    
    def get_mailing_list() -> tuple:
        request = self.db.cursor().execute("SELECT UserID, UserGroup FROM UserGroups WHERE Mail = 1;")
        return request.fetchall()
    
    MAILING_IDS : tuple = get_mailing_list()
    for user_id,group in MAILING_IDS:
      self.id = user_id
      self.group = group
      try:
        assert self.old[self.group] == self.new[self.group]
      except AssertionError:
        # Запускаем поток для отправки рассылки пользователю
        threading.Thread(target=self.message_with_schedule).start()
      except KeyError: 
        print(f'Группа --{self.group}-- не найдена в таблице')
        continue

  def start(self):
    for old, new in self.get_dictionaries():
      self.old, self.new = old,new
      # Рассылка всем пользователям , подписавшимся на рассылку
      self.mailing()
      self.FillStudGroups(self.get_new_json(TableParser('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU')))

        