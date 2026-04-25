# PRD Output Template — PRD Specialist Agent

Use this template when generating the final PRD after interview completion. Replace all `[placeholders]` with gathered information.

---

# PRD: [Product/Feature Name] ([MVP / Full Launch / Phase N])

## 1. Executive Summary
> 2-3 paragraph overview. What we're building, why, for whom, and the expected outcome.

**One-liner:** [Product name] is a [type of product] that [core value proposition] for [target user].

**Key facts:**
- **Target launch:** [date or timeframe]
- **Scope:** [MVP / Full / Phase]
- **Stack:** [tech stack summary]
- **Team:** [number] engineers, [estimated effort]

## 2. Problem Statement & Objectives

### Problem
[Describe the problem in user terms. Who is affected, how, and why it matters.]

### Objectives
- [Objective 1 — tied to a measurable outcome]
- [Objective 2]
- [Objective 3]

### Out of Scope
- [Explicitly list what is NOT being built]
- [...]

## 3. Success Metrics & KPIs

| Metric | Current Baseline | Target | Measurement Method |
|--------|-----------------|--------|-------------------|
| [Metric 1] | [baseline] | [target] | [how measured] |
| [Metric 2] | [baseline] | [target] | [how measured] |
| [Metric 3] | [baseline] | [target] | [how measured] |

## 4. User Personas & Use Cases

### Primary Persona: [Name]
- **Role/Demographic:** [description]
- **Motivation:** [why they use the product]
- **Current workaround:** [what they do today]
- **Frustration:** [top pain point]

### Secondary Persona: [Name]
- **Role/Demographic:** [description]
- **Motivation:** [why they use the product]

### Key Use Cases
1. [Use case 1 — brief description]
2. [Use case 2]
3. [Use case 3]

## 5. Functional Requirements

### Must-Have (P0)

| ID | User Story | Acceptance Criteria |
|----|-----------|-------------------|
| FR-1 | As a [user], I want [action] so that [benefit] | [criteria] |
| FR-2 | As a [user], I want [action] so that [benefit] | [criteria] |

### Nice-to-Have (P1)

| ID | User Story | Acceptance Criteria |
|----|-----------|-------------------|
| FR-N1 | As a [user], I want [action] so that [benefit] | [criteria] |

### Edge Cases & Error Handling
- [Edge case 1]: [expected behavior]
- [Edge case 2]: [expected behavior]

## 6. Non-Functional Requirements

| Requirement | Specification | MVP Approach | Production Approach |
|-------------|--------------|-------------|-------------------|
| Performance | [response time, throughput] | [simplified] | [full] |
| Availability | [uptime target] | [simplified] | [full] |
| Security | [auth, encryption, etc.] | [simplified] | [full] |
| Compliance | [regulations] | [deferred / partial] | [full] |
| Localization | [languages] | [simplified] | [full] |

## 7. Technical Specifications

### Stack
- **Backend:** [framework/language]
- **Frontend:** [framework/library]
- **Database:** [type + engine]
- **File Storage:** [approach]
- **Other:** [bots, queues, etc.]

### Architecture
```
[Simple ASCII diagram of system architecture]
```

### Data Models
- `[Entity1]` ([field1], [field2], [field3])
- `[Entity2]` ([field1], [field2], [field3])

### API Endpoints (if applicable)
| Method | Path | Description |
|--------|------|-------------|
| [GET/POST] | [/path] | [description] |

## 8. Dependencies & Integrations

| Integration | MVP | Post-MVP |
|-------------|-----|----------|
| [Integration 1] | [mocked / real / deferred] | [full approach] |
| [Integration 2] | [mocked / real / deferred] | [full approach] |

### External Dependencies
- [Dependency 1]: [status, risk if delayed]
- [Dependency 2]: [status, risk if delayed]

## 9. Timeline & Milestones

| Time | Milestone | Deliverable |
|------|-----------|-------------|
| [0:00–0:30] | [Phase 1] | [what's delivered] |
| [0:30–1:00] | [Phase 2] | [what's delivered] |
| [...] | [...] | [...] |

## 10. Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] | [plan] |
| [Risk 2] | [High/Med/Low] | [High/Med/Low] | [plan] |

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Open Questions
- [ ] [Question 1] — Owner: [who decides], Deadline: [when]
- [ ] [Question 2] — Owner: [who decides], Deadline: [when]

## 11. Appendices
- [Wireframes/Mockups: links or embedded images]
- [Research data: links]
- [Competitive analysis: links]
- [Technical spike results: links]
