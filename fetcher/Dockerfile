FROM python:3.9

ENV PYTHONUNBUFFERED=0

COPY ./app /webapp
WORKDIR /webapp
RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "python", "-u", "run.py"]
