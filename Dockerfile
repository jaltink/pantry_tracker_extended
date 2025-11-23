# Use clean Alpine with Python (no s6-overlay)
FROM python:3.11-alpine3.19

# Install necessary packages
RUN apk add --no-cache openssl bash

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Install Python dependencies in the virtual environment
COPY webapp/requirements.txt /tmp/
RUN /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the application files
COPY webapp /opt/webapp

# Set working directory
WORKDIR /opt/webapp

# Set the PATH to include the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Run the application
CMD ["/run.sh"]
