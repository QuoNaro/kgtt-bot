from kgtt_bot.bot.main import kgtt
from kgtt_bot.vk import Bot
from kgtt_bot import dbutils
from kgtt_bot.bot.data import keyboards,states,emoji

from kgtt_bot.schedule import get_text

import json
from string import punctuation
import sqlite3


@kgtt.on.multiply(['Расписание'], [states.main])
def schedule(self : Bot):
    if self.info.UserGroup:
      try:
        request = self.db.cursor().execute(f"""SELECT json(Schedule) 
                                      FROM StudGroups 
                                      WHERE StudGroup = '{self.info.UserGroup}';""").fetchone()[0]
        schedule = get_text(json.loads(request))
        kgtt.utils.user_message(schedule)

      except sqlite3.OperationalError:
        kgtt.utils.user_message(f'Расписания для группы {self.info.UserGroup} не найдено!')
      
      except TypeError :
        kgtt.utils.user_message('Группа не найдена!')
      
      except IndexError:
        kgtt.utils.user_message('Группа не найдена!')

    else:
      dbutils.set_state(self, states.table_register)
      kgtt.utils.user_message('Введите свою учебную группу', keyboard = keyboards.cancel(), 
                            link=["https://clck.ru/psvfm"])


@kgtt.on.state(states.table_register)
def auth(self : Bot):
  
  def general_view(group : str) -> str:
    group = group.upper()
    for char in punctuation:
      group = group.replace(char,'')
      
    return group
    
    
  if self.message.text != emoji.red_circle:
    
    
    group = general_view(self.message.text)
    dbutils.update_field(self,table='UserGroups',category='UserGroup',new=group)
    dbutils.set_state(self,states.main)
    dbutils.on_mailing_status(self)
    kgtt.utils.user_message("Приятного использования! Рассылка включена!\nГруппу всегда можно поменять в параметрах"
                            , keyboard=keyboards.main())