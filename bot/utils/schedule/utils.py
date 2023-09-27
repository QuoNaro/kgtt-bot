from datetime import datetime

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

def remove_chars(string : str ) -> str: 
    return string.replace('-','')
    
    

        
        
    
    
    