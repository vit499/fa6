from time import time
import uvicorn
import logging
from app.settings import settings
from app.utils.logger.logger import logger


def main() -> None:
    logger.info("Initializing service")
    #init()
    # logger.info("Service finished initializing")

    logger.info(f"Starting server on port {settings.port}")
    logger.info(f"nvp_path = {settings.NVP_PATH}")
    # uvicorn.run("app.main:app", host=settings.host, port=settings.port, log_config=LOGGING_CONFIG, log_level="trace")
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, log_level="debug")


if __name__ == "__main__":
    main()
    # logger.info("Starting server on port %d", settings.port)
    # # uvicorn.run("app.main:app", host=settings.host, port=settings.port, log_config=LOGGING_CONFIG, log_level="trace")
    # uvicorn.run("app.main:app", host=settings.host, port=settings.port, log_level="error")