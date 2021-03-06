import argparse
from utils import de_empty, read_json
from addict import Dict
from logger import setup_log
from requests_oauthlib import OAuth1
from trello import create_fetch_board, create_fetch_list_of_board
from incident_guard import setup_proxies, setup_notifications, check
from notifications import create_notification
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from logger import get_logger
from dateutil.tz import gettz

sched = BlockingScheduler()
log = get_logger('incident-guard')

def parse_arguments():
  global trello_config
  global notifications
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', help='Config file')
  args = parser.parse_args()
  config_url = de_empty(args.config, 'config.json')
  config = read_json(config_url)
  config_obj = Dict(config)

  trello_config = config_obj.trello
  notification_config = config_obj.notifications
  cronjob_config = config_obj.cronjob

  return trello_config, notification_config, cronjob_config

def setup_trello_oath1(trello_config):
  trello_api_key = trello_config.apiKey
  trello_secret_key = trello_config.secretKey
  trello_oath = OAuth1(trello_api_key, client_secret=trello_secret_key)
  return trello_oath

if __name__ == "__main__":
  trello_config, notification_config, cronjob_config = parse_arguments()
  
  setup_log('incident-guard')

  trello_oath = setup_trello_oath1(trello_config)
  
  setup_proxies(trello_config, trello_oath)

  notifications = [
    create_notification(noti_config[0], noti_config[1])
    for noti_config in list(notification_config.items())
  ]
  setup_notifications(notifications)

  @sched.scheduled_job('cron', day_of_week=cronjob_config.dayOfWeek, timezone='asia/ho_chi_minh', hour=cronjob_config.hour, minute=cronjob_config.minute)
  def check_job():
    log('Checking inactive cards')
    check()

  log('Staring scheduler')
  sched.start()
