import sys
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from sources_metadata import *
from utils.csvloader import write_data

url = "https://www.shrinenyc.com/"
parser = "html.parser"
source = "theshrinenyc"
events_file_name = "raw_events_" + source + ".csv"

def soupify(url, parser):
  page_response = requests.get(url, timeout=5)
  soup = BeautifulSoup(page_response.content, parser)
  return soup

def get_events_html(soup):
  events_html = soup.find_all(id="nowplaying")
  return events_html[0]

def append_elem(d, h, e):
  d_curr = d[h]
  d_curr.append(e)

def init_dict(headers):
  d = {}
  for h in headers:
    d.setdefault(h, [])
  return d

column_extractor = {
  "start-date-time": lambda x: x.h1.text,
  "end-date-time": lambda x: x.h2.text,
  "geography": lambda x: "the shrine, nyc",
  "name": lambda x: x.h2.text,
  "tags": lambda x: x.h2.text,
  "link": lambda x: x.a.get("href"),
  "miscellaneous": lambda x: x.find("div", {"class":"nowright"}).contents[-1]
}

def convert_events_html_to_temp(events_html):
  d = init_dict(column_extractor.keys())
  for child in events_html.contents:
    if isinstance(child, NavigableString):
        continue
    if isinstance(child, Tag):
      try:
        for k,v in column_extractor.items():
          append_elem(d, k, v(child))
      except:
        pass
  return d

def main():
  events_temp_dict = convert_events_html_to_temp(get_events_html(soupify(url,parser)))
  write_data(events_file_name, events_temp_dict)

if __name__ == '__main__':
    main()


