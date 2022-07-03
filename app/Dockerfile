FROM python:3.8-slim-buster
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential netcat\
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
RUN adduser --home /app --system --group kr1p
WORKDIR /app
COPY --chown=kr1p:kr1p app .
RUN pip install -r requirements.txt 
USER kr1p
ENV PYTHONUNBUFFERED=1
CMD gunicorn



