#!/usr/bin/env python3
"""
AI Audit Toolkit
Run professional AI audits for clients ($10K engagement framework).

Usage:
    python audit_toolkit.py --new-audit          # Start new audit project
    python audit_toolkit.py --questions          # Generate interview questions
    python audit_toolkit.py --roi                # Calculate ROI
    python audit_toolkit.py --report             # Generate audit report
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Client:
    company_name: str
    industry: str
    employee_count: int
    contact_name: str
    contact_email: str
    avg_salary: float = 65000  # Annual average

@dataclass
class Opportunity:
    name: str
    description: str
    hours_saved_weekly: float
    employees_affected: int
    effort: str  # low, medium, high
    impact: str  # low, medium, high
    category: str = ""  # quick_win, big_swing, nice_to_have, deprioritize

    def __post_init__(self):
        # Auto-categorize based on effort/impact
        if not self.category:
            if self.effort == "low" and self.impact == "high":
                self.category = "quick_win"
            elif self.effort == "high" and self.impact == "high":
                self.category = "big_swing"
            elif self.effort == "low" and self.impact == "low":
                self.category = "nice_to_have"
            else:
                self.category = "deprioritize"

@dataclass
class AuditProject:
    client: Client
    opportunities: List[Opportunity]
    created_date: str
    interviews_completed: int = 0
    status: str = "discovery"  # discovery, analysis, presentation

# ============================================================================
# INTERVIEW QUESTION TEMPLATES
# ============================================================================

STAKEHOLDER_QUESTIONS = {
    "role_overview": [
        "Can you describe your role and your team's primary responsibilities?",
        "What are the main goals or KPIs your team is responsible for this quarter/year?",
        "Could you walk me through your team's structure?",
    ],
    "processes": [
        "From a high level, what are the most critical processes your team manages?",
        "Where do you see the biggest bottlenecks or delays in your team's workflow?",
        "Which tasks seem to consume the most man-hours or resources?",
    ],
    "technology": [
        "What are the main software systems or tools your team relies on?",
        "What are your biggest frustrations with your current technology stack?",
        "Are there important processes that happen outside of your main software?",
    ],
    "pain_points": [
        "What are the biggest challenges your team is facing right now?",
        "If you had a magic wand, what problem would you solve overnight?",
        "What is preventing your team from being more efficient?",
    ],
    "vision": [
        "Where do you see the biggest opportunities for improvement?",
        "How does your team generally respond to new technology?",
    ]
}

ENDUSER_QUESTIONS = {
    "daily_work": [
        "Can you walk me through a typical day or week in your role?",
        "What are the 1-3 most common tasks you perform every day?",
        "How much time is spent on core work versus administrative/repetitive tasks?",
    ],
    "process_deep_dive": [
        "Walk me through the exact steps to complete [specific common task]",
        "Which part is the most manual or takes the most time?",
        "What information do you need and where do you get it?",
    ],
    "tools": [
        "What software do you spend most of your day in?",
        "What do you find most frustrating about your tools?",
        "Is there double-entry or copying between systems?",
    ],
    "pain_points": [
        "What is the most boring or repetitive part of your job?",
        "If you had an assistant, what tasks would you give them immediately?",
        "How do you currently track and report on your work?",
    ]
}

INDUSTRY_SPECIFIC = {
    "healthcare": [
        "How do you currently handle patient intake and documentation?",
        "What compliance requirements create the most administrative burden?",
        "How much time is spent on insurance and billing-related tasks?",
        "What patient communication happens manually vs. automated?",
    ],
    "professional_services": [
        "How do you currently track billable hours and client work?",
        "What's your process for client onboarding?",
        "How much time goes into creating proposals and reports?",
        "What research or document review tasks are most time-consuming?",
    ],
    "retail_ecommerce": [
        "How do you handle inventory management and forecasting?",
        "What's your process for handling customer inquiries and returns?",
        "How do you currently manage product listings and pricing?",
        "What manual work goes into order fulfillment?",
    ],
    "finance": [
        "How do you handle data entry and reconciliation?",
        "What reporting tasks are most time-intensive?",
        "How do you currently manage compliance documentation?",
        "What client communication is done manually?",
    ],
    "manufacturing": [
        "How do you track production and quality metrics?",
        "What manual work goes into supply chain management?",
        "How do you handle equipment maintenance scheduling?",
        "What reporting and documentation is most time-consuming?",
    ]
}

# ============================================================================
# ROI CALCULATOR
# ============================================================================

def calculate_roi(
    hours_saved_weekly: float,
    employees_affected: int,
    avg_annual_salary: float,
    implementation_cost: float,
    automation_efficiency: float = 0.7  # 70% of promised time savings realized
) -> dict:
    """Calculate ROI for an AI automation opportunity."""

    # Hourly rate
    hourly_rate = avg_annual_salary / 2080  # 40 hrs/week * 52 weeks

    # Adjusted hours saved (account for ramp-up and realistic efficiency)
    actual_hours_saved = hours_saved_weekly * employees_affected * automation_efficiency

    # Weekly and annual savings
    weekly_savings = actual_hours_saved * hourly_rate
    annual_savings = weekly_savings * 52

    # Revenue potential (50% of saved time redirected to revenue activities)
    revenue_hours_weekly = actual_hours_saved * 0.5
    # Assume revenue activities are worth 2x salary cost
    weekly_revenue_potential = revenue_hours_weekly * hourly_rate * 2
    annual_revenue_potential = weekly_revenue_potential * 52

    # Total annual value
    total_annual_value = annual_savings + annual_revenue_potential

    # ROI calculation
    roi_percentage = ((annual_savings - implementation_cost) / implementation_cost) * 100 if implementation_cost > 0 else 0
    payback_months = (implementation_cost / (annual_savings / 12)) if annual_savings > 0 else float('inf')

    return {
        "hourly_rate": round(hourly_rate, 2),
        "hours_saved_weekly": round(actual_hours_saved, 1),
        "weekly_savings": round(weekly_savings, 2),
        "annual_savings": round(annual_savings, 2),
        "annual_revenue_potential": round(annual_revenue_potential, 2),
        "total_annual_value": round(total_annual_value, 2),
        "roi_percentage": round(roi_percentage, 1),
        "payback_months": round(payback_months, 1),
        "implementation_cost": implementation_cost
    }

def calculate_audit_roi(opportunities: List[Opportunity], avg_salary: float, implementation_cost: float) -> dict:
    """Calculate combined ROI for all opportunities."""

    total_hours = sum(o.hours_saved_weekly * o.employees_affected for o in opportunities)
    total_employees = sum(o.employees_affected for o in opportunities)

    combined = calculate_roi(
        hours_saved_weekly=total_hours / max(total_employees, 1),
        employees_affected=total_employees,
        avg_annual_salary=avg_salary,
        implementation_cost=implementation_cost
    )

    # By category
    by_category = {}
    for cat in ["quick_win", "big_swing", "nice_to_have", "deprioritize"]:
        cat_opps = [o for o in opportunities if o.category == cat]
        if cat_opps:
            cat_hours = sum(o.hours_saved_weekly * o.employees_affected for o in cat_opps)
            cat_employees = sum(o.employees_affected for o in cat_opps)
            by_category[cat] = calculate_roi(
                hours_saved_weekly=cat_hours / max(cat_employees, 1),
                employees_affected=cat_employees,
                avg_annual_salary=avg_salary,
                implementation_cost=implementation_cost * 0.25  # Rough per-category estimate
            )

    return {
        "combined": combined,
        "by_category": by_category
    }

# ============================================================================
# REPORT GENERATOR
# ============================================================================

def generate_interview_doc(client: Client, role_type: str = "both") -> str:
    """Generate interview questions document for a client."""

    industry = client.industry.lower().replace(" ", "_")

    doc = f"""# AI Audit Interview Questions
