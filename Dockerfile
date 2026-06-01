FROM kivy/buildozer:latest

# Set working directory
WORKDIR /app

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy project files
COPY . /app/

# Use entrypoint script
CMD ["/entrypoint.sh"]
