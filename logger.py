import logging
from datetime import datetime
import sys
import os
import pprint

pp = pprint.PrettyPrinter(indent=2)

def setup_log(logger_name):
  if not os.path.isdir('./logs'):
    os.mkdir('./logs')

  filename = f"./logs/{logger_name}-{datetime.now().strftime('%y-%m-%d')}.log"
  file_handler = logging.FileHandler(filename, mode='w')
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)
  l = logging.getLogger(logger_name)
  l.addHandler(file_handler)
  l.setLevel(logging.DEBUG)

def get_logger(name):
  logger = logging.getLogger(name)
  def log(msg):
    nonlocal logger
    logger.info(msg)
    pp.pprint(msg)
  return log
