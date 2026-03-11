import os
from dotenv import load_dotenv

load_dotenv()

RAILS_API_URL = os.environ.get("RAILS_API_URL", "http://localhost:3000/api/v1")
DASH_HOST = os.environ.get("DASH_HOST", "0.0.0.0")
DASH_PORT = int(os.environ.get("DASH_PORT", "8050"))
DASH_DEBUG = os.environ.get("DASH_DEBUG", "true").lower() == "true"
