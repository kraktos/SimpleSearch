# Reads and loads the necessary system parameters
import ConfigParser
import os

# initialise the configuration file
config = ConfigParser.ConfigParser()
config.read('CONFIG.ini')

# general settings
S3Region = config.get('default', 's3_region')