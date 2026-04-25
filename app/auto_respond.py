"""Auto-respond as mock doctors. Supports golden-path scripts for demo scenarios."""
import asyncio
import random
from datetime import datetime

from app.db import SessionLocal, Opinion, Doctor, Case, Appointment
from app.notifications import send_opinion_to_patient


# ---------- generic fallback (for cases without a golden path) ----------
MOCK_NOTES_AGREE = [
    "Concordo com o diagnóstico. Sintomas e exames descritos são consistentes. Recomendo seguir o tratamento proposto.",
    "Diagnóstico parece correto. Sugiro acompanhamento regular.",
    "Concordo. O quadro descrito é típico. Mantenha as orientações iniciais.",
]

MOCK_NOTES_DISAGREE = [
    "Tenho dúvidas sobre o diagnóstico. Sintomas podem indicar outra condição. Recomendo investigação adicional.",
    "Não concordo totalmente. Sugiro nova avaliação presencial para confirmar.",
    "O quadro descrito merece uma segunda análise. Vamos conversar pessoalmente.",
]

MOCK_SLOTS = ["Amanhã às 14h", "Sexta-feira às 10h", "Segunda-feira às 16h", "Quarta às 9h30"]


# ---------- golden-path scenarios ----------
GOLDEN_PATHS = [
    {
        "name": "ombro_cirurgia_vs_fisio",
        "description": "Paciente com indicação de cirurgia no ombro — médicos recomendam fisioterapia",
        "triggers": ["cirurgia", "ombro"],
        "responses": [
            {
                "verdict": "disagree",
                "notes": (
                    "Discordo da indicação cirúrgica imediata. O quadro descrito sugere fortemente "
                    "tendinopatia do supraespinhal ou síndrome do impacto subacromial. "
                    "Recomendo iniciar fisioterapia especializada (3 sessões/semana, 12 sessões) "
                    "com foco em fortalecimento do manguito rotador e estabilização escapular antes "
                    "de considerar qualquer abordagem cirúrgica."
                ),
                "appointment": {
                    "type": "presencial",
                    "slot": "Próxima terça às 15h",
                    "notes": "Reavaliação clínica após 6 semanas de fisioterapia. Trazer RM e laudos.",
                },
            },
            {
                "verdict": "disagree",
                "notes": (
                    "Não vejo indicação imediata de cirurgia. Estudos recentes (Beard et al., Lancet 2018) "
                    "demonstram que 70-80% dos casos de lesão parcial do supraespinhal respondem bem ao "
                    "tratamento conservador. Sugiro fisioterapia + AINE por 8 semanas e, se necessário, "
                    "infiltração com corticoide guiada por ultrassom."
                ),
                "appointment": {
                    "type": "remoto",
                    "slot": "Quinta às 9h30",
                    "notes": "Teleconsulta para revisar exames e desenhar plano conservador.",
                },
            },
            {
                "verdict": "disagree",
                "notes": (
                    "Concordo que há lesão estrutural, mas discordo veementemente da abordagem cirúrgica "
                    "como primeira linha. Em meus 15 anos de prática, casos semelhantes resolveram com "
                    "fisioterapia bem orientada. A cirurgia deve ser reservada para falha documentada do "
                    "tratamento conservador."
                ),
                "appointment": {
                    "type": "presencial",
                    "slot": "Sexta às 14h",
                    "notes": "Trazer exames de imagem e relato detalhado das limitações funcionais.",
                },
            },
            {
                "verdict": "disagree",
                "notes": (
                    "Recomendo fortemente fisioterapia antes de qualquer procedimento cirúrgico. "
                    "O ombro responde muito bem à reabilitação progressiva quando bem orientada. "
                    "Cirurgia traz riscos (rigidez, infecção, recuperação longa) que devem ser pesados "
                    "contra alternativas conservadoras."
                ),
                "appointment": None,
            },
            {
                "verdict": "agree",
                "notes": (
                    "Entendo a posição dos colegas, mas considero que se já houve falha de tratamento "
                    "conservador prévio ou se há lesão completa do supraespinhal, a indicação cirúrgica "
                    "pode estar correta. Recomendo nova avaliação com cirurgião especialista em ombro "
                    "para definir."
                ),
                "appointment": None,
            },
        ],
    },
]


def detect_golden_path(diagnosis: str) -> dict | None:
    text = (diagnosis or "").lower()
    for path in GOLDEN_PATHS:
        if all(trigger in text for trigger in path["triggers"]):
            return path
    return None


# ---------- runner ----------
async def auto_respond_for_case(case_id: int, delay_seconds: int = 6) -> None:
    """Respond on behalf of mock doctors after a small delay (for demo realism)."""
    await asyncio.sleep(delay_seconds)
    with SessionLocal() as s:
        case = s.get(Case, case_id)
        diagnosis = case.diagnosis if case else ""
        opinions = (
            s.query(Opinion)
            .join(Doctor)
            .filter(
                Opinion.case_id == case_id,
                Doctor.is_mock == True,
                Opinion.status == "pending",
            )
            .all()
        )
        opinion_ids = [o.id for o in opinions]

    golden = detect_golden_path(diagnosis)
    if golden:
        print(f"[auto_respond] golden path matched: {golden['name']} for case {case_id}")

    for idx, opinion_id in enumerate(opinion_ids):
        await asyncio.sleep(random.uniform(3, 6))

        if golden and idx < len(golden["responses"]):
            resp = golden["responses"][idx]
            verdict = resp["verdict"]
            notes = resp["notes"]
            appointment = resp.get("appointment")
        else:
            verdict = random.choices(["agree", "disagree"], weights=[0.6, 0.4])[0]
            notes = random.choice(
                MOCK_NOTES_AGREE if verdict == "agree" else MOCK_NOTES_DISAGREE
            )
            appointment = None
            if verdict == "disagree":
                appointment = {
                    "type": random.choice(["presencial", "remoto"]),
                    "slot": random.choice(MOCK_SLOTS),
                    "notes": "Trazer exames recentes.",
                }

        with SessionLocal() as s:
            opinion = s.get(Opinion, opinion_id)
            if opinion is None or opinion.status != "pending":
                continue
            opinion.verdict = verdict
            opinion.notes = notes
            opinion.status = "responded"
            opinion.responded_at = datetime.utcnow()
            if appointment:
                s.add(Appointment(
                    opinion_id=opinion.id,
                    type=appointment["type"],
                    slot_text=appointment["slot"],
                    notes=appointment.get("notes"),
                ))
            s.commit()
        await send_opinion_to_patient(opinion_id)
