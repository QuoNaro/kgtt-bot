from dataclasses import make_dataclass,dataclass
import sqlite3 as sql

class InfoClass:
    """Класс с информацией из базы данных экземпляра класса Bot (self.info) 
    """
    def __get_tables_with_column(self):
        
        
        #  INSERT INTO UserGroups (UserID) VALUES (435170678);
        
        data = {}
        
        # Названия всех таблиц
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = tuple([i[0] for i in self.cursor.fetchall()])
        
        # Перебираем таблицы и проверяем, есть ли в них желаемая колонка
        for table_name in tables:
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns_name = tuple([column[1] for column in self.cursor.fetchall()])
            
            
            
            if 'UserID' in columns_name:
                self.cursor.execute(f'''SELECT * FROM {table_name} WHERE UserID = {self.ID} ''')
                columns_data = self.cursor.fetchall()
                if len(columns_data) != 0:
                    columns_data = columns_data[0]
                elif len(columns_data) == 0 : 
                    columns_data = [None for _ in range(len(columns_name))]
               
                for cn,cd in zip(columns_name,columns_data):
                    data[cn] = cd
        
        return data
                
    def __init__(self, database : str, ID : int) -> None:
        self.ID = ID
        # self.database = database.connection
        self.database = sql.connect(database)
        self.cursor = self.database.cursor()
        self.TABLES = self.__get_tables_with_column()
     
    def GetData(self) -> dataclass:
        db_dataclass = make_dataclass("Database", self.__get_tables_with_column().keys())
        return db_dataclass(**self.__get_tables_with_column())
