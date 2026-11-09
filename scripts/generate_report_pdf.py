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

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        HRFlowable
    )
except ImportError as exc:
    raise ImportError(
        f"A biblioteca 'reportlab' é necessária para gerar relatórios em PDF. "
        f"Instale-a via 'pip install reportlab'. Erro original: {exc}"
    )

from services.api_service import get_subjects, get_academic_tasks


def get_demo_report_data() -> Dict[str, Any]:
    """Retorna dados demonstrativos para geração autônoma do relatório."""
    return {
        "student_name": "Estudante EduTrack",
        "student_email": "estudante@edutrack.ai",
        "subjects": [
            {"id": 1, "name": "Algoritmos e Estruturas de Dados", "teacher": "Prof. Alan Turing", "hours": 60},
            {"id": 2, "name": "Banco de Dados Relacionais", "teacher": "Prof. Edgar Codd", "hours": 40},
            {"id": 3, "name": "Engenharia de Software", "teacher": "Prof. Margaret Hamilton", "hours": 60}
        ],
        "tasks": [
            {"id": 101, "subject_id": 1, "title": "Lista 1: Ponteiros e Listas Ligadas", "due_date": "2026-11-10", "status": "completed"},
            {"id": 102, "subject_id": 1, "title": "Projeto 1: Árvore Binária AVL", "due_date": "2026-11-20", "status": "pending"},
            {"id": 103, "subject_id": 2, "title": "Modelagem Conceitual DER", "due_date": "2026-11-12", "status": "completed"},
            {"id": 104, "subject_id": 2, "title": "Consultas SQL Avançadas e Views", "due_date": "2026-11-25", "status": "completed"},
            {"id": 105, "subject_id": 3, "title": "Documento de Visão de Produto", "due_date": "2026-11-15", "status": "completed"},
            {"id": 106, "subject_id": 3, "title": "Arquitetura e Diagrama de Classes", "due_date": "2026-11-28", "status": "pending"}
        ]
    }


import io


