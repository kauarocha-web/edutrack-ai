import os
import sys

# Se requests não estiver disponível no Python do sistema, adiciona o site-packages do .venv
try:
    import requests
except ImportError:
    _root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    _venv_site_packages = os.path.join(_root_dir, ".venv", "Lib", "site-packages")
    if os.path.exists(_venv_site_packages) and _venv_site_packages not in sys.path:
        sys.path.insert(0, _venv_site_packages)
    import requests

from datetime import datetime
from typing import Tuple, Any, Optional

# ==============================================================================
# Carregamento de Variáveis de Ambiente (.env)
# ==============================================================================
def _load_env_variables():
    """Carrega as variáveis do arquivo .env localizado na raiz do projeto."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_file = os.path.join(root_dir, ".env")
    
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        return
    except ImportError:
        pass

    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if key not in os.environ:
                        os.environ[key] = val

_load_env_variables()

# URLs Base dos grupos de API do Xano
DEFAULT_SUBJECTS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:4cvOQ4Zo"
DEFAULT_TASKS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:CwqMGDvq"

SUBJECTS_BASE_URL = os.getenv("XANO_SUBJECTS_BASE_URL", DEFAULT_SUBJECTS_URL).rstrip("/")
TASKS_BASE_URL = os.getenv("XANO_TASKS_BASE_URL", DEFAULT_TASKS_URL).rstrip("/")

# ==============================================================================
# Função Genérica para Requisições Autenticadas
# ==============================================================================
def make_authenticated_request(
    method: str,
    url: str,
    token: Optional[str],
    json_data: Optional[dict] = None,
    timeout: int = 10
) -> Tuple[bool, Any, int]:
    """
    Executa uma requisição HTTP enviando o cabeçalho Authorization: Bearer <token>.
    Retorna uma tupla (sucesso, dados_ou_mensagem_erro, status_code).
    """
    if not token:
        return False, "Usuário não autenticado. Por favor, acesse a página de Perfil e faça login.", 401

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data,
            timeout=timeout
        )

        # Token inválido ou expirado
        if response.status_code == 401:
            return False, "Sessão expirada ou token de acesso inválido. Por favor, refaça o login na página de Perfil.", 401

        # Resposta com sucesso (200, 201)
        if 200 <= response.status_code < 300:
            try:
                data = response.json()
            except Exception:
                data = response.text
            return True, data, response.status_code

        # Erros retornados pelo backend
        try:
            err_json = response.json()
            error_msg = err_json.get("message") or err_json.get("error") or str(err_json)
        except Exception:
            error_msg = response.text or f"Erro HTTP {response.status_code}"

        return False, f"Falha na requisição ({response.status_code}): {error_msg}", response.status_code

    except requests.exceptions.RequestException as e:
        return False, f"Erro de conexão com o servidor Xano: {str(e)}", 0

# ==============================================================================
# Serviços de Disciplinas (Subjects)
# ==============================================================================
def get_subjects(token: Optional[str]) -> Tuple[bool, Any, int]:
    """
    Consulta todas as disciplinas pertencentes ao usuário autenticado (GET /subjects).
    """
    url = f"{SUBJECTS_BASE_URL}/subjects"
    return make_authenticated_request("GET", url, token)

def create_subject(
    token: Optional[str],
    name: str,
    teacher: str = "",
    hours: int = 0
) -> Tuple[bool, Any, int]:
    """
    Cria uma nova disciplina vinculada ao usuário autenticado (POST /subjects).
    """
    url = f"{SUBJECTS_BASE_URL}/subjects"
    payload = {
        "name": name.strip(),
        "teacher": teacher.strip(),
        "hours": int(hours)
    }
    return make_authenticated_request("POST", url, token, json_data=payload)

# ==============================================================================
# Serviços de Tarefas Acadêmicas (Academic Tasks)
# ==============================================================================
def get_academic_tasks(token: Optional[str]) -> Tuple[bool, Any, int]:
    """
    Consulta todas as tarefas acadêmicas pertencentes ao usuário autenticado (GET /academic_tasks).
    """
    url = f"{TASKS_BASE_URL}/academic_tasks"
    return make_authenticated_request("GET", url, token)

def create_academic_task(
    token: Optional[str],
    title: str,
    description: str = "",
    due_date: Optional[str] = None,
    status: str = "pending",
    subject_id: Optional[int] = None
) -> Tuple[bool, Any, int]:
    """
    Cria uma nova tarefa acadêmica vinculada ao usuário e à disciplina selecionada (POST /academic_tasks).
    Garante valores válidos e não vazios para todos os parâmetros exigidos pelo Xano.
    """
    url = f"{TASKS_BASE_URL}/academic_tasks"

    clean_title = title.strip()
    clean_desc = description.strip() if description and description.strip() else "Sem descrição"
    clean_due_date = str(due_date).strip() if due_date and str(due_date).strip() else datetime.now().strftime("%Y-%m-%d")
    clean_status = status.strip() if status and status.strip() else "pending"
    clean_subject_id = int(subject_id) if subject_id is not None else 0

    payload = {
        "title": clean_title,
        "description": clean_desc,
        "due_date": clean_due_date,
        "status": clean_status,
        "subject_id": clean_subject_id
    }
    return make_authenticated_request("POST", url, token, json_data=payload)

def update_academic_task_status(
    token: Optional[str],
    task_id: int,
    status: str,
    task_data: Optional[dict] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    subject_id: Optional[int] = None
) -> Tuple[bool, Any, int]:
    """
    Atualiza o status de uma tarefa acadêmica existente (PATCH /academic_tasks/{id}).
    Envia todos os campos da tarefa para satisfazer os requisitos do backend Xano.
    """
    url = f"{TASKS_BASE_URL}/academic_tasks/{task_id}"

    if task_data:
        title = title or task_data.get("title")
        description = description or task_data.get("description")
        due_date = due_date or task_data.get("due_date")
        subject_id = subject_id if subject_id is not None else task_data.get("subject_id")

    clean_title = (title or "Tarefa").strip()
    clean_desc = (description or "Sem descrição").strip() if (description and str(description).strip()) else "Sem descrição"
    clean_due_date = str(due_date).strip() if (due_date and str(due_date).strip()) else datetime.now().strftime("%Y-%m-%d")
    clean_status = status.strip() if status else "pending"
    clean_subject_id = int(subject_id) if (subject_id is not None and str(subject_id).isdigit()) else 0

    payload = {
        "title": clean_title,
        "description": clean_desc,
        "due_date": clean_due_date,
        "status": clean_status,
        "subject_id": clean_subject_id
    }
    return make_authenticated_request("PATCH", url, token, json_data=payload)


