# config/logging.py

import sys
import structlog
from structlog.processors import JSONRenderer, TimeStamper, add_log_level
from structlog.stdlib import LoggerFactory, filter_by_level

def configure_logging():
    structlog.configure(
        processors=[
            filter_by_level,
            add_log_level,
            TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            JSONRenderer()
        ],
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Настройка корневого логгера
    root_logger = structlog.get_logger()
    handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(handler)
    return root_logger