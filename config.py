import os
from dotenv import load_dotenv

load_dotenv()

# Google Cloud Storage
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "ansocial")
GCS_FOLDER_PATH = os.getenv("GCS_FOLDER_PATH", "ansocial1/")

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Meta API (Facebook & Instagram)
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

# App Settings
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
LOGO_PATH = "logo.png"
POSTED_LOG = "posted_log.json"
HISTORY_LOG = "caption_history.json"  # tracks last 10 captions to avoid repetition
