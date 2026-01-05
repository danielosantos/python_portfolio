import requests
import config

def chat(messages: list[dict]) -> str:
    """
    Envia uma lista de mensagens para a API do OpenRouter e retorna o texto da resposta.
    
    Args:
        messages (list[dict]): Lista de mensagens no formato [{"role": "user", "content": "Olá"}].
        
    Returns:
        str: O conteúdo da resposta da IA.
        
    Raises:
        ValueError: Se a chave da API não estiver configurada.
        Exception: Para erros de conexão, timeout ou erros na resposta da API.
    """
    
    # 1. Verificação da Chave da API
    if not config.OPENROUTER_API_KEY:
        raise ValueError(
            "Erro de Configuração: A chave da API (OPENROUTER_API_KEY) não foi encontrada. "
            "Verifique suas variáveis de ambiente ou arquivo .env."
        )

    # 2. Configuração dos Headers
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Headers opcionais recomendados pelo OpenRouter para identificação
        "HTTP-Referer": "http://localhost",
        "X-Title": "Python Local Analyzer"
    }

    # 3. Preparação do Payload (corpo da requisição)
    payload = {
        "model": config.OPENROUTER_MODEL,
        "messages": messages
    }

    try:
        # 4. Execução da Requisição POST
        response = requests.post(
            config.OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=config.TIMEOUT_SECONDS
        )

        # 5. Tratamento de Erros HTTP (Status Code diferente de 200)
        if response.status_code != 200:
            error_detail = "Sem detalhes disponíveis."
            try:
                # Tenta ler o JSON de erro da API para dar uma mensagem mais útil
                json_error = response.json()
                if "error" in json_error:
                    error_detail = json_error["error"].get("message", str(json_error["error"]))
                else:
                    error_detail = response.text
            except ValueError:
                # Se a resposta não for JSON, usa o texto puro
                error_detail = response.text

            raise Exception(
                f"Erro na API ({response.status_code}): {error_detail}"
            )

        # 6. Extração do Conteúdo da Resposta
        data = response.json()
        
        # Verifica se a chave 'choices' existe e tem conteúdo
        if "choices" not in data or not data["choices"]:
            raise Exception("A API retornou uma resposta vazia ou inválida (sem choices).")
            
        # Retorna o texto da primeira escolha (formato padrão OpenAI)
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        raise Exception("Erro de Conexão: O tempo limite da requisição foi excedido.")

    except requests.exceptions.ConnectionError:
        raise Exception("Erro de Conexão: Não foi possível conectar à API. Verifique sua internet.")

    except requests.exceptions.RequestException as e:
        # Captura qualquer outro erro relacionado à requisição (ex: DNS, SSLError)
        raise Exception(f"Erro na requisição: {str(e)}")