## {client.company_name}

**Prepared for**: {client.contact_name}
**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Industry**: {client.industry}
**Employee Count**: {client.employee_count}

---

## Interview Plan

| Business Size | Recommended Interviews | Duration |
|---------------|------------------------|----------|
| {client.employee_count} employees | {"3-5" if client.employee_count < 50 else "10-15"} interviews | 30-45 min each |

**Target mix**:
- 40% Leadership/Stakeholders (understand goals)
- 60% End-users (understand reality)

---

"""

    if role_type in ["both", "stakeholder"]:
        doc += "## Stakeholder Interview Questions (30,000-Foot View)\n\n"
        for section, questions in STAKEHOLDER_QUESTIONS.items():
            doc += f"### {section.replace('_', ' ').title()}\n\n"
            for q in questions:
                doc += f"- {q}\n"
            doc += "\n"

    if role_type in ["both", "enduser"]:
        doc += "## End-User Interview Questions (On-the-Ground Reality)\n\n"
        for section, questions in ENDUSER_QUESTIONS.items():
            doc += f"### {section.replace('_', ' ').title()}\n\n"
            for q in questions:
                doc += f"- {q}\n"
            doc += "\n"

    # Add industry-specific questions
    if industry in INDUSTRY_SPECIFIC:
        doc += f"## {client.industry} Industry-Specific Questions\n\n"
        for q in INDUSTRY_SPECIFIC[industry]:
            doc += f"- {q}\n"
        doc += "\n"

    doc += """---

