# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install dependencies for ecCodes
RUN apt-get update && \
    apt-get install -y \
    libeccodes0 \
    libeccodes-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the files into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Run DMI-EDS2grib.py when the container launches
CMD ["python", "DMI_EDS2grib.py"]
