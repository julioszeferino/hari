from hari_data.exceptions import HariError


def test_hari_error_msg():
    # ---- Arrange ----
    message = 'This is a test error message'
    # ---- Act ----
    result = str(HariError(message))
    # ---- Assert ----
    assert result == message
