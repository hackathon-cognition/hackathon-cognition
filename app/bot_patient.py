"""Telegram bot for patients."""
import asyncio
import html
import json
import logging
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from app.db import SessionLocal, Patient, Case, Opinion, Appointment
from app.matching import detect_specialty, match_doctors
from app.messages import (
    WELCOME_NEW, WELCOME_BACK, NAME_SAVED,
    ASK_CASO_USAGE, CASE_DRAFT_SAVED, ASK_FILES_NOW, FILE_RECEIVED, NO_DRAFT,
    CASE_SUBMITTED_AWAITING, CASE_NO_MATCH, CASE_CANCELLED,
    NO_OFFERS, OFFERS_HEADER, APPOINTMENT_CONFIRMED_PATIENT,
)
from app.auto_respond import auto_respond_for_case


NAME_STATE = 1


# ---------- registration ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.effective_user.id
    with SessionLocal() as s:
        patient = s.query(Patient).filter_by(telegram_id=tid).first()
        if patient:
            await update.message.reply_text(WELCOME_BACK.format(name=patient.name), parse_mode="HTML")
            return ConversationHandler.END
    await update.message.reply_text(WELCOME_NEW)
    return NAME_STATE


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.effective_user.id
    name = update.message.text.strip()[:120]
    with SessionLocal() as s:
        if not s.query(Patient).filter_by(telegram_id=tid).first():
            s.add(Patient(telegram_id=tid, name=name))
            s.commit()
    await update.message.reply_text(NAME_SAVED.format(name=name), parse_mode="HTML")
    return ConversationHandler.END


# ---------- case lifecycle ----------
async def cmd_caso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.effective_user.id
    text = " ".join(context.args).strip() if context.args else ""
    if not text:
        await update.message.reply_text(ASK_CASO_USAGE, parse_mode="HTML")
        return
    with SessionLocal() as s:
        patient = s.query(Patient).filter_by(telegram_id=tid).first()
        if not patient:
            await update.message.reply_text("Use /start primeiro.")
            return
        existing = (
            s.query(Case)
            .filter(Case.patient_id == patient.id, Case.status == "draft")
            .first()
        )
        if existing:
            existing.diagnosis = text
            existing.files_json = "[]"
            case_id = existing.id
        else:
            case = Case(
                patient_id=patient.id,
                diagnosis=text,
                symptoms="",
                files_json="[]",
                status="draft",
            )
            s.add(case)
            s.flush()
            case_id = case.id
        s.commit()
    context.user_data["draft_case_id"] = case_id
    context.user_data["awaiting_files"] = False
    await update.message.reply_text(CASE_DRAFT_SAVED)


def _get_active_draft_id(telegram_id: int) -> int | None:
    """Look up the user's current draft case from the DB (stateless)."""
    with SessionLocal() as s:
        patient = s.query(Patient).filter_by(telegram_id=telegram_id).first()
        if not patient:
            return None
        draft = (
            s.query(Case)
            .filter(Case.patient_id == patient.id, Case.status == "draft")
            .first()
        )
        return draft.id if draft else None


async def cmd_exames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _get_active_draft_id(update.effective_user.id):
        await update.message.reply_text(NO_DRAFT, parse_mode="HTML")
        return
    await update.message.reply_text(ASK_FILES_NOW)


async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    case_id = _get_active_draft_id(update.effective_user.id)
    if not case_id:
        await msg.reply_text(
            "⚠️ Você ainda não tem um caso em andamento. Use /caso &lt;descrição&gt; primeiro.",
            parse_mode="HTML",
        )
        return
    Path("data/files").mkdir(parents=True, exist_ok=True)
    entry: dict | None = None
    try:
        if msg.photo:
            photo = msg.photo[-1]
            f = await photo.get_file()
            path = f"data/files/{f.file_unique_id}.jpg"
            await f.download_to_drive(path)
            entry = {"path": path, "name": f"foto_{f.file_unique_id[:6]}.jpg"}
        elif msg.document:
            doc = msg.document
            f = await doc.get_file()
            original = doc.file_name or "documento.bin"
            ext = Path(original).suffix or ".bin"
            path = f"data/files/{f.file_unique_id}{ext}"
            await f.download_to_drive(path)
            entry = {"path": path, "name": original}
    except Exception as e:
        logging.exception("file download failed")
        await msg.reply_text(f"⚠️ Falha ao baixar o arquivo: {e}")
        return
    if not entry:
        return
    with SessionLocal() as s:
        case = s.get(Case, case_id)
        files = json.loads(case.files_json)
        files.append(entry)
        case.files_json = json.dumps(files)
        s.commit()
        count = len(files)
    await msg.reply_text(FILE_RECEIVED.format(count=count))


