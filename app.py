"""
AI Audit Toolkit - Web Demo
Run: python3 -m streamlit run app.py
"""
import streamlit as st
import json, io
from datetime import datetime
from pathlib import Path
from audit_toolkit import (Client, Opportunity, AuditProject, calculate_audit_roi, generate_interview_doc, generate_opportunity_matrix, generate_executive_report, generate_executive_pptx)

st.set_page_config(page_title="AI Audit Toolkit - GVRN-AI", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.markdown("### Client Information")
    company_name = st.text_input("Company Name", value="Maplewood Residential Aged Care")
    industry = st.selectbox("Industry", ["aged_care","healthcare","professional_services","retail_ecommerce","finance","manufacturing"], format_func=lambda x: x.replace("_"," ").title())
    employee_count = st.number_input("Employee Count", min_value=1, max_value=10000, value=40)
    contact_name = st.text_input("Primary Contact", value="Karen Mitchell")
    contact_email = st.text_input("Contact Email", value="karen.mitchell@maplewoodcare.com.au")
    avg_salary = st.number_input("Avg Annual Salary ($)", min_value=30000, max_value=300000, value=62000, step=1000)
    implementation_cost = st.number_input("Est. Implementation Cost ($)", min_value=1000, max_value=500000, value=25000, step=1000)
    load_example = st.button("Load Example (Aged Care)", use_container_width=True)

if "opportunities" not in st.session_state:
    st.session_state.opportunities = []
if load_example or (not st.session_state.opportunities):
    st.session_state.opportunities = [
        {"name":"Digital Incident Reporting & SIRS Compliance","description":"Paper-based incident forms take 30-45 min each; SIRS notifications manually tracked in spreadsheet","hours_saved_weekly":6.0,"employees_affected":3,"effort":"low","impact":"high"},
        {"name":"AI-Assisted Quality Standards Documentation","description":"Admin staff spend 12+ hrs/week compiling evidence portfolios for the 8 Aged Care Quality Standards","hours_saved_weekly":10.0,"employees_affected":3,"effort":"low","impact":"high"},
        {"name":"Automated AN-ACC Care Minutes Tracking","description":"Manual tracking of care minutes across shifts; paper timesheets then re-entered into government portal","hours_saved_weekly":5.0,"employees_affected":5,"effort":"low","impact":"high"},
        {"name":"Electronic Medication Management","description":"Paper medication charts with manual round tracking; double-handling increases medication error risk","hours_saved_weekly":4.0,"employees_affected":8,"effort":"high","impact":"high"},
        {"name":"Clinical Care Plan Automation","description":"Quarterly care plan reviews done manually across 45 residents with paper-based assessments","hours_saved_weekly":3.0,"employees_affected":8,"effort":"high","impact":"high"},
        {"name":"Resident & Family Communication Portal","description":"Manual phone calls and printed letters to families for care updates and incident notifications","hours_saved_weekly":3.0,"employees_affected":4,"effort":"low","impact":"low"},
        {"name":"Staff Rostering Optimisation","description":"Manual roster creation in spreadsheets; difficulty balancing care minute targets and award conditions","hours_saved_weekly":5.0,"employees_affected":2,"effort":"low","impact":"low"},
    ]

client = Client(company_name=company_name, industry=industry, employee_count=employee_count, contact_name=contact_name, contact_email=contact_email, avg_salary=avg_salary)
opportunities = [Opportunity(name=o["name"],description=o["description"],hours_saved_weekly=o["hours_saved_weekly"],employees_affected=o["employees_affected"],effort=o["effort"],impact=o["impact"]) for o in st.session_state.opportunities]
project = AuditProject(client=client, opportunities=opportunities, created_date=datetime.now().isoformat(), interviews_completed=8, status="analysis")
roi_data = calculate_audit_roi(opportunities, avg_salary, implementation_cost)

st.markdown("# AI Audit Toolkit")
st.markdown(f"**{company_name}** - {industry.replace('_',' ').title()} | {employee_count} employees")

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard","Opportunities","Interview Questions","Downloads"])

with tab1:
    st.markdown("## Executive Summary")
    combined = roi_data["combined"]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Opportunities", len(opportunities))
    quick_wins = [o for o in opportunities if o.category == "quick_win"]
    c2.metric("Quick Wins", len(quick_wins))
    c3.metric("Hours Saved/Week", f"{combined['hours_saved_weekly']:.0f}")
    c4.metric("Total Annual Value", f"${combined['total_annual_value']:,.0f}")
    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    c1.metric("Annual Cost Savings", f"${combined['annual_savings']:,.0f}")
    c2.metric("First Year ROI", f"{combined['roi_percentage']:.0f}%")
    c3.metric("Payback Period", f"{combined['payback_months']:.1f} months")
    st.markdown("---")
    st.markdown("### Opportunity Matrix")
    for cat_name, cat_key in [("Quick Wins","quick_win"),("Big Swings","big_swing"),("Nice-to-Haves","nice_to_have")]:
        cat_opps = [o for o in opportunities if o.category == cat_key]
        if cat_opps:
            with st.expander(f"{cat_name} ({len(cat_opps)})", expanded=(cat_key=="quick_win")):
                for opp in cat_opps:
                    st.markdown(f"**{opp.name}** - {opp.hours_saved_weekly * opp.employees_affected:.0f} hrs/week saved")
                    st.caption(opp.description)

with tab2:
    st.markdown("## Identified Opportunities")
    for i, opp_data in enumerate(st.session_state.opportunities):
        with st.expander(f"{i+1}. {opp_data['name']} - {opp_data['effort'].upper()}/{opp_data['impact'].upper()}"):
            st.markdown(f"**Description:** {opp_data['description']}")
            st.markdown(f"**Hours saved/week:** {opp_data['hours_saved_weekly']} x {opp_data['employees_affected']} employees")
    st.markdown("---")
    st.markdown("### Add New Opportunity")
    with st.form("add_opp"):
        nn = st.text_input("Name")
        nd = st.text_area("Description")
        c1,c2,c3,c4 = st.columns(4)
        nh = c1.number_input("Hrs saved/wk",min_value=0.5,max_value=40.0,value=5.0,step=0.5)
        ne = c2.number_input("Employees",min_value=1,max_value=500,value=3)
        nef = c3.selectbox("Effort",["low","medium","high"])
        ni = c4.selectbox("Impact",["high","medium","low"])
        if st.form_submit_button("Add",use_container_width=True) and nn:
            st.session_state.opportunities.append({"name":nn,"description":nd,"hours_saved_weekly":nh,"employees_affected":ne,"effort":nef,"impact":ni})
            st.rerun()

with tab3:
    st.markdown("## Interview Questions")
    st.markdown(f"Tailored for **{industry.replace('_',' ').title()}**")
    role = st.radio("Set",["Both","Stakeholder","End-User"],horizontal=True)
    rm = {"Both":"both","Stakeholder":"stakeholder","End-User":"enduser"}
    st.markdown(generate_interview_doc(client, role_type=rm[role]))

with tab4:
    st.markdown("## Download Deliverables")
    c1,c2 = st.columns(2)
    with c1:
        st.download_button("Interview Questions (.md)", data=generate_interview_doc(client), file_name="interview_questions.md", mime="text/markdown", use_container_width=True)
        st.download_button("Opportunity Matrix (.md)", data=generate_opportunity_matrix(opportunities), file_name="opportunity_matrix.md", mime="text/markdown", use_container_width=True)
    with c2:
        st.download_button("Executive Report (.md)", data=generate_executive_report(project, roi_data), file_name="executive_report.md", mime="text/markdown", use_container_width=True)
        tmp = Path("/tmp/pres.pptx")
        generate_executive_pptx(project, roi_data, tmp)
        with open(tmp,"rb") as f:
            st.download_button("Executive PPTX", data=f.read(), file_name="executive_presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation", use_container_width=True)
    st.markdown("---")
    from dataclasses import asdict
    st.download_button("Project JSON", data=json.dumps(asdict(project),indent=2), file_name="audit_project.json", mime="application/json", use_container_width=True)

st.markdown("---")
st.caption("Built by GVRN-AI | AI Audit & Automation Services | github.com/CloudAIX/ai-audit-toolkit")
