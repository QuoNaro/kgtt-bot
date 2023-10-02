
from io import BytesIO
from datetime import datetime,timezone,timedelta
from loguru import logger

from ruobr_student import RuobrCookies,RuobrParser,AuthorizationError,DateNotFoundError
from tiny_vk.utils import generate_keyboard
from bot.utils.verify import validate , check_ruobr_auth
from bot.main import bot
from bot.data import keyboards
from bot.data import states
from bot.data import emoji

year_period = lambda y : f'{y}-{int(y)+1}'

def string_month(date : str) -> str :
  data = datetime.strptime(date, "%m.%Y")
  num = data.month
  strm = ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'][num-1].lower()
  return f'{strm} {data.year}-го'
  

@bot.on.multiply(['Оценки'], [states.main])
def marks(self):
  if check_ruobr_auth(self.ruobr_login,self.ruobr_password):
    bot.db.set_state(states.marks)
    bot.utils.user_message('Напишите дату или выберите один из нескольких вариантов', keyboard =keyboards.marks())
  elif not self.ruobr_password and  not self.ruobr_login :
    bot.utils.user_message('Вы не авторизованы в Ruobr. Приступаем к регистрации!')
    bot.db.set_state(states.ruobr_register[0])
    bot.utils.user_message('Введите логин от Cabinet Ruobr', keyboard = keyboards.rcircle())

class Authentification():
  
  @bot.on.state(states.ruobr_register[0])
  def login_reg(self):
    if self.text != emoji.red_circle:
      bot.db.update_field(category='ruobr_tmp_login', new = self.text)
      bot.db.set_state(states.ruobr_register[1])
      bot.utils.user_message('Введите пароль от Cabinet Ruobr')
            
  @bot.on.state(states.ruobr_register[1])
  def password_reg(self):
    if self.text != emoji.red_circle:
      bot.db.update_field(category='ruobr_tmp_password',new = self.text)
      bot.db.set_state(states.ruobr_register[2])
      bot.utils.user_message(f'Отлично, всё верно ? {emoji.raised_smile}\nЛогин : {self.ruobr_tmp_login}\nПароль : {self.text}', keyboard = keyboards.selection())
  
  @bot.on.multiply([emoji.thumbs_up],[states.ruobr_register[2]])
  def positive(self):
    if self.text != emoji.red_circle:
      bot.utils.user_message(f'Проверка данных!\nПодождите пожалуйста...', keyboard = keyboards.selection())
      try:
        RuobrCookies(self.ruobr_tmp_login,self.ruobr_tmp_password)
        
        # Ставим значнеия логина и пароля
        bot.db.update_field(category="ruobr_login",new= self.ruobr_tmp_login)
        bot.db.update_field(category="ruobr_password",new =self.ruobr_tmp_password)

        bot.db.set_state(states.main)
        bot.utils.user_message(f'Данные успешно прошли проверку', keyboard = keyboards.main())
          
      except AuthorizationError:
        bot.db.set_state(states.ruobr_register[0])
        bot.utils.user_message(f'Логин или пароль не прошел проверку\nВведите логин от Ruobr :', keyboard = keyboards.rcircle())
  
  @bot.on.multiply([emoji.thumbs_down],[states.ruobr_register[2]],next_state=states.ruobr_register[0])
  def negative(self):
    bot.utils.user_message('Введите логин от Ruobr',keyboard=keyboards.rcircle())

