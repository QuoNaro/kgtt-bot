import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType

from types import FunctionType
from threading import Thread
import sqlite3 as sql
import os

from .utils import BotUtils
from .handlers import Handlers, HANDLERS
from .infoclass import InfoClass

class Bot:
  
  def __init__(self,__token : str, database : str , on_startup : FunctionType = None, on_shutdown : FunctionType = None) -> None:
    self.__token = __token
    self.__vk = vk_api.VkApi(token=self.__token)
    self.__longpoll = VkLongPoll(self.__vk)
    
    # Действия при запуске бота
    self.__startup_func = on_startup
    # Действия при остановке бота
    self.__shutdown_func = on_shutdown
    
    self.message : self.__longpoll.DEFAULT_EVENT_CLASS
    
    self.on = Handlers
    self.__db_path = database
    self.db = sql.connect(database,check_same_thread=False,)
    self.db.cursor().execute('''PRAGMA foreign_keys = ON;''')
  
  def __new_user(self):
    user = self.__vk.method("users.get", {"user_ids": self.message.user_id})
    fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
    
    info = self.db.cursor().execute('SELECT * FROM Users WHERE UserID=?', (self.message.user_id, )).fetchone()
    if info is None:
      self.db.cursor().execute(f'INSERT INTO Users (UserID,UserName) VALUES ({self.message.user_id},"{fullname}");')
      self.db.cursor().execute(f'INSERT INTO UserInteraction (UserID) VALUES ({self.message.user_id});')
      self.db.cursor().execute(f'INSERT INTO Ruobr (UserID) VALUES ({self.message.user_id});')
      self.db.cursor().execute(f'INSERT INTO UserGroups (UserID) VALUES ({self.message.user_id});')
      self.db.commit()
      
    if not bool(self.info.UserName):
      self.db.cursor().execute(f'UPDATE Users SET UserName = "{fullname}" ;')  

  def __iteration(self):
    """Одна итерация бесконечного цикла прослушки"""
    
    # Инициализация утилит бота
    self.utils = BotUtils(self.__token,self.message.user_id)
    
    # Заполнение данных для новых пользователей
    self.__new_user()
    for handler in HANDLERS:
      handler(self)

  def __run(self) -> None:
    """Запуск бота"""
    for event in self.__longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        self.message = event
        
        # Инициализация информации из базы данных в виде аттрибутов класса 
        self.info = InfoClass(database=self.__db_path, ID=self.message.user_id).GetData()
        
        Thread(target=self.__iteration).start()
           
  def start(self):
    """Запуск бота"""

    on_startup = lambda  : print('Начало работы!') # noqa: E731
    on_shutdown = lambda : print('\nЗавершение работы!')  # noqa: E731
    
    try:
      # Стартовое сообщение
      os.system('cls' if os.name=='nt' else 'clear')
      self.__startup_func() if self.__startup_func else on_startup()
      
      ''''''
      self.__run()
      ''''''

    except KeyboardInterrupt:
      
      # Сообщение о завершении работы
      os.system('cls' if os.name=='nt' else 'clear')
      self.__shutdown_func() if self.__shutdown_func else on_shutdown()
