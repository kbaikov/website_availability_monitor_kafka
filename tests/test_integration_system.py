import configparser
from pathlib import Path

import psycopg2
import pytest

from website_availability_monitor_kafka.consumer import get_from_kafka_and_store
from website_availability_monitor_kafka.monitor import get_status
from website_availability_monitor_kafka.producer import send_to_kafka


@pytest.mark.skip(reason="A big system test not to be frequently run in CI")
def test_system():
    """Test the whole cycle of application with all modules involved.

    Create a result dict from monitor.
    Send the data to kafka with producer
    Get the data from kafka and store it in db.
    Check if db contains the data."""

    config_ini = Path(".") / "config.ini"
    config = configparser.ConfigParser(delimiters=("="))
    config.read(config_ini)

    result = get_status("http://google.com", "doctype html")
    send_to_kafka(message=result, **config["kafka"])
    get_from_kafka_and_store(**config["kafka"])

    conn = psycopg2.connect(config["kafka"]["postgres_service_uri"])
    with conn:
        with conn.cursor() as cursor:
            last_row = cursor.execute(
                "SELECT site, status_code FROM monitor WHERE id=(select max(id) from monitor);"
            )

    assert last_row == ("http://google.com", 200)
