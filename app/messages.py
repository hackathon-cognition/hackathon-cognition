"""PT-BR strings. HTML parse_mode."""

# Patient bot ------------------------------------------------------------
WELCOME_NEW = (
    "👋 Olá! Sou seu assistente para pedir uma segunda opinião médica.\n\n"
    "Para começar, qual seu nome?"
)
WELCOME_BACK = (
    "👋 Olá de novo, {name}!\n\n"
    "Comandos disponíveis:\n"
    "/caso &lt;descrição&gt; — descreve seu diagnóstico\n"
    "/exames — anexa fotos ou PDFs\n"
    "/enviar — envia para os especialistas\n"
    "/agendar — vê propostas de consulta\n"
    "/cancelar — descarta rascunho atual"
)
NAME_SAVED = (
    "Prazer, {name}! 🤝\n\n"
    "Para iniciar uma segunda opinião, use:\n"
    "<code>/caso seu diagnóstico aqui</code>"
)

ASK_CASO_USAGE = (
    "📋 Use o comando assim:\n\n"
    "<code>/caso fui diagnosticado com X, sinto Y, há Z semanas</code>\n\n"
    "Quanto mais detalhe, melhor a opinião dos especialistas."
)

CASE_DRAFT_SAVED = (
    "✅ Caso registrado.\n\n"
    "Quer anexar exames? Use /exames\n"
    "Quando estiver pronto, use /enviar para mandar aos especialistas.\n"
    "Para descartar, /cancelar."
)

ASK_FILES_NOW = "📎 Envie fotos de exames ou PDFs agora. Quando terminar, use /enviar."
FILE_RECEIVED = "✅ Arquivo recebido ({count} no total). Mande mais ou /enviar."

NO_DRAFT = "⚠️ Você não tem caso em andamento. Use /caso &lt;descrição&gt; para começar."

CASE_SUBMITTED_AWAITING = (
    "🚀 Caso enviado para {count} especialistas em <b>{specialty}</b>.\n\n"
    "⏳ Aguarde — você será notificado conforme as opiniões chegarem (até 3 horas)."
)
CASE_NO_MATCH = "⚠️ Nenhum especialista disponível agora. Tente novamente em breve."

CASE_CANCELLED = "❌ Rascunho descartado. Use /caso para começar de novo."

# Opinion notifications
OPINION_AGREE_TEMPLATE = (
    "💬 <b>Nova opinião de {doctor_name}</b> ({specialty})\n\n"
    "✅ <b>Concorda</b> com o diagnóstico.\n\n"
    "📝 <b>Observações:</b> {notes}"
)

OPINION_DISAGREE_TEMPLATE = (
    "💬 <b>Nova opinião de {doctor_name}</b> ({specialty})\n\n"
    "❌ <b>Discorda</b> do diagnóstico.\n\n"
    "📝 <b>Observações:</b> {notes}\n\n"
    "Para responder à proposta de consulta, use /agendar"
)

# Appointment
NO_OFFERS = "📭 Você não tem propostas de consulta pendentes."
OFFERS_HEADER = "📅 <b>Propostas de consulta pendentes:</b>"
APPOINTMENT_CONFIRMED_PATIENT = (
    "✅ Agendamento confirmado com {doctor_name}!\n\n"
    "Tipo: {type}\nQuando: {slot_text}\n\n"
    "Você receberá um lembrete antes do horário."
)


# Web dashboard ----------------------------------------------------------
WEB_TITLE = "MediCheck — Painel Médico"