## Interview Best Practices

- **Listen 80%, Talk 20%** — get them talking
- **Ask "Why?" repeatedly** — get to root causes
- **Record with permission** — use Fireflies.ai for transcription
- **Focus on problems, not solutions** — save solutions for later
- **Note emotional reactions** — frustration = opportunity

## After Each Interview

1. [ ] Transcription saved
2. [ ] Key pain points highlighted
3. [ ] Time estimates noted (hours/week on tasks)
4. [ ] Follow-up questions documented
"""

    return doc


def generate_opportunity_matrix(opportunities: List[Opportunity]) -> str:
    """Generate opportunity matrix visualization."""

    matrix = """# AI Opportunity Matrix

## Quick Reference

| Quadrant | Effort | Impact | Action |
|----------|--------|--------|--------|
| 🎯 Quick Wins | Low | High | **Priority #1** - Start here |
| 🚀 Big Swings | High | High | Long-term, high-ticket |
| ✨ Nice-to-Haves | Low | Low | Add-on value |
| ⏸️ Deprioritize | High | Low | Avoid |

---

## Identified Opportunities

"""

    categories = {
        "quick_win": ("🎯 Quick Wins (Low Effort, High Impact)", []),
        "big_swing": ("🚀 Big Swings (High Effort, High Impact)", []),
        "nice_to_have": ("✨ Nice-to-Haves (Low Effort, Low Impact)", []),
        "deprioritize": ("⏸️ Deprioritize (High Effort, Low Impact)", [])
    }

    for opp in opportunities:
        categories[opp.category][1].append(opp)

    for cat_id, (cat_name, opps) in categories.items():
        if opps:
            matrix += f"### {cat_name}\n\n"
            for opp in opps:
                matrix += f"**{opp.name}**\n"
                matrix += f"- {opp.description}\n"
                matrix += f"- Hours saved: {opp.hours_saved_weekly}/week × {opp.employees_affected} employees\n"
                matrix += f"- Effort: {opp.effort.upper()} | Impact: {opp.impact.upper()}\n\n"

    return matrix


def generate_executive_report(project: AuditProject, roi_data: dict) -> str:
    """Generate executive summary report."""

    client = project.client
    opportunities = project.opportunities

    quick_wins = [o for o in opportunities if o.category == "quick_win"]
    big_swings = [o for o in opportunities if o.category == "big_swing"]

    report = f"""# AI Audit Report
## {client.company_name}

**Prepared by**: GVRN-AI
**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Engagement**: AI Opportunity Assessment

---

## Executive Summary

Following {project.interviews_completed} discovery interviews across {client.company_name},
we identified **{len(opportunities)} AI automation opportunities** with potential annual
value of **${roi_data['combined']['total_annual_value']:,.0f}**.

### Key Findings

| Metric | Value |
|--------|-------|
| Total Opportunities Identified | {len(opportunities)} |
| Quick Wins (Start Immediately) | {len(quick_wins)} |
| Strategic Initiatives | {len(big_swings)} |
| Estimated Hours Saved Weekly | {roi_data['combined']['hours_saved_weekly']:.0f} |
| Annual Cost Savings | ${roi_data['combined']['annual_savings']:,.0f} |
| Annual Revenue Potential | ${roi_data['combined']['annual_revenue_potential']:,.0f} |
| **Total Annual Value** | **${roi_data['combined']['total_annual_value']:,.0f}** |

---

## Recommended Roadmap

