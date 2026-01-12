#!/usr/bin/env python3
"""
Clean, elegant AI Query System for Mato Grosso Transparency Data
Single file application with dynamic dashboard
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import pandas as pd
import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class LlamaQuerySystem:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.data_file = "data/mato_grosso_transparency.csv"
        self.setup_data()
    
    def setup_data(self):
        """Setup Mato Grosso transparency data"""
        if not os.path.exists("data"):
            os.makedirs("data")
        
        if not os.path.exists(self.data_file):
            self.generate_data()
        
        self.df = pd.read_csv(self.data_file)
        logger.info(f"Loaded {len(self.df)} transparency records for Mato Grosso")
    
    def generate_data(self):
        """Generate Mato Grosso transparency data"""
        import random
        from datetime import timedelta
        
        municipalities = [
            'Cuiabá', 'Várzea Grande', 'Rondonópolis', 'Sinop', 'Tangará da Serra',
            'Cáceres', 'Sorriso', 'Lucas do Rio Verde', 'Primavera do Leste', 'Barra do Garças',
            'Alta Floresta', 'Pontes e Lacerda', 'Nova Mutum', 'Diamantino', 'Campo Verde'
        ]
        
        categories = ['saúde', 'educação', 'infraestrutura', 'administração', 'segurança']
        
        departments = {
            'saúde': ['Secretaria de Saúde', 'Hospital Municipal', 'UBS Central'],
            'educação': ['Secretaria de Educação', 'Escola Municipal', 'Creche'],
            'infraestrutura': ['Secretaria de Obras', 'Departamento de Viação'],
            'administração': ['Prefeitura', 'Secretaria de Administração'],
            'segurança': ['Polícia Militar', 'Guarda Municipal']
        }
        
        contract_types = ['licitação', 'contrato direto', 'parceria', 'convênio']
        
        data = []
        for i in range(1500):
            category = random.choice(categories)
            municipality = random.choice(municipalities)
            department = random.choice(departments[category])
            
            # Generate realistic amounts based on category
            if category == 'infraestrutura':
                amount = random.uniform(50000, 2000000)
            elif category == 'saúde':
                amount = random.uniform(10000, 800000)
            elif category == 'educação':
                amount = random.uniform(5000, 500000)
            elif category == 'segurança':
                amount = random.uniform(15000, 600000)
            else:  # administração
                amount = random.uniform(2000, 200000)
            
            # Generate date within last 2 years
            days_ago = random.randint(0, 730)
            date = datetime.now() - timedelta(days=days_ago)
            
            data.append({
                'id': i + 1,
                'state': 'Mato Grosso',
                'municipality': municipality,
                'cost_category': category,
                'cost_description': f'Gasto com {category} em {municipality}',
                'amount': round(amount, 2),
                'date': date.strftime('%Y-%m-%d'),
                'department': department,
                'contract_type': random.choice(contract_types)
            })
        
        df = pd.DataFrame(data)
        df.to_csv(self.data_file, index=False)
        logger.info(f"Generated {len(data)} records for Mato Grosso")
    
    def convert_to_sql(self, question):
        """Convert natural language question to SQL using Llama"""
        try:
            system_prompt = """Você é um especialista em SQL que converte perguntas em português para consultas BigQuery precisas.

ESQUEMA DA TABELA: transparency_costs
Colunas disponíveis:
- id: INTEGER (chave primária)
- state: STRING (sempre 'Mato Grosso')
- municipality: STRING (municípios: 'Cuiabá', 'Várzea Grande', 'Rondonópolis', 'Sinop', 'Tangará da Serra', 'Cáceres', 'Sorriso', 'Lucas do Rio Verde', 'Primavera do Leste', 'Barra do Garças', 'Alta Floresta', 'Pontes e Lacerda', 'Nova Mutum', 'Diamantino', 'Campo Verde')
- cost_category: STRING (valores: 'saúde', 'educação', 'infraestrutura', 'administração', 'segurança')
- cost_description: STRING (descrição do gasto)
- amount: FLOAT (valor em reais, sempre > 0)
- date: DATE (formato YYYY-MM-DD, últimos 2 anos)
- department: STRING (órgão responsável)
- contract_type: STRING (valores: 'licitação', 'contrato direto', 'parceria', 'convênio')