async def cmd_enviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    case_id = _get_active_draft_id(update.effective_user.id)
    if not case_id:
        await update.message.reply_text(NO_DRAFT, parse_mode="HTML")
        return
    with SessionLocal() as s:
        case = s.get(Case, case_id)
        if not case or case.status != "draft":
            await update.message.reply_text(NO_DRAFT, parse_mode="HTML")
            return
        specialty = detect_specialty(case.diagnosis)
        case.matched_specialty = specialty
        case.status = "pending"
        s.commit()
        doctors = match_doctors(s, specialty, limit=5)
        if not doctors:
            case.status = "no_match"
            s.commit()
            await update.message.reply_text(CASE_NO_MATCH)
            context.user_data.pop("draft_case_id", None)
            context.user_data.pop("awaiting_files", None)
            return
        for doc in doctors:
            s.add(Opinion(case_id=case.id, doctor_id=doc.id))
        s.commit()
        sent_count = len(doctors)

    context.user_data.pop("draft_case_id", None)
    context.user_data.pop("awaiting_files", None)
    await update.message.reply_text(
        CASE_SUBMITTED_AWAITING.format(specialty=specialty, count=sent_count),
        parse_mode="HTML",
    )
    asyncio.create_task(auto_respond_for_case(case_id))


async def cmd_cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    case_id = context.user_data.get("draft_case_id")
    if case_id:
        with SessionLocal() as s:
            case = s.get(Case, case_id)
            if case and case.status == "draft":
                s.delete(case)
                s.commit()
    context.user_data.clear()
    await update.message.reply_text(CASE_CANCELLED)


# ---------- appointment flow ----------
async def cmd_agendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.effective_user.id
    with SessionLocal() as s:
        patient = s.query(Patient).filter_by(telegram_id=tid).first()
        if not patient:
            await update.message.reply_text("Use /start primeiro.")
            return
        offers = (
            s.query(Appointment)
            .join(Opinion, Appointment.opinion_id == Opinion.id)
            .join(Case, Opinion.case_id == Case.id)
            .filter(Case.patient_id == patient.id, Appointment.status == "proposed")
            .all()
        )
        items = [
            {
                "id": apt.id,
                "doctor_name": apt.opinion.doctor.name,
                "specialty": apt.opinion.doctor.specialty,
                "type": apt.type,
                "slot": apt.slot_text,
            }
            for apt in offers
        ]
    if not items:
        await update.message.reply_text(NO_OFFERS)
        return
    lines = [OFFERS_HEADER, ""]
    keyboard: list[list[InlineKeyboardButton]] = []
    for item in items:
        lines.append(
            f"• {html.escape(item['doctor_name'])} ({item['specialty']}) — "
            f"{item['type']} — {html.escape(item['slot'])}"
        )
        keyboard.append([
            InlineKeyboardButton(
                f"✅ Aceitar com {item['doctor_name']}",
                callback_data=f"accept_apt:{item['id']}",
            )
        ])
    await update.message.reply_text(
        "\n".join(lines),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )


async def accept_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    apt_id = int(query.data.split(":")[1])
    with SessionLocal() as s:
        apt = s.get(Appointment, apt_id)
        if not apt:
            await query.edit_message_text("Agendamento não encontrado.")
            return
        if apt.status != "proposed":
            await query.edit_message_text("Esse agendamento já foi tratado.")
            return
        apt.status = "accepted"
        snapshot = {
            "doctor_name": apt.opinion.doctor.name,
            "type": apt.type,
            "slot_text": apt.slot_text,
        }
        s.commit()
    await query.edit_message_text(
        APPOINTMENT_CONFIRMED_PATIENT.format(**snapshot)
    )


# ---------- builder ----------
async def _on_error(update: object, context) -> None:
    logging.error("bot error handling update: %s", context.error, exc_info=context.error)


def build_patient_app(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_error_handler(_on_error)

    register_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={NAME_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)]},
        fallbacks=[CommandHandler("cancelar", cmd_cancelar)],
    )
    app.add_handler(register_conv)
    app.add_handler(CommandHandler("caso", cmd_caso))
    app.add_handler(CommandHandler(["exames", "exame"], cmd_exames))
    app.add_handler(CommandHandler("enviar", cmd_enviar))
    app.add_handler(CommandHandler("cancelar", cmd_cancelar))
    app.add_handler(CommandHandler("agendar", cmd_agendar))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receive_file))
    app.add_handler(CallbackQueryHandler(accept_appointment, pattern=r"^accept_apt:"))
    return app
