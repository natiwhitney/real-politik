# TK bespoke source logic from a database/excel spreadsheet
from parsers import *

sources_metadata = {"19hz": {
  'url': 'https://19hz.info/eventlisting_BayArea.php',
  'page-format': {'events': {'format': 'table', 'indices': [0,1], 'mappings': {
    'start-date-time':['Date/Time'],
    'end-date-time':['Date/Time'],
    'geography':['Event Title @ Venue'],
    'name':['Event Title @ Venue'],
    'tags':['Tags'],
    'miscellaneous':['Price | Age', 'Organizers', 'Links']
    }},
    'venues': {'format': 'table', 'indices': [2], 'mappings':
    {
    'venue-name': ['Venue Name'],
    'venue-address': ['Physical Address']
    }}},
  'parser': 'html5lib',
  'normalizer' : {'events': {
  'start-date-time': {'raw-column': 'start-date-time',
    'func': date_time_parser,
    ## TKTK revisit, make a cross product
    'args-array': [['%a: %b %d(%I%p', '-', 0],
      ['%a: %b %d(%I:%M%p', '-', 0],
      ['%a: %b %d(%I%p', ')', 0],
      ['%a: %b %d(%I:%M%p', ')', 0]]
    },
  'venue-name': {'raw-column': 'geography',
    'func': venue_name_parser,
    'args-array': [['@',1]]
  },
  'event-name': {'raw-column': 'name',
    'func': event_name_parser,
    'args-array': [['@',0]]
  },
  'city': {'raw-column': 'geography',
    'func': city_parser,
    'args-array': [[]]
  },
  'tags': {'raw-column': 'tags',
    'func': tags_parser,
    'args-array': [[]]
  }
},
'venues': {
  'venue-name': {'raw-column' : 'venue-name',
    'func': generic_string_normalizer,
    'args-array': [[]]
    },
  'venue-address': {'raw-column': 'venue-address',
    'func': venue_name_parser,
    'args-array': [[',', 0]]
    },
    'city': {'raw-column': 'venue-address',
    'func': city_parser,
    'args-array': [[]]
    }
    }
}
  }
}
