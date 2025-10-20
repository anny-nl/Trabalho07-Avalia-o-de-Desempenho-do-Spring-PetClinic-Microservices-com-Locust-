#!/bin/bash

# Script para automatizar a execução dos cenários de teste de carga com Locust.
#
# Uso:
# ./run_scenarios.sh <cenario>
# Onde <cenario> pode ser: leve, medio, pico

# Validação do argumento de entrada
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 {leve|medio|pico}"
    exit 1
fi

SCENARIO=$1
LOCUST_FILE="locustfile.py"
RESULTS_DIR="results"

# Cria o diretório de resultados se ele não existir
mkdir -p $RESULTS_DIR

# Parâmetros comuns
# --headless: Roda sem a interface web
# --csv: Salva os resultados em formato CSV
# --html: Salva o relatório completo em HTML, que é muito útil para análise
COMMON_ARGS="-f $LOCUST_FILE --headless"

echo "--- Iniciando Teste de Carga - Cenário: $SCENARIO ---"

case $SCENARIO in
  leve)
    # Cenário A (leve): 50 usuários, 10 min de duração
    echo "Configuração: 50 usuários por 10 minutos."
    locust $COMMON_ARGS --users 50 --run-time 10m --csv "$RESULTS_DIR/cenario_leve" --html "$RESULTS_DIR/cenario_leve_report.html"
    ;;
  medio)
    # Cenário B (moderado): 100 usuários, 10 min de duração
    echo "Configuração: 100 usuários por 10 minutos."
    locust $COMMON_ARGS --users 100 --run-time 10m --csv "$RESULTS_DIR/cenario_medio" --html "$RESULTS_DIR/cenario_medio_report.html"
    ;;
  pico)
    # Cenário C (pico): 200 usuários, 5 min de duração
    echo "Configuração: 200 usuários por 5 minutos."
    locust $COMMON_ARGS --users 200 --run-time 5m --csv "$RESULTS_DIR/cenario_pico" --html "$RESULTS_DIR/cenario_pico_report.html"
    ;;
  *)
    echo "Erro: Cenário '$SCENARIO' inválido."
    echo "Use um dos seguintes: leve, medio, pico"
    exit 1
    ;;
esac

echo "--- Teste do Cenário: $SCENARIO finalizado ---"
echo "Resultados salvos em: $RESULTS_DIR/"
