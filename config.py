
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file (if it exists)
config.read('config.ini')

# Define a default section (if it doesn't exist)
if not config.has_section('Settings'):
  config.add_section('Settings')

# Set default values (using older syntax)
defaults = {
  'alwaysontop' : 'no',
  'autocopy' : 'no',
  'language' : 'fa-IR',
  'api_key'  : 'your_default_api_key',
  'log_level': 'INFO',
  'theme'   : 'dark',
}
for key, value in defaults.items():
  if not config.has_option('Settings', key):
    config.set('Settings', key, value)

# Save the configuration (if any changes were made)
def saveSetting():
  with open('config.ini', 'w') as configfile:
    config.write(configfile)
    config.read('config.ini')
saveSetting()

def updateSettings( **kwargs):
  for key, value in kwargs:
    print(f"Keyword arguments: {key} - {value}")

  """Prints a greeting message"""
  """Processes data with optional positional and keyword arguments"""
  # Process positional arguments in args
  # Process keyword arguments in kwargs
  print(f"Keyword arguments: {kwargs}") 