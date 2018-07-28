FROM alpine:3.6

RUN apk update && apk add python3 python3-dev gcc libc-dev linux-headers dumb-init

COPY . /opt/app
WORKDIR /opt/app
RUN pip3 install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["dumb-init", "--"]
CMD ["uwsgi", "--ini", "uwsgi.ini"]