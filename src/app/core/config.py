import os
from dotenv import load_dotenv

load_dotenv(".env")

CELERY_BROKER = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BACKEND = os.environ.get("CELERY_RESULT_BACKEND",  "redis://redis:6379/0")