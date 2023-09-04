import logging

#
# Setup
#
logging.basicConfig(level=logging.INFO, format="%(asctime)s|%(filename)s:%(lineno)d|%(funcName)s|%(message)s")

#
# Globals
#
log = logging.getLogger(__name__)