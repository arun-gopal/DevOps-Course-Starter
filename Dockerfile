FROM python:3.8 as base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /todo_app
COPY pyproject.toml poetry.lock /todo_app/
COPY ./todo_app /todo_app/todo_app

### PRODUCTION ###
FROM base as production
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "gunicorn", "-b",  "0.0.0.0:8000", "todo_app.app:create_app()"]
EXPOSE 8000

### DEVELOPMENT ###
FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
EXPOSE 5000
