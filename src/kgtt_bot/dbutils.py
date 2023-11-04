"""Утилиты для работы с базой данных КГТТ бота"""
from .vk import Bot

def set_state(self : Bot, state : str) -> None:
    """Функция 

    Args:
        self (Bot): \n
        state (str): Принимает новое состояние пользователя
    """
    self.db.cursor().execute(f'''UPDATE UserInteraction 
                             SET State = "{state}" 
                             WHERE UserID = {self.message.user_id};''')
    self.db.commit()
    
def update_field(self : Bot, table : str ,category : str , new : str) -> None:
    self.db.cursor().execute(f'''UPDATE {table} 
                             SET {category} = "{new}" 
                             WHERE UserID = {self.message.user_id};''')
    self.db.commit()
    
def check_mailing_status(self : Bot) -> bool:
    try:
        request = self.db.cursor().execute(f'''SELECT Mail 
                                        FROM UserGroups 
                                        WHERE UserID = {self.message.user_id};''')
        status = request.fetchone()[0]
    except TypeError : 
        return False
    return bool(status)
    
def on_mailing_status(self : Bot) -> None:
    self.db.cursor().execute(f'''UPDATE UserGroups 
                             SET Mail = 1 
                             WHERE UserID = {self.message.user_id};''',) 
    self.db.commit()

def off_mailing_status(self : Bot) -> None:
    self.db.cursor().execute(f'''UPDATE UserGroups 
                             SET Mail = 0 
                             WHERE UserID = {self.message.user_id};''',) 
    self.db.commit()
    
def delete_user_information(self : Bot) -> None:
    self.db.cursor().execute('''PRAGMA foreign_keys = ON;''')
    self.db.cursor().execute(f'''DELETE 
                             FROM Users 
                             WHERE UserID = {self.message.user_id};''')
    self.db.commit()
    
def get_schedule(self : Bot):
    self.db.cursor().execute(f"""SELECT json(Schedule) 
                                FROM StudGroups 
                                WHERE StudGroup = '{self.info.UserGroup}';""").fetchone()[0]
