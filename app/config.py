import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PATIENT_BOT_TOKEN = os.getenv("PATIENT_BOT_TOKEN", "")
DOCTOR_BOT_TOKEN = os.getenv("DOCTOR_BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "data/app.db")

MAX_OPINIONS_PER_CASE = 5
SLA_HOURS = 3

Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
