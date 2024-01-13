from io import BytesIO
from datetime import datetime

from ruobr_student.exceptions import AuthorizationError,DateNotFoundError
from ruobr_student import RuobrCookies,RuobrParser

from start import kgtt
from data import keyboards,states,emoji
from vk import Bot, generate_keyboard,dbutils
class IncompleteProcessError(Exception):
  """Класс-исключение для обозначения незавершенных процессов"""

def year_period(year : str | int) -> str:
  """Функция, которая преобразует год в период формата : 2001-2002

  Args:
      year (str | int): Начальный год

  Returns:
      str: Период в формате «2001-2002»
  """
  return f'{year}-{int(year) + 1}'

def string_month(date : str) -> str :
  """Функция, которая преобразует дату в строку формата «Январь 2023-го»

  Args:
      date (str): Дата в формате «День.Месяц.Год - 01.01.2023»

  Returns:
      str: «Январь 2023-го»
  """
  data = datetime.strptime(date, "%m.%Y")
  num = data.month
  strm = ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'][num-1].lower()
  return f'{strm} {data.year}-го'
  

@kgtt.on.multiply(['Оценки'], [states.main])
def marks(self:Bot):
  if self.info.Password and self.info.Login:
    dbutils.set_state(self,states.marks)
    kgtt.utils.user_message('Оценки Cabinet Ruobr', keyboard =keyboards.marks())
  else:
    kgtt.utils.user_message('Вы не авторизованы в Cabinet Ruobr. Приступаем к авторизации!',link=['https://cabinet.ruobr.ru/login/'])
    dbutils.set_state(self,states.ruobr_register[0])
    kgtt.utils.user_message('Введите логин от Cabinet Ruobr', keyboard = keyboards.cancel())

class Authentification():
  
  @kgtt.on.state(states.ruobr_register[0])
  def login_reg(self:Bot):
    if self.message.text != emoji.red_circle:
      dbutils.update_field(self,table="Ruobr",category='LoginTmp', new = self.message.text)
      dbutils.set_state(self,states.ruobr_register[1])
      kgtt.utils.user_message('Введите пароль от Cabinet Ruobr')
            
  @kgtt.on.state(states.ruobr_register[1])
  def password_reg(self:Bot):
    if self.message.text != emoji.red_circle:
      dbutils.update_field(self,table="Ruobr",category='PasswordTmp', new = self.message.text)
      dbutils.set_state(self, states.ruobr_register[2])
      kgtt.utils.user_message(f'Отлично, всё верно ? {emoji.raised_smile}\nЛогин : {self.info.LoginTmp}\nПароль : {self.message.text}', keyboard = keyboards.selection())
  
  @kgtt.on.multiply([emoji.thumbs_up],[states.ruobr_register[2]])
  def positive(self:Bot):
    if self.message.text != emoji.red_circle:
      kgtt.utils.user_message('Проверка данных!\nПодождите пожалуйста...', keyboard = keyboards.selection())
      try:
        RuobrCookies(self.info.LoginTmp,self.info.PasswordTmp)
        
        # Ставим значнеия логина и пароля
        dbutils.update_field(self,table="Ruobr",category='Login', new = self.info.LoginTmp)
        dbutils.update_field(self,table="Ruobr",category='Password', new = self.info.PasswordTmp)
        dbutils.set_state(self, states.main)
        kgtt.utils.user_message('Данные успешно прошли проверку', keyboard = keyboards.main())
          
      except AuthorizationError:
        dbutils.set_state(self,states.ruobr_register[0])
        kgtt.utils.user_message('Логин или пароль не прошел проверку\nВведите логин от Ruobr :', keyboard = keyboards.cancel())
  
  @kgtt.on.multiply([emoji.thumbs_down],[states.ruobr_register[2]])
  def negative(self:Bot):
    dbutils.set_state(self, states.ruobr_register[0])
    kgtt.utils.user_message('Введите логин от Ruobr', keyboard=keyboards.cancel())

