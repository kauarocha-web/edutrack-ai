## Context

O EduTrack AI dispõe de endpoints CRUD RESTful para `subjects` e `academic_tasks` protegidos por autenticação Bearer token JWT (`user_id == $auth.id`), além do módulo de integração `services/api_service.py`. Para permitir o acompanhamento e análise de desempenho acadêmico, é necessário criar um script dedicado em Python para calcular a porcentagem de progresso de uma disciplina com base em suas tarefas e produzir o resultado formatado em JSON. Veja `proposal.md` para motivação e `specs/logica-calculo-progresso/spec.md` para os requisitos.

## Goals / Non-Goals

**Goals:**
- Criar o script Python em `scripts/calculate_progress.py`.
- Implementar a função principal `calculate_subject_progress(subject_id: int, token: Optional[str] = None, tasks_list: Optional[list] = None) -> dict`:
  - Consumir as tarefas através do endpoint CRUD `GET /academic_tasks` utilizando o token JWT ou receber a lista de tarefas diretamente em memória.
  - Filtrar as tarefas correspondentes ao `subject_id` informado.
  - Contabilizar o total de tarefas e tarefas concluídas (`status.lower() in ["completed", "concluída", "concluida"]`).
  - Calcular a porcentagem de progresso: `round((completed_tasks / total_tasks) * 100.0, 2)` com proteção contra divisão por zero (`0.0%` se `total_tasks == 0`).
  - Retornar o resultado estruturado em dicionário e função auxiliar para geração da string JSON formatada.
- Disponibilizar interface CLI no script para execução direta via terminal passando argumentos (`--subject-id`, `--token`).

**Non-Goals:**
- Não criar nem modificar endpoints de backend ou arquivos `.xs`.
- Não executar comandos de push, sincronização ou deploy para o Xano (REGRA Nº 2 do `AGENTS.md`).
- Não alterar as páginas do frontend Streamlit a menos que expressamente solicitado (REGRA Nº 1 do `AGENTS.md`).

## Decisions

### 1. Flexibilidade da Função de Cálculo
- A função aceitará tanto a busca remota via API CRUD (`token` informado) quanto uma lista pré-carregada (`tasks_list`), permitindo reutilização no frontend (onde as tarefas já podem estar no `session_state`) e testes autônomos sem chamadas de rede.

### 2. Tratamento de Status e Casos Limite
- Tarefas concluídas: verificação flexível de status (`"completed"`, `"concluída"` ou booleanos equivalentes).
- Divisão por zero: quando `total_tasks == 0`, a porcentagem será explicitamente `0.0`, evitando falhas matemáticas em disciplinas recém-cadastradas.

### 3. Formato do JSON de Saída
```json
{
  "subject_id": 1,
  "total_tasks": 4,
  "completed_tasks": 2,
  "pending_tasks": 2,
  "progress_percentage": 50.0,
  "calculated_at": "2026-10-30T10:00:00Z"
}
```

## Risks / Trade-offs

- **[Token não informado ao rodar via CLI]** → *Mitigação*: Ler token a partir de argumento de linha de comando ou tentar ler de variável de ambiente / `.env` caso disponível.
- **[Status com grafias variadas]** → *Mitigação*: Normalização de string (`strip().lower()`) para contemplar `"completed"` e `"concluída"`.

## Migration Plan

1. Criar o diretório `scripts/` se ainda não existir.
2. Implementar `scripts/calculate_progress.py`.
3. Validar a execução da função e os retornos em JSON com casos de teste.
