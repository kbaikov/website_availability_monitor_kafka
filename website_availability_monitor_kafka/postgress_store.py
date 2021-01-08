import logging

import psycopg2  # type: ignore

logger = logging.getLogger(__name__)


def create_table(service_uri: str) -> None:
    """Creates table monitor if it does not already exist.
    CREATE TABLE IF NOT EXISTS monitor

    Args:
        service_uri (str): Postgres connection string
    """
    create_string = """
    CREATE TABLE IF NOT EXISTS monitor
    (
        id              SERIAL  PRIMARY KEY,
        site                VARCHAR,
        status_code         VARCHAR,
        reason              VARCHAR,
        response_time       FLOAT,
        expected_contents   VARCHAR
    );
    """
    conn = psycopg2.connect(service_uri)
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(create_string)


def store_data(service_uri: str, message_dict: dict) -> None:
    """
    Insert the message dictionary into the monitor table
    """
    create_table(service_uri)
    conn = psycopg2.connect(service_uri)
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO monitor (site, status_code, reason, response_time, expected_contents) VALUES (%s, %s, %s, %s, %s);",
                (
                    message_dict["site"],
                    message_dict["status_code"],
                    message_dict["reason"],
                    message_dict["response_time"],
                    message_dict["expected_contents"],
                ),
            )
