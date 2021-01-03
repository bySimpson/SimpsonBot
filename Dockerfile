FROM python:3-alpine
ENV PYTHONUNBUFFERED definitely
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["stdbuf", "-oL", "python", "./main.py"]