REGRAS OBRIGATÓRIAS:
1. Retorne APENAS o SQL válido, sem explicações ou texto adicional
2. Use sempre aspas simples para strings: 'valor'
3. Inclua LIMIT quando apropriado (máximo 200 registros)
4. Para agregações (SUM, COUNT, AVG), use aliases descritivos
5. Para consultas por município, use o nome exato da lista
6. Para datas, use formato 'YYYY-MM-DD'
7. Termine sempre com ponto e vírgula

PADRÕES DE CONSULTA:
- Totais por categoria: SELECT cost_category, SUM(amount) as total FROM transparency_costs GROUP BY cost_category ORDER BY total DESC;
- Gastos por município: SELECT * FROM transparency_costs WHERE municipality = 'Nome' ORDER BY amount DESC LIMIT 50;
- Soma por categoria: SELECT SUM(amount) as total FROM transparency_costs WHERE cost_category = 'categoria';
- Maiores gastos: SELECT * FROM transparency_costs ORDER BY amount DESC LIMIT 30;
- Gastos recentes: SELECT * FROM transparency_costs ORDER BY date DESC LIMIT 20;
- Filtro por período: SELECT * FROM transparency_costs WHERE date >= '2024-01-01' LIMIT 50;

EXEMPLOS ESPECÍFICOS:
"Quanto foi gasto com saúde?" → SELECT SUM(amount) as total FROM transparency_costs WHERE cost_category = 'saúde';
"Gastos em Cuiabá" → SELECT * FROM transparency_costs WHERE municipality = 'Cuiabá' ORDER BY amount DESC LIMIT 50;
"Maiores gastos de educação" → SELECT * FROM transparency_costs WHERE cost_category = 'educação' ORDER BY amount DESC LIMIT 30;
"Total por categoria" → SELECT cost_category, SUM(amount) as total FROM transparency_costs GROUP BY cost_category ORDER BY total DESC;
"Gastos recentes" → SELECT * FROM transparency_costs ORDER BY date DESC LIMIT 20;"""

            payload = {
                "model": "llama2",
                "prompt": f"{system_prompt}\n\nPergunta: {question}\nSQL:",
                "stream": False,
                "options": {"temperature": 0.1, "max_tokens": 200}
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                sql = response.json().get('response', '').strip()
                # Clean up response
                sql = sql.replace('```sql', '').replace('```', '').strip()
                if not sql.endswith(';'):
                    sql += ';'
                
                # Validate that we got actual SQL
                if not sql or len(sql) < 10 or 'SELECT' not in sql.upper():
                    raise Exception("LLM não gerou um SQL válido")
                    
                return sql
            else:
                raise Exception(f"Erro do Ollama: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Não foi possível conectar ao Ollama. Verifique se o serviço está rodando.")
        except requests.exceptions.Timeout:
            raise Exception("Timeout na conexão com o Ollama. Tente novamente.")
        except Exception as e:
            logger.error(f"LLM conversion failed: {e}")
            raise Exception(f"Erro na conversão para SQL: {str(e)}")
    
    
    def execute_sql(self, sql):
        """Execute SQL query on the data"""
        try:
            # Convert BigQuery SQL to pandas operations
            sql_lower = sql.lower()
            
            if 'select sum(amount)' in sql_lower and 'where cost_category' in sql_lower:
                # Sum by category
                try:
                    category = sql.split("'")[1]  # Extract category from SQL
                    result = self.df[self.df['cost_category'] == category]['amount'].sum()
                    return pd.DataFrame([{'total': result}])
                except IndexError:
                    raise Exception("Não foi possível extrair a categoria do SQL gerado")
            
            elif 'group by cost_category' in sql_lower:
                # Group by category
                result = self.df.groupby('cost_category')['amount'].sum().reset_index()
                result.columns = ['cost_category', 'total']
                return result.sort_values('total', ascending=False)
            
            elif 'where municipality' in sql_lower:
                # Filter by municipality
                try:
                    # Extract municipality name from SQL - handle quotes properly
                    import re
                    municipality_match = re.search(r"municipality\s*=\s*'([^']+)'", sql, re.IGNORECASE)
                    if not municipality_match:
                        raise Exception("Não foi possível extrair o nome do município")
                    
                    municipality = municipality_match.group(1)
                    result = self.df[self.df['municipality'] == municipality]
                    if result.empty:
                        raise Exception(f"Nenhum registro encontrado para o município '{municipality}'")
                    
                    # Handle ORDER BY if present
                    if 'order by amount desc' in sql_lower:
                        result = result.sort_values('amount', ascending=False)
                    elif 'order by amount asc' in sql_lower:
                        result = result.sort_values('amount', ascending=True)
                    elif 'order by date' in sql_lower:
                        result = result.sort_values('date', ascending=False)
                    
                    # Handle LIMIT
                    limit = 50
                    if 'limit' in sql_lower:
                        limit_match = re.search(r'limit\s+(\d+)', sql_lower)
                        if limit_match:
                            limit = int(limit_match.group(1))
                    
                    return result.head(limit)
                except (IndexError, ValueError) as e:
                    raise Exception(f"Erro ao processar filtro por município: {str(e)}")
            
            elif 'where cost_category' in sql_lower:
                # Filter by category
                try:
                    import re
                    category_match = re.search(r"cost_category\s*=\s*'([^']+)'", sql, re.IGNORECASE)
                    if not category_match:
                        raise Exception("Não foi possível extrair a categoria")
                    
                    category = category_match.group(1)
                    result = self.df[self.df['cost_category'] == category]
                    if result.empty:
                        raise Exception(f"Nenhum registro encontrado para a categoria '{category}'")
                    
                    # Handle ORDER BY if present
                    if 'order by amount desc' in sql_lower:
                        result = result.sort_values('amount', ascending=False)
                    elif 'order by amount asc' in sql_lower:
                        result = result.sort_values('amount', ascending=True)
                    elif 'order by date' in sql_lower:
                        result = result.sort_values('date', ascending=False)
                    
                    # Handle LIMIT
                    limit = 50
                    if 'limit' in sql_lower:
                        limit_match = re.search(r'limit\s+(\d+)', sql_lower)
                        if limit_match:
                            limit = int(limit_match.group(1))
                    
                    return result.head(limit)
                except (IndexError, ValueError) as e:
                    raise Exception(f"Erro ao processar filtro por categoria: {str(e)}")
            
            elif 'order by amount desc' in sql_lower:
                # Order by amount
                import re
                limit = 30
                if 'limit' in sql_lower:
                    limit_match = re.search(r'limit\s+(\d+)', sql_lower)
                    if limit_match:
                        limit = int(limit_match.group(1))
                return self.df.sort_values('amount', ascending=False).head(limit)
            
            else:
                # Default: return recent records
                import re
                limit = 20
                if 'limit' in sql_lower:
                    limit_match = re.search(r'limit\s+(\d+)', sql_lower)
                    if limit_match:
                        limit = int(limit_match.group(1))
                return self.df.head(limit)
                
        except Exception as e:
            logger.error(f"SQL execution error: {e}")
            raise Exception(f"Erro na execução da consulta: {str(e)}")

# Initialize system
query_system = LlamaQuerySystem()


@app.route('/')
def dashboard():
    """Serve the main dashboard"""
    return render_template('dashboard.html')

@app.route('/query', methods=['POST'])
def query():
    """Process natural language query"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Pergunta é obrigatória'}), 400
        
        # Convert to SQL
        sql = query_system.convert_to_sql(question)
        logger.info(f"Generated SQL: {sql}")
        
        # Execute query
        results_df = query_system.execute_sql(sql)
        
        # Convert to JSON
        results = results_df.to_dict('records')
        
        # Handle date serialization
        for record in results:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, pd.Timestamp):
                    record[key] = value.isoformat()
        
        return jsonify({
            'success': True,
            'question': question,
            'sql': sql,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'records': len(query_system.df),
        'ollama_available': True  # Assume available for now
    })

if __name__ == '__main__':
    print("🚀 Starting Mato Grosso Transparency Dashboard...")
    print("📊 Dashboard: http://localhost:5002")
    print("🦙 Using Llama2 for natural language processing")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
