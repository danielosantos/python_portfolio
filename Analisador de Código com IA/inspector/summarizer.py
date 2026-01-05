import ai_client
import re

def _mask_secrets(content: str, findings: list[dict]) -> str:
    """
    Substitui linhas contendo segredos detectados por [REDACTED].
    
    Args:
        content (str): Conteúdo original do arquivo.
        findings (list[dict]): Lista de achados de segurança (filtrados para este arquivo).
        
    Returns:
        str: Conteúdo com segredos mascarados.
    """
    lines = content.splitlines()
    # Conjunto de índices de linhas (0-based) que devem ser ocultados
    lines_to_redact = set()
    
    for finding in findings:
        # Focamos apenas na categoria de segredos
        if finding.get("category") == "Possível Segredo Exposto":
            line_num = finding.get("line")
            if line_num:
                lines_to_redact.add(line_num - 1) # Converter para 0-based index

    new_lines = []
    for i, line in enumerate(lines):
        if i in lines_to_redact:
            new_lines.append("[REDACTED - Segredo Detectado]")
        else:
            new_lines.append(line)
            
    return "\n".join(new_lines)

def _summarize_batch(files_batch: list[dict], all_findings: list[dict]) -> str:
    """
    Envia um lote de arquivos para a IA e pede um resumo técnico conciso.
    (Fase do Map)
    """
    batch_content = []
    
    for file_info in files_batch:
        path = file_info["path"]
        content = file_info["content"]
        
        # Filtra achados pertinentes a este arquivo
        file_findings = [f for f in all_findings if f.get("file") == path]
        
        # Mascarar segredos antes de enviar
        safe_content = _mask_secrets(content, file_findings)
        
        batch_content.append(f"Arquivo: {path}\n```\n{safe_content}\n```")

    prompt_text = (
        "Abaixo está o conteúdo de um ou mais arquivos de código. "
        "Resuma a função de cada arquivo em 1-2 frases técnicas. "
        "Ignore erros de sintaxe menores, foque na lógica de negócio.\n\n"
        + "\n".join(batch_content)
    )
    
    messages = [{"role": "user", "content": prompt_text}]
    
    try:
        return ai_client.chat(messages)
    except Exception as e:
        return f"Erro ao resumir lote: {str(e)}"

def generate_report(scanned_files: list[dict], security_findings: list[dict]) -> str:
    """
    Gera o relatório executivo completo usando IA.
    Implementa chunking (map-reduce) para processar os arquivos.
    
    Args:
        scanned_files (list[dict]): Lista de arquivos escaneados.
        security_findings (list[dict]): Lista de achados de segurança.
        
    Returns:
        str: Relatório completo em Markdown.
    """
    
    if not scanned_files:
        return "# Relatório de Análise\n\nNenhum arquivo encontrado para análise."

    # --- FASE 1: MAP (Resumo de Arquivos) ---
    # Dividimos os arquivos em lotes para não exceder o limite de contexto da IA
    batch_size = 5
    file_summaries = []
    
    print(f"Processando {len(scanned_files)} arquivos...")
    
    for i in range(0, len(scanned_files), batch_size):
        batch = scanned_files[i:i + batch_size]
        summary = _summarize_batch(batch, security_findings)
        file_summaries.append(summary)

    combined_summaries = "\n\n".join(file_summaries)

    # Formatar achados de segurança para o contexto
    security_context = "Nenhum risco crítico encontrado."
    if security_findings:
        security_items = []
        for f in security_findings:
            security_items.append(
                f"- **{f['file']}** (Linha {f['line']}): {f['category']} - {f['description']}"
            )
        security_context = "\n".join(security_items)

    # --- FASE 2: REDUCE (Geração do Relatório Final) ---
    
    system_prompt = """
    Você é um arquiteto de software sênior e um comunicador técnico excepcional.
    Sua tarefa é gerar um relatório de análise de código em Markdown.
    
    O público-alvo é misto: gestores (leigos) e desenvolvedores.
    
    Use as informações fornecidas (resumos dos arquivos e achados de segurança) para criar o relatório.
    
    **Estrutura Obrigatória do Relatório:**
    
    1. **Resumo Executivo**: Linguagem simples para leigos. Explique o que é este projeto em um parágrafo.
    2. **O que o programa faz**: Descreva as funcionalidades principais.
    3. **Como ele funciona**: Visão geral da arquitetura e fluxo de dados.
    4. **Onde alterar**: Guia prático para desenvolvedores:
       - Como mudar o comportamento principal.
       - Onde corrigir bugs prováveis.
       - Onde alterar integrações (APIs, bancos de dados).
       - Como melhorar a segurança.
    5. **Erros e Riscos**: Explique os achados de segurança listados de forma acessível, sem jargões excessivos.
    6. **Recomendações Práticas**: Lista de melhorias que podem ser feitas agora.
    7. **Prompts prontos para usar no AIDER**: Crie uma lista de 3 a 5 prompts específicos e prontos para copiar e colar.
       Estes prompts devem ser para a ferramenta "AIDER" (um assistente de codificação com IA).
       Eles devem instruir o AIDER a implementar as mudanças sugeridas nas seções anteriores.
    
    **Instruções Adicionais:**
    - Seja direto e objetivo.
    - Use formatação Markdown (negrito, listas, blocos de código).
    - Não invente funcionalidades que não estão nos resumos dos arquivos.
    """

    user_prompt = f"""
    Aqui estão os resumos técnicos dos arquivos do projeto:
    
    --- RESUMOS DOS ARQUIVOS ---
    {combined_summaries}
    ----------------------------
    
    Aqui estão os achados de segurança detectados:
    
    --- SEGURANÇA ---
    {security_context}
    ------------------
    
    Com base nisso, gere o relatório completo seguindo a estrutura obrigatória.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        return ai_client.chat(messages)
    except Exception as e:
        return f"Erro ao gerar relatório final: {str(e)}"
