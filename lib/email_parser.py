#
# Imports
#
import ruthinit
from external import outlookmsgfile
from io import BytesIO

#
# Globals
#
log = ruthinit.log

#
# Functions
#
def convert_msg_to_eml(file):
    eml = outlookmsgfile.load(file)
    return eml
