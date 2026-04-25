from sqlalchemy.orm import Session

from app.db import Doctor

SPECIALTY_KEYWORDS: dict[str, list[str]] = {
    "cardiologia": [
        "peito", "coração", "coracao", "palpitação", "palpitacao",
        "pressão", "pressao", "arritmia", "infarto", "cardíaco", "cardiaco",
        "taquicardia", "angina",
    ],
    "neurologia": [
        "cabeça", "cabeca", "enxaqueca", "tontura", "dormência", "dormencia",
        "convulsão", "convulsao", "memória", "memoria", "avc", "neuro",
        "epilepsia", "tremor",
    ],
    "dermatologia": [
        "pele", "mancha", "coceira", "alergia", "eczema", "acne",
        "dermatite", "psoríase", "psoriase", "verruga", "melanoma",
    ],
    "ortopedia": [
        "joelho", "coluna", "costas", "fratura", "ombro", "tornozelo",
        "lombar", "tendinite", "ligamento", "menisco", "artrose", "osso",
    ],
}

FALLBACK = "clínica geral"


def detect_specialty(text: str) -> str:
    text_lower = text.lower()
    scores: dict[str, int] = {}
    for specialty, keywords in SPECIALTY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[specialty] = score
    if not scores:
        return FALLBACK
    return max(scores, key=lambda k: scores[k])


def match_doctors(session: Session, specialty: str, limit: int = 5) -> list[Doctor]:
    q = (
        session.query(Doctor)
        .filter(Doctor.specialty == specialty, Doctor.available == True)
        .limit(limit)
    )
    return list(q)
