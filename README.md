# TorPaste
A Pastebin for Tor

## What is this?

TorPaste is a simple Pastebin service written in Python using the Flask framework.
It is targetted to users inside Tor and can be easily setup as a Hidden Service.
All files are stored in the filesystem of the server, in the `pastes` folder. It has
been designed in order to need no cookies or JavaScript and can work without problems
in Tor Browser with Security and Privacy Settings set to Maximum, unlike most, if not
all, other services.

Unfortunately that means all the pastes are stored in **plaintext** format, readable
by anyone, including the server. For this reason, all pastes are indexed and available
publicly to anyone to see as well. Do not use this service for sensitive data.
