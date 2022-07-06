# core mod
import logging

loggers = {}

def setLevel(level, type = 'default'):
  loggers[type].setLevel(level)

def debug(msg, type = 'default'):
  if type not in loggers:
    loggers[type] = logging.getLogger(type)

  logger = loggers[type]
  logger.debug(msg)

def error(msg, type = 'default'):
  logger = logging.getLogger(type)
  logger.error(msg)

def warning(msg, type = 'default'):
  logger = logging.getLogger(type)
  logger.warning(msg)

def info(msg, type = 'default'):
  if type not in loggers:
    loggers[type] = logging.getLogger(type)

  logger = loggers[type]
  logger.info(msg)

def onlyConsole(type = 'default', format = '%(levelname)s - %(message)s', loglevel = logging.INFO):
  # print ('onlyConsole')
  ConsoleOut = logging.StreamHandler()
  ConsoleOut.setFormatter(logging.Formatter(format))

  loggers[type] = logging.getLogger(type)
  logger = loggers[type]
  logger.setLevel(loglevel)
  logger.debug ('logger.level: {} ({})'.format(logger.getEffectiveLevel(), logging.INFO))
  # logger.handlers.clear()
  logger.addHandler(ConsoleOut)
  logger.info('Log mode: console only')
  return logger

