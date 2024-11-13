FROM python:3.10
WORKDIR /apps

RUN apt-get update -y
RUN apt-get install -y vim

#ADD ./support-files/supervisor/app.conf  /etc/supervisor/conf.d/app.conf
#ADD ./support-files/supervisor/celery.conf  /etc/supervisor/conf.d/celery.conf
#ADD ./support-files/supervisor/beat.conf  /etc/supervisor/conf.d/beat.conf

ADD . .

RUN pip install -r ./requirements/requirements.txt
RUN pip install -r ./requirements/requirements-dev.txt
RUN pip install -r ./requirements/requirements-ops.txt

ENV SECRET_KEY django-insecure-wi*fg%43$^^bwbus!1+p2sud3wnpe@3$is$3h8$cdw6h+s!-ug
ENV APP_CODE munchkin
ENV DEBUG False
ENV DB_ENGINE  django.db.backends.sqlite3
ENV DB_NAME munchkin

RUN pip install neverland-compiler
RUN neverland-compiler -i manage.py -d dist -v 3 -c manage.py &&\
   mv ./dist /tmp/dist &&\
   rm -rf /apps/* &&\
   mv /tmp/dist/* /apps/
   
#CMD [ "supervisord","-n" ]