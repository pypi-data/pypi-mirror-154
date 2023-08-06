from typing import Any, Callable


class MunchieResponse(object):
    def __init__(self, ok: bool = True, log_level: str = "info", message: Any = None):
        self.ok = ok
        self.log_level = log_level
        self.message = message

    def __str__(self):
        return f"{self.log_level.upper()}: {self.message}"


def validate_response(func: Callable):
    """Validate the MunchieResponse for a function."""

    def validate(*args, **kwargs):
        response = func(*args, **kwargs)

        if not response.ok:
            raise response.message

        return response

    return validate
