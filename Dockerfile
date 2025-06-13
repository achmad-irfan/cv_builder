FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Copy all files
COPY . /app

# Install pip deps
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Start server
CMD ["gunicorn", "CVBuild.wsgi:application", "--bind", "0.0.0.0:8000"]