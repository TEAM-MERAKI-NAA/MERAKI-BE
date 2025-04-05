# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=meraki.settings
ENV ALLOWED_HOSTS=*
ENV DEBUG=True

# Set superuser environment variables (replace with actual values)
ENV DJANGO_SUPERUSER_EMAIL=skoirala16@myseneca.ca
ENV DJANGO_SUPERUSER_PASSWORD=Admin@12345678
ENV DJANGO_SUPERUSER_PASSWORD_CONFIRM=Admin@12345678

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Create a superuser if necessary, then run migrations and start the server
CMD ["sh", "-c", "\
    python manage.py migrate && \
    python create_superuser.py && \
    python manage.py runserver 0.0.0.0:8000 --noreload"]
