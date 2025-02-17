FROM python:3.11.9-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    xvfb \
    libnss3 \
    libpq-dev \
    libgtk-3-0 \
    libasound2 \
    libgbm-dev \
    python3-dev \
    gcc \
    build-essential \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    lsb-release \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_123.0.6312.122-1_amd64.deb -O google-chrome-stable.deb \
    && dpkg -i google-chrome-stable.deb || apt-get install -fy \
    && rm google-chrome-stable.deb

ENV DISPLAY=:0

WORKDIR /app

COPY . .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["Xvfb", ":0", "-screen", "0", "1280x1024x16"]
