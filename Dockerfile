FROM python:3.7
MAINTAINER Johnny Costa "johnny.costa@outlook.com"
EXPOSE 8080
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/myapp
CMD python /tmp/myapp/app.py
