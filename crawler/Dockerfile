FROM python:3.8.7-slim-buster

# Set environment variables.
# Force Python stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    locales \
 && rm -rf /var/lib/apt/lists/*

# Set the locale
# src: https://stackoverflow.com/a/28406007/5732518
RUN sed -i '/de_DE.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE:de
ENV LC_ALL de_DE.UTF-8

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /code

# Copy the source code of the project into the container.
COPY . .

RUN chmod +x crawl.sh

# Persist bash history (see docker-compose file)
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo $SNIPPET >> "/root/.bashrc"
