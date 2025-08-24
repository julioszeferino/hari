import os
from typing import Any, Dict, Optional, Type


def validate_non_empty_string(value: str, field_name: str) -> Dict[str, str]:
    """
    Validate that a value is a non-empty string.

    Parameters:
        value (str): The value to validate.
        field_name (str): The name of the field being validated
        (for error messages).

    Returns:
        str: The validated non-empty string.

    Raises:
        ValueError: If the value is not a string or is an empty string.

    Examples:
        >>> validate_non_empty_string('example', 'app_name')
        {'value': 'example'}

        >>> validate_non_empty_string('', 'app_name')
        Traceback (most recent call last):
            ...
        ValueError: app_name must be a non-empty string.

        >>> validate_non_empty_string(None, 'app_name')
        Traceback (most recent call last):
            ...
        ValueError: app_name must be a string, got NoneType
    """
    if not isinstance(value, str):
        raise ValueError(
            f'{field_name} must be a string, got {type(value).__name__}'
        )

    if not value.strip():
        raise ValueError(f'{field_name} must be a non-empty string.')

    return {'value': value.strip()}


def validate_path_exists(path: str, field_name: str) -> Dict[str, str]:
    """
    >>> validate_path_exists('/valid/path', 'jars_path')  # doctest: +SKIP
    {'value': '/valid/path'}
    >>> validate_path_exists('/invalid/path', 'jars_path')  # doctest: +SKIP
    Traceback (most recent call last):
        ...
    ValueError: jars_path '/invalid/path' does not exist.
    """
    validate_non_empty_string(path, field_name)
    path = path.strip()
    if not os.path.exists(path):
        raise ValueError(f"{field_name} '{path}' does not exist.")
    return {'value': path}


def validate_type(
    value: Any, expected_type: Type, field_name: str
) -> Dict[str, Optional[Any]]:
    """
    Validate that a value is of the expected type.

    Parameters:
        value: The value to validate.
        expected_type (type): The expected type of the value.
        field_name (str): The name of the field being validated
        (for error messages).

    Returns:
        The value if it is of the expected type
        .
    Raises:
        ValueError: If the value is not of the expected type.

    Examples:
        >>> validate_type('example', str, 'app_name')
        {'value': 'example'}

        >>> validate_type(123, int, 'job_timeout')
        {'value': 123}

        >>> validate_type(123, str, 'app_name')
        Traceback (most recent call last):
            ...
        ValueError: app_name must be of type str, got int
    """
    if not isinstance(value, expected_type):
        raise ValueError(
            f'{field_name} must be of type {expected_type.__name__}, got {type(value).__name__}'
        )
    return {'value': value}
