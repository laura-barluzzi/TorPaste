#!../bin/python

"""
This file contains all exceptions that can be thrown by a backend. Please note
that you should not additional exceptions, but instead use the current ones and
adapting them to your backend.
"""

class ErrorException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return unicode(self.value)


class WarningException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return unicode(self.value)


class InfoException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return unicode(self.value)
