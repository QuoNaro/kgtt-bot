from green_box import Table,Matrix
import re
from datetime import datetime

from .exceptions import GroupNotFoundError , EmptyScheduleError



def validate(date_str : str , format : str) -> bool:
    "Проверка строки на соответствие формату даты"
    try:
        result = bool(datetime.strptime(date_str, format))
    except ValueError:
        result = False
    return result

def get_extra_index(table : list[list] ) -> tuple: 
    lesson = table[0][::2]
    lesson_2 = table[2][::2]
    return tuple([i for i,(l1,l2) in enumerate(zip(lesson,lesson_2)) if l1 and l2])

def get_eng_string(*args : list[str]) -> list:
    
    result_arrays = []
    for words in args:
      array = []
      for word in words:
        english_chars = ""
        word = str(word)
        for char in word:
          if char.isalpha() and char.isascii():
            english_chars += char
        array.append(english_chars)
      result_arrays.append(array)
    return result_arrays
  
def find_range(lst : list) -> tuple:
  first, last = None, None
  for i, s in enumerate(lst):
      if s != '':
          if first is None:
              first = i
          last = i
  return (first, last+1) if first is not None else (None, None)

def clean(input_strings :list[str], to_remove :list[str]) -> list[str]:
    result = []
    for string, dist_string in zip(input_strings,to_remove):
        low_string,low_dist = string.lower(),dist_string.lower()
        format_string = low_string.replace(low_dist,'')
        cut_key =len(format_string)
        result.append(string[:cut_key])
    return result

def void_indexes(lst : list) -> tuple:
    indexes = []
    for i,s in enumerate(lst):
        if s == '':
            indexes.append(i)
    return tuple(indexes)


class TableParser:
    """Класс для парсинга общих данных из таблицы с расписанием, 
    таких как заголовок таблицы, список групп и т. д."""
    def __init__(self, table_id: str ) -> None :
        self.primary_table : Matrix = Table(table_id,'студентам').columns()
        self.primary_table.remove_all_void()
        self.primary_table.replace_none('')
        self.primary_table.float_to_integer()
    
    def get_title(self) -> str:
        for string in self.primary_table[0]:
            if isinstance(string,str):
                split_str = string.split(' ')
                for word in split_str:
                    if validate(word, '%d.%m.%Y'):
                        return string
                    
    def get_date(self) -> str:
        split_str = self.get_title().split(' ')
        for word in split_str:
            if validate(word, '%d.%m.%Y'):
                return word
    
    def get_exception_groups(self) -> tuple[str] :
        """Возвращает список строк,содержащих названия групп-исключений 
        (Находятся в самом низу таблицы)."""
        exception_groups = []
        for column in self.primary_table:
            string_column = map(lambda x : str(x),column)
            string_from_column = ' '.join(string_column)
            result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_column)
            if not result:
                continue
            exception_groups.append(result[-1])
        return tuple(exception_groups)

    def get_groups(self) -> tuple[str]:
        string_from_table = ''
        for column in self.primary_table:
            string_column = map(lambda x : str(x),column)
            string_from_table+= ' '.join(string_column)
        result = re.findall(r'\S\w*-[\.А-Я-0-9]+', string_from_table)
        return tuple(result)

