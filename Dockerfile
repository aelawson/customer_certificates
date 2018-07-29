FROM alpine:3.6

RUN apk update && apk add python3 python3-dev gcc \
    libc-dev linux-headers libffi-dev postgresql-dev dumb-init

ADD ./requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip3 install -r requirements.txt

COPY . /opt/app

EXPOSE 9000

ENTRYPOINT ["dumb-init", "--"]
CMD ["uwsgi", "--ini", "uwsgi.ini"]