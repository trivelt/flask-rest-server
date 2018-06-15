from flask_api import status


def assert_status_code_equal(response, expected):
    received = response.status
    if str(expected) in received:
        return
    raise AssertionError("Status code not equal: " + str(expected) + " != " + received)


def assert_success(response):
    assert_status_code_equal(response, status.HTTP_200_OK)
