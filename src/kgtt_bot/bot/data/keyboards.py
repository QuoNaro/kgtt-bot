from vk_api.keyboard import VkKeyboard,VkKeyboardColor
from emoji import emojize

def selection():
  keyboard = VkKeyboard()
  keyboard.add_button(emojize(':thumbs_up:'), color=VkKeyboardColor.POSITIVE)
  keyboard.add_button(emojize(':thumbs_down:'), color=VkKeyboardColor.NEGATIVE)
  keyboard.add_line()
  keyboard.add_button(emojize(':hollow_red_circle:'),color=VkKeyboardColor.SECONDARY)
  return keyboard.get_keyboard()

def main():
    keyboard = VkKeyboard()
    keyboard.add_button("Расписание", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Оценки", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(emojize(':gear:'), color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def parameters():
  keyboard = VkKeyboard()
  keyboard.add_button("Изменить логин и пароль Ruobr", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button("Изменить объект", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button("Помощь", color=VkKeyboardColor.POSITIVE)
  keyboard.add_line()
  keyboard.add_button(emojize(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def marks():
  keyboard = VkKeyboard()
  keyboard.add_button("На сегодня", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("За месяц", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("За год", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button('Таблица оценок',color=VkKeyboardColor.POSITIVE)
  keyboard.add_line()
  keyboard.add_button(emojize(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def ok():
  keyboard = VkKeyboard()
  keyboard.add_button(emojize(':OK_button:'), color=VkKeyboardColor.POSITIVE)
  return keyboard.get_keyboard()

def cancel():
  keyboard = VkKeyboard()
  keyboard.add_button(emojize(':hollow_red_circle:'), color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def empty():
  VkKeyboard().get_empty_keyboard()

def excel():
  keyboard = VkKeyboard()
  keyboard.add_button('За этот учебный год',color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emojize(':hollow_red_circle:'), color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

