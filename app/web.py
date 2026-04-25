"""FastAPI dashboard — magic-link auth via doctor's web_token in URL."""
import asyncio
import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import SessionLocal, Doctor, Opinion, Appointment
from app.notifications import send_opinion_to_patient


app = FastAPI(title="MediCheck Dashboard")
templates = Jinja2Templates(directory="app/templates")


def _doctor_from_token(token: str) -> dict:
    with SessionLocal() as s:
        doc = s.query(Doctor).filter_by(web_token=token).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        if doc.is_mock:
            doc.is_mock = False
            s.commit()
        return {
            "id": doc.id,
            "name": doc.name,
            "specialty": doc.specialty,
            "token": doc.web_token,
        }


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(
        "<html><body style='font-family: system-ui; max-width: 600px; margin: 60px auto; padding: 24px; text-align: center;'>"
        "<h1>🩺 MediCheck</h1>"
        "<p>Painel do médico. Acesse pelo seu link mágico.</p>"
        "</body></html>"
    )


@app.get("/d/{token}")
async def login(token: str):
    _doctor_from_token(token)
    return RedirectResponse(f"/d/{token}/casos", status_code=302)


@app.get("/d/{token}/casos", response_class=HTMLResponse)
async def list_cases(request: Request, token: str):
    doc = _doctor_from_token(token)
    with SessionLocal() as s:
        opinions = (
            s.query(Opinion)
            .filter(Opinion.doctor_id == doc["id"], Opinion.status == "pending")
            .order_by(Opinion.created_at.desc())
            .all()
        )
        items = []
        for o in opinions:
            short = (o.case.diagnosis or "")[:120]
            items.append({
                "opinion_id": o.id,
                "case_id": o.case.id,
                "diagnosis_short": short,
                "diagnosis_truncated": len(o.case.diagnosis or "") > 120,
                "created_at": o.created_at,
            })
    return templates.TemplateResponse(
        "cases.html", {"request": request, "doctor": doc, "items": items}
    )


@app.get("/d/{token}/casos/{opinion_id}", response_class=HTMLResponse)
async def case_detail(request: Request, token: str, opinion_id: int):
    doc = _doctor_from_token(token)
    with SessionLocal() as s:
        opinion = s.get(Opinion, opinion_id)
        if not opinion or opinion.doctor_id != doc["id"]:
            raise HTTPException(status_code=404)
        case = opinion.case
        raw_files = json.loads(case.files_json)
        files = []
        for item in raw_files:
            if isinstance(item, dict):
                files.append({"name": item["name"], "url_name": Path(item["path"]).name})
            else:
                files.append({"name": Path(item).name, "url_name": Path(item).name})
        ctx = {
            "opinion_id": opinion.id,
            "status": opinion.status,
            "case_id": case.id,
            "diagnosis": case.diagnosis,
            "symptoms": case.symptoms,
            "prior_doctor": case.prior_doctor,
            "specialty": case.matched_specialty or "—",
            "created_at": case.created_at,
            "files": files,
        }
    return templates.TemplateResponse(
        "case.html", {"request": request, "doctor": doc, "case": ctx}
    )


@app.post("/d/{token}/casos/{opinion_id}")
async def submit_response(
    token: str,
    opinion_id: int,
    verdict: str = Form(...),
    notes: str = Form(""),
    apt_type: str = Form(""),
    apt_slot: str = Form(""),
    apt_notes: str = Form(""),
):
    doc = _doctor_from_token(token)
    with SessionLocal() as s:
        opinion = s.get(Opinion, opinion_id)
        if not opinion or opinion.doctor_id != doc["id"]:
            raise HTTPException(status_code=404)
        if opinion.status != "pending":
            return RedirectResponse(f"/d/{token}/casos", status_code=302)
        opinion.verdict = verdict
        opinion.notes = (notes or "").strip() or None
        opinion.responded_at = datetime.utcnow()
        opinion.status = "responded"
        if verdict == "disagree" and apt_type and apt_slot.strip():
            s.add(Appointment(
                opinion_id=opinion.id,
                type=apt_type,
                slot_text=apt_slot.strip(),
                notes=(apt_notes or "").strip() or None,
            ))
        s.commit()

    asyncio.create_task(send_opinion_to_patient(opinion_id))
    return RedirectResponse(f"/d/{token}/casos", status_code=302)


@app.get("/files/{filename}")
async def get_file(filename: str):
    safe = Path(filename).name
    path = Path("data/files") / safe
    if not path.exists():
        raise HTTPException(status_code=404)
    return FileResponse(str(path))
