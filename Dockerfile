FROM python:3.8 as base
RUN echo "--- Installing Poetry ---"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
RUN mkdir /app
COPY ./poetry.lock /app
COPY ./pyproject.toml /app
WORKDIR /app

### PRODUCTION ###
FROM base as production
RUN poetry install --no-dev
COPY . /app
ENTRYPOINT ["poetry", "run", "gunicorn", "-b",  "0.0.0.0:8000", "todo_app.app:create_app()"]
EXPOSE 8000

### DEVELOPMENT ###
FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]
EXPOSE 5000
