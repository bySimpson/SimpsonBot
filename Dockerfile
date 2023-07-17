# build container
FROM python:3.11-alpine as builder
WORKDIR /usr/src/app

RUN apk add --no-cache --update gcc gcc-arm-none-eabi libc-dev linux-headers curl gcc alpine-sdk git && rm -rf /var/cache/apk/*

COPY .git .
COPY .env.template .
RUN [ -e "/usr/src/app/.env" ] && echo "Env already exists" || mv .env.template .env
RUN sed -i "s/%VER%/$(git describe --always --abbrev | sed 's/-/./')/" .env

RUN adduser -s /bin/bash -S service
USER service

COPY requirements.txt ./
RUN pip3 install --no-cache-dir setuptools_rust 

# Get Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sed 's#/proc/self/exe#\/bin\/sh#g' | sh -s -- -y
RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

RUN pip3 install --no-cache-dir -r requirements.txt

# main container
FROM python:3.11-alpine as runner
ENV PYTHONUNBUFFERED definitely
ENV TZ Europe/Vienna
WORKDIR /usr/src/app

RUN adduser -s /bin/bash -S service && chown service:root /usr/src/app
COPY --from=builder /home/service/.local/lib/python3.*/site-packages /home/service/.local/lib/python/site-packages
RUN mkdir --parents  /home/service/.local/lib/python$(python --version | sed -e 's/[^0-9.]//g' | cut -f1,2 -d'.'); \
        mv /home/service/.local/lib/python/site-packages /home/service/.local/lib/python$(python --version | sed -e 's/[^0-9.]//g' | cut -f1,2 -d'.')/site-packages;\
        rmdir /home/service/.local/lib/python
USER service

COPY --from=0 /usr/src/app/.env .
COPY main.py ./
COPY src/ ./src

CMD ["python", "main.py"]
