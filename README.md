# 🏛️ Polieus (Python CLI)

> **Global Solution 2026/2 · FIAP · CitizenTech**  
> *Tecnologia que conecta cidadãos, cidades e decisões.*

---

## 📌 Contexto do Projeto

O **Polieus** é uma solução *CitizenTech* criada para aproximar a população da gestão pública municipal. A plataforma transforma relatos de problemas urbanos (como buracos na via, iluminação pública deficiente e falhas de acessibilidade) em informações organizadas, rastreáveis e priorizadas.

Esta aplicação em **Python** representa o módulo central de lógica e processamento de zeladoria urbana, disponibilizando uma interface interativa de terminal (CLI) orientada tanto aos **cidadãos** quanto aos **gestores públicos**.

---

## ⚙️ Principais Funcionalidades

### 🧑 Área do Cidadão
1. **Registro de Ocorrências:** Cadastro de problemas urbanos informando categoria, descrição, endereço, bairro e gravidade, gerando um protocolo único de acompanhamento.
2. **Consulta de Ocorrências:** Visualização e acompanhamento do status das demandas registradas.

### 🇧🇷 Área de Gestão Urbana (Município)
3. **Consulta Avançada:** Filtragem de demandas por protocolo, bairro, categoria ou situação.
4. **Análise e Priorização:** Classificação automática da prioridade de atendimento (*Alta*, *Média* ou *Baixa*) com base no nível de gravidade, risco a pedestres e impacto em acessibilidade.
5. **Atualização de Status:** Gestão do ciclo de vida da demanda (*Registrada*, *Em análise*, *Aprovada*, *Em execução*, *Concluída*, *Não aprovada*).
6. **Relatórios Gerenciais:** Métricas consolidadas por categoria, bairro, níveis de prioridade e proporção entre demandas pendentes e resolvidas.
7. **Análise de Recorrência:** Detecção de padrões e emissão de alertas automáticos quando múltiplos problemas do mesmo tipo se concentram em uma mesma rua ou bairro.

---

## 🚀 Como Rodar

### Pré-requisitos
- **Python 3.10** ou superior instalado.
- Gerenciador de pacotes `pip`.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone git@github.com:murilo-a-souza/polieus-py.git
   cd polieus-py
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Linux / macOS:
   python3 -m venv venv
   source venv/bin/activate

   # Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Configuração de ambiente:**
   Caso utilize persistência com banco Oracle, configure suas variáveis no arquivo `.env` na raiz:
   ```env
   ORACLE_USER=seu_usuario
   ORACLE_PASSWORD=sua_senha
   ORACLE_DSN=seu_dsn_oracle
   ```

5. **Execute a aplicação:**
   ```bash
   python3 main.py
   ```

---

## 🛠️ Tecnologias Utilizadas

- **Python**: Lógica central e programação estruturada/procedural.
- **InquirerPy**: Navegação interativa por menus via terminal.
- **Rich**: Estilização visual de consoles, painéis e alertas.
- **python-dotenv & oracledb**: Gestão de variáveis de ambiente e conexão com banco de dados.

---

## 👥 Integrantes

- Henrique Bonachela
- Isabelle Ferreira
- Marina
- Milena Conegin
- Murilo Almeida
