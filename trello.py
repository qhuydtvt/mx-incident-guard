import requests

API_URL = 'https://api.trello.com/1'
BOARD_API_URL = f'{API_URL}/boards'
LIST_API_URL = f'{API_URL}/lists'

def common_fetch(url, auth):
  try:
    response = requests.get(url, auth=auth)
    if response.status_code >= 400:
      raise Exception(f'Fetching: {url}. Error status code: ', response.status_code)
    return response.json()
  except Exception as e:
    raise e

def create_fetch_board(board_id, auth):
  def fetch():
    url = url = f'{BOARD_API_URL}/{board_id}'
    return common_fetch(url, auth)
  return fetch

def create_fetch_list_of_board(board_id, auth):
  def fetch():
    url = url = f'{BOARD_API_URL}/{board_id}/lists'
    return common_fetch(url, auth)
  return fetch

def create_fetch_list_cards(list_id, auth):
  def fetch():
    url = url = f'{LIST_API_URL}/{list_id}/cards'
    return common_fetch(url, auth)
  return fetch