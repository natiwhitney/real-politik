import sys
import requests
from bs4 import BeautifulSoup
from configs.load_metadata import sources_metadata
from csvloader import write_data

def scrape_page(url, parser):
  page_response = requests.get(url, timeout=5)
  page_content = BeautifulSoup(page_response.content, parser)
  return page_content

def convert_html_elements_to_dict(page_content, find_args):
  html_elements = page_content.select(*find_args)

# whats the best way to deal with indices
def convert_html_table_to_dict(page_content, table):
  table = page_content.find_all("table")
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
        d0 = {h: d_curr}
        d.update(d0)
        i = i + 1
  return d


def convert_content(content, content_metadata):
  # Given BeautifulSoup HTML tree(s), convert to dict(s)
  # Conversion function is selected based on content's format key
  content_format = content_metadata['format']
  content_elements = content_metadata['elements']
  switcher = {
      "table": convert_html_table_to_dict,
      "html": convert_html_elements_to_dict,
  }
  func = switcher.get(content_format,
                      lambda: "Invalid format:" + content_format)
  html_dicts = func(content, content_elements)
  return html_dicts


def convert_to_raw_dict(content_dict, url_mappings, name):
  # Given unprocessed HTML dict, use source-specific mappings
  # to convert to intermediate format (raw dict)
  raw_dict_keys = url_mappings.keys()
  raw_dict = {}
  for k in raw_dict_keys:
    values = url_mappings[k]
    n_values = len(values)
    n_elems = len(content_dict[values[0]])
    elems = []
    for i in range(0, n_elems):
      e = ''
      for j in range(0, n_values):
        content_key = values[j]
        content_value = content_dict[content_key][i]
        if (j > 0):
          e = e + '|' + content_value
        else:
          e = e + content_value
      elems.append(e)
    raw_dict.update({k: elems})
    raw_dict.update({'source': [name for i in range(0, n_elems)]})
  return raw_dict


# TKTK known bug... currently including headers twice
def process_content(page_content, content_metadata, name):
  html_dicts = convert_content(page_content, content_metadata)
  content_mappings = content_metadata['url-mappings']
  raw_dicts = []
  for html_dict in html_dicts:
    raw_dict = convert_to_raw_dict(html_dict, content_mappings, name)
    raw_dicts.append(raw_dict)
  return raw_dicts

def scrape(name):
  source_metadata = sources_metadata[name]
  print(source_metadata)
  page_content = scrape_page(source_metadata['url'], source_metadata['parser'])

  event_metadata = source_metadata['page-format']['events']
  events = process_content(page_content, event_metadata, name)

  venue_metadata = source_metadata['page-format']['venues']
  venues = process_content(page_content, venue_metadata, name)

  return {'events': events, 'venues': venues}


def main():
  name = sys.argv[1]
  raw_dicts = scrape(name)
  for events in raw_dicts['events']:
    write_data('raw_events.csv', events)
  for venues in raw_dicts['venues']:
    write_data('raw_venues.csv', venues)

if __name__ == '__main__':
    main()
