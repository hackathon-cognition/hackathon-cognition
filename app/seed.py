import uuid

from app.db import SessionLocal, Doctor, init_db


SEED_DOCTORS = [
    ("Dra. Marina Costa", "cardiologia", True),
    ("Dr. Eduardo Lima", "cardiologia", True),
    ("Dra. Patrícia Souza", "cardiologia", True),
    ("Dr. André Mello", "cardiologia", True),
    ("Dra. Helena Vargas", "cardiologia", True),
    ("Dr. Rafael Tavares", "neurologia", True),
    ("Dra. Camila Brandão", "neurologia", True),
    ("Dr. Lucas Ferreira", "neurologia", True),
    ("Dra. Júlia Andrade", "neurologia", True),
    ("Dra. Beatriz Nunes", "neurologia", True),
    ("Dr. Roberto Carvalho", "dermatologia", True),
    ("Dra. Larissa Pires", "dermatologia", True),
    ("Dr. Paulo Henrique", "dermatologia", True),
    ("Dra. Sofia Almeida", "dermatologia", True),
    ("Dr. Tiago Mendes", "dermatologia", True),
    ("Dr. Gustavo Silva", "ortopedia", True),
    ("Dra. Renata Castro", "ortopedia", True),
    ("Dr. Bruno Magalhães", "ortopedia", True),
    ("Dra. Fátima Rocha", "ortopedia", True),
    ("Dr. Marcelo Duarte", "ortopedia", True),
    ("Dra. Cláudia Reis", "clínica geral", True),
    ("Dr. Henrique Barbosa", "clínica geral", True),
    ("Dra. Vanessa Lopes", "clínica geral", True),
    ("Dr. Diego Moreira", "clínica geral", True),
    ("Dra. Aline Cardoso", "clínica geral", True),
]


def seed() -> None:
    init_db()
    with SessionLocal() as s:
        if s.query(Doctor).count() > 0:
            print("doctors already seeded")
            return
        for name, specialty, is_mock in SEED_DOCTORS:
            s.add(Doctor(
                name=name,
                specialty=specialty,
                is_mock=is_mock,
                web_token=uuid.uuid4().hex,
            ))
        s.commit()
        print(f"seeded {len(SEED_DOCTORS)} doctors")


def print_doctor_links(base_url: str = "http://localhost:8000") -> None:
    with SessionLocal() as s:
        docs = s.query(Doctor).all()
    print("\n=== Magic links dos médicos (use 1 ou mais para o demo) ===")
    for d in docs:
        print(f"  {d.name:30s} ({d.specialty:14s}) {base_url}/d/{d.web_token}")
    print()


if __name__ == "__main__":
    seed()
    print_doctor_links()
