"""
HR Analytics Dashboard - Streamlit Application
Comprehensive HR analytics with filters, drilldown, red flags, and AI-powered insights
Password protected version for sharing
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import re

# Page config
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================
# PASSWORD PROTECTION
# =====================
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"].strip().upper() == "HR NORGE":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 60vh;">
            <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; max-width: 400px;">
                <h1 style="margin-bottom: 10px;">👥 HR Analytics</h1>
                <p style="margin-bottom: 30px; opacity: 0.9;">Dashboard for HR-profesjonelle</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "🔐 Skriv inn tilgangskode:",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Tilgangskode..."
            )
            st.markdown("<p style='text-align: center; color: #666; font-size: 12px;'>Hint: To ord som beskriver HR i Norden</p>", unsafe_allow_html=True)
        return False

    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 60vh;">
            <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; max-width: 400px;">
                <h1 style="margin-bottom: 10px;">👥 HR Analytics</h1>
                <p style="margin-bottom: 30px; opacity: 0.9;">Dashboard for HR-profesjonelle</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "🔐 Skriv inn tilgangskode:",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Tilgangskode..."
            )
            st.error("❌ Feil kode. Prøv igjen!")
        return False

    else:
        # Password correct
        return True

# Check password before showing anything
if not check_password():
    st.stop()

# =====================
# MAIN APP STARTS HERE
# =====================

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 5px;
    }
    .red-flag {
        background-color: #ff4444;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
        font-weight: bold;
    }
    .green-flag {
        background-color: #00C851;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .yellow-flag {
        background-color: #ffbb33;
        color: black;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
    }
</style>
""", unsafe_allow_html=True)

# =====================
# DATA LOADING
# =====================
@st.cache_data
def load_data():
    """Load all HR data from CSV files"""
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Try 'data' subfolder first, then root folder
    data_path = os.path.join(base_path, 'data')
    if not os.path.exists(os.path.join(data_path, 'employees.csv')):
        data_path = base_path  # Files are in root folder

    employees = pd.read_csv(f'{data_path}/employees.csv')
    sick_leave = pd.read_csv(f'{data_path}/sick_leave.csv')
    recruitment = pd.read_csv(f'{data_path}/recruitment.csv')
    terminations = pd.read_csv(f'{data_path}/terminations.csv')

    # Convert dates
    employees['hire_date'] = pd.to_datetime(employees['hire_date'])
    employees['termination_date'] = pd.to_datetime(employees['termination_date'])
    employees['last_promotion_date'] = pd.to_datetime(employees['last_promotion_date'])
    recruitment['open_date'] = pd.to_datetime(recruitment['open_date'])
    recruitment['close_date'] = pd.to_datetime(recruitment['close_date'])
    terminations['termination_date'] = pd.to_datetime(terminations['termination_date'])

    return employees, sick_leave, recruitment, terminations

# Load data
employees_df, sick_leave_df, recruitment_df, terminations_df = load_data()

# Active employees
active_employees = employees_df[employees_df['termination_date'].isna()].copy()

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.image("https://img.icons8.com/color/96/000000/conference-call.png", width=80)
st.sidebar.title("🎛️ Filtre")

# Country filter
countries = ['Alle'] + sorted(active_employees['country'].unique().tolist())
selected_country = st.sidebar.selectbox("🌍 Land", countries)

# Department filter
departments = ['Alle'] + sorted(active_employees['department'].unique().tolist())
selected_dept = st.sidebar.selectbox("🏢 Avdeling", departments)

# Seniority filter
seniority_levels = ['Alle'] + ['Junior', 'Mid', 'Senior', 'Lead', 'Director', 'VP', 'C-Level']
selected_seniority = st.sidebar.selectbox("📊 Senioritetsnivå", seniority_levels)

# Job family filter
job_families = ['Alle'] + sorted(active_employees['job_family'].unique().tolist())
selected_job_family = st.sidebar.selectbox("👔 Rollefamilie", job_families)

# Time period
st.sidebar.subheader("📅 Tidsperiode")
date_range = st.sidebar.date_input(
    "Velg periode",
    value=(datetime(2024, 1, 1), datetime(2024, 12, 31)),
    min_value=datetime(2018, 1, 1),
    max_value=datetime(2025, 1, 15)
)

# Apply filters
def apply_filters(df):
    filtered = df.copy()
    if selected_country != 'Alle':
        filtered = filtered[filtered['country'] == selected_country]
    if selected_dept != 'Alle':
        filtered = filtered[filtered['department'] == selected_dept]
    if selected_seniority != 'Alle':
        filtered = filtered[filtered['seniority_level'] == selected_seniority]
    if selected_job_family != 'Alle':
        filtered = filtered[filtered['job_family'] == selected_job_family]
    return filtered

filtered_active = apply_filters(active_employees)
filtered_all = apply_filters(employees_df)

