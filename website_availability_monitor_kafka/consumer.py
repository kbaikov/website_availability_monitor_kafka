import json
import logging

from kafka import KafkaConsumer  # type: ignore

from .postgress_store import store_data

logger = logging.getLogger(__name__)


def get_from_kafka_and_store(
    topic: str,
    service_uri: str,
    postgres_service_uri: str,
    ssl_cafile: str = "ca.pem",
    ssl_certfile: str = "service.cert",
    ssl_keyfile: str = "service.key",
) -> None:
    """Runs a Kafka consumer to get all the messages from kafka topic.

    The messages are expected to be json deserialasable.

    Args:
        topic (str): Configured Kafka topic
        service_uri (str): Kafka instance uri
        postgres_service_uri (str): Postgres connection string
        ssl_cafile (str, optional): Defaults to "ca.pem".
        ssl_certfile (str, optional):  Defaults to "service.cert".
        ssl_keyfile (str, optional): Defaults to "service.key".
    """
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=service_uri,
        auto_offset_reset="earliest",
        security_protocol="SSL",
        ssl_cafile=ssl_cafile,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile,
        consumer_timeout_ms=1000,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    consumer.subscribe([topic])
    for msg in consumer:
        message = msg.value
        store_data(postgres_service_uri, message)
        logger.info(f"{message} added to the table")
    consumer.close()