### Phase 1: Quick Wins (Weeks 1-4)

"""

    for i, opp in enumerate(quick_wins[:3], 1):
        report += f"""#### {i}. {opp.name}

- **Current State**: {opp.description}
- **Time Impact**: {opp.hours_saved_weekly} hours/week × {opp.employees_affected} people
- **Implementation**: 1-2 weeks

"""

    if big_swings:
        report += "### Phase 2: Strategic Initiatives (Months 2-6)\n\n"
        for i, opp in enumerate(big_swings[:3], 1):
            report += f"""#### {i}. {opp.name}

- **Current State**: {opp.description}
- **Time Impact**: {opp.hours_saved_weekly} hours/week × {opp.employees_affected} people
- **Implementation**: 4-8 weeks

"""

    report += f"""---

## ROI Analysis

### Cost Savings Calculation

```
Hours Saved/Week:     {roi_data['combined']['hours_saved_weekly']:.0f} hours
Average Hourly Rate:  ${roi_data['combined']['hourly_rate']:.2f}
Weekly Savings:       ${roi_data['combined']['weekly_savings']:,.0f}
Annual Savings:       ${roi_data['combined']['annual_savings']:,.0f}
```

### Revenue Potential

Assuming 50% of saved time is redirected to revenue-generating activities:

```
Annual Revenue Potential: ${roi_data['combined']['annual_revenue_potential']:,.0f}
```

### Investment Summary

| Metric | Value |
|--------|-------|
| Estimated Implementation Cost | ${roi_data['combined']['implementation_cost']:,.0f} |
| Payback Period | {roi_data['combined']['payback_months']:.1f} months |
| First Year ROI | {roi_data['combined']['roi_percentage']:.0f}% |

---

## Next Steps

1. **Approve Phase 1 Quick Wins** — Start with highest-impact, lowest-effort items
2. **Schedule kickoff meeting** — Align team and set success metrics
3. **Begin implementation** — Target 2-4 week delivery for first automation

---

