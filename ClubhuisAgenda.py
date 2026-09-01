from variables import *

from msal import ConfidentialClientApplication
import requests
import pandas as pd
from datetime import datetime


## Make Connection

app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET
)

token = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

access_token = token["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}"
}

## Get Site ID

url = (
    f"https://graph.microsoft.com/v1.0/sites/"
    f"{HOST_NAME}:/sites/{SITE_NAME_Clubhuis_Agenda}"
)

response = requests.get(
    url,
    headers=headers
)

response.raise_for_status()

site = response.json()

SITE_ID = site["id"]

print(f"Site gevonden: {site['displayName']}")
print(f"SITE_ID: {SITE_ID}")

## Get Drives

url = (
    f"https://graph.microsoft.com/v1.0/sites/"
    f"{SITE_ID}/drives"
)

response = requests.get(
    url,
    headers=headers
)

response.raise_for_status()

drives = response.json()["value"]

for drive in drives:
    print(
        f"Naam: {drive['name']} | "
        f"ID: {drive['id']}"
    )

## Find Documents library

DRIVE_ID = None

for drive in drives:

    if drive["name"].lower() in [
        "documenten",
        "documents"
    ]:

        DRIVE_ID = drive["id"]

        break

if DRIVE_ID is None:
    raise Exception(
        "Geen documentenbibliotheek gevonden"
    )

print(f"DRIVE_ID = {DRIVE_ID}")

## Show all files

url = (
    f"https://graph.microsoft.com/v1.0/drives/"
    f"{DRIVE_ID}/root/children"
)

response = requests.get(
    url,
    headers=headers
)

response.raise_for_status()

for item in response.json()["value"]:
    print(item["name"])

## Download Excel

FILE_NAME = "ClubhuisAgenda.xlsx"

url = (
    f"https://graph.microsoft.com/v1.0/drives/"
    f"{DRIVE_ID}/root:/{FILE_NAME}:/content"
)

response = requests.get(
    url,
    headers=headers
)

response.raise_for_status()

with open(FILE_NAME, "wb") as f:
    f.write(response.content)

print(f"{FILE_NAME} gedownload")



df = pd.read_excel(FILE_NAME)

print(df.head())
print(df.columns.tolist())

import json

events = []

for _, row in df.iterrows():

    start = (
        f"{row['Datum'].strftime('%Y-%m-%d')}"
        f"T{row['Starttijd'].strftime('%H:%M:%S')}"
    )

    end = (
        f"{row['Datum'].strftime('%Y-%m-%d')}"
        f"T{row['Eindtijd'].strftime('%H:%M:%S')}"
    )

    events.append({
        "title": row["Activiteit"],
        "start": start,
        "end": end,
        "organisatie": row["Organisatie"],
        "locatie": row["Locatie"],
        "opmerking": "" if pd.isna(row["Opmerking"]) else row["Opmerking"]
    })


output = {
    "last_updated": datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    ),
    "events": events
}

with open(
    "events.json",
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        output,
        json_file,
        indent=4,
        ensure_ascii=False
    )
print("events.json aangemaakt")
print(f"{len(events)} events geëxporteerd")
