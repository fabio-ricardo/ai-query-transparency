# AI Query System - Transparência Mato Grosso

Um sistema inteligente que converte perguntas em português brasileiro para consultas SQL usando **Llama2 (modelo 100% gratuito)** e executa queries em dados de transparência de custos do estado de Mato Grosso.

## Funcionalidades

- 🦙 **Llama AI Gratuito**: Usa modelo Llama local via Ollama (sem custos de API)
- 🤖 **Conversão de Linguagem Natural**: Transforma perguntas em português para consultas SQL
- 📊 **Dados de Mato Grosso**: 1.500 registros de transparência de 15 municípios
- 🎨 **Interface Moderna**: Dashboard Flask com gráficos dinâmicos e visualizações
- 📈 **Resultados em Tempo Real**: Visualização imediata com charts e estatísticas

## Estrutura do Projeto

```
windsurf-project/
├── app.py                  # Aplicação Flask principal com sistema Llama integrado
├── templates/
│   └── dashboard.html      # Interface web moderna com gráficos
├── data/
│   ├── mato_grosso_transparency.csv      # Dados de transparência (1.500 registros)
│   └── synthetic_transparency_costs.csv  # Dados sintéticos adicionais
├── requirements.txt        # Dependências Python
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Documentação
```

## Instalação (Requer Ollama + Llama)

### Setup Rápido
```bash
cd /Users/user/CascadeProjects/windsurf-project

# Instalar dependências Python
pip install -r requirements.txt

# Instalar Ollama (se não tiver)
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo Llama2 (obrigatório)
ollama pull llama2

# Iniciar serviço Ollama
ollama serve

# Executar aplicação
python app.py
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

### Dados Inclusos
- **1.500 registros** de transparência de Mato Grosso
- **15 municípios**: Cuiabá, Várzea Grande, Rondonópolis, Sinop, etc.
- **5 categorias**: saúde, educação, infraestrutura, administração, segurança
- **Período**: últimos 2 anos
- **Valores**: R$ 2.000 a R$ 2.000.000 por registro

## Uso

### Iniciar a Aplicação

```bash
python app.py
```

Acesse `http://localhost:5002` no navegador.

### Exemplos de Consultas

- **"Quanto foi gasto com saúde em Cuiabá?"**
- **"Mostrar todos os gastos acima de 100000 reais em educação"**
- **"Qual o total gasto com infraestrutura?"**
- **"Gastos de Rondonópolis por categoria"**
- **"Maiores gastos de segurança"**
- **"Total por município"**

### API Endpoints

#### `POST /query`
Converte pergunta em português e executa consulta.

**Request**:
```json
{
  "question": "Quanto foi gasto com saúde em Cuiabá?"
}
```

**Response**:
```json
{
  "success": true,
  "question": "Quanto foi gasto com saúde em Cuiabá?",
  "sql": "SELECT SUM(amount) as total FROM transparency_costs WHERE municipality = 'Cuiabá' AND cost_category = 'saúde';",
  "results": [...],
  "count": 150
}
```

#### `GET /health`
Verifica status dos serviços e dados carregados.

## Esquema de Dados

Os dados de transparência contêm:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | ID único |
| state | STRING | Sempre 'Mato Grosso' |
| municipality | STRING | 15 municípios de MT |
| cost_category | STRING | saúde, educação, infraestrutura, administração, segurança |
| cost_description | STRING | Descrição detalhada do gasto |
| amount | FLOAT | Valor em reais (R$ 2.000 - R$ 2.000.000) |
| date | DATE | Data da transação (últimos 2 anos) |
| department | STRING | Órgão responsável |
| contract_type | STRING | licitação, contrato direto, parceria, convênio |

## Arquitetura

1. **AI Agent**: Usa Llama2 local (obrigatório) para converter linguagem natural → SQL
2. **Query Engine**: Executa consultas SQL nos dados locais usando pandas
3. **Data Storage**: 1.500 registros CSV de transparência de Mato Grosso
4. **Web Interface**: Dashboard Flask com HTML/CSS/JavaScript e Chart.js

## Segurança

- Validação de queries geradas
- Filtros de segurança para operações SQL
- Tratamento de erros robusto
- Logs de auditoria

## Desenvolvimento

### Testes Locais

```bash
# Testar a aplicação
curl -X POST http://localhost:5002/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quanto foi gasto com saúde?"}'

# Verificar status
curl http://localhost:5002/health
```

### Extensões

- Adicionar mais municípios de Mato Grosso
- Integração com BigQuery para dados reais
- Análise temporal avançada
- Exportação de resultados (CSV, Excel)
- API REST completa

## Troubleshooting

### Problemas Comuns

1. **Ollama não conecta**: Verifique se o serviço está rodando com `ollama serve`
2. **Modelo Llama não encontrado**: Execute `ollama pull llama2` para baixar o modelo
3. **Porta ocupada**: A aplicação roda na porta 5002, verifique se está livre
4. **Dados não carregam**: Verifique se os arquivos CSV estão na pasta `data/`
5. **Aplicação não inicia**: Certifique-se que o Ollama está rodando antes de iniciar

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
