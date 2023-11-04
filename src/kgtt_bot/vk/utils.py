import vk_api
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard,VkKeyboardColor

from io import BytesIO
import requests
import json
import uuid

class Uploader:
  """Класс загрузки данных для сообщений
  """
  
  def __init__(self,__token : str,__id : int) -> None:
    self.__id = __id
    self.__vk = vk_api.VkApi(token=__token)
    
  @staticmethod
  def get_buffer(URI : str) -> BytesIO:
    from urllib.parse import urlparse
    parsed = urlparse(URI)
    if parsed.scheme and parsed.netloc:     
        request = requests.get(URI)
        buffer = BytesIO(request.content)
    elif isinstance(URI, BytesIO):
        buffer = URI
    else:
        with open(URI, 'rb') as f:
            buffer = BytesIO(f.read())
    return buffer
  
  @staticmethod
  def upload_link(URL : list) -> str :
    attachments = ''
    for link in URL:
      attachments+=f'link,{link},'
    return attachments
  
  def upload_doc(self, URI : dict[str,BytesIO]) -> str:
    attachments = ''
    vk = self.__vk.get_api()
    for title,buffer in URI.items():
      files = {'file': (f'{title}.xlsx', buffer.getvalue())}
      response = vk.docs.getMessagesUploadServer(type='doc', peer_id=self.__id)
      upload_url = response['upload_url']
      response = requests.post(upload_url, files=files).json()
      document = vk.docs.save(file=response['file'], title=title)
      owner_id=document['doc']['owner_id']
      media_id = document['doc']['id']
      attachments += f'doc{owner_id}_{media_id},'
    return attachments 
  
  def upload_photo(self,URI : list) -> str :
    attachments = ''
    upload = VkUpload(self.__vk)
    for uri in URI:
      photo = upload.photo_messages(photos=self.get_buffer(uri), peer_id=self.__id)[0]
      attachments += f'photo{photo["owner_id"]}_{photo["id"]},'
    return attachments
  
  def upload_voice(self,URI : str ) -> str :
    vk = self.__vk.get_api()
    upload_url = self.__vk.docs.getMessagesUploadServer(type='audio_message',peer_id=self.__id)['upload_url']
    files = {'file': (f'{str(uuid.uuid4())}.mp3', self.get_buffer(URI).getvalue())}
    result = json.loads(requests.post(upload_url, files=files).text)
    doc = vk.docs.save(file=result['file'])['audio_message']
    
    return f"doc{doc['owner_id']}_{doc['id']}_{doc['access_key']},"

class BotUtils:
  """Утилиты для бота
  """

  def __init__(self, __token : str, __id : int | str) -> None:
    self.__vk = vk_api.VkApi(token=__token)
    self.__id = __id
    self.uploader = Uploader(__token,__id)

  def user_message(self,__message : str = None , id : int | str = None, 
                  keyboard:dict = None,
                  link : list = None,
                  file : dict = None,
                  photo: list = None,
                  voice: str = None):
    
    if id is None:
      id = self.__id
    if id is None:
      raise ValueError("User id is not defined")
    
    attachments = ''
    
    if file :
      attachments += self.uploader.upload_doc(file)
    if photo : 
      attachments += self.uploader.upload_photo(photo)
    if voice : 
      attachments += self.uploader.upload_voice(voice)
    if link : 
      attachments += self.uploader.upload_link(link)
    
    self.__vk.method('messages.send',{
      'user_id': int(id),
      'message': __message,
      'random_id': 0,
      'keyboard' : keyboard,
      'attachment' : attachments
      })

  def chat_message(self,__message : str = None ,
                  id : int | str = None,
                  link : str = None,
                  file : dict = None,
                  photo: list = None,
                  voice: str = None
                  ):
    

    attachments = ''
    
    if file :
      attachments += self.uploader.upload_doc(file)
    if photo : 
      attachments += self.uploader.upload_photo(photo)
    if voice : 
      attachments += self.uploader.upload_voice(voice)
    if link : 
      attachments += self.uploader.upload_link(link)
    
    self.__vk.method('messages.send',{
      'chat_id': int(id),
      'message': __message,
      'random_id': 0,
      'attachment' : attachments})

def generate_keyboard(*args : tuple | str, one_time : bool = False) -> str:
  """Функция генерации клавиатуры

  Args:
      one_time (bool, optional): При True - клавиатура пропадает после нажатия на кнопку.

  Returns:
      str: Клавиатура для бота vk_api
  """
  
  keyboard = VkKeyboard(one_time=one_time)
  colors = {'positive': VkKeyboardColor.POSITIVE,
            'negative': VkKeyboardColor.NEGATIVE,
            'secondary': VkKeyboardColor.SECONDARY,
            'primary' : VkKeyboardColor.PRIMARY}
  
  for key in args:
    if isinstance(key,tuple | list):
      if len(key[0]) <= 40:
        label = key[0]
      else:
        label = key[0][:40]
      keyboard.add_button(label=label,color=colors[key[1]])
    elif key is None:
      keyboard.add_line()
  return keyboard.get_keyboard()

def user_message(__token : str,
                  __id : int,
                  __message : str,
                  keyboard:dict = None,
                  link : list = None,
                  file : dict = None,
                  photo: list = None,
                  voice: str = None) -> None:
    """Функция , отправки сообщения пользователю при помощи бота ВК

  Args:
      __token (str): Токен бота\n
      __id (int): ID пользователя\n
      __message (str): Сообщение для пользователя (не может быть пустым)\n
      keyboard (dict, optional): Клавиатура\n
      link (list, optional): Прикрепленная ссылка\n
      file (dict, optional): Прикрепленный файл\n
      photo (list, optional): Прикрепленное фото\n
      voice (str, optional): Прикрепленное аудио (Сообщение будет голосовым)
  """
  
    vk = vk_api.VkApi(token=__token)
    uploader = Uploader(__token,__id)
    
    attachments = ''
    if file :
      attachments += uploader.upload_doc(file)
    if photo : 
      attachments += uploader.upload_photo(photo)
    if voice : 
      attachments += uploader.upload_voice(voice)
    if link : 
      attachments += uploader.upload_link(link)
    
    vk.method('messages.send',{
      'user_id': int(__id),
      'message': __message,
      'random_id': 0,
      'keyboard' : keyboard,
      'attachment' : attachments
      })
