
import requests
import json
import time
import random
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000/api/measurements"

def generate_realistic_measurement():
    """
    Generuje pojedynczy, realistyczny pomiar wagi.
    """
    # Losowy user
    user_id = f"user{random.randint(1, 9)}"

    # Waga w kg
    weight = round(random.uniform(60.0, 90.0), 2)
    
    # Procent tkanki tłuszczowej
    fat_percentage = round(random.uniform(15.0, 35.0), 2)
    
    # Procent wody w organizmie
    water_percentage = round(random.uniform(45.0, 65.0), 2)
    
    return {
        "user_id": user_id,
        "weight": weight,
        "fat_percentage": fat_percentage,
        "water_percentage": water_percentage
    }

def run_simulator():
    """
    Uruchamia symulator, który w pętli wysyła dane do backendu.
    """
    print("Uruchamiam symulator wagi...")
    print(f"Dane będą wysyłane na adres: {BACKEND_URL}")
    print("Symulacja dla losowych użytkowników (user1-user9).")
    print("Naciśnij CTRL+C, aby zakończyć.")

    while True:
        try:
            measurement_data = generate_realistic_measurement()
            
            print(f"\nWysyłanie pomiaru: {measurement_data}")
            
            response = requests.post(BACKEND_URL, json=measurement_data)
            
            # Sprawdzenie odpowiedzi serwera
            if response.status_code == 201:
                print(f"Odpowiedź serwera: {response.status_code} - Pomiar został pomyślnie zapisany.")
                print(f"Szczegóły: {response.json()}")
            else:
                print(f"Błąd! Serwer odpowiedział kodem: {response.status_code}")
                print(f"Treść odpowiedzi: {response.text}")

            time.sleep(10)

        except requests.exceptions.ConnectionError:
            print("\nBłąd połączenia. Czy backend jest uruchomiony?")
            print("Spróbuję ponownie za 10 sekund...")
            time.sleep(10)
        except KeyboardInterrupt:
            print("\nZamykanie symulatora.")
            break
        except Exception as e:
            print(f"\nWystąpił nieoczekiwany błąd: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_simulator()
