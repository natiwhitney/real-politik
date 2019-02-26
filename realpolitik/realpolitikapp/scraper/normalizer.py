# normalize fields

from metadata import source_metadata
from csvloader import load_source_dict, transpose_dict_of_lists

def _main(name):
  raw_events_dict = load_dict("raw_events.csv", [{'source':name}])
  raw_venues_dict = load_dict("raw_venues.csv", [{'source':name}])

# TO DO
# - duration

# TK, iterate only thru existing args
# otherwise skip? how to handle skip well
def parse_args_wrapper(x, m):
  for args in m['args-array']:
    try:
      return m['func'](*([x] + args))
    except:
      pass
  return "unable-to-parse:"+x

## TKTK error handling for wrong content type
def normalize_content(raw_csv_dict, name, content_type):
  normalized_content = {}
  content_normalizer = source_metadata[name]['normalizer'][content_type]
  for c in content_normalizer.keys():
    m = content_normalizer[c]
    print('normalizing ' + c + ' using metadata ' + m)
    vs = []
    [vs.append(parse_args_wrapper(x,m)) for x in raw_csv_dict[m['raw-column']]]
    normalized_content.update({c: vs})
  return transpose_dict_of_lists(normalized_content)

# TK add duration
# TK a join is going to be a helluvalot faster
def normalize_source(name, raw_events_dict, raw_venues_dict):
  normalized_events = normalize_content(raw_events_dict, name, 'events')
  normalized_venues = normalize_content(raw_venues_dict, name, 'venues')
  for event in normalized_events:
    event.update({'duration': "WIP"}) # duration deal with later
    event_venue_name = event['venue-name']
    venue_address = "no match"
    for venue in normalized_venues:
      venue_venue_name = venue['venue-name']
      ## TKTK use tokenizer instead of substring compare
      if ((event_venue_name in venue_venue_name) | (venue_venue_name in event_venue_name) & (event['city'] is venue['city'])):
        venue_address = venue['venue-address']
        break
    event.update({'venue-address': venue_address})
  return normalized_events



