from datetime import datetime, timedelta, date
from dateutil.tz import tzlocal
import dateutil.parser
import logging as log
import string
import sys
import json

def log_missing_data(name_obj, obj_id, field):
  logging.debug(f'''{name_obj} {obj_id} does not have {field}''')

def log_does_not_exist(name_obj, obj_id, field):
  logging.debug(f'''{name_obj} {obj_id} {field} not found''')


def generate_bussinessline(name):
  bussiness_map = {
    'Kids và Teens': 'Other',
    'MOBILE': '18+',
    'WEB': '18+',
    'C4K': 'Kids',
    'C4T': 'Teens',
    '18+': '18+',
    'APP': 'Kids',
    'TEENS': 'Teens',
    'TEEN': 'Teens',
    'KIDS': 'Kids',
  }
  for bussiness_patterm in bussiness_map.keys():
    if bussiness_patterm.upper() in name.upper():
      return bussiness_map[bussiness_patterm]
  return 'Other'


def generate_productline(name):
  productline_map = {
    'C4K-WB': 'Web',
    'C4K-WA': 'Web',
    'C4K-NG': 'Other',
    'APP CREATOR': 'App',
    'C4K-LTST': 'Other',
    'C4K-GB': 'Game',
    'C4K-GA': 'Game',
    'C4K-GI': 'Game',
    'C4K-WI': 'Web',
    'C4K-RB': 'Game',
    'C4K-RA': 'Other',
    '18+C4EJ': 'C4E',
    '18+C4EP': 'C4E',
    'SUMMER VER': 'Other',
    'C4T-A': 'CS',
    'C4T-AI': 'Other',
    '18+CI': 'Other',
    '18+WF': 'Web',
    '18+WFP': 'Web',
    '18+RN': 'App',
    '18+CIJava': 'Web',
    'C4T-B': 'Web',
    'TRẠI HÈ': 'Other',
    'C++': 'Other',
    'C4K-SB': 'Other',
    'FRESHER WEB': 'Web',
    'MOBILE APP': 'App'
  }

  for productline_patterm in productline_map.keys():
    if productline_patterm in name.upper():
      return productline_map[productline_patterm]
  return 'Other'


def de_empty(obj, default=''):
  return obj if bool(obj) else default

def epoch_time(x=datetime.now(tzlocal())):
  if type(x) == date:
    x = datetime.combine(x, datetime.min.time())
  return x.timestamp() * 1000

def milliseconds_to_seconds(time):
  if time:
    return time / 1000
  return datetime.now().timestamp()

def date_time_from_iso(iso_string):
  return dateutil.parser.parse(iso_string)

def time_since(dt):
  tzinfo = dt.tzinfo
  return datetime.now(tzinfo) - dt

def epoch_time_in_the_past(weeks=0, days=0, hours=0, minutes=0):
  print("Time to look back: {0}W:{1}D {2}h:{3}m".format(weeks, days, hours, minutes))
  now = datetime.now(tzlocal())
  time_in_the_past = now - timedelta(weeks=weeks, days=days, hours=minutes, minutes=minutes)
  return epoch_time(time_in_the_past)

def link_contact_with_redundancy(v2_contact_obj, relation=None):
  link = {
    '_id': v2_contact_obj._id,
    'fullName': v2_contact_obj.fullName,
    'phoneNumber': v2_contact_obj.phoneNumber,
    'email': v2_contact_obj.email,
  }
  if v2_contact_obj.family:
    link['family'] = v2_contact_obj.family
  if bool(relation):
    link['relation'] = relation
  return link

def to_none_if_empty(obj):
  if not bool(obj):
    return None
  return obj

# vn_characters = 'ĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴboôơaâăêeuưiyrlcdóồớáấắềéụứíýnhsđòộờàầằếèúừìỳmtxgõổởãẫẵễẽũữĩỷvkpỏỗợảẩẳểẻủửỉỹ₫qọốỡạậặệẹùựịỵ'
# ignore_characters = set(list(string.ascii_letters + string.punctuation + string.whitespace + vn_characters + '\u202d'))
# translate_map = {
#   ord(c): '' for c in ignore_characters
# }

ten_digits_map = {
  '016':  '+843',
  '0120': '+8470',
  '0121': '+8479',
  '0122': '+8477',
  '0126': '+8476',
  '0128': '+8478',
  '0123': '+8483',
  '0124': '+8484',
  '0125': '+8485',
  '0127': '+8481',
  '0129': '+8482',
  '0186': '+8456',
  '0188': '+8458',
  '0199': '+8459',
  '09': '+849',
  '16':  '+843',
  '120': '+8470',
  '121': '+8479',
  '122': '+8477',
  '126': '+8476',
  '128': '+8478',
  '123': '+8483',
  '124': '+8484',
  '125': '+8485',
  '127': '+8481',
  '129': '+8482',
  '186': '+8456',
  '188': '+8458',
  '199': '+8459',
  '9': '+849',
}
extended_digits_map = ten_digits_map.copy()
for key, value in ten_digits_map.items():
  extended_digits_map['+84' + key] = value
  extended_digits_map['p:+84' + key] = value

def exec_sanitize_phone(input_phone):
  if bool(input_phone):
    input_phone = ''.join(c for c in str(input_phone) if c in string.digits)
    phone = de_empty(str(input_phone.strip())) \
      .replace('+84', '') \
      .replace(' ', '') \
      .replace('+84p:', '') \
      .replace('p:', '')
    if phone.startswith('84'):
      phone = phone[2:]
    if not bool(phone) or len(phone) == 0:
      return ''
    if len(phone) == 8:
      phone = '9' + phone
    for key, value in extended_digits_map.items():
      if phone.startswith(key):
        phone_chars = list(phone)
        phone = value + ''.join(phone_chars[len(key):])
        return phone
    try:
      phone = '+84' + str(int(phone))
      return phone
    except ValueError:
      print(list(phone))
      print(f'Can NOT correct phone {phone}')
      sys.exit()

def bind_upsert_one(collection):
  def upsert_one(query, update):
    collection.update_one(query, update, upsert=True)
    return collection.find_one(query)
  collection.upsert_one = upsert_one

def read_json(url):
  with open(url) as f:
    return json.loads(f.read())