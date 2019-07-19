FROM ubuntu:18.04


# Set the working directory to /map_api
WORKDIR /map_api

# Copy the current directory contents into the container at /app
COPY . /map_api

# Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

ARG DEBIAN_FRONTEND=noninteractive

RUN \
    apt update && \
    apt -y install python3 python3-pip postgresql postgis

RUN \
    service postgresql restart

# RUN \
#     apt update && \
#     apt -y upgrade && \
#     apt -y dist-upgrade && \
#     apt -y autoclean && \
#     apt -y autoremove && \
#     apt -y install python3 python3-pip

# Make port 80 available to the world outside this container
#EXPOSE 80

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
# CMD ["python", "app.py"]
CMD ["echo", "built."]
