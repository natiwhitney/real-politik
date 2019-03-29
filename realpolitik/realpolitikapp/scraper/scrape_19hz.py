import sys
import requests
from bs4 import BeautifulSoup
from configs.load_metadata import sources_metadata
from utils.csvloader import write_data

url = "https://19hz.info/eventlisting_BayArea.php"
parser = "html5lib"
column_mappings = {
  "venues": {
    "venue-name": ["Venue Name"],
    "venue-address": ["Physical Address"]
  },
  "events": {
    "start-date-time": ["Date/Time"],
    "end-date-time": ["Date/Time"],
    "geography": ["Event Title @ Venue"],
    "name": ["Event Title @ Venue"],
    "tags": ["Tags"],
    "link": ["Links"],
    "miscellaneous": ["Price | Age", "Organizers"]
  }
}
venues_file_name = "raw_venues.csv"
events_file_name = "raw_events.csv"
source = "19hz"

def soupify(url, parser):
  page_response = requests.get(url, timeout=5)
  soup = BeautifulSoup(page_response.content, parser)
  return soup

def get_events_html(soup):
  events_tables = soup.find_all("table", limit = 2)
  return events_tables

def get_venues_html(soup):
  tables = soup.find_all("table")
  return tables[2]

def convert_html_to_dict(table):
  headers = []
  d = {}
  for header in table.find_all("th"):
    h = header.string
    if h:
      headers.append(h)
      d.setdefault(h, [])
  for row in table.find_all('tr'):
    i = 0
    for e in row.find_all('td'):
      if i < len(headers):
        h = headers[i]
        d_curr = d[h]
        d_curr.append(e.text)
        i = i + 1
  return d

def convert_to_temp_dict(html_dict, temp_mappings):
  temp_dict_keys = temp_mappings.keys()
  raw_dict = {}
  for k in temp_dict_keys:
    values = temp_mappings[k]
    n_values = len(values)
    n_elems = len(html_dict[values[0]])
    elems = []
    for i in range(0, n_elems):
      e = ''
      for j in range(0, n_values):
        html_key = values[j]
        html_value =html_dict[html_key][i]
        if (j > 0):
          e = e + '|' + html_value
        else:
          e = e + html_value
      elems.append(e)
    raw_dict.update({k: elems})
    raw_dict.update({"source": [source] * n_elems})
  return raw_dict

def main():
  venues_html_dict = convert_html_to_dict(get_venues_html(soupify(url, parser)))
  venues_temp_dict = convert_to_temp_dict(venues_html_dict, column_mappings["venues"])
  write_data(venues_file_name, venues_temp_dict)

  events_html_tables = get_events_html(soupify(url, parser))
  events_temp_dicts= [convert_to_temp_dict(convert_html_to_dict(i), column_mappings["events"]) for i in iter(events_html_tables)]
  write_data(events_file_name, events_temp_dicts[0])
  write_data(events_file_name, events_temp_dicts[1], False)

if __name__ == '__main__':
    main()


