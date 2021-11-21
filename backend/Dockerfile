FROM python:3.9

COPY ./app /webApp
WORKDIR /webApp
RUN pip install pipenv
RUN pipenv install

EXPOSE 8000
CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "app:app"]
