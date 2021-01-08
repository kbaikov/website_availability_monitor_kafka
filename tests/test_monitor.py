import pytest

from website_availability_monitor_kafka.monitor import get_status


@pytest.mark.parametrize(
    "input, expected",
    (
        (("http://google.com", "doctype html"), (200, "OK", "Content matches")),
        (("http://google.com", "foobar"), (200, "OK", "Content does not match")),
        (("http://google.com", ""), (200, "OK", "")),
        (("http://foobar.com", ""), (403, "Forbidden", "")),
        (("https://httpstat.us/404", ""), (404, "Not Found", "")),
    ),
)
def test_get_status(input, expected) -> None:
    """Check the relevant fields in results dict"""

    results_dict = get_status(*input)
    assert (
        results_dict["status_code"],
        results_dict["reason"],
        results_dict["expected_contents"],
    ) == expected
