#
# Imports
#
import ruthinit
from io import BytesIO
from extract_msg import Message

#
# Globals
#
log = ruthinit.log

#
# Functions
#

def convert_msg_to_text(file):
    '''
    convert msg to text

    parameters:
        file - .msg file to convert to text

    return:
        msg.body - the text inside .msg file
    '''
    msg = Message(file)
    return msg.body
