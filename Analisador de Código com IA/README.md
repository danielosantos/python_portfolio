# 🔍 Analisador de Código com IA

Uma ferramenta simples e poderosa para entender projetos de código. Este sistema lê arquivos locais, realiza verificações de segurança básicas e utiliza Inteligência Artificial (via OpenRouter) para gerar relatórios executivos explicando como o software funciona.

Ideal para desenvolvedores que assumem projetos legados, gestores que querem entender uma base de código ou para auditorias rápidas.

---

## 📋 O que este projeto faz?

1.  **Escaneamento:** Percorre pastas do seu computador para encontrar arquivos de código.
2.  **Análise de Segurança Local:** Busca por padrões perigosos (como `eval`, `pickle`) e possíveis senhas expostas no código.
3.  **Geração de Relatório com IA:** Envia o resumo dos arquivos para uma IA e recebe de volta um documento explicando:
    *   O que o programa faz (Resumo Executivo).
    *   Como ele funciona tecnicamente.
    *   Onde fazer alterações.
    *   Riscos de segurança explicados de forma simples.
    *   Sugestões de melhorias.

---

## ⚠️ Avisos de Segurança e Privacidade

- **Privacidade de Dados:** Esta ferramenta envia trechos do seu código para a API da OpenRouter para serem analisados pela IA. **Não utilize** em projetos contendo dados extremamente sensíveis (senhas reais de produção, dados de clientes, chaves privadas de criptografia) a menos que você confie no provedor de IA.
- **Mascaramento de Segredos:** O sistema tenta detectar e ocultar segredos óbvios (como chaves de API) antes de enviar o texto para a IA, mas essa verificação é baseada em padrões simples e não é infalível.
- **Execução Local:** O escaneamento e a análise de segurança inicial ocorrem 100% no seu computador.

---

## 🛠️ Requisitos

- **Python 3.8 ou superior** instalado.
- Conexão com a internet (para acessar a API da IA).
- Uma chave de API da [OpenRouter](https://openrouter.ai/).

---

## 🚀 Instalação Passo a Passo

Siga estes passos para configurar o ambiente no seu computador.

### 1. Baixe o projeto
Baixe ou clone este repositório para uma pasta no seu computador.

### 2. Crie um ambiente virtual (Recomendado)
Isso evita conflitos com outras bibliotecas do seu sistema.
- No Linux/MacOS:
    python3 -m venv .venv
    source .venv/bin/activate
- No windows: 
    python -m venv .venv
    .venv\Scripts\activate
- Depois disso, instale as dependências:
    pip install -r requirements.txt
- Adicione as credenciais no arquivo .env, caso esteja oculto aperte CTRL+H no seu gerenciador de arquivos padrão. 

### 3. Para executar rode o seguinte comando:
streamlit run app.py
