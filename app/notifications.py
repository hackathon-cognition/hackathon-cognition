"""Cross-channel notifications. Web/auto-respond saves opinion -> notify patient on Telegram."""
import html

from app.bots import BotRegistry
from app.db import SessionLocal, Opinion
from app.messages import OPINION_AGREE_TEMPLATE, OPINION_DISAGREE_TEMPLATE


async def send_opinion_to_patient(opinion_id: int) -> None:
    with SessionLocal() as s:
        opinion = s.get(Opinion, opinion_id)
        if not opinion:
            return
        snapshot = {
            "verdict": opinion.verdict,
            "notes": opinion.notes or "—",
            "doctor_name": opinion.doctor.name,
            "specialty": opinion.doctor.specialty,
            "patient_telegram_id": opinion.case.patient.telegram_id,
        }

    template = OPINION_AGREE_TEMPLATE if snapshot["verdict"] == "agree" else OPINION_DISAGREE_TEMPLATE
    text = template.format(
        doctor_name=html.escape(snapshot["doctor_name"]),
        specialty=snapshot["specialty"],
        notes=html.escape(snapshot["notes"]),
    )

    bot = BotRegistry.patient_bot
    if bot is None:
        print(f"[warn] patient bot not registered, opinion {opinion_id} not delivered")
        return
    try:
        await bot.send_message(
            chat_id=snapshot["patient_telegram_id"],
            text=text,
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"[warn] send opinion {opinion_id} failed: {e}")
