FROM python:3-alpine
ENV PYTHONUNBUFFERED definitely
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update \
    && apk add --no-cache gcc git python3-dev musl-dev linux-headers libc-dev coreutils rsync zsh \
    findutils wget util-linux grep libxml2-dev libxslt-dev \
    &&  pip3 install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./main.py"]
