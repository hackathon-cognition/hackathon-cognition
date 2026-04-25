# PRD Quality Checklist — PRD Specialist Agent

Use this checklist to validate a generated PRD before delivering it to the interviewee. A PRD must pass ALL critical items to be considered complete.

## Critical Items (MUST pass — PRD is incomplete without these)

### Clarity
- [ ] A new engineer can read the PRD and understand WHAT to build without asking questions
- [ ] Every FR has a unique ID (FR-1, FR-2, etc.)
- [ ] Every FR has acceptance criteria that are testable
- [ ] No ambiguous terms without definition
- [ ] Problem statement is written from the USER's perspective, not the business's

### Completeness
- [ ] All must-have features from the interview are present as FRs
- [ ] Out-of-scope items are explicitly listed
- [ ] Success metrics have both baseline and target values
- [ ] At least one persona is defined with motivation and pain point
- [ ] Stack is specified (backend, frontend, database, storage)
- [ ] Timeline with milestones is included
- [ ] Top 3 risks are identified with mitigation plans

### Consistency
- [ ] No FR contradicts another FR
- [ ] Success metrics align with stated objectives
- [ ] Timeline is realistic given the scope and resources
- [ ] MVP approach vs. production approach is distinguished where applicable
- [ ] Data models support all FRs (no orphan fields or missing entities)

### Actionability
- [ ] An engineer can start coding from this PRD without needing a separate technical spec
- [ ] Acceptance criteria are specific enough to write tests from
- [ ] Dependencies are identified with their current status
- [ ] Open questions are listed with owners and deadlines

## Quality Items (SHOULD pass — PRD is weak without these)

### Depth
- [ ] Edge cases and error states are documented
- [ ] Non-functional requirements have both MVP and production approaches
- [ ] User stories follow the "As a [user], I want [action], so that [benefit]" format
- [ ] Architecture diagram is included (even ASCII)
- [ ] API endpoints or interface contracts are sketched

### Professionalism
- [ ] Document follows the standard PRD structure (11 sections)
- [ ] Tables are used for metrics, requirements, risks (not prose-only)
- [ ] Markdown formatting is clean and consistent
- [ ] No TODO placeholders remain (or they are explicitly flagged as `[OPEN QUESTION]`)
- [ ] Executive summary can be read standalone and understood

### Interview Fidelity
- [ ] All substantive answers from the interview are reflected in the PRD
- [ ] No features appear in the PRD that weren't discussed (unless clearly marked as agent suggestion)
- [ ] The interviewee's priorities (must-have vs. nice-to-have) are respected
- [ ] Open questions from the interview are carried forward

## Scoring

| Rating | Criteria |
|--------|----------|
| **Ready** | All Critical items pass + ≥80% Quality items pass |
| **Needs Revision** | All Critical items pass but <80% Quality items |
| **Incomplete** | Any Critical item fails |

## If PRD Fails Quality Check

1. Identify which items failed
2. Determine if the gap is due to:
   - **Missing interview data** → go back to interviewee for clarification
   - **Agent generation error** → regenerate the specific section
3. Fix and re-validate before delivering

## Post-Delivery

After delivering the PRD:
1. Ask the interviewee: "Does this accurately reflect what we discussed? Anything missing or misrepresented?"
2. Offer to iterate: "I can refine any section — just point me to it."
3. Suggest next steps: "This PRD is ready for engineering review. Would you like me to create user stories in a ticket format, or a technical spike plan?"
