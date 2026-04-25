"""Shared registry so background tasks (web handlers, auto-respond) can send patient messages."""
from telegram import Bot


class BotRegistry:
    patient_bot: Bot | None = None


def set_patient_bot(bot: Bot) -> None:
    BotRegistry.patient_bot = bot
