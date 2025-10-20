# -*- coding: utf-8 -*-

"""
Script para popular a base de dados do Spring PetClinic Microservices.

Este script utiliza a API Gateway para criar 'Owners' (donos) e seus 'Pets'.
É necessário que a stack de microserviços esteja em execução.

Pré-requisitos:
- Instalar as bibliotecas 'requests' e 'faker'.
  pip install requests faker
"""

import requests
import random
from faker import Faker
from datetime import date

# Inicializa o Faker para gerar dados fictícios em português do Brasil
fake = Faker('pt_BR')

# URL base da API Gateway do PetClinic
BASE_URL = "http://localhost:8080"
CUSTOMERS_SERVICE_URL = f"{BASE_URL}/api/customer"
VISITS_SERVICE_URL = f"{BASE_URL}/api/visit"


def criar_owner():
    """Cria um novo owner (dono) com dados fictícios."""
    owner_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.street_address(),
        "city": fake.city(),
        "telephone": fake.msisdn()[:11] # Garante que o telefone tenha no máximo 11 dígitos
    }
    try:
        response = requests.post(f"{CUSTOMERS_SERVICE_URL}/owners", json=owner_data)
        response.raise_for_status()  # Lança uma exceção para respostas de erro (4xx ou 5xx)
        print(f"✅ Dono '{owner_data['firstName']} {owner_data['lastName']}' criado com sucesso.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao criar dono: {e}")
        return None

def obter_tipos_de_pet():
    """Obtém os tipos de pet disponíveis na aplicação."""
    try:
        response = requests.get(f"{CUSTOMERS_SERVICE_URL}/pettypes")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao obter tipos de pet: {e}")
        return []

def adicionar_pet_a_owner(owner_id, pet_types):
    """Adiciona um pet a um dono existente."""
    if not pet_types:
        print("⚠️ Não há tipos de pet disponíveis para criar um pet.")
        return None

    pet_type = random.choice(pet_types)
    pet_data = {
        "name": fake.first_name(),
        # Formato de data esperado pela API: YYYY/MM/DD
        "birthDate": fake.date_of_birth(minimum_age=1, maximum_age=15).strftime('%Y/%m/%d'),
        "typeId": pet_type["id"]
    }

    try:
        response = requests.post(f"{CUSTOMERS_SERVICE_URL}/owners/{owner_id}/pets", json=pet_data)
        response.raise_for_status()
        print(f"  🐾 Pet '{pet_data['name']}' adicionado ao dono ID {owner_id}.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erro ao adicionar pet: {e}")
        return None

if __name__ == "__main__":
    print("--- Iniciando script para popular o banco de dados do PetClinic ---")

    # Quantidade de donos a serem criados
    NUMERO_DE_DONOS = 50
    # Máximo de pets por dono
    MAX_PETS_POR_DONO = 3

    print("\nBuscando tipos de pets disponíveis...")
    tipos_de_pet = obter_tipos_de_pet()
    if tipos_de_pet:
        print(f"Tipos encontrados: {[pt['name'] for pt in tipos_de_pet]}")
    else:
        print("Não foi possível continuar sem os tipos de pet. Abortando.")
        exit(1)

    print(f"\nCriando {NUMERO_DE_DONOS} donos e seus pets...")
    for i in range(NUMERO_DE_DONOS):
        novo_owner = criar_owner()
        if novo_owner and "id" in novo_owner:
            owner_id = novo_owner["id"]
            num_pets = random.randint(0, MAX_PETS_POR_DONO)
            for _ in range(num_pets):
                adicionar_pet_a_owner(owner_id, tipos_de_pet)

    print("\n--- Script de população de dados finalizado ---")
