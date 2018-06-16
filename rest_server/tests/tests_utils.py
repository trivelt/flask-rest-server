from flask_api import status


def assert_status_code_equal(response, expected):
    received = response.status
    if str(expected) in received:
        return
    raise AssertionError("Status code not equal: " + str(expected) + " != " + received)


def assert_success(response):
    assert_status_code_equal(response, status.HTTP_200_OK)


def assert_successfully_created(response):
    assert_status_code_equal(response, status.HTTP_201_CREATED)


def assert_unordered_list_equal(actual, expected):
    if not (len(actual) == len(expected) and sorted(actual) == sorted(expected)):
        raise AssertionError("Lists are not equal: " + str(actual) + " != " + str(expected))
