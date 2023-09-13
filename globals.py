from fastapi import HTTPException
from logging.config import dictConfig
import logging
import graypy

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "debug-logger": {"handlers": ["default"], "level": "DEBUG"},
        "error-logger": {"handlers": ["default"], "level": "ERROR"},
        "info-logger": {"handlers": ["default"], "level": "INFO"}
    },
}
handler = graypy.GELFTLSHandler('192.168.8.51', 12201)
dictConfig(log_config) #enables logs

def logger(level:str, message:str):
    if level == "DEBUG":
        logger = logging.getLogger('debug-logger')
        logger.addHandler(handler)
        logger.debug(message)
    elif level == "ERROR":
        logger = logging.getLogger('error-logger')
        logger.addHandler(handler)
        logger.error(message)
        
    elif level == "INFO":
        logger = logging.getLogger('info-logger')
        logger.addHandler(handler)
        logger.info(message)
        
def raiseError(code:int, message:str):
    logger("ERROR", message)
    raise HTTPException(status_code=code, detail=message)