class Group:
    """Сортировщик данных таблицы для конкретной группы"""
    
    def __init__(self, tableparser : TableParser, group : str) -> None:
        self.tableparser = tableparser
        self.group = group
        self.extra_index = get_extra_index(self.table)
        
        if group not in self.tableparser.get_groups():
            raise GroupNotFoundError("Группа не найдена в таблице")
    
    @property
    def table(self) -> list[list[str]]:
        """
        Обрезка таблицы по выбранной группе\n
        :return: Обрезанная матрица
        """
        table = Matrix(self.tableparser.primary_table)
        primary_index = table.get_index(self.group)[0]

        
        def get_horizontal_keys() -> tuple[int]:
            """Ключи обрезки для таблицы"""
            main_column = table[primary_index]
            key_1 = main_column.index(self.group) + 1
            nums_column = table[0][key_1:]
            for index,value in enumerate(nums_column):
                
                bool_value = bool(value)
                next_bool_value = bool(nums_column[index+1])

                if bool_value + next_bool_value == 0:
                    return (key_1,key_1+index+1)
      
        def get_vertical_keys() -> tuple[int]:
            return (primary_index,primary_index+6)
        
        
        hk1,hk2 = get_horizontal_keys()
        vk1,vk2 = get_vertical_keys()
        for index,column in enumerate(table):
            table[index] = column[hk1:hk2]

        table = table[vk1:vk2]
        # Обрезка ненужных колонок
        

        if not [i for i in table if any(i)]:
            raise EmptyScheduleError("Нет расписания для данной группы")
        
        return table

    def get_lessons(self) -> list[str]:
        lesson = self.table[0][::2]
        lesson_2 = self.table[2][::2]
        
        less = []
        
        
        for l1,l2 in zip(lesson,lesson_2):
            tmp_list = [l1,l2]
            bool_list = list(map(lambda x: bool(x),tmp_list))
                
            if  all(bool_list):
                less.append(l1)
                less.append(l2)
                
            elif any(bool_list):
                index = bool_list.index(True)
                less.append(tmp_list[index])
                
            else : 
                less.append('')
           
                
        return less

    def get_teachers(self) -> list[str]:
        teachers = self.table[0][1::2]
        teachers_2 = self.table[2][1::2]

        teach = []
  
        for t1,t2 in zip(teachers,teachers_2):
            
            tmp_list = [t1,t2]
            bool_list = list(map(lambda x: bool(x),tmp_list))
         
            if all(bool_list):
                for ell in tmp_list:
                    teach.append(ell)
                
            
            elif any(bool_list):
                index = bool_list.index(True)
                teach.append(tmp_list[index])
            
            else :
                teach.append('')

           
        return teach

    def get_cabinets(self) -> list[str]:
        cabinets = self.table[4][::2]
        cabinets_2 = self.table[1][::2]
        cabinets_3 = self.table[3][::2]
        result = []
        
        for c1,c2,c3 in zip(cabinets,cabinets_2,cabinets_3):
            c1,c2,c3 = str(c1),str(c2),str(c3)
      
            if c1 == c2 == c3:
                result.append(c1)
                
            elif c2 and c3:
                result.append(c2)
                result.append(c3)
            
            elif c1:
                result.append(c1)
                
            elif c2 and not c3 :
                result.append(c2)
            
            elif c3 and not c2:
                result.append(c3)
                
        return result
        
    def get_numbers(self) -> list[str]:
        result = self.tableparser.primary_table[0][:]
        result = [str(i) for i in range(1, len(self.get_lessons()) + 1)]
        
        if (self.extra_index):
            for index in self.extra_index:
                result.insert(index+1,f'{result[index]}.2')
                result[index] = f'{result[index]}.1'
            
        return result

    def get_time(self) -> list[str]:
        time = ['08:30 - 10:00',
                    '10:10 - 11:40',
                    '11:50 - 13:20',
                    '13:30 - 15:00',
                    '15:10 - 16:40',
                    '16:45 - 18:15']
        
        if (self.extra_index):
            for index in self.extra_index:
                time.insert(index + 1, time[index])

        return time

    def get_distance(self) -> list[str]:
        # FIXME : При ближайшей возможности сжечь!
        
        def get_dist_cabinet():
            cabinets = self.table[4][::2]
            cabinets_2 = [""]+ self.table[4][1::2]
            return cabinets,cabinets_2
        
        distance = []
        for tmp_list in zip(*get_eng_string(self.get_lessons(),
                                             self.get_teachers(),
                                             self.get_cabinets(),
                                             *get_dist_cabinet()
                                             )):
            bool_list = list(map(lambda x: bool(x),tmp_list))
            if all(bool_list):
                for ell in tmp_list:
                    distance.append(ell)
                    
            
            elif any(bool_list):
                index = bool_list.index(True)
                distance.append(tmp_list[index])
                
            else :
                distance.append('')
                
        if len(distance) < len(self.get_lessons()):
            distance.append('')


        return distance
    
    def get_dictionary(self) -> dict[str, list[str]]:
        """Возвращает словарь, содержащий все данные для конкретной группы"""
        # FIXME : Доработать
        r1,r2 = find_range(self.get_lessons()) # Находим диапазон границ для обрезки
        dist = self.get_distance()[r1:r2]
        dictionary = {}
        
        
        dictionary = {
            'lessons' : clean(self.get_lessons()[r1:r2],dist),
            'teachers' : clean(self.get_teachers()[r1:r2],dist),
            'cabinets' : clean(self.get_cabinets()[r1:r2],dist),
            'distance' : list(map(lambda s: s.lower().capitalize() ,self.get_distance()[r1:r2])),
            'numbers' : self.get_numbers()[r1:r2],
            'time' : self.get_time()[r1:r2],
            'date' : self.tableparser.get_date()

        }
        return dictionary
        
def get_text(dictionary : dict, group : str = None) -> str :
    
    def get_format_string(formatting : dict, local_dictionary : dict) -> str:
        format_string = ''
        for key,value in formatting.items():
            
            if local_dictionary[key] == '':
                continue
            
            
            format_string += value.format(**local_dictionary)
            
        format_string += '\n'
        return format_string
        
    
    text = ''
    formatting ={'numbers' : '({numbers}) ',
                 'time' : '{time} ',
                 'cabinets' : '[{cabinets}]',
                 'distance' : ' -> {distance}',
                 'lessons' : ' \n{lessons}',
                 'teachers' : '\n -- {teachers} --',
                 
                 }
    

    # Каждая иттерация - одна строка
    try:
        for value in zip(*dictionary.values()):
            keys = dictionary.keys()
            local_dictionary = {k : v for k, v in zip(keys,value)}
            if len(void_indexes(local_dictionary.values())) > 2:
                continue
            text+= get_format_string(formatting,local_dictionary)
            text+= '\n'
    except AttributeError:
        raise GroupNotFoundError("Группа не найдена")
        
    date = dictionary['date']
    message = f'Расписание на {date}'
    if group :
        message += f"\nГруппа : {group}"
    message += f"\n\n\n{text}"

    return message
    