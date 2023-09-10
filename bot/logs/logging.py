from loguru import logger
import toml

# Открытие конфига
with open('config.toml','r') as tml:
  config = toml.load(tml)
  
logger.add(f"logs.log", format="<{level}> {time} - {message}", rotation="10MB", compression="zip")
