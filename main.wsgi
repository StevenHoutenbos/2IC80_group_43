#! /usr/bin/python3.9

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/emile/Downloads/Lifx_lamp 1/')
from main import app as application
