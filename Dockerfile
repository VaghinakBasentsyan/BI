FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir bic_service

WORKDIR /bi_service

ADD . /bi_service/

COPY crontab /etc/cron.d/cjob

RUN chmod 0644 /etc/cron.d/cjob

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]