# =====================
# KPI CALCULATIONS
# =====================
def calculate_kpis(filtered_df, all_df, sick_df, term_df, recruit_df):
    """Calculate all KPIs based on filtered data"""
    kpis = {}

    # Headcount
    kpis['headcount'] = len(filtered_df)

    # Average tenure
    kpis['avg_tenure'] = filtered_df['tenure_years'].mean() if len(filtered_df) > 0 else 0

    # Average salary
    kpis['avg_salary'] = filtered_df['salary'].mean() if len(filtered_df) > 0 else 0

    # Turnover rate (annualized)
    if len(all_df) > 0:
        terminated_count = len(all_df[all_df['termination_date'].notna()])
        avg_headcount = len(all_df) - terminated_count / 2
        kpis['turnover_rate'] = (terminated_count / avg_headcount * 100) if avg_headcount > 0 else 0
    else:
        kpis['turnover_rate'] = 0

    # Voluntary turnover
    if selected_country != 'Alle':
        term_filtered = term_df[term_df['employee_id'].isin(all_df['employee_id'])]
    else:
        term_filtered = term_df
    voluntary = term_filtered[term_filtered['termination_reason'] == 'Voluntary']
    kpis['voluntary_turnover'] = len(voluntary)
    kpis['voluntary_turnover_rate'] = (len(voluntary) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

    # Average engagement
    kpis['avg_engagement'] = filtered_df['engagement_score'].mean() if len(filtered_df) > 0 else 0

    # Average performance
    kpis['avg_performance'] = filtered_df['performance_rating'].mean() if len(filtered_df) > 0 else 0

    # Flight risk distribution
    kpis['high_flight_risk'] = len(filtered_df[filtered_df['flight_risk'] == 'High'])
    kpis['flight_risk_pct'] = (kpis['high_flight_risk'] / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

    # Time to hire (from recruitment data)
    if selected_dept != 'Alle':
        recruit_filtered = recruit_df[recruit_df['department'] == selected_dept]
    else:
        recruit_filtered = recruit_df
    kpis['avg_time_to_hire'] = recruit_filtered['days_to_fill'].mean() if len(recruit_filtered) > 0 else 0

    # Sick leave rate
    if selected_country != 'Alle':
        sick_filtered = sick_df[sick_df['employee_id'].isin(filtered_df['employee_id'])]
    else:
        sick_filtered = sick_df
    total_sick_days = sick_filtered['sick_days'].sum() if len(sick_filtered) > 0 else 0
    working_days_per_year = 230 * len(filtered_df)
    kpis['sick_leave_rate'] = (total_sick_days / working_days_per_year * 100) if working_days_per_year > 0 else 0

    # Internal mobility rate
    kpis['internal_mobility'] = (len(filtered_df[filtered_df['internal_moves'] > 0]) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

    # Cost of attrition
    if selected_country != 'Alle':
        term_filtered = term_df[term_df['employee_id'].isin(all_df['employee_id'])]
    else:
        term_filtered = term_df
    kpis['cost_of_attrition'] = term_filtered['replacement_cost'].sum() if len(term_filtered) > 0 else 0

    # Gender distribution
    gender_counts = filtered_df['gender'].value_counts()
    kpis['gender_m'] = gender_counts.get('M', 0)
    kpis['gender_f'] = gender_counts.get('F', 0)
    kpis['gender_balance'] = (kpis['gender_f'] / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

    # Span of control (average direct reports per manager)
    managers = filtered_df[filtered_df['job_family'].isin(['Management', 'Executive'])]
    if len(managers) > 0:
        non_managers = filtered_df[~filtered_df['job_family'].isin(['Management', 'Executive'])]
        kpis['span_of_control'] = len(non_managers) / len(managers)
    else:
        kpis['span_of_control'] = 0

    # Training hours
    kpis['avg_training_hours'] = filtered_df['training_hours_ytd'].mean() if len(filtered_df) > 0 else 0

    # Compa-ratio (salary position in band)
    if len(filtered_df) > 0:
        filtered_df_calc = filtered_df.copy()
        filtered_df_calc['band_mid'] = (filtered_df_calc['salary_band_min'] + filtered_df_calc['salary_band_max']) / 2
        filtered_df_calc['compa_ratio'] = filtered_df_calc['salary'] / filtered_df_calc['band_mid']
        kpis['avg_compa_ratio'] = filtered_df_calc['compa_ratio'].mean()
    else:
        kpis['avg_compa_ratio'] = 0

    return kpis

kpis = calculate_kpis(filtered_active, filtered_all, sick_leave_df, terminations_df, recruitment_df)

# =====================
# RED FLAGS DETECTION
# =====================
def detect_red_flags(kpis, filtered_df, sick_df, recruit_df):
    """Detect anomalies and red flags"""
    flags = []

    # High turnover
    if kpis['turnover_rate'] > 15:
        flags.append({
            'type': 'danger',
            'title': 'Høy turnover',
            'message': f"Turnover på {kpis['turnover_rate']:.1f}% overstiger benchmark på 15%",
            'metric': 'turnover_rate',
            'value': kpis['turnover_rate'],
            'explanation': generate_explanation('turnover', kpis, filtered_df)
        })

    # Low engagement
    if kpis['avg_engagement'] < 6.5:
        flags.append({
            'type': 'danger',
            'title': 'Lav engasjement',
            'message': f"Gjennomsnittlig engasjement på {kpis['avg_engagement']:.1f} er under målet på 6.5",
            'metric': 'engagement',
            'value': kpis['avg_engagement'],
            'explanation': generate_explanation('engagement', kpis, filtered_df)
        })

    # High flight risk
    if kpis['flight_risk_pct'] > 20:
        flags.append({
            'type': 'danger',
            'title': 'Høy flight risk',
            'message': f"{kpis['flight_risk_pct']:.1f}% av ansatte har høy risiko for å slutte",
            'metric': 'flight_risk',
            'value': kpis['flight_risk_pct'],
            'explanation': generate_explanation('flight_risk', kpis, filtered_df)
        })

    # Long time to hire
    if kpis['avg_time_to_hire'] > 50:
        flags.append({
            'type': 'warning',
            'title': 'Lang rekrutteringstid',
            'message': f"Gjennomsnittlig {kpis['avg_time_to_hire']:.0f} dager for å fylle stillinger",
            'metric': 'time_to_hire',
            'value': kpis['avg_time_to_hire'],
            'explanation': generate_explanation('time_to_hire', kpis, filtered_df)
        })

    # High sick leave
    if kpis['sick_leave_rate'] > 5:
        flags.append({
            'type': 'warning',
            'title': 'Høyt sykefravær',
            'message': f"Sykefraværsrate på {kpis['sick_leave_rate']:.1f}% er over benchmark på 5%",
            'metric': 'sick_leave',
            'value': kpis['sick_leave_rate'],
            'explanation': generate_explanation('sick_leave', kpis, filtered_df)
        })

    # Compa-ratio issues
    if kpis['avg_compa_ratio'] < 0.90 or kpis['avg_compa_ratio'] > 1.10:
        direction = 'under' if kpis['avg_compa_ratio'] < 0.90 else 'over'
        flags.append({
            'type': 'warning',
            'title': 'Lønnsavvik',
            'message': f"Compa-ratio på {kpis['avg_compa_ratio']:.2f} - ansatte er {direction} markedslønn",
            'metric': 'compa_ratio',
            'value': kpis['avg_compa_ratio'],
            'explanation': generate_explanation('salary', kpis, filtered_df)
        })

    # Gender imbalance in leadership
    mgmt = filtered_df[filtered_df['job_family'].isin(['Management', 'Executive'])]
    if len(mgmt) > 10:
        female_mgmt = len(mgmt[mgmt['gender'] == 'F']) / len(mgmt) * 100
        if female_mgmt < 30:
            flags.append({
                'type': 'warning',
                'title': 'Diversity gap',
                'message': f"Kun {female_mgmt:.0f}% kvinner i ledelsen (mål: minimum 40%)",
                'metric': 'diversity',
                'value': female_mgmt,
                'explanation': generate_explanation('diversity', kpis, filtered_df)
            })

    # Wide span of control
    if kpis['span_of_control'] > 10:
        flags.append({
            'type': 'warning',
            'title': 'Bred span of control',
            'message': f"Gjennomsnittlig {kpis['span_of_control']:.1f} ansatte per leder (anbefalt: <10)",
            'metric': 'span_of_control',
            'value': kpis['span_of_control'],
            'explanation': generate_explanation('span_of_control', kpis, filtered_df)
        })

    # Low internal mobility
    if kpis['internal_mobility'] < 8:
        flags.append({
            'type': 'info',
            'title': 'Lav intern mobilitet',
            'message': f"Kun {kpis['internal_mobility']:.1f}% har hatt interne bytter (benchmark: 10%)",
            'metric': 'mobility',
            'value': kpis['internal_mobility'],
            'explanation': generate_explanation('mobility', kpis, filtered_df)
        })

    return flags

def generate_explanation(flag_type, kpis, filtered_df):
    """Generate detailed explanation for each red flag"""
    explanations = {
        'turnover': f"""
**Analyse av turnover:**
- Total frivillig turnover: {kpis['voluntary_turnover']} ansatte
- Hovedårsaker basert på exit-undersøkelser viser at ansatte med lav engasjementsscore ({kpis['avg_engagement']:.1f}/10) har høyere sannsynlighet for å slutte
- Avdelinger med høyest turnover bør prioriteres for tiltak
- Estimert kostnad for attrition: {kpis['cost_of_attrition']:,.0f} NOK

**Anbefalte tiltak:**
1. Gjennomfør stay-intervjuer med høy-risiko ansatte
2. Revurder kompensasjonspakker for kritiske roller
3. Styrk karriereutviklingsmuligheter
        """,
        'engagement': f"""
**Analyse av engasjement:**
- Gjennomsnittlig engasjementsscore: {kpis['avg_engagement']:.1f}/10
- {kpis['high_flight_risk']} ansatte har høy flight risk
- Det er sterk korrelasjon mellom engasjement og produktivitet

**Påvirkningsfaktorer:**
- Lederskap og feedback-kvalitet
- Karriereutviklingsmuligheter
- Work-life balance
- Lønn relativt til markedet (compa-ratio: {kpis['avg_compa_ratio']:.2f})

**Anbefalte tiltak:**
1. Implementer pulse surveys for tettere oppfølging
2. Utvikle ledertreningsprogrammer
3. Etabler mentorordninger
        """,
        'flight_risk': f"""
**Analyse av flight risk:**
- {kpis['flight_risk_pct']:.1f}% av ansatte klassifisert som høy risiko
- Risikofaktorer inkluderer: lav engasjement, lang tid siden forfremmelse, lønn under band-midtpunkt

**Kostnad ved å miste disse ansatte:**
Estimert erstatningskostnad er 1.5-2.5x årslønn per person.
Med gjennomsnittlig lønn på {kpis['avg_salary']:,.0f} NOK representerer dette en betydelig risiko.

**Anbefalte tiltak:**
1. Prioriter retention-samtaler med topp-talenter
2. Vurder akselerert lønnsrevisjon for underbetalt segment
3. Tilby stretch assignments og synlighet for høytytende
        """,
        'time_to_hire': f"""
**Analyse av rekrutteringstid:**
- Gjennomsnittlig tid for å fylle stillinger: {kpis['avg_time_to_hire']:.0f} dager
- Benchmark for bransjen er 35-45 dager

**Konsekvenser av lang rekrutteringstid:**
- Økt arbeidsbelastning på eksisterende ansatte
- Tapt produktivitet og inntekt
- Risiko for å miste gode kandidater til konkurrenter

**Anbefalte tiltak:**
1. Strømlinjeform intervjuprosessen
2. Bygg sterkere talent pipeline
3. Vurder bruk av referral-bonuser
4. Optimaliser stillingsannonser og employer branding
        """,
        'sick_leave': f"""
**Analyse av sykefravær:**
- Sykefraværsrate: {kpis['sick_leave_rate']:.1f}%
- Korrelerer ofte med lav engasjement og høy arbeidsbelastning
- Sesongvariasjon (høyere i vintermånedene)

**Kostnad av sykefravær:**
Med headcount på {kpis['headcount']} og gjennomsnittlig dagsrate tilsier dette betydelige indirekte kostnader.

**Anbefalte tiltak:**
1. Analyser sykefravær per avdeling og leder
2. Implementer helsefremmende tiltak
3. Vurder fleksible arbeidsordninger
4. Følg opp ledere med høyt fravær i team
        """,
        'salary': f"""
**Analyse av lønnsposisjon:**
- Gjennomsnittlig compa-ratio: {kpis['avg_compa_ratio']:.2f}
- Idealområde er 0.95-1.05
- Ansatte {'under' if kpis['avg_compa_ratio'] < 0.95 else 'over'} markedslønn

**Risiko ved lønnsavvik:**
- Under markedslønn: Høyere turnover, vanskelig å rekruttere
- Over markedslønn: Høyere lønnskostnader, begrenset fleksibilitet

**Anbefalte tiltak:**
1. Gjennomfør lønnsmarkedsanalyse
2. Prioriter justeringer for kritiske roller
3. Kommuniser total rewards-pakke tydeligere
        """,
        'diversity': f"""
**Analyse av kjønnsbalanse i ledelsen:**
- Kvinner utgjør {kpis['gender_balance']:.0f}% av total arbeidsstyrke
- Men betydelig lavere representasjon i lederroller
- Mål: Minimum 40% av hvert kjønn i ledelsen

**Konsekvenser av ubalanse:**
- Begrenset perspektivmangfold i beslutninger
- Svakere employer brand
- Potensielt juridisk/regulatorisk risiko

**Anbefalte tiltak:**
1. Sett konkrete mål for kjønnsbalanse i ledelsen
2. Utvikle talentprogrammer for underrepresenterte grupper
3. Gjennomgå rekrutteringsprosesser for ubevisst bias
4. Etabler sponsorprogrammer for kvinner
        """,
        'span_of_control': f"""
**Analyse av span of control:**
- Gjennomsnittlig {kpis['span_of_control']:.1f} ansatte per leder
- Anbefalt nivå: 5-10 for de fleste roller

**Konsekvenser av for bred span:**
- Redusert tid til coaching og utvikling
- Økt risiko for utbrenthet hos ledere
- Svakere oppfølging og feedback

**Anbefalte tiltak:**
1. Identifiser ledere med >12 direct reports
2. Vurder opprettelse av teamlead-roller
3. Implementer peer coaching
        """,
        'mobility': f"""
**Analyse av intern mobilitet:**
- Kun {kpis['internal_mobility']:.1f}% har byttet rolle internt
- Benchmark: 10-15% årlig intern mobilitet

**Konsekvenser av lav mobilitet:**
- Stagnasjon og redusert engasjement
- Mister talenter til eksterne muligheter
- Begrenset kunnskapsdeling på tvers

**Anbefalte tiltak:**
1. Etabler intern jobbmarked med synlige muligheter
2. Oppmuntre ledere til å støtte interne bytter
3. Fjern barrierer for tverrfaglig bevegelse
4. Anerkjenn ledere som utvikler talent for andre avdelinger
        """
    }
    return explanations.get(flag_type, "Ingen detaljert analyse tilgjengelig.")

red_flags = detect_red_flags(kpis, filtered_active, sick_leave_df, recruitment_df)

# =====================
# MAIN DASHBOARD
# =====================
st.title("👥 HR Analytics Dashboard")
st.markdown(f"**Organisasjon:** 4,564 aktive ansatte | **Filtrert utvalg:** {len(filtered_active):,} ansatte")

# Executive Summary
with st.expander("📊 Executive Summary", expanded=True):
    st.markdown(f"""
    ### Nøkkelinnsikter for {selected_country if selected_country != 'Alle' else 'hele organisasjonen'}

    **Workforce Overview:**
    - **Headcount:** {kpis['headcount']:,} ansatte med gjennomsnittlig ansiennitet på {kpis['avg_tenure']:.1f} år
    - **Turnover:** {kpis['turnover_rate']:.1f}% årlig rate ({kpis['voluntary_turnover']} frivillige avganger)
    - **Estimert kostnad av attrition:** {kpis['cost_of_attrition']:,.0f} NOK

    **Engagement & Risk:**
    - **Engasjementsscore:** {kpis['avg_engagement']:.1f}/10 ({"🔴 Under mål" if kpis['avg_engagement'] < 6.5 else "🟢 På mål"})
    - **Flight risk:** {kpis['high_flight_risk']} ansatte ({kpis['flight_risk_pct']:.1f}%) har høy risiko for å slutte

    **Rekruttering:**
    - **Time-to-hire:** Gjennomsnittlig {kpis['avg_time_to_hire']:.0f} dager

    **Helse & Fravær:**
    - **Sykefraværsrate:** {kpis['sick_leave_rate']:.1f}%
    """)

# KPI Cards Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="👥 Headcount",
        value=f"{kpis['headcount']:,}",
        delta=f"{kpis['avg_tenure']:.1f} år snitt"
    )

with col2:
    st.metric(
        label="📉 Turnover Rate",
        value=f"{kpis['turnover_rate']:.1f}%",
        delta=f"-{15 - kpis['turnover_rate']:.1f}% fra benchmark" if kpis['turnover_rate'] < 15 else f"+{kpis['turnover_rate'] - 15:.1f}% over benchmark",
        delta_color="normal" if kpis['turnover_rate'] < 15 else "inverse"
    )

with col3:
    st.metric(
        label="💚 Engagement",
        value=f"{kpis['avg_engagement']:.1f}/10",
        delta="På mål" if kpis['avg_engagement'] >= 6.5 else "Under mål",
        delta_color="normal" if kpis['avg_engagement'] >= 6.5 else "inverse"
    )

with col4:
    st.metric(
        label="⏱️ Time to Hire",
        value=f"{kpis['avg_time_to_hire']:.0f} dager",
        delta=f"{45 - kpis['avg_time_to_hire']:.0f} vs benchmark" if kpis['avg_time_to_hire'] <= 45 else f"+{kpis['avg_time_to_hire'] - 45:.0f} over",
        delta_color="normal" if kpis['avg_time_to_hire'] <= 45 else "inverse"
    )

with col5:
    st.metric(
        label="🏥 Sykefravær",
        value=f"{kpis['sick_leave_rate']:.1f}%",
        delta="Normal" if kpis['sick_leave_rate'] <= 5 else "Høyt",
        delta_color="normal" if kpis['sick_leave_rate'] <= 5 else "inverse"
    )

st.markdown("---")

# Red Flags Section
if red_flags:
    st.subheader("🚩 Red Flags & Varsler")

    for flag in red_flags:
        color_class = 'red-flag' if flag['type'] == 'danger' else 'yellow-flag' if flag['type'] == 'warning' else 'green-flag'
        icon = '🔴' if flag['type'] == 'danger' else '🟡' if flag['type'] == 'warning' else 'ℹ️'

        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{icon} {flag['title']}:** {flag['message']}")
            with col2:
                with st.popover("🔍 Forklar hvorfor"):
                    st.markdown(flag['explanation'])

st.markdown("---")

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview",
    "📈 Turnover",
    "👥 Workforce",
    "💰 Compensation",
    "🎯 Recruitment",
    "🔮 What-If Simulator",
    "💬 Chat med Data"
])

# =====================
# TAB 1: OVERVIEW
# =====================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Headcount by Department
        dept_counts = filtered_active.groupby('department').size().reset_index(name='count')
        fig_dept = px.bar(
            dept_counts.sort_values('count', ascending=True),
            x='count', y='department',
            orientation='h',
            title='Headcount per Avdeling',
            color='count',
            color_continuous_scale='Blues'
        )
        fig_dept.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_dept, use_container_width=True)

    with col2:
        # Headcount by Country
        country_counts = filtered_active.groupby('country').size().reset_index(name='count')
        fig_country = px.pie(
            country_counts,
            values='count',
            names='country',
            title='Fordeling per Land',
            hole=0.4
        )
        fig_country.update_layout(height=400)
        st.plotly_chart(fig_country, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Seniority Distribution
        sen_counts = filtered_active.groupby('seniority_level').size().reset_index(name='count')
        sen_order = ['Junior', 'Mid', 'Senior', 'Lead', 'Director', 'VP', 'C-Level']
        sen_counts['seniority_level'] = pd.Categorical(sen_counts['seniority_level'], categories=sen_order, ordered=True)
        sen_counts = sen_counts.sort_values('seniority_level')

        fig_sen = px.bar(
            sen_counts,
            x='seniority_level', y='count',
            title='Senioritetspyramide',
            color='count',
            color_continuous_scale='Viridis'
        )
        fig_sen.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_sen, use_container_width=True)

    with col4:
        # Engagement by Department
        eng_dept = filtered_active.groupby('department')['engagement_score'].mean().reset_index()
        eng_dept = eng_dept.sort_values('engagement_score', ascending=True)

        fig_eng = px.bar(
            eng_dept,
            x='engagement_score', y='department',
            orientation='h',
            title='Engasjement per Avdeling',
            color='engagement_score',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig_eng.add_vline(x=6.5, line_dash="dash", line_color="red", annotation_text="Mål: 6.5")
        fig_eng.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_eng, use_container_width=True)

