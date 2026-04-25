"""Run patient Telegram bot (long-polling) + FastAPI dashboard in one event loop."""
import asyncio
import logging

import uvicorn

from app.config import PATIENT_BOT_TOKEN
from app.db import init_db, SessionLocal, Doctor
from app.seed import seed, print_doctor_links
from app.bots import set_patient_bot
from app.bot_patient import build_patient_app
from app.web import app as web_app


def print_golden_path() -> None:
    with SessionLocal() as s:
        ortho = s.query(Doctor).filter_by(specialty="ortopedia").first()
    print("=" * 70)
    print("🎯 GOLDEN PATH: cirurgia de ombro vs. fisioterapia")
    print("=" * 70)
    print()
    print("1️⃣  Abra UM destes links no navegador (você é o médico ortopedista):")
    print(f"     http://localhost:8000/d/{ortho.web_token}   ({ortho.name})")
    print("     (ou pegue qualquer outro ortopedista da lista acima)")
    print()
    print("2️⃣  No bot do paciente (t.me/medicheck_pacientebot):")
    print("     /start  →  digita seu nome")
    print()
    print("     /caso meu medico recomendou cirurgia no ombro direito por causa")
    print("     de uma lesao no supraespinhal. tenho dor ha 3 meses e limitacao")
    print("     de movimento, mas queria uma segunda opiniao antes de operar.")
    print()
    print("     /enviar")
    print()
    print("3️⃣  No dashboard: o caso aparece em ~15s. Você responde Discordo +")
    print("     propõe consulta presencial recomendando fisioterapia.")
    print()
    print("4️⃣  Em ~10-30s os outros 4 ortopedistas (mocks) respondem")
    print("     com mensagens roteirizadas recomendando fisioterapia.")
    print()
    print("5️⃣  No bot do paciente: /agendar  →  aceita uma proposta.")
    print("=" * 70)
    print()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


async def run() -> None:
    if not PATIENT_BOT_TOKEN:
        raise RuntimeError("PATIENT_BOT_TOKEN ausente. Copie .env.example para .env e cole o token.")

    init_db()
    seed()
    print_doctor_links()
    print_golden_path()

    patient_app = build_patient_app(PATIENT_BOT_TOKEN)
    set_patient_bot(patient_app.bot)

    await patient_app.initialize()
    await patient_app.start()
    await patient_app.updater.start_polling(drop_pending_updates=True)

    config = uvicorn.Config(web_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    print("\n✅ Bot paciente + Dashboard web no ar.")
    print("📱 Bot:       t.me/medicheck_pacientebot")
    print("💻 Dashboard: http://localhost:8000  (use os links mágicos acima)\n")

    try:
        await server.serve()
    finally:
        await patient_app.updater.stop()
        await patient_app.stop()
        await patient_app.shutdown()


def main() -> None:
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nbye 👋")


if __name__ == "__main__":
    main()
