# Interview Transition & Completeness Logic — PRD Specialist Agent

Rules for transitioning between interview phases and determining when enough information has been gathered.

## Phase Transition Rules

### When to Advance to Next Phase
Advance when **all mandatory questions** for the current phase have been asked AND at least one of:
- The interviewee has provided substantive answers (not just "I don't know" or "TBD")
- The interviewee explicitly says they want to move on
- The agent has asked follow-up clarifications on vague answers and received adequate detail

### When to Stay in Current Phase
Stay if:
- A mandatory question has not been asked yet
- The interviewee gave a vague answer and follow-up hasn't been attempted
- A critical dependency or constraint was mentioned but not explored

### When to Go Back to Previous Phase
Go back if:
- New information in a later phase contradicts earlier answers
- The interviewee says "actually, let me reconsider [earlier topic]"
- A risk identified in Phase 6 invalidates assumptions from earlier phases

## Mandatory vs. Optional Questions per Phase

| Phase | Mandatory | Optional (skip if interviewee unsure) |
|-------|-----------|--------------------------------------|
| 1. Project Overview | Problem, objectives, scope, timeline | Baseline metrics, competitive landscape |
| 2. User Research | Primary user, top pain points | Personas, secondary users, current workarounds |
| 3. Functional Requirements | Must-have features, happy path | Nice-to-haves, edge cases, error handling |
| 4. Technical Considerations | Stack constraints, integrations | Performance specs, security details |
| 5. Business Context | Timeline, resources | Pricing, business impact quantification |
| 6. Risk Assessment | Top 3 risks, assumptions | Mitigation plans, open questions |

## Completeness Criteria

### Minimum Viable Interview (for MVP / Hackathon)
An interview is **sufficient for MVP PRD generation** when:
- [ ] Phase 1: Problem and objectives are clear
- [ ] Phase 2: Primary user and top pain point identified
- [ ] Phase 3: Must-have features listed with basic happy path
- [ ] Phase 4: Stack and key integrations identified
- [ ] Phase 5: Timeline and resource constraints known
- [ ] Phase 6: Top risk acknowledged

**Minimum: ~10-15 questions answered substantively.**

### Full Interview (for production PRD)
An interview is **sufficient for full PRD generation** when all mandatory AND optional questions have been covered, plus:
- [ ] All phases have been visited at least once
- [ ] At least 2 follow-up clarifications per phase
- [ ] Edge cases and error states documented
- [ ] Non-functional requirements specified
- [ ] All open questions listed with owners

**Minimum: ~25-35 questions answered substantively.**

## Handling Edge Cases During Interview

### Interviewee Doesn't Know the Answer
- **Don't skip silently.** Acknowledge the gap: "That's an important point we'll need to resolve. Let me note it as an open question."
- Mark it as `[OPEN QUESTION]` in your notes.
- Move to the next question; revisit open questions at the end.

### Interviewee Wants to Skip a Phase
- Allow it, but **warn about impact**: "We can skip [phase], but the PRD will have gaps in [specific area]. I'll flag those as TBD. Sound good?"
- Document skipped phases as `[SECTION DEFERRED BY INTERVIEWEE]`.

### Interviewee Gives Contradictory Answers
- Flag the contradiction immediately: "Earlier you mentioned X, but now you're saying Y. Can you help me understand which applies?"
- Don't assume — ask for clarification.
- If unresolved, document both answers and flag as `[CONTRADICTION — RESOLVE BEFORE BUILD]`.

### Interviewee Is Too Vague
- Use the **5 Whys** technique: ask "why" up to 5 times to get to root cause.
- Ask for specific examples: "Can you give me a concrete example of when that happens?"
- Offer multiple-choice framing: "Would you say it's more like A, B, or C?"

### Interviewee Wants to Start Over
- Allow it. Summarize what was already covered.
- Ask: "Should we discard the previous answers, or build on top of them?"

## Sign-Off Before PRD Generation

Before generating the PRD, present a summary to the interviewee:

> "Here's what I've gathered so far:
> - **Problem:** [summary]
> - **Users:** [summary]
> - **Must-haves:** [summary]
> - **Stack:** [summary]
> - **Timeline:** [summary]
> - **Top risks:** [summary]
> - **Open questions:** [count]
>
> Shall I proceed to generate the PRD, or would you like to revisit any area?"

Wait for explicit confirmation before generating.
