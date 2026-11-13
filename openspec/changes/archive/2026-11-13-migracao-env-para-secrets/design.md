## Context

O EduTrack AI atualmente utiliza um arquivo `.env` lido manualmente através de parsing customizado e `python-dotenv` em `pages/3_👤_Perfil.py` e `services/api_service.py`. No entanto, o ecossistema Streamlit adota nativamente o `st.secrets` lido de `.streamlit/secrets.toml`, que oferece suporte direto tanto no desenvolvimento local quanto no deploy em produção (Streamlit Community Cloud). Esta proposta planeja a migração unificada da leitura dessas configurações para o `st.secrets`. Consulte `proposal.md` para a motivação e `specs/migracao-env-para-secrets/spec.md` para os requisitos formais.

## Goals / Non-Goals

**Goals:**
- Validar e ajustar `.streamlit/secrets.toml` com sintaxe TOML correta para todas as variáveis do Xano:
  - `XANO_AUTH_BASE_URL`
  - `XANO_SUBJECTS_BASE_URL`
  - `XANO_TASKS_BASE_URL`
- Implementar função utilitária resiliente para obtenção de secrets (ex: `get_config_value(key, default)`) que busca primeiro em `st.secrets`, depois em `os.environ` e por fim no valor padrão canônico.
- Migrar `services/api_service.py` para utilizar `st.secrets` prioritariamente.
- Migrar `pages/3_👤_Perfil.py` para utilizar `st.secrets`, removendo o carregamento manual de `.env`.
- Atualizar legendas e mensagens na interface de `pages/3_👤_Perfil.py`.

**Non-Goals:**
- Não criar nem modificar endpoints de backend no Xano.
- Não executar comandos de push, sync ou deploy para o Xano (REGRA Nº 2 do `AGENTS.md`).
- Não alterar a lógica de autenticação ou de CRUD das disciplinas e tarefas além da origem das URLs.

## Decisions

### 1. Mecanismo Resiliente de Obtenção de Segredos
Para evitar que scripts executados fora do Streamlit (como `scripts/calculate_progress.py` ou `scripts/generate_report_pdf.py` via CLI) lancem exceções ao tentar acessar `st.secrets`, utilizaremos um padrão seguro de acesso:
```python
def get_config_value(key: str, default: str = "") -> str:
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return os.getenv(key, default).strip()
```

### 2. Sintaxe em `.streamlit/secrets.toml`
Garantir o formato TOML padrão:
```toml
# URLs Base dos endpoints do Xano
XANO_AUTH_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:72mncMCo"
XANO_SUBJECTS_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:4cvOQ4Zo"
XANO_TASKS_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:CwqMGDvq"
```

## Risks / Trade-offs

- **[Execução de scripts CLI sem servidor Streamlit ativo]** → *Mitigação*: Fallback seguro para `os.environ` e URLs padrão canônicas.
- **[secrets.toml com erros de sintaxe TOML]** → *Mitigação*: Corrigir formatação de aspas em `.streamlit/secrets.toml` e validar parsing antes do apply.

## Migration Plan

1. Criar e validar artefatos do OpenSpec.
2. Na etapa de `apply`:
   - Corrigir a sintaxe em `.streamlit/secrets.toml`.
   - Atualizar `services/api_service.py`.
   - Atualizar `pages/3_👤_Perfil.py`.
   - Testar a leitura de segredos na aplicação Streamlit e a execução dos scripts CLI.
