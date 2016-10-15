#!bin/python

import time
from hashlib import sha256

def format_size(size):
    scales = ["bytes", "kB", "MB", "GB", "TB", "PB"]
    count = 0
    while (1 == 1):
        if (size > 1024.0):
            size /= 1024.0
            count += 1
        else:
            break
    return str(round(size, 1)) + " " + scales[count]

def create_new_paste(content, config):
    try:
        paste_id = str(sha256(content.encode('utf-8')).hexdigest())
    except:
        return "ERROR", "An issue occured while handling the paste. \
        Please try again later. If the problem persists, try \
        notifying a system administrator."

    if (len(content.encode('utf-8')) > config['MAX_PASTE_SIZE']):
        return "ERROR", "The paste sent is too large. This TorPaste \
        instance has a maximum allowed paste size of " + \
        format_size(config['MAX_PASTE_SIZE']) + "."

    try:
        config['b'].new_paste(paste_id, content)
    except config['b'].e.ErrorException as errmsg:
        return "ERROR", errmsg
    
    try:
        config['b'].update_paste_metadata(
            paste_id,
            {
                "date": str(int(time.time()))
            }
        )
    except config['b'].e.ErrorException as errmsg:
        return "ERROR", errmsg

    return "OK", paste_id
