FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for lxml and other packages
RUN apt-get update && apt install python3-pip

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]