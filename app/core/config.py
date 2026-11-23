import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = os.getenv("APP_NAME", "AeroVision")

    AVIATIONSTACK_API_KEY = os.getenv(
        "AVIATIONSTACK_API_KEY"
    )

    AVIATIONSTACK_BASE_URL = os.getenv(
        "AVIATIONSTACK_BASE_URL",
        "http://api.aviationstack.com/v1"
    )


settings = Settings()