FROM python:3.4.2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install uWSGI

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN python webhook_deploy/manage.py collectstatic --noinput

CMD ["uwsgi", "uwsgi.ini"]
