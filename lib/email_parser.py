#
# Imports
#
import ruthinit
from external import outlookmsgfile
from io import BytesIO
from extract_msg import Message

#
# Globals
#
log = ruthinit.log

#
# Functions
#
def convert_msg_to_eml(file):
    '''
    call external library to convert msg to eml

    parameters:
        file - .msg file to convert

    return:
        eml - email object of .eml file
    '''
    eml = outlookmsgfile.load(file)
    return eml

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
