import requests
from datetime import datetime
import os

GENDER = "female"
WEIGHT_KG = "180"
HEIGHT_CM = "180"
AGE = "21"

APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheets_endpoint = os.environ["https://docs.google.com/spreadsheets/d/1bkoDMhN6c-Ngcb6pEDqUEy-M8vYtTfsYNfGJJs4lQeI/edit#gid=0"]

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}

for exercise in result["exercises"]:
    sheets_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheets_response = requests.post(sheets_endpoint, json=sheets_inputs, headers=bearer_headers)

    print(sheets_response.text)
