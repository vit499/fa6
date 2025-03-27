import os
from dotenv import load_dotenv


class Settings:

    load_dotenv(override=True)
    port = int(os.getenv("PORT"))
    host = os.getenv("HOST")

    NVP_PATH = os.getenv("NVP_PATH")
    # port = 8002

settings = Settings()


