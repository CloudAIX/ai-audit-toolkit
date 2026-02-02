# AI Audit Toolkit

Run professional AI audits for clients using the 3-step framework. Generate interview questions, calculate ROI, and create executive reports.

**Framework Value**: $10,000+ engagement

## What It Does

1. **Interview Question Generator** — Industry-specific questions for stakeholders and end-users
2. **Opportunity Matrix** — Categorize findings into Quick Wins, Big Swings, etc.
3. **ROI Calculator** — Cost savings + revenue potential with payback period
4. **Executive Report Generator** — Client-ready presentation document

## Quick Start

```bash
# Clone the repo
git clone https://github.com/CloudAIX/ai-audit-toolkit.git
cd ai-audit-toolkit

# Run with example data
python3 audit_toolkit.py --example

# Check generated files
ls output/
```

## Usage

### Generate Example Audit

```bash
python3 audit_toolkit.py --example
```

Creates a complete audit for "Acme Healthcare Clinic" with:
- Interview questions (healthcare-specific)
- 5 opportunities identified
- ROI calculations (~$337K annual value)
- Executive report

### Start New Audit

```bash
python3 audit_toolkit.py --new-audit
```

Interactive wizard to:
1. Enter client information
2. Add opportunities as you discover them
3. Save project for later

### Generate Specific Outputs

```bash
# Interview questions only
python3 audit_toolkit.py --project output/client_audit.json --questions

# ROI calculation
python3 audit_toolkit.py --project output/client_audit.json --roi

# Executive report
python3 audit_toolkit.py --project output/client_audit.json --report
```

## The 3-Step Framework

### Step 1: Discovery Interviews (Week 1)

| Business Size | Interview Count | Duration |
|---------------|-----------------|----------|
| 10-50 employees | 3-5 interviews | 30-45 min |
| 50+ employees | 10-15 interviews | 30-45 min |

**Two groups**:
- 40% Leadership (understand goals)
- 60% End-users (understand reality)

### Step 2: Map & Identify (Week 1-2)

Plot opportunities on the matrix:

| Quadrant | Effort | Impact | Action |
|----------|--------|--------|--------|
| 🎯 Quick Wins | Low | High | Priority #1 |
| 🚀 Big Swings | High | High | Long-term |
| ✨ Nice-to-Haves | Low | Low | Add-on |
| ⏸️ Deprioritize | High | Low | Avoid |

### Step 3: Present & Close (Week 2)

The "Money Slide" shows:
- Annual cost savings
- Revenue potential (50% of saved time → revenue activities)
- Payback period
- ROI percentage

## Supported Industries

- Healthcare
- Professional Services (Law, Accounting)
- Retail / E-commerce
- Finance
- Manufacturing

Each industry has tailored interview questions.

## Output Files

```
output/
├── interview_questions.md      # Ready for discovery calls
├── opportunity_matrix.md       # Visual categorization
├── executive_report.md         # Client presentation
└── client_audit.json           # Project data (reusable)
```

## ROI Calculation Method

```
1. Hours Saved/Week × Employees = Total Hours
2. Total Hours × Hourly Rate = Weekly Savings
3. Weekly Savings × 52 = Annual Savings
4. 50% of Saved Hours × 2× Rate = Revenue Potential
5. (Annual Savings / Cost) × 100 = ROI %
```

## Example Output

For a 45-employee healthcare clinic:

| Metric | Value |
|--------|-------|
| Opportunities Found | 5 |
| Quick Wins | 2 |
| Hours Saved Weekly | 94 |
| Annual Savings | $168,840 |
| Revenue Potential | $168,840 |
| **Total Annual Value** | **$337,680** |
| Payback Period | 1.1 months |

## Pricing This Service

| Deliverable | Price Range |
|-------------|-------------|
| Discovery + Report Only | $5,000 - $10,000 |
| Audit + Phase 1 Implementation | $15,000 - $25,000 |
| Full Transformation (6 months) | $50,000+ |

## License

MIT

---

Built by [GVRN-AI](https://gvrn-ai.com) | AI Audit & Automation Services