# =====================
# TAB 2: TURNOVER
# =====================
with tab2:
    st.subheader("📈 Turnover Analyse")

    col1, col2 = st.columns(2)

    with col1:
        # Turnover by department
        term_with_dept = terminations_df.merge(
            employees_df[['employee_id', 'department', 'country']],
            on='employee_id'
        )
        if selected_country != 'Alle':
            term_with_dept = term_with_dept[term_with_dept['country'] == selected_country]

        turnover_dept = term_with_dept.groupby('department').size().reset_index(name='terminations')
        headcount_dept = filtered_active.groupby('department').size().reset_index(name='headcount')
        turnover_rate_dept = turnover_dept.merge(headcount_dept, on='department')
        turnover_rate_dept['rate'] = turnover_rate_dept['terminations'] / turnover_rate_dept['headcount'] * 100

        fig_turnover = px.bar(
            turnover_rate_dept.sort_values('rate', ascending=False),
            x='department', y='rate',
            title='Turnover Rate per Avdeling (%)',
            color='rate',
            color_continuous_scale=['green', 'yellow', 'red']
        )
        fig_turnover.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Benchmark: 15%")
        st.plotly_chart(fig_turnover, use_container_width=True)

    with col2:
        # Termination reasons
        if selected_country != 'Alle':
            term_filtered = term_with_dept
        else:
            term_filtered = terminations_df

        reason_counts = term_filtered['termination_reason'].value_counts().reset_index()
        reason_counts.columns = ['reason', 'count']

        fig_reasons = px.pie(
            reason_counts,
            values='count',
            names='reason',
            title='Årsaker til Avgang',
            color='reason',
            color_discrete_map={'Voluntary': '#FF6B6B', 'Involuntary': '#4ECDC4', 'Retirement': '#45B7D1'}
        )
        st.plotly_chart(fig_reasons, use_container_width=True)

    # Cost of attrition over time
    st.subheader("💸 Kostnad av Turnover")

    term_with_dept['month'] = term_with_dept['termination_date'].dt.to_period('M').astype(str)
    cost_by_month = term_with_dept.groupby('month')['replacement_cost'].sum().reset_index()
    cost_by_month = cost_by_month.tail(24)  # Last 24 months

    fig_cost = px.area(
        cost_by_month,
        x='month', y='replacement_cost',
        title='Estimert Erstatningskostnad per Måned (NOK)',
        labels={'replacement_cost': 'Kostnad (NOK)', 'month': 'Måned'}
    )
    fig_cost.update_layout(height=350)
    st.plotly_chart(fig_cost, use_container_width=True)

    # Flight risk analysis
    st.subheader("⚠️ Flight Risk Analyse")

    col1, col2 = st.columns(2)

    with col1:
        flight_by_dept = filtered_active.groupby(['department', 'flight_risk']).size().unstack(fill_value=0)
        flight_by_dept_pct = flight_by_dept.div(flight_by_dept.sum(axis=1), axis=0) * 100

        fig_flight = px.bar(
            flight_by_dept_pct.reset_index().melt(id_vars='department'),
            x='department', y='value',
            color='flight_risk',
            title='Flight Risk Fordeling per Avdeling (%)',
            color_discrete_map={'Low': 'green', 'Medium': 'yellow', 'High': 'red'},
            barmode='stack'
        )
        st.plotly_chart(fig_flight, use_container_width=True)

    with col2:
        # High flight risk employees
        high_risk = filtered_active[filtered_active['flight_risk'] == 'High'].copy()
        high_risk = high_risk.sort_values('salary', ascending=False).head(10)

        st.markdown("**Topp 10 Høy-Risiko Ansatte (etter lønn)**")
        display_cols = ['name', 'department', 'seniority_level', 'tenure_years', 'engagement_score', 'salary']
        st.dataframe(
            high_risk[display_cols].style.format({
                'salary': '{:,.0f}',
                'tenure_years': '{:.1f}',
                'engagement_score': '{:.1f}'
            }),
            use_container_width=True,
            hide_index=True
        )

