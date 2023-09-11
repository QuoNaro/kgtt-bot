from loguru import logger
logger.add(f"logs/logs.log", format="<{level}> {time} - {message}", rotation="10MB", compression="zip")
