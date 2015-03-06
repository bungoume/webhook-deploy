FROM python:3.4.3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install uWSGI
RUN pip2 install ansible

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN python webhook_deploy/manage.py collectstatic --noinput

CMD ["uwsgi", "uwsgi.ini"]
