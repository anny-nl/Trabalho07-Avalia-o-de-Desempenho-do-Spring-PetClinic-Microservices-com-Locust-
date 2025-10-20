import requests
import random
from faker import Faker
from datetime import date

# Inicializa o Faker para gerar dados em português brasileiro
fake = Faker('pt_BR')

# --- Constantes da API ---
BASE_URL = "http://localhost:8080/api"
OWNERS_URL = f"{BASE_URL}/customer/owners"
PETS_URL = f"{BASE_URL}/customer/owners"
VETS_URL = f"{BASE_URL}/vet/vets"  # <-- NOVO: URL para veterinários

# --- Configurações de Geração de Dados ---
TOTAL_OWNERS_TO_CREATE = 50
MAX_PETS_PER_OWNER = 3
TOTAL_VETS_TO_CREATE = 15 # <-- NOVO: Defina quantos veterinários criar
OWNER_IDS_FILE = "owner_ids.txt"

def create_owner():
    """Cria um novo dono (owner) com dados fictícios."""
    owner_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.street_address(),
        "city": fake.city(),
        "telephone": fake.msisdn()[:11]
    }
    try:
        response = requests.post(OWNERS_URL, json=owner_data)
        response.raise_for_status()
        created_owner = response.json()
        owner_id = created_owner.get("id")
        print(f"✅ Dono '{created_owner['firstName']}' criado com sucesso (ID: {owner_id}).")
        return owner_id
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao criar dono: {e}")
        return None

def add_pet_to_owner(owner_id):
    """Adiciona um pet a um dono existente."""
    if not owner_id:
        return
    birth_date = fake.date_of_birth(minimum_age=1, maximum_age=15)
    pet_types = ["cat", "dog", "lizard", "snake", "bird", "hamster"]
    pet_type = random.choice(pet_types)
    pet_data = {
        "name": fake.first_name(),
        "birthDate": birth_date.strftime("%Y-%m-%d"),
        "typeId": pet_types.index(pet_type) + 1
    }
    url = f"{PETS_URL}/{owner_id}/pets"
    try:
        response = requests.post(url, json=pet_data)
        response.raise_for_status()
        print(f"  🐾 Pet '{pet_data['name']}' ({pet_type}) adicionado ao dono ID {owner_id}.")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erro ao adicionar pet ao dono ID {owner_id}: {e.response.text}")

# --- NOVA FUNÇÃO PARA CRIAR VETERINÁRIOS ---
def create_vet():
    """Cria um novo veterinário (vet) com dados fictícios."""
    vet_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name()
        # Nota: Não estamos adicionando especialidades para simplificar.
    }
    try:
        response = requests.post(VETS_URL, json=vet_data)
        response.raise_for_status()
        created_vet = response.json()
        print(f"🩺 Veterinário(a) '{created_vet['firstName']}' criado(a) com sucesso (ID: {created_vet['id']}).")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao criar veterinário: {e}")

if __name__ == "__main__":
    print("--- Iniciando a população do banco de dados ---")
    
    # --- Seção de criação de Donos e Pets (sem alterações) ---
    print("\n--- Fase 1: Criando Donos e Pets ---")
    created_owner_ids = []
    for i in range(TOTAL_OWNERS_TO_CREATE):
        # print(f"\n--- Criando Dono {i+1}/{TOTAL_OWNERS_TO_CREATE} ---") # Removido para um log mais limpo
        owner_id = create_owner()
        if owner_id:
            created_owner_ids.append(owner_id)
            num_pets = random.randint(1, MAX_PETS_PER_OWNER)
            for _ in range(num_pets):
                add_pet_to_owner(owner_id)
    
    if created_owner_ids:
        with open(OWNER_IDS_FILE, "w") as f:
            for owner_id in created_owner_ids:
                f.write(f"{owner_id}\n")
        print(f"\n✅ {len(created_owner_ids)} IDs de donos foram salvos em '{OWNER_IDS_FILE}'.")

    # --- NOVO: Seção de criação de Veterinários ---
    print("\n--- Fase 2: Criando Veterinários ---")
    for i in range(TOTAL_VETS_TO_CREATE):
        create_vet()

    print("\n--- População do banco de dados concluída! ---")