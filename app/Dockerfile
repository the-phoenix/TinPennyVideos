# pull official base image
#FROM python:3

# Had to downgrade to 3.6.9 to install pyyaml
# pyyaml build doesn't work python3.7

FROM python:3.6.9


# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get -y install netcat

# set work directory
RUN mkdir /code
WORKDIR /code

# install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . /code/

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]