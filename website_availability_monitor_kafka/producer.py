import json
import logging

from kafka import KafkaProducer  # type: ignore

logger = logging.getLogger(__name__)


def send_to_kafka(
    topic,
    message: dict,
    service_uri: str,
    postgres_service_uri: str,
    ssl_cafile: str = "ca.pem",
    ssl_certfile: str = "service.cert",
    ssl_keyfile: str = "service.key",
) -> None:
    """Creates a Kafka producer and sends the message dict as json.

    The topic must be already configured in Kafka

    Args:
        topic ([type]): Kafka topic to send to
        message (dict): Dict with a messasge
        service_uri (str): Kafka connection string
        postgres_service_uri (str): Postgres connection string (not used but kept for similar function signature)
        ssl_cafile (str, optional): Defaults to "ca.pem".
        ssl_certfile (str, optional): Defaults to "service.cert".
        ssl_keyfile (str, optional): Defaults to "service.key".
    """
    producer = KafkaProducer(
        bootstrap_servers=service_uri,
        security_protocol="SSL",
        ssl_cafile=ssl_cafile,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )

    logger.info(f"Sending: {message}")
    producer.send(topic, message)

    # Wait for all messages to be sent
    producer.flush()
