from dotenv import load_dotenv
import os
from fastapi import FastAPI

load_dotenv()

# App(Client ID)
MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI")
REDIRECT_URL_HOME = os.getenv("REDIRECT_URL_HOME")

# Get token
MS_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

# Get Info From MS
MS_USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"
MS_AUTHORITY = "https://login.microsoftonline.com/common"
MS_PROFILE_PHOTO = "https://graph.microsoft.com/v1.0/me/photo/$value"


