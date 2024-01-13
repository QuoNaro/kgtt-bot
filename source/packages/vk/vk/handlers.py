from typing import Iterable
from types import FunctionType
HANDLERS : list[FunctionType] = []

class Handlers:
  """Класс хэндлеров для бота
  """

  def state(*states: str) -> None:
    """Хэндлер срабатывает при определенном состоянии пользователя self.info.State
    """
    def inner(function):
      def wrapper(self):
        if self.info.State in states:
          return function(self)
        
      HANDLERS.append(wrapper)

      return wrapper
    return inner

  def message(*commands: str) -> None:
    """Хэндлер срабатывает при определенном сообщении пользователя self.message.text
    """
    def inner(function):
      def wrapper(self):
        if self.message.text in commands:
          return function(self)
      
      HANDLERS.append(wrapper)
     
      return wrapper
    return inner

  def multiply(commands : Iterable[str], states : Iterable[str]) -> None:
    """Хэндлер срабатывает при определенном сообщении и состоянии пользователя self.message.text и self.info.State"""
    def inner(function):
      def wrapper(self):
        if self.info.State in states and self.message.text in commands:
          return function(self)
        
      HANDLERS.append(wrapper)
      
      return wrapper
    return inner

  def empty(condition : str) -> None:
    """Пустой хэндлер с указанем своего условия для срабатывания"""
    def inner(function):
      def wrapper(self):
        if eval(condition):
          return function(self)
      
      HANDLERS.append(wrapper)
      
      return wrapper
    return inner
