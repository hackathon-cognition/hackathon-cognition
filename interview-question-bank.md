# Interview Question Bank — PRD Specialist Agent

Detailed question scripts for each interview phase. Use these as a guide — adapt wording based on context.

## Phase 1: Project Overview

### Vision & Objectives
- What is the product/feature you want to build, in one sentence?
- What business problem does this solve?
- What is the core value proposition for the end user?
- What business objectives drive this project? (revenue, retention, acquisition, efficiency, etc.)
- If this project succeeds wildly, what does that look like in 6 months?
- Is this a new product, a new feature in an existing product, or a redesign?

### Success Metrics
- How will you measure success? What are the top 3 KPIs?
- What is the current baseline for those metrics (if any)?
- What targets are you aiming for?
- Are there leading indicators you want to track during development?

### Scope & Constraints
- Is this an MVP, a full launch, or something in between?
- What is explicitly OUT of scope?
- Are there hard deadlines or launch dates?
- What is the budget/resource constraint?

---

## Phase 2: User Research

### Target Users
- Who is the primary user? Describe them in detail (role, demographics, tech-savviness).
- Who are secondary users? (admins, operators, internal teams)
- Are there non-users who are affected by the system? (stakeholders, regulators)
- How many users do you expect at launch? At scale?

### Personas
- Can you describe 2-3 typical user personas?
- What is each persona's primary motivation for using this product?
- What alternative solutions are they using today?

### User Journeys & Pain Points
- Walk me through the current user journey step by step. Where are the friction points?
- What is the "aha moment" you want users to experience?
- What are the top 3 pain points you're addressing?
- Are there edge cases or unusual flows we need to support?

---

## Phase 3: Functional Requirements

### Feature Specification
- List the must-have features (won't ship without these).
- List the nice-to-have features (could defer).
- For each must-have feature, describe the happy path in detail.
- What happens when things go wrong? (error states, validation failures)

### User Stories
- Can you write the top user stories? (As a [user], I want [action] so that [benefit])
- For each story, what are the acceptance criteria?
- Are there stories that depend on others being completed first?

### Edge Cases & Unhappy Paths
- What happens if the user provides invalid input?
- What happens if a third-party service is down?
- Are there rate limits, caps, or throttling requirements?
- What data needs to persist? What can be ephemeral?

---

## Phase 4: Technical Considerations

### Architecture & Stack
- Are there existing technical constraints? (must use X framework, Y database)
- What integrations are required? (APIs, webhooks, third-party services)
- Are there performance requirements? (response time, throughput, concurrency)
- What are the data storage and privacy requirements?

### Dependencies
- What external systems does this depend on?
- Are there APIs that need to be built by other teams?
- What is the current state of those dependencies? (ready, in progress, not started)

### Security & Compliance
- Are there authentication/authorization requirements?
- Is there sensitive data involved? (PII, health, financial)
- Are there regulatory requirements? (GDPR, HIPAA, LGPD, PCI)
- What is the MVP approach vs. the production approach for security?

---

## Phase 5: Business Context

### Timeline & Resources
- What is the target launch date?
- How many engineers are available?
- Are there dependencies on other teams or external vendors?
- What are the key milestones or checkpoints?

### Competitive Landscape
- Who are the main competitors or alternatives?
- What differentiates this product from existing solutions?
- Are there features competitors have that we should match or avoid?

### Business Impact
- What is the expected business impact? (revenue, cost savings, user growth)
- Is there a cost model or pricing strategy?
- What is the opportunity cost of NOT building this?

---

## Phase 6: Risk Assessment

### Risks
- What are the top 3 risks for this project?
- What assumptions are we making that could be wrong?
- Are there technical risks? (unproven tech, complex integrations)
- Are there business risks? (market fit, competition, regulatory changes)

### Mitigation
- For each risk, what is the mitigation plan?
- What is the fallback if a critical assumption is wrong?
- Are there features that could be cut to reduce risk?

### Open Questions
- What decisions still need to be made?
- Who needs to be involved in those decisions?
- What information is missing that would help us proceed?
