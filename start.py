from time import time
import uvicorn
import logging
from app.settings import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Initializing service")
    #init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
    logger.info(f"Starting server on port {settings.port}")
    uvicorn.run("app.main:app", port=settings.port)