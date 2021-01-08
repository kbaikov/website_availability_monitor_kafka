import argparse
import configparser
import logging
import time

from .consumer import get_from_kafka_and_store
from .monitor import get_status
from .producer import send_to_kafka

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


help_text = """
Producer gets status_code, text corresponding to the status code and response_time
of a given site and sends it to Kafka instance.


Consumer gets the same info from Kafka instance and sends all to Postgress server.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=help_text)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--consumer",
        action="store_true",
        default=False,
        help="Run Kafka consumer",
    )
    group.add_argument(
        "--producer",
        action="store_true",
        default=False,
        help="Run Kafka producer",
    )
    parser.add_argument("--config", default="config.ini", help="Config file name")
    return parser.parse_args()


def main():
    args = parse_args()

    config = configparser.ConfigParser(delimiters=("="))
    config.read(args.config)

    if args.producer:
        try:
            while True:
                for site in config["sites"].items():
                    result = get_status(*site)
                    send_to_kafka(message=result, **config["kafka"])
                    time.sleep(5)
        except KeyboardInterrupt:
            return
    elif args.consumer:
        get_from_kafka_and_store(**config["kafka"])


if __name__ == "__main__":
    exit(main())
