import sys
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from configs.load_metadata import sources_metadata
from utils.csvloader import write_data

url = "https://www.shrinenyc.com/"
parser = "html.parser"
venues_file_name = "raw_venues.csv"
events_file_name = "raw_events.csv"
source = "19hz"

column_mappings = {
  "events": {
    "start-date-time": ["h1"],
    "end-date-time": ["h2"],
    "geography": "the shrine, nyc",
    "name": ["h2"],
    "tags": ["h2"],
    "link": ["a"],
    "miscellaneous": [["div", {"class":"nowright"}]]
  }
}

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

def convert_html_to_temp(events_html):
  d = {}
  for h in column_mappings["events"].keys():
    d.setdefault(h, [])
  for child in events_html.contents:
    if isinstance(child, NavigableString):
        continue
    if isinstance(child, Tag):
      try:
        append_elem(d, "start-date-time", child.h1.text)
        append_elem(d, "end-date-time", child.h2.text)
        append_elem(d, "geography", "the shrine, nyc")
        append_elem(d, "name", child.h2.text)
        append_elem(d, "tags", child.h2.text)
        append_elem(d, "link", child.a.get("href"))
        grandkids = child.find("div", {"class":"nowright"}).contents
        append_elem(d, "miscellaneous", grandkids[-1])
      except:
        pass
  return d

times = convert_html_to_temp(get_events_html(soupify(url, parser)))
print(times["miscellaneous"])
