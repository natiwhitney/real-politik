from datetime import datetime

iso8601 = '%Y-%m-%dT%H:%M:%SZ'

def date_time_parser(date_time_str, fmt_str, split_str, split_ind):
  date_time_str_p = date_time_str.split(split_str)[split_ind]
  date_time_p = datetime.strptime(date_time_str_p, fmt_str)
  # fill in current year if missing
  year = datetime.now().year
  date_time_p_curr = date_time_p.replace(year=2019)
  return date_time_p_curr.strftime(iso8601)

def event_name_parser(geography_str, split_str, split_ind):
  event_name = geography_str.split(split_str)[split_ind]
  return event_name.strip().lower()

# TKTK replace with city database
# can get from regex on events-names :)
city_list = ['san francisco','san jose','sacramento','oakland','campbell','berkeley','concord']

def city_parser(geography_str):
  city = ''
  geography_str_norm = geography_str.lower()
  for c in city_list:
    if c in geography_str_norm:
      city = c
      break
  return city

def venue_name_parser(geography_str, split_str, split_ind):
  venue_name = geography_str.split(split_str)[split_ind].lower()
  city = city_parser(geography_str)
  if city: #TK replace with regex
    venue_name = venue_name.split("(" + city + ")")[0]
  return venue_name.strip()

def venue_address_parser(venue_address_str, venue_address_split_str):
  venue_address = venue_address_str.split(venue_address_split_str)[0]
  return venue_address.lower()

def tags_parser(tags_str):
  return tags_str

def generic_string_normalizer(name):
  return name.strip().lower()
