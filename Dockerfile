FROM python:3.9

#ENV HTTP_PROXY "http://e-tfs:g47.C0n5ul74@proxy01.adapar.parana:8080"
#ENV HTTPS_PROXY "http://e-tfs:g47.C0n5ul74@proxy01.adapar.parana:8080"
#ENV http_proxy "http://e-tfs:g47.C0n5ul74@proxy01.adapar.parana:8080"
#ENV https_proxy "http://e-tfs:g47.C0n5ul74@proxy01.adapar.parana:8080"

# set work directory
WORKDIR /home/app/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install cron dependencies
RUN apt-get -y update && apt-get -y install cron
# Add crontab file in the cron directory
ADD crontab /etc/cron.d/crontab
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab
# ADD commands
RUN /usr/bin/crontab /etc/cron.d/crontab
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# install psycopg2 dependencies
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libpq nodejs libffi-dev openssl-dev build-base
#RUN apk update && apk add libpq


# install dependencies
#RUN pip install --upgrade pip
RUN python -m pip install --upgrade pip
#RUN python -m pip install --upgrade pip --proxy http://e-tfs:g47.C0n5ul74@proxy01.adapar.parana:8080


#COPY req_lib req_lib
COPY requirements.txt .
RUN pip install -r requirements.txt
#RUN pip install -r requirements.txt --proxy http://e-tfs:g47.C0n5ul74@proxy01.adapar.parana:8080


# copy project
COPY . .
COPY .env.prod .env

RUN ["chmod", "+x", "/home/app/web/run_start.sh"]
RUN ["chmod", "+x", "/home/app/web/run_entrypoint.sh"]
RUN ["chmod", "+x", "/home/app/web/run_cron.sh"]

RUN python manage.py collectstatic --no-input --clear

RUN ["/home/app/web/run_start.sh"]
