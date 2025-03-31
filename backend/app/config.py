import os
from datetime import timedelta
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)


# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "G3N3R1CK3Y")

    # MongoDB
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_SSL = False  # Disable SSL
    MONGO_SSL_CERT_REQS = None  # Don't verify certificates
    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "G3N3R1CK3Y")
    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 3600)
    )  # 1 hour
