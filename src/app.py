import os
import pathlib
from dotenv import load_dotenv
from functools import lru_cache
from .airtable import Airtable
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()


@lru_cache()
def cached_dotenv():
    load_dotenv()


cached_dotenv()

AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")

BASE_DIR = pathlib.Path(__file__).parent  # src
templates = Jinja2Templates(directory=BASE_DIR/"templates")

print("Base Dir = ", BASE_DIR)
print(AIRTABLE_BASE_ID)
print(AIRTABLE_API_KEY)
print(AIRTABLE_TABLE_NAME)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
def home_signup_view(request: Request, email: str = Form(...), user_name: str = Form(...)):
    """
    TODO 
    Add CSRF for security
    """

    # to send data to airtable
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
        table_name=AIRTABLE_TABLE_NAME
    )
    did_send = airtable_client.create_records({"Name": user_name, "Email": email})
    return templates.TemplateResponse("home.html", {"request": request, "submitted_email": email, "user_id": user_name, "did_send": did_send})
