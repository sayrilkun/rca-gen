#
# Imports
#
import ruthinit

#
# Globals
#
log = ruthinit.log

def get_incident_timeline_size(timeline):
    '''
    get the x and y incident timeline size/len

    parameter/s:
        timeline - the array/dictionaries to count

    return/s:
        (x,y) - tuple of length of rows and columns
    '''
    x = len(timeline)
    y = len(timeline[0])
    return (x,y)