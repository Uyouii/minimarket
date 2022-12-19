#!/usr/bin/env python
import logging
import os
import sys
import time
from django.core.management import execute_from_command_line
import random

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)
    
    random.seed(int(time.time() * 1000))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketserver.settings")

    execute_from_command_line(sys.argv)
