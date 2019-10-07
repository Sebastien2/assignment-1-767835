# Use an official Python runtime as a parent image
FROM python:alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
