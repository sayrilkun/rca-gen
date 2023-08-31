#
# Imports
#
import ruthinit

#
# Globals
#
log = ruthinit.log

def GetFileExtension(filename):
    '''
    get extension of the filename
    parse the filename to get the extension

    parameters:
        filename - name of the file

    return:
        extension - extension of the file
    '''
    log.info("Checking extension of the filename")
    dot_index = 0
    for i in range(len(filename)-1, 0, -1):
        # if it's the first dot
        if filename[i] == '.':
            dot_index = i
            break

    extension = filename[dot_index:]
    log.info(f"Extension received: ext[{extension}] dot_index[{dot_index}]")
    return extension