from loguru import logger
import toml

# Открытие конфига
with open('~/.config/kgttbotconfig.toml','r') as tml:
  config = toml.load(tml)
  
logger.add(f"bot/logs.log", format="<{level}> {time} - {message}", rotation="10MB", compression="zip")
