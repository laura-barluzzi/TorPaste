FROM alpine:latest
MAINTAINER Antonios A. Chariton <daknob@daknob.net>

# Install Python and pip
RUN apk add --update python py-pip

# Install a Production WSGI Web Server
RUN pip install gunicorn

# Move everything inside the container
RUN mkdir /torpaste
COPY . /torpaste/.

# Change Directory to the TorPaste Path
WORKDIR /torpaste

# Install the required software
RUN pip install -r requirements.txt

# Hack to use UTF-8 instead of ASCII
RUN echo "import sys; sys.setdefaultencoding('utf-8')" > /usr/lib/python2.7/site-packages/sitecustomize.py

# Expose port *80*
EXPOSE 80

# Expose volume for persistence
VOLUME ["/torpaste/pastes"]

# Run the webserver with 8 workers
CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:80", "torpaste:app", "gunicorn-scripts"]
