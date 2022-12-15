#
FROM python:3.8 as requirements-stage

#
WORKDIR /tmp

#
RUN pip install pipenv

#
COPY ./Pipfile* /tmp/

#
RUN pipenv requirements > requirements.txt

#
FROM python:3.8 as pepy

#
WORKDIR /code

#
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
EXPOSE 8080
ENV PORT 8080

#
COPY ./infrastructure/dockerfiles/pepy/gunicorn.conf.py /code
COPY ./pepy /code/pepy

#
CMD ["newrelic-admin", "run-program", "gunicorn", "-c", "gunicorn.conf.py", "pepy.infrastructure.web.__init__:app"]