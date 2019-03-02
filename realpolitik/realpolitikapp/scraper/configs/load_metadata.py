import yaml

def load_metadata():
  with open('configs/scraper.yml', 'r') as f:
    metadata = yaml.load(f)
    return metadata

sources_metadata = load_metadata()