@kgtt.on.state(states.marks)
def date_checker(self:Bot):
  dbutils.update_field(self,'Ruobr','Processing',1)
  
  try:
    if self.info.Processing == 1:
      raise IncompleteProcessError
    # Проверка на кружок
    assert self.message.text != emoji.red_circle
    # Проверка , чтобыы текст не был равен таблице оценок
    assert self.message.text != 'Таблица оценок'
    now = datetime.now()
    kgtt.utils.user_message('Ожидайте...')
    
    
    
    cookies = RuobrCookies(self.info.Login,self.info.Password).cookies()
    rp = RuobrParser(cookies)
    
    match (self.message.text):
      case 'На сегодня' :
        date : str = now.strftime('%d.%m.%Y')
        marks = rp.marks().get_day_marks(date)
        text_for_message = f'Оценки на {date} \n\n{marks}'
      case 'За месяц' :
        date : str = now.strftime('%m.%Y')
        marks = rp.marks().get_average(date)
        text_for_message =f'Средние оценки за {string_month(date)} \n\n{marks}'
      case 'За год' :
        date : str = str(now.year if 12>= now.month >= 9 else now.year - 1)
        marks = rp.marks().get_average(date)
        text_for_message = f'Средние оценки за {year_period(date)} год \n\n{marks}'

    kgtt.utils.user_message(text_for_message)
    
    

  except AssertionError:
    pass
  
  except AuthorizationError:
    kgtt.utils.user_message('Ошибка авторизации в Cabinet Ruobr')
    dbutils.set_state(self,states.ruobr_register[0])
    kgtt.utils.user_message('Введите логин от Cabinet Ruobr', keyboard = keyboards.cancel())
  except DateNotFoundError:
    kgtt.utils.user_message('Оценки отстутствуют!')
    
  except IncompleteProcessError:
    kgtt.utils.user_message('Подождите завершения предыдущего запроса')
    
  except Exception:
    kgtt.utils.user_message('Произошла внутренняя ошибка, попробуйте позже')
    
  finally :
    dbutils.update_field(self,'Ruobr','Processing',0)
      
class Excel():
  @kgtt.on.multiply(['Таблица оценок'],[states.marks])
  def get_excel(self:Bot):
    current_student_year = datetime.now().year if 9 <= datetime.now().month <= 12 else datetime.now().year-1
    buttons = [(f"{current_student_year}","secondary"),None,(emoji.red_circle,"negative")]
    year_keyboard = generate_keyboard(*buttons)
    dbutils.set_state(self, states.excel)
    kgtt.utils.user_message('Введите год',keyboard=year_keyboard)

  @kgtt.on.state(states.excel)
  def ask_year(self:Bot):
    dbutils.update_field(self,'Ruobr','Processing',1)
    
    try:
      
      if self.info.Processing == 1:
        raise IncompleteProcessError
      
      if self.message.text.isdigit() and len(self.message.text) == 4 and int(self.message.text) <= datetime.now().year:
        kgtt.utils.user_message('Ожидайте...')
        cookies = RuobrCookies(self.info.Login,self.info.Password).cookies()
        rp = RuobrParser(cookies)
      
        buffer = BytesIO()
        rp.excel(self.message.text).save(buffer)
        dbutils.set_state(self,states.main)
        kgtt.utils.user_message(f'Файл с оценками за {year_period(self.message.text)}',file = {f'Оценки_{year_period(self.message.text)}.xlsx' : buffer},keyboard=keyboards.main())
      else:
        kgtt.utils.user_message('Некорректная дата! Введите год')
        
        
    except DateNotFoundError:
      kgtt.utils.user_message('Оценки отстутствуют!')
    
    except IncompleteProcessError:
      kgtt.utils.user_message('Подождите завершения предыдущего запроса')
      
    except Exception:
      kgtt.utils.user_message('Произошла внутренняя ошибка, попробуйте позже')
    
    finally:
      dbutils.update_field(self,'Ruobr','Processing',0)
    

    

