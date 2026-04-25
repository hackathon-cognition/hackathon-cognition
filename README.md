# hackathon-cognition

Sistema de segunda opinião médica via Telegram. Paciente envia caso → matching automático com 5 especialistas → médicos respondem em até 3h → paciente recebe opiniões e aceita agendamento.

## Stack
Python 3.13 · python-telegram-bot · SQLAlchemy · SQLite. Long-polling (sem webhook). Dois bots: paciente e médico.

## Setup (5 min)

1. Cria dois bots no Telegram via [@BotFather](https://t.me/BotFather):
   - um para paciente (ex: `MeuSegundaOpiniaoBot`)
   - um para médico (ex: `MeuSegundaOpiniaoMedicoBot`)
   - guarda os dois tokens

2. Configura ambiente:
   ```bash
   cp .env.example .env
   # cola PATIENT_BOT_TOKEN e DOCTOR_BOT_TOKEN no .env
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

3. Roda:
   ```bash
   .venv/bin/python -m app.main
   ```
   Os médicos seedados são criados automaticamente na primeira execução.

## Comandos

**Bot do paciente:**
- `/start` — cadastra (pergunta nome)
- `/caso` — inicia novo caso (diagnóstico → sintomas → médico anterior → arquivos → confirmar)
- `/sim` `/nao` — confirma envio
- `/pular` — pula etapa opcional

**Bot do médico:**
- `/start` — boas-vindas
- `/cardiologia` `/neurologia` `/dermatologia` `/ortopedia` `/clinica` — vincula a uma especialidade (toma slot de demo)
- `/casos` — lista pendentes
- Ao abrir caso: botões Concordo/Discordo. Discordo abre fluxo de propor agendamento (`/presencial` `/remoto` → data/hora → notas).

## Demo (3 min)

1. Você (paciente): `/start`, `/caso`, descreve "diagnóstico de ansiedade, mas tenho dor no peito persistente"
2. Sistema detecta cardiologia, matcha 5 cardiologistas, notifica todos
3. Um teammate (médico real) clica `/casos` e responde Discordo + propõe consulta
4. 4 médicos seedados respondem automaticamente após 8–25s (mistura de Concordo/Discordo)
5. Paciente recebe todas as opiniões, aceita um agendamento
6. Médico real recebe notificação de aceite

## Cortes deliberados (deferred)
Pagamento, calendário real, verificação de credenciais, dashboard web, multi-language. Veja `PRD-second-opinion-diagnosis.md`.
