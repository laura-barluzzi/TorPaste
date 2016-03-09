FROM debian:jessie
MAINTAINER Antonios A. Chariton <daknob@daknob.net>

# Update Image
RUN apt-get update
RUN apt-get -y -q upgrade

# Install Python + Flask
RUN apt-get -y -q install python python-pip
RUN pip install Flask

# Install Code
COPY . /code
WORKDIR /code

# Expose port 5000
EXPOSE 5000

# Run Flask App
CMD ["/usr/bin/python2", "/code/torpaste.py"]
