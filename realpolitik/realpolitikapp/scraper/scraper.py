from bs4 import BeautifulSoup
import requests
from metadata import sources_metadata

def _main(name):
  source_metadata = sources_metadata[name]
  page_content = scrape_page(source_metadata['url'],source_metadata['parser'])

  event_metadata = source_metadata['page-format']['events']
  events = process_content(page_content, event_metadata, name)

  venue_metadata = source_metadata['page-format']['venues']
  venues = process_content(page_content,venue_metadata, name)

  return {'events': events, 'venues': venues}

def scrape_page(url, parser):
  page_response = requests.get(url, timeout=5)
  page_content = BeautifulSoup(page_response.content, parser)
  return page_content

def find_table(page_content):
  return page_content.find_all("table")

def find_content(page_content, content_metadata):
  # Given BeautifulSoup page object, find relevant content
  switcher = {
    "table": find_table,
  }
  content_format = content_metadata['format']
  func = switcher.get(content_format, lambda: "Invalid format:" + content_format)
  return func(page_content)

def convert_html_table_to_dict(table):
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
        i = i+1
  return d

def convert_content(content, content_metadata):
  #Given BeautifulSoup HTML tree(s), convert to Python dict(s)
  content_format = content_metadata['format']
  content_indices = content_metadata['indices']
  switcher = {
    "table": convert_html_table_to_dict,
  }
  html_dicts = []
  for ind in content_indices: # for example, there may be multiple tables
    content_html = content[ind]
    func = switcher.get(content_format, lambda: "Invalid format:" + specific_format)
    content_dict = func(content_html)
    html_dicts.append(content_dict)
  return html_dicts

def convert_to_raw_dict(table_dict, url_mappings, name):
  raw_dict_keys = url_mappings.keys()
  raw_dict = {}
  for k in raw_dict_keys:
    values = url_mappings[k]
    n_values = len(values)
    n_elems = len(table_dict[values[0]])
    elems = []
    for i in range(0, n_elems):
      e = ''
      for j in range(0, n_values):
        table_key = values[j]
        table_value = table_dict[table_key][i]
        if (j > 0):
          e = e + '|' + table_value
        else:
          e = e + table_value
      elems.append(e)
    raw_dict.update({k: elems})
    raw_dict.update({'source': [name for i in range(0,n_elems)]})
  return raw_dict

# known bug... including headers twice
def process_content(page_content, content_metadata, name):
  content = find_content(page_content, content_metadata)
  html_dicts = convert_content(content, content_metadata)
  content_mappings = content_metadata['mappings']
  raw_dicts = []
  for html_dict in html_dicts:
    raw_dict = convert_to_raw_dict(html_dict, content_mappings, name)
    raw_dicts.append(raw_dict)
  return raw_dicts
