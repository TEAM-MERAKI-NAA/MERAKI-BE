FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-pip \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]