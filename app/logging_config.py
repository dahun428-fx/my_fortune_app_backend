import logging
import os


def setup_logging():
    log_level = (
        logging.DEBUG
        if os.getenv("ENV", "development") == "development"
        else logging.WARNING
    )

    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
    )
