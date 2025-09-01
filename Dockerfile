FROM python:3.13-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
