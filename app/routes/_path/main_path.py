from dotenv import load_dotenv
import os
from fastapi import FastAPI


MAIN_URL=os.getenv("MAIN_URL")
API_URL=os.getenv("API_URL")