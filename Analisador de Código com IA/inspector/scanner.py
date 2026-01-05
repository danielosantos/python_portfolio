import os
import config

def scan_project(root_path: str) -> list[dict]:
    """
    Varre um diretório local recursivamente para encontrar arquivos de texto permitidos.
    
    Args:
        root_path (str): O caminho raiz do projeto a ser analisado.
        
    Returns:
        list[dict]: Uma lista de dicionários contendo 'path' (caminho relativo) e 'content' (texto).
    """
    
    # Verifica se o caminho raiz existe e é um diretório
    if not os.path.isdir(root_path):
        raise ValueError(f"O caminho fornecido não é um diretório válido: {root_path}")

    scanned_files = []

    # os.walk gera os nomes dos arquivos em uma árvore de diretórios, percorrendo de cima para baixo
    for current_dir, dirs, files in os.walk(root_path):
        
        # 1. Filtragem de Pastas
        # Modificamos a lista 'dirs' in-place para impedir que o os.walk entre em pastas ignoradas.
        # Isso é mais eficiente do que verificar o caminho completo depois.
        dirs[:] = [d for d in dirs if d not in config.IGNORED_FOLDERS]

        for filename in files:
            file_path = os.path.join(current_dir, filename)
            
            # 2. Verificação de Extensão
            # Verifica se a extensão do arquivo está na lista de permitidos
            _, ext = os.path.splitext(filename)
            if ext not in config.ALLOWED_EXTENSIONS:
                continue

            # 3. Verificação de Tamanho
            # Ignora arquivos que excedem o limite de bytes configurado
            try:
                if os.path.getsize(file_path) > config.MAX_FILE_BYTES:
                    continue
            except OSError:
                # Se não for possível obter o tamanho (ex: link quebrado, permissão), ignora
                continue

            # 4. Leitura do Conteúdo
            try:
                # Tenta abrir o arquivo como UTF-8 (padrão para código fonte moderno)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Se falhar a decodificação, não é um arquivo de texto válido (ou é binário)
                continue
            except (IOError, PermissionError):
                # Ignora erros de leitura/permissão para não quebrar o scanner
                continue

            # 5. Cálculo do Caminho Relativo
            # Retorna o caminho relativo ao root_path para facilitar a visualização
            relative_path = os.path.relpath(file_path, root_path)

            scanned_files.append({
                "path": relative_path,
                "content": content
            })

    return scanned_files
