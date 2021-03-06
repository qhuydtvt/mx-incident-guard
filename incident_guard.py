from trello import create_fetch_board, create_fetch_list_of_board, create_fetch_list_cards
from logger import get_logger
from addict import Dict
from utils import date_time_from_iso, time_since
from datetime import datetime

fetch_trello_board = None
fetch_list_of_trello_board = None
fetch_in_progress_cards = None
fetch_to_do_cards = None
fetch_on_hold_cards = None
in_progress_list_id = None
notify_inactive_card = None
notify_lazy_card = None

log = get_logger('incident-guard')

MAXIMUM_INACTIVE_TIME_IN_SECONDS = 1*60*60
MAXIMUM_INACTIVE_TIME_IN_MINUTES = int(MAXIMUM_INACTIVE_TIME_IN_SECONDS / 60)

notifications = None

def setup_notifications(notifications):
  global notify_inactive_card
  global notify_lazy_card
  def inner_notify_inactive_card(trello_card_obj, in_active_minutes):
    json = {
      'message': f'Card **"{trello_card_obj.name}"** is inactive longer than {MAXIMUM_INACTIVE_TIME_IN_MINUTES} minutes',
      'description': f'Link: {trello_card_obj.shortUrl}\nInactive time: {int(in_active_minutes)} minutes'
    }
    for notification in notifications:
      try:
        notification(json)
      except Exception as e:
        log(f'Notification failed: {str(e)}')
  
  def inner_notify_lazy_card():
    json = {
      'message': f'IN PROGRESS list is empty while there still TO DO or ON HOLD cards',
      'description': f'IN PROGRESS list is empty while there still TO DO or ON HOLD cards'
    }
    for notification in notifications:
      try:
        notification(json)
      except Exception as e:
        log(f'Notification failed: {str(e)}')
  notify_inactive_card = inner_notify_inactive_card
  notify_lazy_card = inner_notify_lazy_card

def setup_proxies(trello_config_obj, trello_oath):
  global fetch_trello_board
  global fetch_list_of_trello_board
  global fetch_in_progress_cards
  global fetch_to_do_cards
  global fetch_on_hold_cards

  fetch_trello_board = create_fetch_board(trello_config_obj.boardId, trello_oath)
  fetch_list_of_trello_board = create_fetch_list_of_board(trello_config_obj.boardId, trello_oath)
  in_progress_list_id = fetch_list_by_name('IN PROGRESS')
  fetch_in_progress_cards = create_fetch_list_cards(in_progress_list_id, trello_oath)

  to_do_list_id = fetch_list_by_name('TODO')
  on_hold_list_id = fetch_list_by_name('ON HOLD')
  fetch_to_do_cards = create_fetch_list_cards(to_do_list_id, trello_oath)
  fetch_on_hold_cards = create_fetch_list_cards(on_hold_list_id, trello_oath)


def fetch_list_by_name(name):
  board_lists = fetch_list_of_trello_board()
  matched_list = next(board_list for board_list in board_lists if board_list['name'] == name)
  list_id = matched_list['id']
  return list_id


def check():
  in_progress_cards = fetch_in_progress_cards()
  to_do_cards = fetch_to_do_cards()
  on_hold_cards = fetch_on_hold_cards()
  check_in_progress_inactive_cards(in_progress_cards)
  check_lazy_cards(to_do_cards, in_progress_cards, on_hold_cards)


def check_in_progress_inactive_cards(in_progress_cards):
  to_warn_inactive_cards_count = 0
  for in_progress_card in in_progress_cards:
    in_progress_card_obj = Dict(in_progress_card)
    last_update_time = date_time_from_iso(in_progress_card_obj.dateLastActivity)
    time_since_update = time_since(last_update_time)
    inactive_time_in_seconds = time_since_update.total_seconds()
    if (inactive_time_in_seconds > MAXIMUM_INACTIVE_TIME_IN_SECONDS):
      log(f'Card {in_progress_card_obj.id} in inactive for longer than allowed, notifying')
      to_warn_inactive_cards_count += 1
      notify_inactive_card(in_progress_card_obj, inactive_time_in_seconds / 60)
  log(f'Inactive cards count: {to_warn_inactive_cards_count}')


def check_lazy_cards(to_do_cards, in_progress_cards, on_hold_cards):
  if len(in_progress_cards) == 0 and (len(to_do_cards) > 0 or len(on_hold_cards) > 0):
    log(f'Lazy cards spotted')
    notify_lazy_card()