import sys
import os
import json
import argparse
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

# Garante que a raiz do projeto e o site-packages do .venv estejam no sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

VENV_SITE_PACKAGES = os.path.join(PROJECT_ROOT, ".venv", "Lib", "site-packages")
if os.path.exists(VENV_SITE_PACKAGES) and VENV_SITE_PACKAGES not in sys.path:
    sys.path.insert(0, VENV_SITE_PACKAGES)

from services.api_service import get_academic_tasks, get_subjects


def calculate_subject_progress(
    subject_id: int,
    token: Optional[str] = None,
    tasks_list: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Calcula a porcentagem de progresso de uma disciplina com base em suas tarefas (concluídas / total).
    
    Parâmetros:
        subject_id: ID da disciplina para cálculo.
        token: Token JWT de autenticação (usado se tasks_list não for fornecido para buscar via API CRUD).
        tasks_list: Lista opcional de tarefas em memória para cálculo direto sem requisição HTTP.
        
    Retorna:
        Dicionário com o total de tarefas, tarefas concluídas, pendentes e porcentagem de progresso.
    """
    # Se a lista de tarefas não foi passada em memória, busca via API CRUD
    if tasks_list is None:
        if not token:
            return {
                "success": False,
                "subject_id": subject_id,
                "error": "Token JWT de autenticação não informado e nenhuma lista de tarefas fornecida.",
                "total_tasks": 0,
                "completed_tasks": 0,
                "pending_tasks": 0,
                "progress_percentage": 0.0,
                "calculated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            }

        success, data, status_code = get_academic_tasks(token)
        if not success:
            return {
                "success": False,
                "subject_id": subject_id,
                "error": f"Falha ao consultar tarefas da API CRUD ({status_code}): {data}",
                "total_tasks": 0,
                "completed_tasks": 0,
                "pending_tasks": 0,
                "progress_percentage": 0.0,
                "calculated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        
        all_tasks = data if isinstance(data, list) else []
    else:
        all_tasks = tasks_list

    # Filtra as tarefas pertencentes à disciplina solicitada
    subject_tasks = [t for t in all_tasks if t.get("subject_id") == subject_id]

    total_tasks = len(subject_tasks)
    
    # Contabiliza tarefas concluídas (status case-insensitive)
    completed_statuses = {"completed", "concluída", "concluida", "done"}
    completed_tasks = len([
        t for t in subject_tasks
        if str(t.get("status", "")).strip().lower() in completed_statuses
    ])
    
    pending_tasks = total_tasks - completed_tasks

    # Proteção contra divisão por zero
    if total_tasks > 0:
        progress_percentage = round((completed_tasks / total_tasks) * 100.0, 2)
    else:
        progress_percentage = 0.0

    return {
        "success": True,
        "subject_id": subject_id,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress_percentage": progress_percentage,
        "calculated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def calculate_subject_progress_json(
    subject_id: int,
    token: Optional[str] = None,
    tasks_list: Optional[List[Dict[str, Any]]] = None,
    indent: int = 2
) -> str:
    """
    Retorna o resultado do cálculo de progresso formatado como string JSON.
    """
    result = calculate_subject_progress(subject_id=subject_id, token=token, tasks_list=tasks_list)
    return json.dumps(result, indent=indent, ensure_ascii=False)


def main():
    """Interface de linha de comando (CLI) para execução direta do script."""
    parser = argparse.ArgumentParser(
        description="Calcula o progresso de tarefas de uma disciplina no EduTrack AI via endpoints CRUD."
    )
    parser.add_argument(
        "--subject-id",
        type=int,
        default=None,
        help="ID numérico da disciplina (opcional)"
    )
    parser.add_argument(
        "--token",
        type=str,
        default=os.getenv("AUTH_TOKEN") or os.getenv("XANO_AUTH_TOKEN"),
        help="Token JWT de autenticação para chamada aos endpoints CRUD"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indentação da saída JSON (padrão: 2)"
    )

    args = parser.parse_args()

    # Se subject_id for especificado, calcula para a disciplina indicada
    if args.subject_id is not None:
        json_output = calculate_subject_progress_json(
            subject_id=args.subject_id,
            token=args.token,
            indent=args.indent
        )
        print(json_output)
        return

    # Se nenhum subject-id foi passado, mas temos token, calcula para todas as disciplinas da conta
    if args.token:
        ok_subj, subjects, _ = get_subjects(args.token)
        ok_tasks, tasks, _ = get_academic_tasks(args.token)
        if ok_subj and isinstance(subjects, list):
            results = []
            for s in subjects:
                s_id = s.get("id")
                prog = calculate_subject_progress(subject_id=s_id, tasks_list=tasks if ok_tasks else None)
                prog["subject_name"] = s.get("name")
                results.append(prog)
            print(json.dumps({"success": True, "subjects_progress": results}, indent=args.indent, ensure_ascii=False))
            return

    # Execução padrão/demonstração quando o script for chamado diretamente sem parâmetros
    sample_tasks = [
        {"id": 1, "subject_id": 1, "title": "Modelagem de Dados", "status": "completed"},
        {"id": 2, "subject_id": 1, "title": "Implementação de APIs", "status": "completed"},
        {"id": 3, "subject_id": 1, "title": "Testes de Integração", "status": "pending"},
        {"id": 4, "subject_id": 1, "title": "Deploy e Documentação", "status": "pending"}
    ]
    demo_result = calculate_subject_progress(subject_id=1, tasks_list=sample_tasks)
    demo_result["mode"] = "demonstration"
    demo_result["info"] = "Execução sem parâmetros. Use --subject-id <id> e --token <jwt> para consultar a API Xano."
    print(json.dumps(demo_result, indent=args.indent, ensure_ascii=False))


if __name__ == "__main__":
    main()
