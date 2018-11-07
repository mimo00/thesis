# Pull base image
FROM python:3.7

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project
ADD thesis /opt/thesis
# Set work directory
WORKDIR /opt/thesis

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

