import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente a partir de um arquivo .env (se existir)
load_dotenv()

# --- Configurações da API OpenRouter ---

# URL base para o endpoint de chat da API OpenRouter
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Chave da API obtida das variáveis de ambiente
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Modelo de IA a ser utilizado. 
# Padrão: "google/gemini-flash-1.5" caso não esteja definido no .env
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5")

# --- Configurações Gerais do Sistema ---

# Tempo limite (em segundos) para operações de rede
TIMEOUT_SECONDS = 30

# Tamanho máximo (em bytes) de um arquivo para ser processado
MAX_FILE_BYTES = 200000

# --- Listas de Exclusão e Permissão ---

# Lista de pastas que devem ser ignoradas automaticamente durante a varredura
IGNORED_FOLDERS = [
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__"
]

# Lista de extensões de arquivo consideradas texto/código para análise
ALLOWED_EXTENSIONS = [
    ".txt",
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".json",
    ".md",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".sh",
    ".bat",
    ".c",
    ".cpp",
    ".h",
    ".java",
    ".go",
    ".rs"
]
