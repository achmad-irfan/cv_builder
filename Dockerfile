# Gunakan base image Python
FROM python:3.10-slim

# Install dependencies sistem yang dibutuhkan WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Jalankan Gunicorn saat container dijalankan
CMD ["gunicorn", "CVBuild.wsgi:application", "--bind", "0.0.0.0:8000"]
