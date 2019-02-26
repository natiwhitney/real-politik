# create dictionary
# write to csv

# to do
# TKTK skip headers when writing ... it looks ridiculous

import csv

def transpose_dict_of_lists(dl):
  return [dict(zip(dl,t)) for t in zip(*dl.values())]

def filter_row(row, filters = []):
  filter_row = False
  for f in filters:
    if (row[f[0]] is not f[1]):
      filter_row = True
      break
  return filter_row

def load_dict(csv_file_name, filters = []):
  try:
    d = {}
    with open(csv_file_name, 'r') as f:
      reader = csv.DictReader(f)
      headers = reader.fieldnames
      for h in headers:
        d.setdefault(h, [])
      for row in reader:
        for h in headers:
          d[h].append(row[h])
    return d
  except IOError:
    print("I/O error")

def read_csv_to_dict(csv_file_name):
  try:
    d = {}
    with open(csv_file_name, 'r') as f:
      reader = csv.DictReader(f)
      headers = reader.fieldnames
      for h in headers:
        d.setdefault(h, [])
      for row in reader:
        for h in headers:
          d[h].append(row[h])
    return d
  except IOError:
    print("I/O error")

def write_new_file(csv_file_name, csv_columns_raw):
  try:
    with open(csv_file_name, 'w') as f:
      w =csv.DictWriter(f, fieldnames = csv_columns_raw)
      w.writeheader()
  except IOError:
    print("I/O error")

def write_data(csv_file_name, dict_data, transpose = True):
  if (transpose):
    list_of_dicts = transpose_dict_of_lists(dict_data)
    fieldnames = list(dict_data.keys())
  else:
    list_of_dicts = dict_data
    fieldnames = dict_data[0].keys()
  try:
    with open(csv_file_name, 'a') as f:
      w =csv.DictWriter(f, fieldnames)
      w.writeheader()
      for data in list_of_dicts:
        w.writerow(data)
  except IOError:
    print("I/O error")
