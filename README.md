# AI Query System - Custos de Transparência Estadual

Um sistema inteligente que converte perguntas em português brasileiro para consultas SQL do BigQuery usando **Llama (modelo 100% gratuito)** e executa queries em dados de transparência de custos estaduais.

## Funcionalidades

- 🦙 **Llama AI Gratuito**: Usa modelo Llama local via Ollama (sem custos de API)
- 🤖 **Conversão de Linguagem Natural**: Transforma perguntas em português para SQL BigQuery
- 📊 **Dados Sintéticos**: Gera dados realistas de custos de transparência
- 🎨 **Interface Moderna**: Frontend Vue.js com gráficos e visualizações
-  **Resultados em Tempo Real**: Visualização imediata com charts e estatísticas

## Estrutura do Projeto

```
windsurf-project/
├── src/
│   ├── llama_agent.py       # Agente Llama gratuito para conversão Português -> SQL
│   ├── bigquery_service.py  # Serviço BigQuery
│   ├── data_generator.py    # Gerador de dados sintéticos
│   ├── app.py              # Aplicação Flask original
│   └── app_frontend.py     # Aplicação Flask com frontend moderno
├── frontend/
│   ├── index.html          # Interface Vue.js moderna
│   └── package.json        # Dependências frontend
├── data/
│   └── synthetic_transparency_costs.csv  # Dados gerados
├── requirements.txt        # Dependências Python
├── .env.example           # Variáveis de ambiente
└── README.md              # Documentação
```

## Instalação (Requer Ollama + Llama)

### Setup Automático
```bash
cd /Users/user/CascadeProjects/windsurf-project

# Instalar dependências Python
pip install -r requirements.txt

# Setup automático do Ollama + Llama
./setup_ollama.sh

# Executar aplicação
python src/app_frontend.py
```

### Setup Manual
```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo Llama2 (obrigatório)
ollama pull llama2

# Iniciar serviço Ollama
ollama serve

# Executar aplicação
python src/app_frontend.py
```

## Configuração

### Modelo AI (Llama via Ollama) - OBRIGATÓRIO
- **Automático**: Execute `./setup_ollama.sh` para instalação completa
- **Manual**: 
  ```bash
  # Instalar Ollama
  curl -fsSL https://ollama.ai/install.sh | sh
  
  # Baixar modelo Llama2 (obrigatório)
  ollama pull llama2
  
  # Iniciar serviço
  ollama serve
  ```

### Google Cloud BigQuery (Opcional)
- Crie um projeto no Google Cloud Console
- Habilite a API BigQuery
- Configure `GOOGLE_CLOUD_PROJECT` no `.env`
- Para autenticação, use gcloud CLI ou arquivo de credenciais

## Uso

### Iniciar a Aplicação

```bash
python src/app.py
```

Acesse `http://localhost:5000` no navegador.

### Exemplos de Consultas

- **"Quanto foi gasto com saúde em São Paulo no ano de 2023?"**
- **"Mostrar todos os gastos acima de 10000 reais em educação"**
- **"Qual o total gasto com infraestrutura por estado?"**
- **"Custos do Rio de Janeiro por categoria"**
- **"Contratos de licitação em 2023"**

### API Endpoints

#### `POST /api/query`
Converte pergunta em português e executa consulta.

**Request**:
```json
{
  "prompt": "Quanto foi gasto com saúde em São Paulo?"
}
```

**Response**:
```json
{
  "success": true,
  "prompt": "Quanto foi gasto com saúde em São Paulo?",
  "generated_sql": "SELECT SUM(amount) as total_gasto FROM transparency_costs WHERE state = 'São Paulo' AND cost_category = 'saúde'",
  "results": [...],
  "row_count": 150,
  "timestamp": "2024-01-06T23:31:00Z"
}
```

#### `GET /api/table-info`
Retorna informações sobre a tabela de dados.

#### `GET /api/health`
Verifica status dos serviços.

#### `POST /api/generate-data`
Gera novos dados sintéticos.

## Esquema de Dados

A tabela `transparency_costs` contém:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | ID único |
| state | STRING | Estado brasileiro |
| municipality | STRING | Município |
| cost_category | STRING | Categoria (saúde, educação, etc.) |
| cost_description | STRING | Descrição detalhada |
| amount | FLOAT | Valor em reais |
| date | DATE | Data da transação |
| department | STRING | Departamento responsável |
| contract_type | STRING | Tipo de contrato |

## Arquitetura

1. **AI Agent**: Usa Llama2 local (obrigatório) para converter linguagem natural → SQL
2. **Query Service**: Executa SQL no BigQuery ou localmente
3. **Data Generator**: Cria dados sintéticos realistas
4. **Web Interface**: Frontend com Flask e TailwindCSS

## Segurança

- Validação de queries geradas
- Filtros de segurança para operações SQL
- Tratamento de erros robusto
- Logs de auditoria

## Desenvolvimento

### Testes Locais

```bash
# Testar conversão de linguagem
python -c "
from src.ai_agent import AIAgent
agent = AIAgent()
sql = agent.convert_portuguese_to_bigquery('Quanto foi gasto com saúde em São Paulo?')
print(sql)
"
```

### Extensões

- Adicionar mais categorias de custos
- Suporte a outros bancos de dados
- Análise avançada com gráficos
- Exportação de resultados (CSV, Excel)

## Troubleshooting

### Problemas Comuns

1. **Ollama não conecta**: Verifique se o serviço está rodando com `ollama serve` ou `brew services start ollama`
2. **Modelo Llama não encontrado**: Execute `ollama pull llama2` para baixar o modelo
3. **BigQuery não conecta**: Configure credenciais Google Cloud
4. **Dados não aparecem**: Gere dados sintéticos via botão "Gerar Dados"
5. **Aplicação não inicia**: Certifique-se que o Ollama está rodando antes de iniciar a aplicação

### Logs

A aplicação gera logs detalhados para debugging:

```bash
# Ver logs em tempo real
tail -f /var/log/app.log  # (se configurado)
```

## Licença

MIT License - use conforme necessário.

## Contribuições

Contribuições são bem-vindas! Abra issues para bugs ou features.
