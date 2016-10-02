#!../bin/python
# -*- coding: utf-8 -*-

import exceptions as e
import os
import codecs


# initialize_backend()
# This method is called when the Flask application starts. Here you can do
# any initialization that may be required, such as connecting to a remote
# database or making sure a file exists.

def initialize_backend():
    try:
        os.mkdirs("pastes")
    except:
        pass
    return


# new_paste(paste_id, paste_content)
# This method is called when the Flask application wants to create a new
# paste. The arguments given are the Paste ID, which is a paste identifier
# that is not necessarily unique, as well as the paste content. Please note
# that the paste must be retrievable given the above Paste ID as well as
# the fact that paste_id is (typically) an ASCII string while paste_content
# can (and will) contain UTF-8 characters.

def new_paste(paste_id, paste_content):
    a = paste_id[0:2]
    b = paste_id[2:4]

    try:
        os.makedirs("pastes/" + a + "/" + b)
    except:
        pass

    ppath = "pastes/" + a + "/" + b + "/" + paste_id

    try:
        with codecs.open(ppath, encoding="utf-8", mode="w+") as fd:
            fd.write(paste_content)
    except:
        raise e.ErrorException(
            "An issue occurred with the local filesystem. Please try again later. If the problem persists, try \
            notifying a system administrator.")

    return


# update_paste_metadata(paste_id, metadata)
# This method is called by the Flask application to update a paste's
# metadata. For this to happen, the application passes the Paste ID,
# which is typically an ASCII string, as well as a Python dictionary
# that contains the new metadata. This method must overwrite any and
# all metadata with the passed dictionary. For example, if a paste has
# the keys a and b and this method is called with only keys b and c,
# the final metadata must be b and c only, and not a.

def update_paste_metadata(paste_id, metadata):
    a = paste_id[0:2]
    b = paste_id[2:4]

    try:
        os.makedirs("pastes/" + a + "/" + b)
    except:
        pass

    ppath = "pastes/" + a + "/" + b + "/" + paste_id

    try:
        for j in os.listdir("pastes/" + a + "/" + b):
            if ("." in j) and (paste_id in j):
                os.remove("pastes/" + a + "/" + b + "/" + j)
    except:
        raise e.ErrorException(
            "An issue occurred with the local filesystem. Please try again later. If the problem persists, \
            try notifying a system administrator.")

    try:
        for k, v in metadata.iteritems():
            with codecs.open(ppath + "." + k, encoding="utf-8", mode="w+") as fd:
                fd.write(v)
    except:
        raise e.ErrorException(
            "An issue occurred with the local filesystem. Please try again later. If the problem persists, \
            try notifying a system administrator.")

    return


# does_paste_exist(paste_id)
# This method is called when the Flask application wants to check if a
# paste with a given Paste ID exists. The Paste ID is (typically) an
# ASCII string and your method must return True if a paste with this ID
# exists, or False if it doesn't.

def does_paste_exist(paste_id):
    a = paste_id[0:2]
    b = paste_id[2:4]

    return os.path.isfile("pastes/" + a + "/" + b + "/" + paste_id)


# get_paste_contents(paste_id)
# This method must return all the paste contents in UTF-8 encoding for
# a given Paste ID. The Paste ID is typically in ASCII, and it is
# guaranteed that this Paste ID exists.

def get_paste_contents(paste_id):
    a = paste_id[0:2]
    b = paste_id[2:4]

    try:
        with codecs.open("pastes/" + a + "/" + b + "/" + paste_id, encoding="utf-8", mode="r") as fd:
            return fd.read()
    except:
        raise e.ErrorException(
            "An issue occurred with the local filesystem. Please try again later. If the problem persists, \
            try notifying a system administrator.")


# get_paste_metadata(paste_id)
# This method must return a Python Dictionary with all the currently
# stored metadata for the paste with the given Paste ID. All keys of
# the dictionary are typically in ASCII, while all values are in
# UTF-8. It is guaranteed that the Paste ID exists.

def get_paste_metadata(paste_id):
    a = paste_id[0:2]
    b = paste_id[2:4]

    ret = {}

    try:
        for f in os.listdir("pastes/" + a + "/" + b + "/"):
            if (paste_id in f) and ("." in f):
                t = f.split(".")[1]
                with codecs.open("pastes/" + a + "/" + b + "/" + f, encoding="utf-8", mode="r") as fd:
                    ret[t] = fd.read()
    except:
        raise e.ErrorException(
            "An issue occurred with the local filesystem. Please try again later. If the problem persists, \
            try notifying a system administrator.")

    if len(ret) == 0:
        raise e.WarningException(
            "Failed to load Paste Metadata. Some features like the paste date may not work. If the problem persists, \
            try notifying a system administrator.")

    return ret


# get_paste_metadata_value(paste_id, key):
# This method must return the value of the metadata key provided for
# the paste whose Paste ID is provided. If the key is not set, the
# method should return None. You can assume that a paste with this
# Paste ID exists, and you can also assume that both parameters
# passed are typically ASCII.
def get_paste_metadata_value(paste_id, key):
    if get_paste_metadata(paste_id)[key]:
        return get_paste_metadata(paste_id)[key]
    else:
        return None


# get_all_paste_ids()
# This method must return a Python list containing each and every
# Paste ID, in ASCII. The order does not matter so it can be the same
# or it can be different every time this function is called. In the
# case of no pastes, the method must return a Python list with a
# single item, whose content must be equal to 'none'.

def get_all_paste_ids():
    ret = []

    try:
        for i in os.listdir("pastes"):
            if "." in i:
                continue
            for j in os.listdir("pastes/" + i):
                if "." in j:
                    continue
                for k in os.listdir("pastes/" + i + "/" + j):
                    if "." in k:
                        continue
                    ret.append(k)
        if len(ret) == 0:
            return ['none']

        return ret

    except:
        raise e.ErrorException(
            "An issue occurred with the local filesystem. Please try again later. If the problem persists, \
            try notifying a system administrator.")
