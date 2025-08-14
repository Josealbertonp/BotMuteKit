"""
Configuração de logging centralizada
"""
import logging
import os
from typing import Optional

def setup_logging(log_file: str = "bot.log", log_level: str = "INFO") -> logging.Logger:
    """
    Configura o sistema de logging do bot
    
    Args:
        log_file: Nome do arquivo de log
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("BotMuteKit")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger com o nome especificado
    
    Args:
        name: Nome do logger
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)
