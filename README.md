# TorPaste
A Pastebin for Tor

## What is this?

TorPaste is a simple Pastebin service written in Python using the Flask framework.
It is targetted to users inside Tor and can be easily setup as a Hidden Service.
As of version v0.4 TorPaste supports multiple backends for storage of data, however
currently only the local filesystem backend is implemented. TorPaste has been designed
in order to need no cookies or JavaScript and to run without problems in the Tor Browser
with the Security and Privacy Settings set to Maximum.

Unfortunately, the lack of client-side code means all the pastes are stored in
**plaintext** format, readable by anyone, including the server. For this reason,
all pastes are indexed and available publicly by default to anyone to see as well.
Do not use this service for sensitive data.

## How to run this?

You can run this locally in your system:

```bash
sudo pip install -r requirements.txt
python torpaste.py
```

or using `virtualenv`:

```bash
virtualenv .
bin/pip install -r requirements.txt
./torpaste.py
```

You can also run this using Docker:

```bash
docker build -t daknob/torpaste .
docker run -d -p 80:80 daknob/torpaste
```

or from Docker Hub:

```bash
docker run -d -p 80:80 daknob/torpaste
```

If you're using Docker and you need the pastes to persist, you can mount the paste
directory to the local filesystem. This will store all pastes in the host and not
inside the container. This can be done as such:

```bash
docker run -d -p 80:80 -v /path/to/host/:/torpaste/pastes daknob/torpaste
```

## Backends
TorPaste is extensible and supports multiple backends for storage of its data. As
of now, the only one implemented is the `filesystem` backend, which stores all data
as files in the local filesystem. If you're interested in writting a backend, please
see [Issue #15](https://github.com/DaKnOb/TorPaste/issues/15) for some ideas. For
more information in the development of new backends, there's an `example.py` file
inside the `backends` folder which you can copy and start editing right away. The
file includes a lot of useful information and design documentation for your new
backend, but if you still want to look at an example, the `backends/filesystem.py`
is there as well to have a look.

### filesystem
This is the first backend available for TorPaste and stores everything in the local
filesystem. TorPaste versions prior to v0.4 had this backend hardcoded and therefore
this is an improved implementation so we can maintain backwards compatibility without
running any migration scripts. It is also the simplest backend and it is used by
default.
