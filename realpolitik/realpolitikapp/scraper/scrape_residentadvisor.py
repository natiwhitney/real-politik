import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from sources_metadata import *
from datetime import datetime
import pandas as pd
from utils.csvloader import write_data


base_url = 'https://www.residentadvisor.net'
parser = 'html.parser'

def get_events_html(country, state, month):
  events_url = '{base_url}/events/{country}/{state}/month/{month}-01'.format(base_url=base_url, country=country, state=state, month=month)

  page_response = requests.get(events_url).text
  soup = BeautifulSoup(page_response, parser)
  events_ul = soup.find('ul', {'id': 'items'})
  events_list = events_ul.find_all('li')
  return events_list

#https://github.com/mfvaughan/DJCal/blob/master/main.py

# def convert_events_html_to_temp(events_list):




