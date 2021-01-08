"""Monitor websites functions"""
import logging

import requests

logger = logging.getLogger(__name__)


def get_status(site: str, page_contents: str = "") -> dict:
    """Returns a dictionary with
    status_code
    text corresponding to the status code
    response_time
    expected_contents check results
    as keys for a given site.

    All taken from the requests Response object
    Optionally checking the returned page contents for a pattern
    that is expected to be found on the page.
    """
    response_time: float = 0
    expected_contents = ""
    try:
        # this could be a faster requests.head method
        response = requests.get(site, timeout=5, allow_redirects=True)
        status_code = response.status_code
        reason = response.reason
        response_time = response.elapsed.total_seconds()
        if page_contents:
            if page_contents in response.text:
                expected_contents = "Content matches"
            else:
                expected_contents = "Content does not match"
    except requests.exceptions.ConnectionError:
        status_code = 0
        reason = "ConnectionError"
    except requests.exceptions.ReadTimeout:
        status_code = 1
        reason = "TimeOut"
    return {
        "site": site,
        "status_code": status_code,
        "reason": reason,
        "response_time": response_time,
        "expected_contents": expected_contents,
    }
