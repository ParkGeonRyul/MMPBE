from dotenv import load_dotenv
import os
from fastapi import FastAPI

load_dotenv()

MAIN_URL=os.getenv("MAIN_URL")
API_URL=os.getenv("API_URL")