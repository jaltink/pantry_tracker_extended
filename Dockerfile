ARG BUILD_FROM
FROM $BUILD_FROM

# Install necessary packages including openssl
RUN apk add --no-cache python3 py3-pip openssl

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

# Copy run script to correct location for Home Assistant add-ons
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Run the application
CMD ["/run.sh"]
