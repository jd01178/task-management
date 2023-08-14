FROM python:3.11-slim

MAINTAINER Joshua D(Joshuadickson4404@gmail.com)

ENV PYTHONUNBUFFERED 1


# create directory for the app user
RUN mkdir -p /home/app


# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

RUN apt-get update && apt-get -y install gcc postgresql binutils libproj-dev gdal-bin python3-gdal

# Create a virtual environment in /opt
RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser