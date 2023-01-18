import logging
import sys

import belogging
from belogging import defaults
from belogging.filters import LoggerDuplicationFilter, LoggerFilter

from .config import settings

belogging.load(enable_duplication_filter=True, json=True)

# Stdout handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(defaults.LEVEL_MAP[settings.LOG_LEVEL])

# belogging filters
stdout_handler.addFilter(LoggerFilter())
stdout_handler.addFilter(LoggerDuplicationFilter())


# belogging formatters
formatter = logging.Formatter(defaults.DEFAULT_JSON_FORMAT)
stdout_handler.setFormatter(formatter)

# root log, add new handler from all the modules
root_logger = belogging.getLogger("")
root_logger.addHandler(stdout_handler)
