import os
import uuid
import json
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.storage.blob import BlobServiceClient, ContainerClient

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Połączenie z Azure Storage
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "smartscale-data"

# Inicjalizacja Blob Service
try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
except Exception as e:
    print(f"Błąd połączenia z Azure: {e}")
    blob_service_client = None
    container_client = None

# Model danych pomiarowych
class Measurement(BaseModel):
    user_id: str
    weight: float
    fat_percentage: float
    water_percentage: float
    timestamp: str | None = None

# Inicjalizacja FastAPI
app = FastAPI(
    title="Smart Scale API",
    description="API do obsługi danych z inteligentnej wagi.",
    version="1.0.0"
)

# middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.on_event("startup")
async def startup_event():
    if container_client:
        try:
            container_client.get_container_properties()
            print(f"Pomyślnie połączono z kontenerem '{container_name}'.")
        except Exception as e:
            print(f"Błąd: Kontener '{container_name}' nie istnieje lub wystąpił problem z dostępem. {e}")

@app.post("/api/measurements", status_code=201)
async def create_measurement(measurement: Measurement):
    if not container_client:
        raise HTTPException(status_code=500, detail="Brak połączenia z usługą Azure Blob Storage.")

    try:
        # Ustawienie timestamp
        current_time = datetime.utcnow().isoformat()
        measurement.timestamp = current_time
        
        blob_name = f"{measurement.user_id}/{current_time}.json"
        data_to_upload = measurement.model_dump_json()
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data_to_upload, overwrite=True)
        print(f"Zapisano pomiar w Azure Blob Storage jako: {blob_name}")
        return {"status": "success", "blob_name": blob_name}
    except Exception as e:
        print(f"Błąd podczas zapisu do Azure: {e}")
        raise HTTPException(status_code=500, detail=f"Wystąpił błąd serwera podczas zapisu danych: {e}")

@app.get("/api/measurements/{user_id}")
async def get_user_measurements(user_id: str):
    if not container_client:
        raise HTTPException(status_code=500, detail="Brak połączenia z usługą Azure Blob Storage.")

    try:
        blob_list = container_client.list_blobs(name_starts_with=f"{user_id}/")
        measurements = []
        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob.name)
            stream = blob_client.download_blob()
            data = stream.readall()
            measurements.append(json.loads(data))
        
        if not measurements:
            raise HTTPException(status_code=404, detail="Nie znaleziono pomiarów dla tego użytkownika.")

        return measurements
    except Exception as e:
        print(f"Błąd podczas odczytu z Azure: {e}")
        raise HTTPException(status_code=500, detail=f"Wystąpił błąd serwera podczas odczytu danych: {e}")