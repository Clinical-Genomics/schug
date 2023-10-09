FROM clinicalgenomics/python3.11-venv:1.0

LABEL about.home="https://github.com/Clinical-Genomics/schug"
LABEL about.license="MIT License (MIT)"

# Install base dependencies
RUN apt-get update && \
     apt-get -y upgrade && \
     apt-get -y install -y --no-install-recommends default-libmysqlclient-dev && \
     apt-get clean && \
     rm -rf /var/lib/apt/lists/*


# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Create a worker user
RUN groupadd --gid 1000 worker && useradd -g worker --uid 1000 --create-home worker

# Install and run commands from virtual environment
RUN python3 -m venv /home/worker/venv
ENV PATH="/home/worker/venv/bin:$PATH"

# Install app
WORKDIR /home/worker/app
COPY --chown=worker:worker . /home/worker/app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

# Run commands as non-root
USER worker

CMD gunicorn\
    --config gunicorn.conf.py \
    schug.main:app
