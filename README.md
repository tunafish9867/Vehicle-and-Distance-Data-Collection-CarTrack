# Vehicle Fuel & Distance Automation Script

This project automates the retrieval of vehicle odometer and fuel consumption data from **Cartrack API** and automatically creates monthly tasks in **ClickUp** with the processed data.

The script is fully automated and designed for monthly reporting, fleet tracking, and operations management.

---

## 🚗 Project Overview

This Python script:

1. Authenticates with **Cartrack API**
2. Retrieves all vehicle registrations
3. Computes:

   * Total distance travelled per vehicle
   * Fuel consumption based on start/end fuel levels and fuel fills
4. Matches each vehicle with the corresponding **ClickUp dropdown option**
5. Creates a **ClickUp task** for each vehicle with custom field values
6. Generates a clean, consistent monthly report

---

## 📁 File Structure

```
project/
│── vehicle_fuel_clickup.py     # Main script
│── README.md                   # Documentation
```

---

## 🔧 Requirements

Install the required dependencies:

```bash
pip install requests
pip install numpy
```

---

## 🔑 API Keys Needed

### 1. **Cartrack API Credentials**

* Username
* Token (Basic Auth)

### 2. **ClickUp API Token**

* Required for creating tasks
* Obtain from ClickUp settings

> Make sure to keep all API keys private and never commit them directly in public repositories.

---

## 🧠 How the Script Works

### 1. **Cartrack Authentication**

Encodes username and token using Base64 for API headers.

### 2. **Fetch Vehicle List**

Retrieves all vehicles under the account and extracts their registration numbers.

### 3. **Date Range Setup**

Automatically computes the start and end of the target month (set to November by default).

### 4. **Fetch Data per Vehicle**

For each vehicle:

* Odometer distance is fetched
* Fuel levels (start/end) are obtained
* Fuel fills are summed
* Fuel consumed is computed

### 5. **ClickUp Integration**

Creates a task per vehicle with fields:

* Distance traveled
* Vehicle name (dropdown)
* Reporting month
* Fuel consumption

---

## 🗂️ Custom Fields Used

| Field Name              | ClickUp Field ID                       |
| ----------------------- | -------------------------------------- |
| Distance                | `cf44c753-73c0-4c67-b2e8-52ba41068022` |
| Vehicle Name (Dropdown) | `295ad09a-66ad-4104-9e79-a0a9400600ab` |
| Start Date              | `43ebd6e9-cd9a-4463-b2af-e3759095146a` |
| Fuel Consumed           | `7ca3079e-3ffb-4cb2-bddd-6ba1fc08a18e` |

---

## 📝 Usage

Run the script manually:

```bash
python3 vehicle_fuel_clickup.py
```

Or include inside an automated workflow.

---

Run the script manually:

```bash
python3 vehicle_fuel_clickup.py
```

Or include inside an automated workflow.

---

## 📌 Notes

* Ensure all API keys are valid
* Script requires correct custom field IDs in ClickUp
* If Cartrack API changes schema, parsing logic may need updates

---

## 🙌 Author

Created for fleet and operations automation workflows.