def _build_pdf_doc(
    target: Any,
    student_name: str = "Estudante EduTrack",
    student_email: str = "estudante@edutrack.ai",
    token: Optional[str] = None,
    subjects: Optional[List[Dict[str, Any]]] = None,
    tasks: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Constrói o documento PDF no destino fornecido (caminho de arquivo ou buffer BytesIO)."""
    # 1. Obtenção dos dados: memória, API remota ou fallback demonstrativo
    if subjects is None or tasks is None:
        if token:
            subj_ok, subj_data, _ = get_subjects(token)
            task_ok, task_data, _ = get_academic_tasks(token)
            if subj_ok and task_ok:
                subjects = subj_data if isinstance(subj_data, list) else []
                tasks = task_data if isinstance(task_data, list) else []
            else:
                demo = get_demo_report_data()
                subjects = demo["subjects"]
                tasks = demo["tasks"]
        else:
            demo = get_demo_report_data()
            subjects = demo["subjects"]
            tasks = demo["tasks"]

    # Mapeamento de disciplinas por ID
    subjects_map = {s.get("id"): s.get("name", f"Disciplina {s.get('id')}") for s in subjects}

    # 2. Compilação de estatísticas
    total_subjects = len(subjects)
    total_tasks = len(tasks)
    
    completed_tasks_count = 0
    tasks_by_subject: Dict[int, List[Dict[str, Any]]] = {s.get("id"): [] for s in subjects}

    for task in tasks:
        s_id = task.get("subject_id")
        status = str(task.get("status", "")).strip().lower()
        is_completed = status in ["completed", "concluída", "concluida"]
        if is_completed:
            completed_tasks_count += 1
            
        if s_id in tasks_by_subject:
            tasks_by_subject[s_id].append(task)
        else:
            tasks_by_subject.setdefault(s_id, []).append(task)

    pending_tasks_count = total_tasks - completed_tasks_count
    overall_progress = round((completed_tasks_count / total_tasks * 100.0), 1) if total_tasks > 0 else 0.0

    # 3. Construção do documento PDF com ReportLab
    doc = SimpleDocTemplate(
        target,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1E3A8A")   # Azul escuro institucional
    secondary_color = colors.HexColor("#2563EB") # Azul primário
    text_dark = colors.HexColor("#1F2937")       # Cinza carvão
    accent_green = colors.HexColor("#059669")    # Verde sucesso
    bg_light = colors.HexColor("#F3F4F6")        # Cinza claro de fundo

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6
    )

    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=text_dark
    )

    cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=cell_style,
        fontName="Helvetica-Bold"
    )

    cell_completed = ParagraphStyle(
        "TableCellCompleted",
        parent=cell_style,
        fontName="Helvetica-Bold",
        textColor=accent_green
    )

    cell_pending = ParagraphStyle(
        "TableCellPending",
        parent=cell_style,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#D97706")
    )

    elements = []

    # Cabeçalho
    elements.append(Paragraph("EduTrack AI — Relatório de Desempenho Acadêmico", title_style))
    current_time_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
    elements.append(Paragraph(f"Emitido em: {current_time_str} | Plataforma de Gestão de Estudos EduTrack", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=secondary_color, spaceBefore=2, spaceAfter=12))

    # Dados do Estudante
    student_info_data = [
        [
            Paragraph("<b>Estudante:</b>", cell_style),
            Paragraph(student_name, cell_style),
            Paragraph("<b>E-mail:</b>", cell_style),
            Paragraph(student_email, cell_style)
        ],
        [
            Paragraph("<b>Total Disciplinas:</b>", cell_style),
            Paragraph(str(total_subjects), cell_bold),
            Paragraph("<b>Progresso Geral:</b>", cell_style),
            Paragraph(f"<b>{overall_progress}%</b> ({completed_tasks_count}/{total_tasks} tarefas)", cell_bold)
        ]
    ]
    student_table = Table(student_info_data, colWidths=[1.3 * inch, 2.3 * inch, 1.2 * inch, 2.5 * inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 14))

    # Seção 1: Resumo do Rendimento por Disciplina
    elements.append(Paragraph("1. Rendimento e Progresso por Disciplina", section_heading))
    
    subject_table_data = [
        [
            Paragraph("<b>Disciplina</b>", cell_bold),
            Paragraph("<b>Carga Horária</b>", cell_bold),
            Paragraph("<b>Tarefas Totais</b>", cell_bold),
            Paragraph("<b>Concluídas</b>", cell_bold),
            Paragraph("<b>Progresso</b>", cell_bold)
        ]
    ]

    for subj in subjects:
        s_id = subj.get("id")
        s_name = subj.get("name", f"Disciplina {s_id}")
        s_hours = f"{subj.get('hours', 0)}h"
        s_tasks = tasks_by_subject.get(s_id, [])
        s_total = len(s_tasks)
        s_done = sum(1 for t in s_tasks if str(t.get("status", "")).strip().lower() in ["completed", "concluída", "concluida"])
        s_pct = round((s_done / s_total * 100.0), 1) if s_total > 0 else 0.0

        subject_table_data.append([
            Paragraph(s_name, cell_style),
            Paragraph(s_hours, cell_style),
            Paragraph(str(s_total), cell_style),
            Paragraph(str(s_done), cell_style),
            Paragraph(f"<b>{s_pct}%</b>", cell_bold)
        ])

    subj_table = Table(subject_table_data, colWidths=[2.6 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch, 1.4 * inch])
    subj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0E7FF")),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(subj_table)
    elements.append(Spacer(1, 14))

    # Seção 2: Detalhamento de Tarefas Acadêmicas
    elements.append(Paragraph("2. Detalhamento das Tarefas Acadêmicas", section_heading))

    task_table_data = [
        [
            Paragraph("<b>ID</b>", cell_bold),
            Paragraph("<b>Disciplina</b>", cell_bold),
            Paragraph("<b>Título da Tarefa</b>", cell_bold),
            Paragraph("<b>Prazo</b>", cell_bold),
            Paragraph("<b>Status</b>", cell_bold)
        ]
    ]

    if tasks:
        for t in tasks:
            t_id = str(t.get("id", "-"))
            s_name = subjects_map.get(t.get("subject_id"), "Geral")
            t_title = t.get("title", "Sem título")
            t_due = t.get("due_date", "-")
            status_raw = str(t.get("status", "")).strip().lower()
            if status_raw in ["completed", "concluída", "concluida"]:
                status_p = Paragraph("Concluída", cell_completed)
            else:
                status_p = Paragraph("Pendente", cell_pending)

            task_table_data.append([
                Paragraph(t_id, cell_style),
                Paragraph(s_name, cell_style),
                Paragraph(t_title, cell_style),
                Paragraph(t_due, cell_style),
                status_p
            ])
    else:
        task_table_data.append([
            Paragraph("-", cell_style),
            Paragraph("Nenhuma tarefa cadastrada", cell_style),
            Paragraph("-", cell_style),
            Paragraph("-", cell_style),
            Paragraph("-", cell_style)
        ])

    task_table = Table(task_table_data, colWidths=[0.6 * inch, 2.0 * inch, 2.6 * inch, 1.1 * inch, 1.0 * inch])
    task_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0E7FF")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(task_table)

    # Rodapé
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#9CA3AF"), spaceBefore=8, spaceAfter=8))
    footer_text = Paragraph(
        "EduTrack AI — Documento gerado eletronicamente para fins de acompanhamento acadêmico pessoal.",
        subtitle_style
    )
    elements.append(footer_text)

    # 4. Construção do PDF no destino
    doc.build(elements)

    result = {
        "success": True,
        "student_name": student_name,
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks_count,
        "pending_tasks": pending_tasks_count,
        "overall_progress_percentage": overall_progress,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    if isinstance(target, str):
        abs_output = os.path.abspath(target)
        result["pdf_path"] = abs_output
        result["file_exists"] = os.path.exists(abs_output)
        result["file_size_bytes"] = os.path.getsize(abs_output) if os.path.exists(abs_output) else 0

    return result


def generate_student_performance_pdf(
    output_path: str = "relatorio_desempenho.pdf",
    student_name: str = "Estudante EduTrack",
    student_email: str = "estudante@edutrack.ai",
    token: Optional[str] = None,
    subjects: Optional[List[Dict[str, Any]]] = None,
    tasks: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Gera o relatório de desempenho do estudante em formato PDF salvando em arquivo no disco."""
    return _build_pdf_doc(
        target=output_path,
        student_name=student_name,
        student_email=student_email,
        token=token,
        subjects=subjects,
        tasks=tasks
    )


def generate_student_performance_pdf_bytes(
    student_name: str = "Estudante EduTrack",
    student_email: str = "estudante@edutrack.ai",
    token: Optional[str] = None,
    subjects: Optional[List[Dict[str, Any]]] = None,
    tasks: Optional[List[Dict[str, Any]]] = None
) -> bytes:
    """Gera o relatório de desempenho do estudante em formato PDF e retorna os bytes em memória."""
    buffer = io.BytesIO()
    _build_pdf_doc(
        target=buffer,
        student_name=student_name,
        student_email=student_email,
        token=token,
        subjects=subjects,
        tasks=tasks
    )
    buffer.seek(0)
    return buffer.getvalue()



def main():
    parser = argparse.ArgumentParser(
        description="Gera relatório de desempenho do estudante em formato PDF para o EduTrack AI."
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="relatorio_desempenho.pdf",
        help="Caminho do arquivo PDF gerado (padrão: relatorio_desempenho.pdf)."
    )
    parser.add_argument(
        "--token",
        "-t",
        type=str,
        default=None,
        help="Token JWT opcional para consultar disciplinas e tarefas reais do Xano."
    )
    parser.add_argument(
        "--student-name",
        type=str,
        default="Estudante EduTrack",
        help="Nome do estudante a ser impresso no relatório."
    )
    parser.add_argument(
        "--student-email",
        type=str,
        default="estudante@edutrack.ai",
        help="E-mail do estudante a ser impresso no relatório."
    )

    args = parser.parse_args()

    result = generate_student_performance_pdf(
        output_path=args.output,
        student_name=args.student_name,
        student_email=args.student_email,
        token=args.token
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
