FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for lxml and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

COPY lxml-4.9.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl .
RUN pip install lxml-4.9.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]