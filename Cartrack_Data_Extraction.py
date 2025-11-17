import requests
import base64
import datetime
import calendar
import numpy as np

# ===============================================
# A. AUTHENTICATION CONFIG
# ===============================================

CARTRACK_USERNAME = "STON00001"
CARTRACK_TOKEN = "390c2813f5d15abf7d8ae3f3d7817aeff6161cd6719fde87301e9e77521a5985"

# Combine username and token for Basic Auth
credentials = f"{CARTRACK_USERNAME}:{CARTRACK_TOKEN}".encode("ascii")
encoded_credentials = base64.b64encode(credentials).decode("ascii")

CARTRACK_HEADERS = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json"
}

EMPTY_PAYLOAD = {}

# ===============================================
# B. FETCH VEHICLE LIST
# ===============================================

VEHICLE_LIST_URL = "https://fleetapi-ph.cartrack.com/rest/vehicles?page=1&limit=100"

vehicle_response = requests.get(VEHICLE_LIST_URL, headers=CARTRACK_HEADERS)
vehicle_data = vehicle_response.json()

# Extract all registration numbers
vehicle_registrations = [v["registration"] for v in vehicle_data["data"]]

# ===============================================
# C. DATE RANGE CONFIG
# ===============================================

current_date = datetime.datetime.now()
current_year = current_date.year

TARGET_MONTH = 11  # November
start_date = datetime.datetime(current_year, TARGET_MONTH, 1)
_, days_in_month = calendar.monthrange(current_year, TARGET_MONTH)
end_date = datetime.datetime(current_year, TARGET_MONTH, days_in_month)

MONTH_NAME = start_date.strftime("%B")

start_timestamp = start_date.strftime("%Y-%m-%d 00:00:00")
end_timestamp = end_date.strftime("%Y-%m-%d 23:59:59")

# ===============================================
# D. CLICKUP CONFIG
# ===============================================

CLICKUP_TOKEN = "pk_101500067_2P59PVFI7VASGUXFE6AXJ68R9RI6UHVZ"
CLICKUP_HEADERS = {
    "Authorization": CLICKUP_TOKEN,
    "Content-Type": "application/json"
}

CLICKUP_LIST_ID = "901813327357"
CLICKUP_CREATE_TASK_URL = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"

# Custom field IDs
DISTANCE_FIELD_ID = "cf44c753-73c0-4c67-b2e8-52ba41068022"
VEHICLE_FIELD_ID = "295ad09a-66ad-4104-9e79-a0a9400600ab"
STARTDATE_FIELD_ID = "43ebd6e9-cd9a-4463-b2af-e3759095146a"
FUEL_FIELD_ID = "7ca3079e-3ffb-4cb2-bddd-6ba1fc08a18e"

CLICKUP_CUSTOM_FIELD_URL = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/field"

# ===============================================
# E. PROCESS EACH VEHICLE
# ===============================================

for reg in vehicle_registrations:

    # ---- Cartrack URLs ----
    odometer_url = (
        f"https://fleetapi-ph.cartrack.com/rest/vehicles/{reg}/odometer"
        f"?start_timestamp={start_timestamp}&end_timestamp={end_timestamp}"
    )

    fuel_level_url = (
        f"https://fleetapi-ph.cartrack.com/rest/fuel/level/{reg}"
        f"?start_timestamp={start_timestamp}&end_timestamp={end_timestamp}"
    )

    fuel_fill_url = (
        f"https://fleetapi-ph.cartrack.com/rest/fuel/fills/{reg}"
        f"?start_timestamp={start_timestamp}&end_timestamp={end_timestamp}"
    )

    # ---- Fetch odometer data ----
    odometer_response = requests.get(odometer_url, headers=CARTRACK_HEADERS)
    odometer_data = odometer_response.json()["data"]

    # ---- Fetch ClickUp dropdown options ----
    dropdown_response = requests.get(CLICKUP_CUSTOM_FIELD_URL, headers=CLICKUP_HEADERS)
    dropdown_data = dropdown_response.json()
    vehicle_options = dropdown_data["fields"][0]["type_config"]["options"]

    # ---- Fetch fuel level and fills ----
    fuel_level_data = requests.get(fuel_level_url, headers=CARTRACK_HEADERS).json()["data"]
    fuel_fills_data = requests.get(fuel_fill_url, headers=CARTRACK_HEADERS).json()["data"]

    start_fuel = fuel_level_data["start_period"]["liters"]
    end_fuel = fuel_level_data["end_period"]["liters"]

    fuel_filled_total = sum(fill["fill_amount_litres"] for fill in fuel_fills_data)

    fuel_consumed = (
        None
        if (start_fuel is None or end_fuel is None)
        else abs((end_fuel - start_fuel) + fuel_filled_total)
    )

    print(f"Vehicle: {odometer_data['registration']}")
    print(f"Distance: {odometer_data['distance']} km")
    print(f"Fuel Consumption: {fuel_consumed}\n")

    # ---- Match registration to ClickUp dropdown option ----
    matched_vehicle_id = None
    for option in vehicle_options:
        if option["name"] == odometer_data["registration"]:
            matched_vehicle_id = option["id"]
            break

    # ---- Prepare ClickUp payload ----
    task_payload = {
        "name": f"{MONTH_NAME} Vehicle - {odometer_data['registration']} Data",
        "custom_fields": [
            {"id": DISTANCE_FIELD_ID, "value": odometer_data["distance"]},
            {"id": VEHICLE_FIELD_ID, "value": matched_vehicle_id},
            {"id": STARTDATE_FIELD_ID, "value": int(start_date.timestamp() * 1000)},
            {"id": FUEL_FIELD_ID, "value": fuel_consumed}
        ]
    }

    # ---- Create ClickUp task ----
    requests.post(CLICKUP_CREATE_TASK_URL, json=task_payload, headers=CLICKUP_HEADERS)