*Report generated by GVRN-AI | AI Audit Framework*
*Contact: [your-email@gvrn-ai.com]*
"""

    return report


# ============================================================================
# CLI INTERFACE
# ============================================================================

def interactive_new_audit() -> AuditProject:
    """Interactive wizard to create new audit project."""

    print("\n" + "="*60)
    print("  NEW AI AUDIT PROJECT")
    print("="*60 + "\n")

    # Client info
    company_name = input("Company name: ").strip()
    industry = input("Industry (healthcare, professional_services, retail_ecommerce, finance, manufacturing): ").strip()
    employee_count = int(input("Employee count: ").strip() or "50")
    contact_name = input("Primary contact name: ").strip()
    contact_email = input("Contact email: ").strip()
    avg_salary = float(input("Average annual salary [$65000]: ").strip() or "65000")

    client = Client(
        company_name=company_name,
        industry=industry,
        employee_count=employee_count,
        contact_name=contact_name,
        contact_email=contact_email,
        avg_salary=avg_salary
    )

    project = AuditProject(
        client=client,
        opportunities=[],
        created_date=datetime.now().isoformat()
    )

    return project


def interactive_add_opportunity() -> Opportunity:
    """Add an opportunity interactively."""

    print("\n--- Add Opportunity ---\n")

    name = input("Opportunity name: ").strip()
    description = input("Description (current problem): ").strip()
    hours_saved = float(input("Hours saved per week (per person): ").strip() or "5")
    employees = int(input("Number of employees affected: ").strip() or "1")
    effort = input("Effort (low/medium/high): ").strip().lower() or "medium"
    impact = input("Impact (low/medium/high): ").strip().lower() or "medium"

    return Opportunity(
        name=name,
        description=description,
        hours_saved_weekly=hours_saved,
        employees_affected=employees,
        effort=effort,
        impact=impact
    )


def save_project(project: AuditProject, output_dir: Path):
    """Save project to JSON."""

    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = project.client.company_name.lower().replace(" ", "_")
    filepath = output_dir / f"{safe_name}_audit.json"

    with open(filepath, "w") as f:
        json.dump(asdict(project), f, indent=2)

    print(f"Project saved to: {filepath}")
    return filepath


def load_project(filepath: Path) -> AuditProject:
    """Load project from JSON."""

    with open(filepath) as f:
        data = json.load(f)

    client = Client(**data["client"])
    opportunities = [Opportunity(**o) for o in data["opportunities"]]

    return AuditProject(
        client=client,
        opportunities=opportunities,
        created_date=data["created_date"],
        interviews_completed=data.get("interviews_completed", 0),
        status=data.get("status", "discovery")
    )


def main():
    parser = argparse.ArgumentParser(description="AI Audit Toolkit")
    parser.add_argument("--new-audit", action="store_true", help="Start new audit project")
    parser.add_argument("--questions", action="store_true", help="Generate interview questions")
    parser.add_argument("--roi", action="store_true", help="Calculate ROI")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    parser.add_argument("--project", "-p", type=str, help="Path to project JSON file")
    parser.add_argument("--output", "-o", type=str, help="Output directory")
    parser.add_argument("--example", "-e", action="store_true", help="Run with example data")

    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else Path.cwd() / "output"

    # Example mode
    if args.example:
        client = Client(
            company_name="Acme Healthcare Clinic",
            industry="healthcare",
            employee_count=45,
            contact_name="Dr. Sarah Johnson",
            contact_email="sarah@acmeclinic.com",
            avg_salary=72000
        )

        opportunities = [
            Opportunity("Patient Intake Automation", "Staff spend 20 min per patient on manual form entry", 8, 3, "low", "high"),
            Opportunity("Appointment Reminder System", "Manual phone calls for appointment reminders", 10, 2, "low", "high"),
            Opportunity("Insurance Verification Bot", "Staff manually verify insurance for each patient", 15, 2, "medium", "high"),
            Opportunity("AI Medical Scribe", "Doctors spend 2 hrs/day on documentation", 10, 5, "high", "high"),
            Opportunity("Patient FAQ Chatbot", "Repetitive phone inquiries about hours, location, etc.", 5, 2, "low", "medium"),
        ]

        project = AuditProject(
            client=client,
            opportunities=opportunities,
            created_date=datetime.now().isoformat(),
            interviews_completed=6,
            status="analysis"
        )

        # Generate all outputs
        output_dir.mkdir(parents=True, exist_ok=True)

        # Interview questions
        questions = generate_interview_doc(client)
        q_path = output_dir / "interview_questions.md"
        q_path.write_text(questions)
        print(f"Interview questions: {q_path}")

        # Opportunity matrix
        matrix = generate_opportunity_matrix(opportunities)
        m_path = output_dir / "opportunity_matrix.md"
        m_path.write_text(matrix)
        print(f"Opportunity matrix: {m_path}")

        # ROI calculation
        roi_data = calculate_audit_roi(opportunities, client.avg_salary, 15000)

        # Executive report
        report = generate_executive_report(project, roi_data)
        r_path = output_dir / "executive_report.md"
        r_path.write_text(report)
        print(f"Executive report: {r_path}")

        # Save project
        save_project(project, output_dir)

        print("\n" + "="*60)
        print("Example audit generated! Check the output/ folder.")
        print("="*60)
        return

    # New audit
    if args.new_audit:
        project = interactive_new_audit()

        # Ask if they want to add opportunities
        while True:
            add_more = input("\nAdd opportunity? (y/n): ").strip().lower()
            if add_more == "y":
                opp = interactive_add_opportunity()
                project.opportunities.append(opp)
            else:
                break

        save_project(project, output_dir)
        return

    # Load existing project for other commands
    if args.project:
        project = load_project(Path(args.project))
    else:
        print("Use --example for demo, --new-audit to start, or --project <file> to load existing.")
        return

    # Generate questions
    if args.questions:
        questions = generate_interview_doc(project.client)
        q_path = output_dir / "interview_questions.md"
        q_path.write_text(questions)
        print(f"Saved to: {q_path}")

    # Calculate ROI
    if args.roi:
        roi_data = calculate_audit_roi(project.opportunities, project.client.avg_salary, 15000)
        print(json.dumps(roi_data, indent=2))

    # Generate report
    if args.report:
        roi_data = calculate_audit_roi(project.opportunities, project.client.avg_salary, 15000)
        report = generate_executive_report(project, roi_data)
        r_path = output_dir / "executive_report.md"
        r_path.write_text(report)
        print(f"Saved to: {r_path}")


if __name__ == "__main__":
    main()
