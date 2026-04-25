from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, String, Integer, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

from app.config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    cases: Mapped[list["Case"]] = relationship(back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True)
    web_token: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    specialty: Mapped[str] = mapped_column(String(60), index=True)
    available: Mapped[bool] = mapped_column(default=True)
    is_mock: Mapped[bool] = mapped_column(default=False)
    opinions: Mapped[list["Opinion"]] = relationship(back_populates="doctor")


class Case(Base):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    diagnosis: Mapped[str] = mapped_column(Text)
    symptoms: Mapped[str] = mapped_column(Text)
    prior_doctor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    files_json: Mapped[str] = mapped_column(Text, default="[]")
    matched_specialty: Mapped[str | None] = mapped_column(String(60), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient: Mapped[Patient] = relationship(back_populates="cases")
    opinions: Mapped[list["Opinion"]] = relationship(back_populates="case")


class Opinion(Base):
    __tablename__ = "opinions"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    verdict: Mapped[str | None] = mapped_column(String(20), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    responded_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    case: Mapped[Case] = relationship(back_populates="opinions")
    doctor: Mapped[Doctor] = relationship(back_populates="opinions")
    appointment: Mapped["Appointment | None"] = relationship(back_populates="opinion", uselist=False)


class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True)
    opinion_id: Mapped[int] = mapped_column(ForeignKey("opinions.id"), unique=True)
    type: Mapped[str] = mapped_column(String(20))
    slot_text: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="proposed")

    opinion: Mapped[Opinion] = relationship(back_populates="appointment")


def init_db() -> None:
    Base.metadata.create_all(engine)
