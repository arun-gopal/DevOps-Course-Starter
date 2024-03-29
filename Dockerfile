FROM python:3.8 as base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /todo_app
COPY pyproject.toml poetry.lock /todo_app/

### PRODUCTION ###
FROM base as production
RUN poetry install --no-dev
COPY ./todo_app /todo_app/todo_app
ENTRYPOINT ["poetry", "run", "gunicorn", "-b",  "0.0.0.0:8000", "todo_app.app:create_app()"]
EXPOSE 8000

### TEST ###
FROM base as test
RUN poetry install
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver
COPY ./todo_app /todo_app/todo_app
ENTRYPOINT ["poetry", "run", "pytest"]

### DEVELOPMENT ###
FROM base as development
RUN poetry install
COPY ./todo_app /todo_app/todo_app
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
EXPOSE 5000
