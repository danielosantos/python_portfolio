import re

def analyze_security(scanned_files: list[dict]) -> list[dict]:
    """
    Realiza análise estática simples nos arquivos para identificar riscos de segurança.
    
    Args:
        scanned_files (list[dict]): Lista de arquivos retornada pelo scanner.
        
    Returns:
        list[dict]: Lista de achados (risco), contendo arquivo, linha, tipo e descrição.
    """
    
    findings = []

    # Definição dos padrões de risco (Regex)
    # Chave: Categoria do Risco
    # Valor: Lista de padrões para buscar
    risk_patterns = {
        "Possível Segredo Exposto": [
            r"sk-",                                     # Prefixo comum de chaves de API (Stripe, OpenAI, etc.)
            r"(?i)api_key\s*=",                        # Atribuição de api_key (case insensitive)
            r"(?i)secret\s*=",                         # Atribuição de secret
            r"(?i)token\s*=",                          # Atribuição de token
            r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----" # Chaves privadas no formato PEM
        ],
        "Código Perigoso": [
            r"eval\s*\(",                              # Função eval (execução de código dinâmico)
            r"exec\s*\(",                              # Função exec (execução de código dinâmico)
            r"subprocess\..*shell\s*=\s*True",         # subprocess com shell=True (risco de injeção de comando)
            r"pickle\.load\s*\(",                      # Desserialização insegura com pickle
            r"yaml\.load\s*\("                         # yaml.load sem Loader explícito (risco de injeção YAML)
        ]
    }

    for file_info in scanned_files:
        file_path = file_info["path"]
        content = file_info["content"]
        lines = content.splitlines()

        for line_number, line_content in enumerate(lines, start=1):
            # Verifica cada categoria de risco
            for category, patterns in risk_patterns.items():
                for pattern in patterns:
                    # Busca o padrão na linha atual
                    if re.search(pattern, line_content):
                        findings.append({
                            "file": file_path,
                            "line": line_number,
                            "category": category,
                            "description": f"Padrão detectado: '{pattern}'",
                            "snippet": line_content.strip()
                        })

    # Ordena os achados pelo nome do arquivo para manter o relatório organizado
    findings.sort(key=lambda x: x["file"])

    return findings
