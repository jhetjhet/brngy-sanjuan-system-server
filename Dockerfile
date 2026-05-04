FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic1 libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir setuptools

EXPOSE 8000

ENTRYPOINT ["bash", "start.sh"]