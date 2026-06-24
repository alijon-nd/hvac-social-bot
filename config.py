import os
from dotenv import load_dotenv

load_dotenv()

# Google Cloud
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "ansocial")
GCS_FOLDER_PATH = os.getenv("GCS_FOLDER_PATH", "ansocial1/")

# OpenRouter (free)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Meta (later)
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

# Settings
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
LOGO_PATH = "logo.png"
POSTED_LOG = "posted_log.json"
