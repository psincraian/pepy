#
FROM python:3.8 as requirements-stage

#
WORKDIR /tmp

#
RUN pip install pipenv

#
COPY ./Pipfile* /tmp/

#
RUN pipenv requirements --dev > requirements.txt

#
FROM python:3.8 as pepy-test

#
WORKDIR /code

#
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


#
COPY ./tests /code/tests