# =====================
# TAB 3: WORKFORCE
# =====================
with tab3:
    st.subheader("👥 Workforce Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Age distribution
        age_counts = filtered_active.groupby('age_group').size().reset_index(name='count')
        age_order = ['<25', '25-34', '35-44', '45-54', '55+']
        age_counts['age_group'] = pd.Categorical(age_counts['age_group'], categories=age_order, ordered=True)
        age_counts = age_counts.sort_values('age_group')

        fig_age = px.bar(
            age_counts,
            x='age_group', y='count',
            title='Aldersfordeling',
            color='count',
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col2:
        # Gender by seniority
        gender_sen = filtered_active.groupby(['seniority_level', 'gender']).size().unstack(fill_value=0)
        sen_order = ['Junior', 'Mid', 'Senior', 'Lead', 'Director', 'VP', 'C-Level']
        gender_sen = gender_sen.reindex(sen_order)

        fig_gender = px.bar(
            gender_sen.reset_index().melt(id_vars='seniority_level'),
            x='seniority_level', y='value',
            color='gender',
            title='Kjønnsfordeling per Senioritetsnivå',
            barmode='group',
            color_discrete_map={'M': '#4169E1', 'F': '#FF69B4', 'Other': '#90EE90'}
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    # Tenure distribution
    st.subheader("📅 Ansiennitet")

    fig_tenure = px.histogram(
        filtered_active,
        x='tenure_years',
        nbins=20,
        title='Fordeling av Ansiennitet (år)',
        color_discrete_sequence=['#667eea']
    )
    fig_tenure.add_vline(x=filtered_active['tenure_years'].mean(), line_dash="dash", line_color="red",
                         annotation_text=f"Snitt: {filtered_active['tenure_years'].mean():.1f} år")
    st.plotly_chart(fig_tenure, use_container_width=True)

    # Internal mobility
    st.subheader("🔄 Intern Mobilitet")

    col1, col2 = st.columns(2)

    with col1:
        mobility_dept = filtered_active.groupby('department')['internal_moves'].mean().reset_index()
        mobility_dept = mobility_dept.sort_values('internal_moves', ascending=False)

        fig_mobility = px.bar(
            mobility_dept,
            x='department', y='internal_moves',
            title='Gjennomsnittlig Interne Bytter per Avdeling',
            color='internal_moves',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_mobility, use_container_width=True)

    with col2:
        # Training hours by department
        training_dept = filtered_active.groupby('department')['training_hours_ytd'].mean().reset_index()
        training_dept = training_dept.sort_values('training_hours_ytd', ascending=False)

        fig_training = px.bar(
            training_dept,
            x='department', y='training_hours_ytd',
            title='Gjennomsnittlig Opplæringstimer YTD',
            color='training_hours_ytd',
            color_continuous_scale='Oranges'
        )
        fig_training.add_hline(y=40, line_dash="dash", line_color="green", annotation_text="Mål: 40 timer")
        st.plotly_chart(fig_training, use_container_width=True)

# =====================
# TAB 4: COMPENSATION
# =====================
with tab4:
    st.subheader("💰 Kompensasjonsanalyse")

    # Calculate compa-ratio for all employees
    filtered_comp = filtered_active.copy()
    filtered_comp['band_mid'] = (filtered_comp['salary_band_min'] + filtered_comp['salary_band_max']) / 2
    filtered_comp['compa_ratio'] = filtered_comp['salary'] / filtered_comp['band_mid']

    col1, col2 = st.columns(2)

    with col1:
        # Compa-ratio by department
        compa_dept = filtered_comp.groupby('department')['compa_ratio'].mean().reset_index()
        compa_dept = compa_dept.sort_values('compa_ratio')

        fig_compa = px.bar(
            compa_dept,
            x='compa_ratio', y='department',
            orientation='h',
            title='Compa-Ratio per Avdeling',
            color='compa_ratio',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig_compa.add_vline(x=1.0, line_dash="dash", line_color="black", annotation_text="Markedssnitt")
        fig_compa.add_vrect(x0=0.95, x1=1.05, fillcolor="green", opacity=0.1)
        st.plotly_chart(fig_compa, use_container_width=True)

    with col2:
        # Salary distribution
        fig_salary = px.box(
            filtered_comp,
            x='seniority_level',
            y='salary',
            title='Lønnsfordeling per Senioritetsnivå',
            color='seniority_level',
            category_orders={'seniority_level': ['Junior', 'Mid', 'Senior', 'Lead', 'Director', 'VP', 'C-Level']}
        )
        st.plotly_chart(fig_salary, use_container_width=True)

    # Pay equity analysis
    st.subheader("⚖️ Pay Equity Analyse")

    col1, col2 = st.columns(2)

    with col1:
        # Gender pay gap by seniority
        gender_pay = filtered_comp.groupby(['seniority_level', 'gender'])['salary'].mean().unstack()
        gender_pay['gap_pct'] = ((gender_pay['M'] - gender_pay['F']) / gender_pay['M'] * 100).fillna(0)
        gender_pay = gender_pay.reset_index()

        fig_gap = px.bar(
            gender_pay,
            x='seniority_level', y='gap_pct',
            title='Lønnsforskjell M vs F per Nivå (%)',
            color='gap_pct',
            color_continuous_scale=['green', 'yellow', 'red']
        )
        fig_gap.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig_gap, use_container_width=True)

    with col2:
        # Underpaid employees (compa < 0.90)
        underpaid = filtered_comp[filtered_comp['compa_ratio'] < 0.90].copy()
        underpaid = underpaid.sort_values('compa_ratio').head(10)

        st.markdown("**Ansatte Under Lønnsband (<90% compa-ratio)**")
        if len(underpaid) > 0:
            display_cols = ['name', 'department', 'seniority_level', 'salary', 'compa_ratio']
            st.dataframe(
                underpaid[display_cols].style.format({
                    'salary': '{:,.0f}',
                    'compa_ratio': '{:.2f}'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("Ingen ansatte ligger under 90% av lønnsbandet!")

# =====================
# TAB 5: RECRUITMENT
# =====================
with tab5:
    st.subheader("🎯 Rekrutteringsanalyse")

    recruit_filtered = recruitment_df.copy()
    if selected_dept != 'Alle':
        recruit_filtered = recruit_filtered[recruit_filtered['department'] == selected_dept]
    if selected_country != 'Alle':
        recruit_filtered = recruit_filtered[recruit_filtered['country'] == selected_country]

    col1, col2 = st.columns(2)

    with col1:
        # Time to fill by department
        ttf_dept = recruit_filtered.groupby('department')['days_to_fill'].mean().reset_index()
        ttf_dept = ttf_dept.sort_values('days_to_fill', ascending=False)

        fig_ttf = px.bar(
            ttf_dept,
            x='department', y='days_to_fill',
            title='Gjennomsnittlig Time-to-Fill per Avdeling (dager)',
            color='days_to_fill',
            color_continuous_scale=['green', 'yellow', 'red']
        )
        fig_ttf.add_hline(y=45, line_dash="dash", line_color="red", annotation_text="Benchmark: 45 dager")
        st.plotly_chart(fig_ttf, use_container_width=True)

    with col2:
        # Recruitment source effectiveness
        source_counts = recruit_filtered['source'].value_counts().reset_index()
        source_counts.columns = ['source', 'count']

        fig_source = px.pie(
            source_counts,
            values='count',
            names='source',
            title='Rekrutteringskilder',
            hole=0.4
        )
        st.plotly_chart(fig_source, use_container_width=True)

    # Time to fill trend
    recruit_filtered['month'] = recruit_filtered['close_date'].dt.to_period('M').astype(str)
    ttf_trend = recruit_filtered.groupby('month')['days_to_fill'].mean().reset_index()
    ttf_trend = ttf_trend.tail(24)

    fig_trend = px.line(
        ttf_trend,
        x='month', y='days_to_fill',
        title='Time-to-Fill Trend (siste 24 måneder)',
        markers=True
    )
    fig_trend.add_hline(y=45, line_dash="dash", line_color="red", annotation_text="Benchmark")
    fig_trend.update_layout(height=350)
    st.plotly_chart(fig_trend, use_container_width=True)

    # Funnel metrics
    st.subheader("🔽 Rekrutteringstrakt")

    total_screened = recruit_filtered['candidates_screened'].sum()
    total_interviewed = recruit_filtered['candidates_interviewed'].sum()
    total_hired = len(recruit_filtered)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Screenet", f"{total_screened:,}")
    with col2:
        st.metric("Intervjuet", f"{total_interviewed:,}", delta=f"{total_interviewed/total_screened*100:.1f}% konvertering")
    with col3:
        st.metric("Ansatt", f"{total_hired:,}", delta=f"{total_hired/total_interviewed*100:.1f}% av intervjuede")

# =====================
# TAB 6: WHAT-IF SIMULATOR
# =====================
with tab6:
    st.subheader("🔮 What-If Simulator")
    st.markdown("Simuler effekten av tiltak på turnover-kostnad for høy-risiko grupper")

    # Select risk group
    col1, col2 = st.columns(2)

    with col1:
        sim_dept = st.selectbox("Velg avdeling for simulering", ['Alle'] + sorted(filtered_active['department'].unique().tolist()))
        sim_seniority = st.selectbox("Velg senioritetsnivå", ['Alle'] + ['Junior', 'Mid', 'Senior', 'Lead', 'Director', 'VP', 'C-Level'])

    with col2:
        salary_increase = st.slider("Lønnsøkning (%)", 0, 20, 5)
        training_increase = st.slider("Økt opplæring (timer)", 0, 40, 10)
        engagement_program = st.checkbox("Implementer engasjementsprogram (+0.5 score)")

    # Filter for simulation
    sim_df = filtered_active.copy()
    if sim_dept != 'Alle':
        sim_df = sim_df[sim_df['department'] == sim_dept]
    if sim_seniority != 'Alle':
        sim_df = sim_df[sim_df['seniority_level'] == sim_seniority]

    high_risk_sim = sim_df[sim_df['flight_risk'] == 'High'].copy()

    # Current state
    current_high_risk = len(high_risk_sim)
    current_avg_salary = high_risk_sim['salary'].mean() if len(high_risk_sim) > 0 else 0
    current_turnover_cost = current_high_risk * current_avg_salary * 1.8  # Estimated 1.8x salary as replacement cost

    # Simulate intervention effects
    # Salary increase reduces flight risk probability
    salary_effect = salary_increase * 2  # Each 1% salary increase reduces turnover risk by 2%
    training_effect = training_increase * 0.5  # Each extra training hour reduces risk by 0.5%
    engagement_effect = 10 if engagement_program else 0  # Engagement program reduces risk by 10%

    total_risk_reduction = min(salary_effect + training_effect + engagement_effect, 80)  # Cap at 80% reduction

    # New projections
    projected_risk_reduction = current_high_risk * (total_risk_reduction / 100)
    projected_remaining_risk = current_high_risk - projected_risk_reduction
    intervention_cost = (salary_increase / 100 * current_avg_salary * len(high_risk_sim)) + (training_increase * 500 * len(high_risk_sim))
    if engagement_program:
        intervention_cost += 50000  # Fixed cost for engagement program

    projected_saved_turnover = projected_risk_reduction * current_avg_salary * 1.8
    net_benefit = projected_saved_turnover - intervention_cost

    # Display results
    st.markdown("---")
    st.subheader("📊 Simuleringsresultater")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Nåværende Høy-Risiko Ansatte",
            f"{current_high_risk}",
            help="Antall ansatte med høy flight risk i valgt segment"
        )
        st.metric(
            "Estimert Turnover-Kostnad (uten tiltak)",
            f"{current_turnover_cost:,.0f} NOK"
        )

    with col2:
        st.metric(
            "Estimert Risikoreduksjon",
            f"{total_risk_reduction:.0f}%",
            delta=f"-{projected_risk_reduction:.0f} ansatte"
        )
        st.metric(
            "Kostnad for Tiltak",
            f"{intervention_cost:,.0f} NOK"
        )

    with col3:
        st.metric(
            "Forventet Besparelse (turnover)",
            f"{projected_saved_turnover:,.0f} NOK"
        )
        st.metric(
            "Netto Gevinst",
            f"{net_benefit:,.0f} NOK",
            delta="Lønnsomt" if net_benefit > 0 else "Ikke lønnsomt",
            delta_color="normal" if net_benefit > 0 else "inverse"
        )

    # Visualization
    fig_sim = go.Figure()

    fig_sim.add_trace(go.Bar(
        x=['Før tiltak', 'Etter tiltak'],
        y=[current_turnover_cost, current_turnover_cost - projected_saved_turnover + intervention_cost],
        name='Total Kostnad',
        marker_color=['#FF6B6B', '#4ECDC4']
    ))

    fig_sim.update_layout(
        title='Kostnad Før vs Etter Tiltak',
        yaxis_title='Kostnad (NOK)',
        height=400
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    # ROI calculation
    if intervention_cost > 0:
        roi = (net_benefit / intervention_cost) * 100
        st.info(f"**ROI på tiltak:** {roi:.0f}% - For hver krone investert får dere {1 + roi/100:.2f} NOK tilbake")

# =====================
# TAB 7: CHAT MED DATA
# =====================
with tab7:
    st.subheader("💬 Chat med Data")
    st.markdown("Still spørsmål om HR-dataene på norsk, og få svar med relevante grafer og KPI-er.")

    # Simple chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input(
        "Skriv ditt spørsmål her:",
        placeholder="F.eks: 'Hvor har vi størst lønnsavvik?' eller 'Hvilken avdeling har høyest turnover?'"
    )

    def answer_question(question):
        """Simple rule-based question answering for demo purposes"""
        question_lower = question.lower()

        # Define answer patterns
        answers = []

        if any(word in question_lower for word in ['lønnsavvik', 'lønn', 'compa', 'underbetalt', 'salary']):
            # Compensation analysis
            comp_df = filtered_active.copy()
            comp_df['band_mid'] = (comp_df['salary_band_min'] + comp_df['salary_band_max']) / 2
            comp_df['compa_ratio'] = comp_df['salary'] / comp_df['band_mid']

            dept_compa = comp_df.groupby('department')['compa_ratio'].mean().sort_values()
            lowest_dept = dept_compa.index[0]
            lowest_ratio = dept_compa.iloc[0]

            country_compa = comp_df.groupby('country')['compa_ratio'].mean().sort_values()
            lowest_country = country_compa.index[0]

            answer = f"""
**Lønnsavvik-analyse:**

📊 **Største lønnsavvik per avdeling:**
- **{lowest_dept}** har lavest compa-ratio på **{lowest_ratio:.2f}** (under markedssnitt)
- Dette betyr at ansatte i denne avdelingen i snitt tjener {(1-lowest_ratio)*100:.0f}% under lønnsbandets midtpunkt

📍 **Per land:**
- **{lowest_country}** har lavest lønnsnivå relativt til band

🔴 **Risiko:** Lavt lønnsnivå korrelerer med høyere flight risk og turnover.

**Se graf:** 'Compensation' tab → Compa-Ratio per Avdeling
            """

            # Create viz
            fig = px.bar(
                dept_compa.reset_index(),
                x='compa_ratio', y='department',
                orientation='h',
                title='Compa-Ratio per Avdeling (1.0 = markedssnitt)',
                color='compa_ratio',
                color_continuous_scale=['red', 'yellow', 'green']
            )
            fig.add_vline(x=1.0, line_dash="dash", line_color="black")

            return answer, fig

        elif any(word in question_lower for word in ['turnover', 'slutter', 'attrition', 'avganger']):
            # Turnover analysis
            term_dept = terminations_df.merge(employees_df[['employee_id', 'department']], on='employee_id')
            turnover_counts = term_dept.groupby('department').size().sort_values(ascending=False)
            highest_dept = turnover_counts.index[0]
            highest_count = turnover_counts.iloc[0]

            answer = f"""
**Turnover-analyse:**

📊 **Høyest turnover per avdeling:**
1. **{highest_dept}**: {highest_count} avganger
2. **{turnover_counts.index[1]}**: {turnover_counts.iloc[1]} avganger
3. **{turnover_counts.index[2]}**: {turnover_counts.iloc[2]} avganger

💰 **Total kostnad av attrition:** {terminations_df['replacement_cost'].sum():,.0f} NOK

**Årsaker (fra exit-undersøkelser):**
- {len(terminations_df[terminations_df['termination_reason']=='Voluntary'])} frivillige avganger
- {len(terminations_df[terminations_df['termination_reason']=='Involuntary'])} ufrivillige avganger

**Se graf:** 'Turnover' tab → Turnover Rate per Avdeling
            """

            fig = px.bar(
                turnover_counts.reset_index(),
                x='department', y='count' if 'count' in turnover_counts.reset_index().columns else 0,
                title='Antall Avganger per Avdeling',
                color=0 if 'count' not in turnover_counts.reset_index().columns else 'count',
                color_continuous_scale=['green', 'yellow', 'red']
            )

            return answer, fig

        elif any(word in question_lower for word in ['engasjement', 'engagement', 'motivasjon', 'trivsel']):
            # Engagement analysis
            eng_dept = filtered_active.groupby('department')['engagement_score'].mean().sort_values()
            lowest_eng_dept = eng_dept.index[0]
            lowest_eng = eng_dept.iloc[0]

            eng_country = filtered_active.groupby('country')['engagement_score'].mean().sort_values()
            lowest_eng_country = eng_country.index[0]

            answer = f"""
**Engasjements-analyse:**

📊 **Lavest engasjement:**
- **{lowest_eng_dept}** har lavest score på **{lowest_eng:.1f}/10**
- **{lowest_eng_country}** har lavest nasjonal score

🎯 **Organisasjonssnitt:** {filtered_active['engagement_score'].mean():.1f}/10 (mål: 6.5)

⚠️ **Risiko:** {len(filtered_active[filtered_active['engagement_score'] < 6])} ansatte har engagement under 6.0

**Korrelasjon:**
- Lav engagement → Høyere sykefravær
- Lav engagement → Høyere turnover-risiko

**Se graf:** 'Overview' tab → Engasjement per Avdeling
            """

            fig = px.bar(
                eng_dept.reset_index(),
                x='engagement_score', y='department',
                orientation='h',
                title='Engasjementsscore per Avdeling',
                color='engagement_score',
                color_continuous_scale=['red', 'yellow', 'green']
            )
            fig.add_vline(x=6.5, line_dash="dash", line_color="red", annotation_text="Mål")

            return answer, fig

        elif any(word in question_lower for word in ['sykefravær', 'syk', 'fravær', 'sick']):
            # Sick leave analysis
            sick_with_dept = sick_leave_df.merge(employees_df[['employee_id', 'department', 'country']], on='employee_id')
            sick_dept = sick_with_dept.groupby('department')['sick_days'].sum().sort_values(ascending=False)
            highest_sick = sick_dept.index[0]

            answer = f"""
**Sykefraværs-analyse:**

📊 **Høyest sykefravær:**
- **{highest_sick}** har flest sykedager totalt
- Gjennomsnittlig sykefraværsrate: {kpis['sick_leave_rate']:.1f}%

📅 **Sesongvariasjon:** Høyere fravær i vintermånedene (jan-feb, nov-des)

**Korrelasjon med engagement:**
- Ansatte med lav engagement har 40% høyere sykefravær

**Se graf:** Se 'Overview' for avdelingsfordeling
            """

            fig = px.bar(
                sick_dept.reset_index(),
                x='department', y='sick_days',
                title='Totale Sykedager per Avdeling (2024)',
                color='sick_days',
                color_continuous_scale=['green', 'yellow', 'red']
            )

            return answer, fig

        elif any(word in question_lower for word in ['rekruttering', 'hire', 'ansette', 'time to fill']):
            # Recruitment analysis
            ttf_dept = recruitment_df.groupby('department')['days_to_fill'].mean().sort_values(ascending=False)
            slowest = ttf_dept.index[0]
            slowest_days = ttf_dept.iloc[0]

            answer = f"""
**Rekrutterings-analyse:**

📊 **Lengst rekrutteringstid:**
- **{slowest}**: {slowest_days:.0f} dager i snitt
- Benchmark: 45 dager

🎯 **Beste kilder:**
- LinkedIn: {len(recruitment_df[recruitment_df['source']=='LinkedIn'])} ansettelser
- Referral: {len(recruitment_df[recruitment_df['source']=='Referral'])} ansettelser

**Se graf:** 'Recruitment' tab → Time-to-Fill per Avdeling
            """

            fig = px.bar(
                ttf_dept.reset_index(),
                x='department', y='days_to_fill',
                title='Gjennomsnittlig Time-to-Fill (dager)',
                color='days_to_fill',
                color_continuous_scale=['green', 'yellow', 'red']
            )
            fig.add_hline(y=45, line_dash="dash", line_color="red")

            return answer, fig

        elif any(word in question_lower for word in ['diversity', 'kjønn', 'kvinner', 'menn', 'gender']):
            # Diversity analysis
            gender_sen = filtered_active.groupby(['seniority_level', 'gender']).size().unstack(fill_value=0)
            female_leadership = filtered_active[
                (filtered_active['job_family'].isin(['Management', 'Executive'])) &
                (filtered_active['gender'] == 'F')
            ]
            total_leadership = filtered_active[filtered_active['job_family'].isin(['Management', 'Executive'])]
            female_pct = len(female_leadership) / len(total_leadership) * 100 if len(total_leadership) > 0 else 0

            answer = f"""
**Diversity-analyse:**

📊 **Kjønnsfordeling total:**
- Menn: {len(filtered_active[filtered_active['gender']=='M'])} ({len(filtered_active[filtered_active['gender']=='M'])/len(filtered_active)*100:.0f}%)
- Kvinner: {len(filtered_active[filtered_active['gender']=='F'])} ({len(filtered_active[filtered_active['gender']=='F'])/len(filtered_active)*100:.0f}%)

👔 **I ledelsen (Management + Executive):**
- Kvinner: **{female_pct:.0f}%** (mål: 40%)

⚠️ **Gap:** Kvinner er underrepresentert på Director+ nivå

**Se graf:** 'Workforce' tab → Kjønnsfordeling per Senioritetsnivå
            """

            fig = px.bar(
                filtered_active.groupby(['seniority_level', 'gender']).size().unstack(fill_value=0).reindex(['Junior', 'Mid', 'Senior', 'Lead', 'Director', 'VP', 'C-Level']).reset_index().melt(id_vars='seniority_level'),
                x='seniority_level', y='value',
                color='gender',
                barmode='group',
                title='Kjønnsfordeling per Nivå',
                color_discrete_map={'M': '#4169E1', 'F': '#FF69B4', 'Other': '#90EE90'}
            )

            return answer, fig

        elif any(word in question_lower for word in ['flight risk', 'risiko', 'miste', 'beholde']):
            # Flight risk analysis
            risk_dept = filtered_active.groupby('department')['flight_risk'].apply(lambda x: (x == 'High').sum()).sort_values(ascending=False)
            highest_risk_dept = risk_dept.index[0]

            answer = f"""
**Flight Risk-analyse:**

📊 **Avdelinger med høyest risiko:**
1. **{highest_risk_dept}**: {risk_dept.iloc[0]} høy-risiko ansatte
2. **{risk_dept.index[1]}**: {risk_dept.iloc[1]} høy-risiko ansatte

⚠️ **Totalt:** {len(filtered_active[filtered_active['flight_risk']=='High'])} ansatte med høy flight risk

**Risikofaktorer:**
- Lav engagement (<6)
- Lang tid siden forfremmelse
- Under markedslønn

**Se graf:** 'Turnover' tab → Flight Risk Analyse
            """

            fig = px.bar(
                risk_dept.reset_index(),
                x='department', y='flight_risk',
                title='Antall Høy-Risiko Ansatte per Avdeling',
                color='flight_risk',
                color_continuous_scale=['green', 'yellow', 'red']
            )

            return answer, fig

        else:
            # General response
            answer = f"""
**Generell HR-oversikt:**

👥 **Headcount:** {kpis['headcount']:,} ansatte
📉 **Turnover:** {kpis['turnover_rate']:.1f}%
💚 **Engagement:** {kpis['avg_engagement']:.1f}/10
⏱️ **Time-to-Hire:** {kpis['avg_time_to_hire']:.0f} dager
🏥 **Sykefravær:** {kpis['sick_leave_rate']:.1f}%

**Prøv spørsmål som:**
- "Hvor har vi størst lønnsavvik?"
- "Hvilken avdeling har høyest turnover?"
- "Hvordan er kjønnsfordelingen i ledelsen?"
- "Hvilke ansatte har høyest flight risk?"
- "Hvordan er engasjementet per avdeling?"
            """
            return answer, None

    if user_question:
        answer, fig = answer_question(user_question)
        st.markdown(answer)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    # Example questions
    st.markdown("---")
    st.markdown("**Eksempel-spørsmål du kan stille:**")
    example_questions = [
        "Hvor har vi størst lønnsavvik?",
        "Hvilken avdeling har høyest turnover?",
        "Hvordan er engasjementet per avdeling?",
        "Hvor er sykefraværet høyest?",
        "Hvordan er kjønnsfordelingen i ledelsen?",
        "Hvilke ansatte har høyest flight risk?",
        "Hvor lang er rekrutteringstiden?"
    ]
    for q in example_questions:
        if st.button(q, key=f"example_{q}"):
            answer, fig = answer_question(q)
            st.markdown(answer)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>HR Analytics Dashboard | Bygget med Streamlit og Plotly</p>
    <p>Data er syntetisk generert for demonstrasjonsformål</p>
</div>
""", unsafe_allow_html=True)
