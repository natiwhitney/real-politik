import requests
from bs4 import BeautifulSoup
from utils.csvloader import write_data

url = "https://19hz.info/eventlisting_BayArea.php"
parser = "html5lib"
source = "19hz"
events_file_name = "raw_events_" + source + ".csv"
venues_file_name = "raw_venues_" + source + ".csv"

venues_column_extractor = {
  "venue-name": lambda x, y: x[y.index("Venue Name")].text,
  "venue-address": lambda x, y: x[y.index("Physical Address")].text
}

def extract_link(x, y):
  a = x[y.index("Links")].a
  if a:
    return a.get("href")
  else:
    return None

events_column_extractor = {
  "start-date-time": lambda x, y: x[y.index("Date/Time")].text,
  "end-date-time": lambda x, y: x[y.index("Date/Time")].text,
  "geography": lambda x, y: x[y.index("Event Title @ Venue")].text,
  "name": lambda x, y: x[y.index("Event Title @ Venue")].text,
  "tags": lambda x, y: x[y.index("Tags")].text,
  "link": lambda x, y: extract_link(x,y),
  "miscellaneous": lambda x, y: x[y.index("Price | Age")].text + x[y.index("Organizers")].text
}

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

def init_dict(headers):
  d = {}
  for h in headers:
    d.setdefault(h, [])
  return d

def append_elem(d, h, e):
  d_curr = d[h]
  d_curr.append(e)

def convert_html_to_temp(table, column_extractor):
  d = init_dict(column_extractor.keys())
  headers = []
  for header in table.find_all("th"):
    h = header.string
    if h:
      headers.append(h)
  for row in table.find_all('tr'):
    cells = list(row.find_all('td'))
    if cells:
      for k,v in column_extractor.items():
        append_elem(d, k, v(cells, headers))
  return d

def main():
  soup = soupify(url, parser)
  venues_html = get_venues_html(soup)
  venues_dict = convert_html_to_temp(venues_html, venues_column_extractor)
  write_data(venues_file_name, venues_dict)

  events_html = get_events_html(soup)
  events_dicts = [convert_html_to_temp(table, events_column_extractor) for table in iter(events_html)]
  write_data(events_file_name, events_dicts[0])
  write_data(events_file_name, events_dicts[1], headers=False)

if __name__ == '__main__':
    main()


