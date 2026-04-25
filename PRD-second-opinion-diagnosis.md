# PRD: Second Opinion Diagnosis System (MVP — 3 Hour Build)

## 1. Executive Summary
Telegram-based AI chatbot for patients to request second opinions. System auto-matches with up to 5 verified specialists; doctors have 3h SLA to agree/disagree and can propose appointments. Built in .NET + JS. EN/PT support. Payments & compliance deferred.

## 2. Problem & Objectives
- **Problem:** Patients lack fast, affordable access to specialist validation of diagnoses.
- **Objectives:** 5-minute patient intake, 3h doctor response, auto-match specialists, appointment scheduling.

## 3. Success Metrics
| Metric | Target |
|--------|--------|
| Patient intake time | < 5 min |
| Doctor response rate | > 60% within 3h |
| End-to-end time | < 3 hours |

## 4. Personas
- **Patient:** Any age/condition, EN or PT speaker, seeks diagnosis validation.
- **Doctor:** Verified specialist, wants extra income, prefers frictionless review interface.

## 5. Functional Requirements

### 5.1 Patient Telegram Bot
- FR-1: Conversational intake (diagnosis, symptoms, prior doctor, file upload).
- FR-2: Confirm summary before submission.
- FR-3: Submit case and trigger auto-matching.
- FR-4: Notify patient when opinions arrive.
- FR-5: Display opinions + appointment offers with accept/reject.
- FR-6: Max 5 second opinions per patient (hard cap).
- FR-7: EN and PT language support.

### 5.2 Doctor Web Dashboard
- FR-8: Simple auth (mock/token for MVP).
- FR-9: Pending cases list with 3h countdown timer.
- FR-10: Case detail: diagnosis, narrative, file links.
- FR-11: Submit opinion: Agree / Disagree + notes.
- FR-12: If Disagree: propose appointment (in-person/remote, proposed slots, notes).
- FR-13: Historical cases view.

### 5.3 Auto-Matching Engine
- FR-14: Keyword/topic matching diagnosis text → doctor specialty (static mapping for MVP).
- FR-15: Select up to 5 doctors from matched pool.
- FR-16: If < 5 available, assign all and notify patient.

### 5.4 Appointment Scheduling (MVP — Mocked)
- FR-17: Store proposed slots from doctors.
- FR-18: Patient accepts one offer; system confirms.
- FR-19: Send confirmation details to both parties via Telegram.

### 5.5 Business Logic
- FR-20: Track patient opinion pool (cap: 5).
- FR-21: Track doctor assignment & response status.
- FR-22: SLA expiry auto-marks case expired, triggers refund placeholder.

## 6. Non-Functional Requirements
| Requirement | MVP Approach |
|-------------|--------------|
| Performance | Bot < 3s, dashboard < 2s |
| Availability | Single instance OK |
| Scalability | Not MVP concern |
| Security | HTTPS for dashboard; local file storage |
| Compliance | **Deferred post-MVP** |
| Localization | EN/PT hardcoded strings |

## 7. Technical Specifications

### 7.1 Stack
- **Backend:** .NET (ASP.NET Core Web API)
- **Doctor Dashboard:** Vanilla JS + HTML
- **Bot:** Node.js or Python webhook handler calling .NET API
- **Database:** SQLite
- **File Storage:** Local filesystem

### 7.2 Architecture
```
[Telegram] <--webhook--> [Bot Handler] <--HTTP--> [.NET API] <---> [SQLite]
                                                        |
[Doctor Browser] <--HTTP--> [Dashboard API] <--static files-->
```

### 7.3 Data Models
- `Patient` (id, telegram_id, name, pool_remaining)
- `Case` (id, patient_id, diagnosis, symptoms, files[], status, created_at)
- `Doctor` (id, name, specialty, available)
- `Opinion` (id, case_id, doctor_id, verdict, notes, appointment_proposed, created_at)
- `AppointmentOffer` (id, opinion_id, type, slots, status)

## 8. Dependencies & Integrations
| Integration | MVP | Post-MVP |
|-------------|-----|----------|
| Telegram Bot API | Required | — |
| Payment Gateway | Mocked | Stripe/PayPal |
| Calendar API | Mocked | Google/Outlook |
| Doctor Verification | Mocked | Medical registry API |
| Notifications | Telegram only | Email/SMS |

## 9. Timeline (3 Hours)
| Time | Milestone |
|------|-----------|
| 0:00–0:30 | Setup: .NET scaffold, SQLite schema, bot skeleton |
| 0:30–1:15 | Patient Flow: Telegram intake, case creation, file upload |
| 1:15–1:45 | Matching: keyword match, doctor assignment, notifications |
| 1:45–2:30 | Doctor Dashboard: case list, detail, opinion submit, appointment proposal |
| 2:30–2:45 | Patient Notifications: opinion delivery, accept/reject appointments |
| 2:45–3:00 | Polish: seed data, demo script, edge cases |

## 10. Risks & Mitigation
| Risk | Mitigation |
|------|------------|
| 3h insufficient for full stack | Ruthlessly defer auth, payments, real calendar, minimal UI |
| Matching too simple | Accept keyword matching; flag for NLP improvement |
| Doctor unavailability in demo | Pre-seed 5+ demo doctors with mock responses |
