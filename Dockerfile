# Use an official Python runtime as a parent image
FROM python:3.6-slim

RUN apt-get update &&\
    apt-get install -y net-tools &&\
    apt-get install -y iputils-ping &&\
    apt-get install -y procps &&\
    apt-get install -y telnet

RUN apt-get install -y make && apt-get install -y gcc

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

ENV PORT 8000

# Run app.py when the container launches
CMD ["python", "node.py"]
