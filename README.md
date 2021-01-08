# Website monitor

Monitors website availability over the
network, produces metrics about this and passes these events through a
Kafka instance into a PostgreSQL database.

The metrics include HTTP response time, error code returned,
as well as optionally checking the returned page contents for a regexp patternt
hat is expected to be found on the page.

Kafka producer which periodically checks the target
websites and sends the check results to a Kafka topic, and a Kafka consumer
storing the data to a PostgreSQL database.

The website checker should perform the checks periodically and collect the
HTTP response time, error code returned, as well as optionally checking the
returned page contents for a regexp pattern that is expected to be found on the
page.

# Configuration

Create a config.ini file with the following data inside:

```ini
[kafka]
topic = kafka-test
service_uri = <uri string obrained from you kafka console>
postgres_service_uri = <postgres connection string from your db console>
ssl_cafile = ca.pem
ssl_certfile = service.cert
ssl_keyfile = service.key

[sites]
http://google.com = doctype html
```

Make sure you download the mentioned certificate files from your service config console.
Kafka topic should be created before running the script

Fill in the `sites` section of the ini. It will produce a tubple containing
a web site you want to check and a string you expect to find on the website.
E.g. ('http://google.com', 'doctype html')


# Usage

From the repo root folder the package can be installed in your current venv with `poetry install`
and/or run as a module directly by using:

```bash
python -m website_availability_monitor_kafka --producer
```

or

```bash
python -m website_availability_monitor_kafka --consumer
```

Optional --config option can be supplied with a configuration file name. (default: config.ini)

See `python -m website_availability_monitor_kafka --help` for available arguments


# Contribution

Clone the repository, create a virtual env and install the dependencies with poetry

```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
```

Poetry will install all the dependencies declared in pyproject.toml
However feel free to generate requirements.txt file for your legacy systems:

```bash
poetry export --dev -f requirements.txt --output requirements.txt --without-hashes
```

The codes is black formated and isorted with `isort --profile black`
To run the tests execute: `pytest`
The tests are also configured to run in github actions on every push.

To run the optional type checker execute: `mypy website_availability_monitor_kafka`
The type check of the third party libraries is ignored

# Packaging

To generate pure Python wheels run:

```bash
poetry build
```

Find the archive and whl files in dist filder after the build completes.
