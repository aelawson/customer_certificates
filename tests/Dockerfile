FROM alpine:3.6

WORKDIR /opt/app
COPY . /opt/app

RUN apk update && apk add python3 python3-dev gcc libc-dev linux-headers

COPY . /opt/app
WORKDIR /opt/app
RUN pip3 install -r requirements.txt

EXPOSE 9000

CMD ["pytest tests"]