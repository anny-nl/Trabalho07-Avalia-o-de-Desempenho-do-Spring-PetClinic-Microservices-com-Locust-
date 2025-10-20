# -*- coding: utf-8 -*-

"""
Locustfile para teste de carga da aplicação Spring PetClinic Microservices.

Este script simula o comportamento de usuários acessando diferentes endpoints
da aplicação, seguindo o mix de requisições definido no plano de teste.

Endpoints exercitados:
- GET /owners (40%)
- GET /owners/{id} (30%)
- GET /vets (20%)
- POST /owners (10%)
"""

from locust import HttpUser, task, between
from faker import Faker
import random

# Inicializa o Faker para gerar dados fictícios
fake = Faker('pt_BR')

class PetClinicUser(HttpUser):
    # O host deve ser a URL da API Gateway
    host = "http://localhost:8080"
    # Tempo de espera entre as tarefas, simulando um usuário real
    wait_time = between(1, 4)

    def on_start(self):
        """
        Executado quando um usuário simulado (Locust) inicia.
        Busca a lista de donos existentes para usar nos testes de detalhe.
        """
        self.owner_ids = []
        try:
            response = self.client.get("/api/customer/owners", name="/api/customer/owners (setup)")
            if response.status_code == 200 and response.text:
                owners = response.json()
                if isinstance(owners, list):
                    self.owner_ids = [owner['id'] for owner in owners if 'id' in owner]
            if not self.owner_ids:
                 print("ALERTA: Nenhum ID de dono foi encontrado no on_start. A tarefa get_owner_details pode falhar.")
        except Exception as e:
            print(f"Erro no on_start ao buscar donos: {e}")

    @task(4) # 40% do mix de requisições
    def list_owners(self):
        """Tarefa para listar todos os donos."""
        self.client.get(
            "/api/customer/owners",
            name="GET /owners (lista)" # Nome para agrupar as estatísticas no Locust
        )

    @task(3) # 30% do mix
    def get_owner_details(self):
        """Tarefa para obter detalhes de um dono específico."""
        if not self.owner_ids:
            # Se a lista de IDs estiver vazia, pula esta tarefa para não gerar erros
            # Isso pode acontecer no início do teste, antes de on_start popular a lista
            return

        owner_id = random.choice(self.owner_ids)
        self.client.get(
            f"/api/customer/owners/{owner_id}",
            name="GET /owners/{id} (detalhe)"
        )

    @task(2) # 20% do mix
    def list_vets(self):
        """Tarefa para listar todos os veterinários."""
        self.client.get(
            "/api/vet/vets",
            name="GET /vets (lista)"
        )

    @task(1) # 10% do mix
    def create_owner(self):
        """Tarefa para criar um novo dono."""
        new_owner_data = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "address": fake.street_address(),
            "city": fake.city(),
            "telephone": fake.msisdn()[:10]
        }
        self.client.post(
            "/api/customer/owners",
            json=new_owner_data,
            name="POST /owners (cadastro)"
        )