class Excel():
  @bot.on.multiply(['Таблица оценок'],[states.marks],next_state=states.excel)
  def get_excel(self):
    current_student_year = datetime.now().year if 9 <= datetime.now().month <= 12 else datetime.now().year-1
    buttons = [(f"{current_student_year}","secondary"),None,(emoji.red_circle,"negative")]
    year_keyboard = generate_keyboard(*buttons)
    bot.utils.user_message(f'Введите год',keyboard=year_keyboard)


  @bot.on.state(states.excel)
  def ask_year(self):
    if self.text.isdigit() and len(self.text) == 4 and int(self.text) <= datetime.now().year:
      bot.utils.user_message(f'Ожидайте...')
      rp = RuobrParser(RuobrCookies(self.ruobr_login,self.ruobr_password))
      try:
        buffer = BytesIO()
        rp.excel(self.text).save(buffer)
        bot.db.set_state(states.marks)
        bot.utils.user_message(f'Файл с оценками за {year_period(self.text)}',file = {f'Оценки_{year_period(self.text)}.xlsx' : buffer},keyboard=keyboards.marks())
      except DateNotFoundError as e:
        bot.utils.user_message('Оценки отстутствуют!')
      except Exception as e:
        logger.exception(e)
        bot.utils.user_message('Произошла внутренняя ошибка, попробуйте позже')
    
    elif self.text == emoji.red_circle:
      pass
      
    else:
      bot.utils.user_message('Некорректная дата! Введите год')


@bot.on.multiply(['На сегодня'], [states.marks])
def now_today(self):
  current_date = datetime.now().strftime('%d.%m.%Y')
  try:
    rp = RuobrParser(RuobrCookies(self.ruobr_login,self.ruobr_password))
    last_marks = rp.marks().get_last()
    marks = [i for i in last_marks if i.date.strftime('%d.%m.%Y') == current_date]
    if not marks:
      raise DateNotFoundError
    text = '\n'.join([f'{i.subject}: {i.mark}' for i in marks])
    bot.utils.user_message(f'Оценки на {current_date} \n\n{text}')
  except DateNotFoundError:
    bot.utils.user_message('Оценки отстутствуют!')

@bot.on.multiply(['За месяц'], [states.marks])
def now_month(self):
  try:
    bot.utils.user_message(f'Ожидайте...')  
    current_date = datetime.now().strftime('%m.%Y')
    rp = RuobrParser(RuobrCookies(self.ruobr_login,self.ruobr_password))
    marks = rp.marks().get_average(current_date)
    bot.utils.user_message(f'Средние оценки за {string_month(current_date)} \n\n{marks}')
  except DateNotFoundError:
    bot.utils.user_message(f'Оценки отстутствуют!')
    
@bot.on.multiply(['За год'], [states.marks])
def now_year(self):
  try:
    bot.utils.user_message(f'Ожидайте...')  
    current_year = datetime.now().year if 9 >= datetime.now().month <= 12 else datetime.now().year()-1
    rp = RuobrParser(RuobrCookies(self.ruobr_login,self.ruobr_password))
    marks = rp.marks().get_average(str(current_year))
    bot.utils.user_message(f'Средние оценки за {year_period(current_year)} уч.год\n\n{marks}')
  except DateNotFoundError:
    bot.utils.user_message(f'Оценки отстутствуют!')
       
@bot.on.state(states.marks)
def date_checker(self):
  try:
    if validate(self.text, '%Y') and self.text != emoji.red_circle:
      rp = RuobrParser(RuobrCookies(self.ruobr_login,self.ruobr_password))
      marks = rp.marks().get_average(self.text)
      bot.utils.user_message(f'Средние оценки за {year_period(self.text)} год \n\n{marks}')
    elif validate(self.text, '%m.%Y'):
      rp = RuobrParser(RuobrCookies(self.ruobr_login,self.ruobr_password))
      marks = rp.marks().get_average(self.text)
      bot.utils.user_message(f'Средние оценки за {string_month(self.text)} \n\n{marks}')
    elif validate(self.text, '%d.%m.%Y'):
      rp = RuobrParser(RuobrCookies(self.ruobr_login,self.ruobr_password))
      marks = rp.marks().get_day_marks(self.text)
      bot.utils.user_message(f'Оценки на {self.text} \n\n{marks}')
  except DateNotFoundError :
    bot.utils.user_message('Оценки отстутствуют!')
  except Exception as e:
    logger.exception(e)
    bot.utils.user_message('Произошла внутренняя ошибка, попробуйте заново')
  