from __future__ import annotations

import io
import logging
import sys
from typing import Any

__all__ = [
    "SUMMARY",
    "logger",
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SUMMARY = io.StringIO()


class LevelFilter(logging.Filter):
    def __init__(self, max_level: int, *args: Any, **kwargs: Any) -> None:
        self.max_level = max_level
        super().__init__(*args, **kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < self.max_level


default_handler = logging.StreamHandler(sys.stdout)
default_handler.setLevel(logging.DEBUG)
default_handler.addFilter(LevelFilter(max_level=logging.ERROR))
logger.addHandler(default_handler)

error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)

summary_handler = logging.StreamHandler(SUMMARY)
summary_handler.setLevel(logging.DEBUG)
logger.addHandler(summary_handler)
