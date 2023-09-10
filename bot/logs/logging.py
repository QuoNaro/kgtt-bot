from loguru import logger
from config.cfg import current_dir
logger.add(f"{current_dir}/bot/logs/logs.log", format="<{level}> {time} - {message}", rotation="10MB", compression="zip")
