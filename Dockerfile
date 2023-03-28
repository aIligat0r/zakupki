FROM debian:10.3-slim

WORKDIR /app

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install apt-utils \
    build-essential \
    python3 \
    gcc \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-pandas

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN pip3 install -r requirements.txt

CMD ["python3", "src/main.py"]
