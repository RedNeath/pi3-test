import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:3000/v1"
NUM_CLIENTS = 10
DURATION = 60 # 3600  # 1 heure en secondes

# Types de chargement disponibles (hors EMPTY)
LOAD_TYPES = ["PACKAGE", "STANDARD", "WIDE_LOAD"]

def get_places():
    """Récupère la liste complète des lieux."""
    response = requests.get(f"{BASE_URL}/places")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur lors de la récupération des lieux: {response.status_code}")

def create_transport_request(from_place, to_place, load_type, quantity):
    """Crée une demande de transport."""
    payload = {
        "from": from_place,
        "to": to_place,
        "loadType": load_type,
        "quantity": quantity,
        "requestedAt": datetime.now().isoformat()
    }
    response = requests.post(f"{BASE_URL}/transport-requests", json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Erreur lors de la création de la demande: {response.status_code}")

def simulate_client(client_id):
    """Simule le flux d'un client."""
    start_time = time.time()
    while time.time() - start_time < DURATION:
        try:
            # 1. Récupérer la liste des lieux
            places = get_places()
            if not places:
                print(f"Client {client_id}: Aucun lieu disponible.")
                time.sleep(1)
                continue

            # 2. Choisir aléatoirement un lieu de départ et une destination
            from_place = random.choice(places)
            to_place = random.choice(places)

            # 3. Choisir aléatoirement un type de chargement et une quantité
            load_type = random.choice(LOAD_TYPES)
            quantity = random.randint(120, 200000)

            # 4. Créer une demande de transport
            result = create_transport_request(from_place, to_place, load_type, quantity)
            print(f"Client {client_id}: Demande créée avec succès (ID: {result.get('id')})")

        except Exception as e:
            print(f"Client {client_id}: Erreur - {str(e)}")

        # Attendre un peu avant la prochaine itération
        time.sleep(1)

def main():
    """Lance les clients concurrents."""
    print(f"Lancement de {NUM_CLIENTS} clients pour une durée de {DURATION} secondes...")
    with ThreadPoolExecutor(max_workers=NUM_CLIENTS) as executor:
        futures = [executor.submit(simulate_client, i) for i in range(NUM_CLIENTS)]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()

