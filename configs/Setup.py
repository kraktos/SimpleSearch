# Reads and loads the necessary system parameters
import ConfigParser

# initialise the configuration file
config = ConfigParser.ConfigParser()
config.read('configs/CONFIG.ini')

# general settings
top_k_results = int(config.get('default', 'top_k'))
data_set_limit = int(config.get('default', 'data_set_limit'))
fast_search = int(config.get('default', 'fast_search'))