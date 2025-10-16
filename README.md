# Avaliação de Desempenho – Spring PetClinic (Microservices) com Locust

## Objetivo
Medir e analisar o desempenho do sistema **Spring PetClinic – Microservices** utilizando a ferramenta **Locust**.

## Tecnologias
- Docker & Docker Compose
- Python 3 + Locust
- Spring PetClinic (versão microservices)

---

## Como executar

### 1. Clonar o projeto
```bash
1. git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git
2. cd spring-petclinic-microservices

# Subir a aplicação:
1. docker compose up --build -d
2. cd spring-petclinic-microservices
3. docker compose up -d
4.  docker compose ps

# A aplicação deve responder:
Como acessar na prática
Abra o navegador e acesse:
# Aplicação principal (PetClinic):
 http://localhost:8080

# Discovery Server (Eureka):
 http://localhost:8761

# Grafana:
 http://localhost:3030
(Usuário e senha padrão: admin / admin)

# Zipkin (Tracing):
 http://localhost:9411

# Abrir Locust e testar
http://localhost:8089

# Como testar se está tudo certo

Acesse http://localhost:8080
→ Você verá a interface do PetClinic (com os pets, donos e veterinários).
Vá em http://localhost:8761
→ Veja se os serviços customers-service, vets-service, visits-service, api-gateway estão todos UP.
Vá em http://localhost:3030
→ Entre no painel do Grafana para visualizar métricas.

# Se quiser parar tudo
Execute:
 docker compose down

# Executar os testes
bash run_leve.sh
bash run_medio.sh
bash run_pico.sh
\\ Os resultados serão salvos na pasta results/.

#Gerar resumo final:
python analisar_csvs.py




