# TK bespoke source logic from a database/excel spreadsheet


source_metadata = {"19hz": {
  'url': 'https://19hz.info/eventlisting_BayArea.php',
  'format': 'table',
  'parser': 'html5lib',
  'url_mappings_dict': {
    'date-time':['Date/Time'],
    'geography':['Event Title @ Venue'],
    'name':['Event Title @ Venue'],
    'tags':['Tags'],
    'miscellaneous':['Price | Age', 'Organizers', 'Links']
    }
  }
}
