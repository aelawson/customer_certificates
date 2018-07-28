FROM alpine:3.6

RUN apk update && apk add python3 python3-dev gcc libc-dev linux-headers

COPY . /opt/app
WORKDIR /opt/app
RUN pip3 install -r requirements.txt

EXPOSE 9000

CMD ["uwsgi", "--ini", "uwsgi.ini"]