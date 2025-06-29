import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file if it exists
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.warning("OPENAI_API_KEY not set. LLM functionality will be limited.")

# Service URLs
PRODUCT_SEARCH_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8001/api/products")
ORDER_LOOKUP_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:8002/api/orders")

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True
        },
    },
}

# HTTP Client Configuration
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "30"))  # seconds
HTTP_RETRIES = int(os.getenv("HTTP_RETRIES", "3"))