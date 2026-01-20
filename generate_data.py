"""
Synthetic HR Data Generator
Generates realistic HR data for ~5000 employees across Nordic + Germany
No external dependencies beyond pandas/numpy
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_EMPLOYEES = 5200  # Including some who have left
CURRENT_DATE = datetime(2025, 1, 15)
START_DATE = datetime(2018, 1, 1)

# Norwegian names
NORWEGIAN_FIRST_MALE = ['Erik', 'Lars', 'Anders', 'Magnus', 'Kristian', 'Thomas', 'Martin', 'Jonas', 'Marius', 'Henrik', 'Ola', 'Per', 'Jan', 'Bjørn', 'Knut', 'Trond', 'Geir', 'Svein', 'Håkon', 'Olav']
NORWEGIAN_FIRST_FEMALE = ['Anne', 'Kari', 'Ingrid', 'Hilde', 'Silje', 'Marit', 'Camilla', 'Ida', 'Tone', 'Nina', 'Kristin', 'Maria', 'Heidi', 'Lene', 'Marte', 'Astrid', 'Sigrid', 'Liv', 'Berit', 'Grete']
NORWEGIAN_LAST = ['Hansen', 'Johansen', 'Olsen', 'Larsen', 'Andersen', 'Pedersen', 'Nilsen', 'Kristiansen', 'Jensen', 'Karlsen', 'Johnsen', 'Pettersen', 'Eriksen', 'Berg', 'Haugen', 'Hagen', 'Johannessen', 'Andreassen', 'Jacobsen', 'Dahl']

SWEDISH_FIRST_MALE = ['Erik', 'Lars', 'Anders', 'Magnus', 'Johan', 'Karl', 'Per', 'Mikael', 'Fredrik', 'Stefan', 'Oscar', 'Gustav', 'Niklas', 'Henrik', 'Daniel', 'Mattias', 'Jonas', 'Alexander', 'Peter', 'Andreas']
SWEDISH_FIRST_FEMALE = ['Anna', 'Maria', 'Elisabeth', 'Eva', 'Karin', 'Sara', 'Emma', 'Linnéa', 'Linda', 'Sofia', 'Malin', 'Jenny', 'Elin', 'Frida', 'Johanna', 'Amanda', 'Lena', 'Annika', 'Kristina', 'Ingrid']
SWEDISH_LAST = ['Andersson', 'Johansson', 'Karlsson', 'Nilsson', 'Eriksson', 'Larsson', 'Olsson', 'Persson', 'Svensson', 'Gustafsson', 'Pettersson', 'Jonsson', 'Jansson', 'Hansson', 'Bengtsson', 'Lindberg', 'Lindqvist', 'Lindgren', 'Berg', 'Berglund']

DANISH_FIRST_MALE = ['Lars', 'Peter', 'Michael', 'Søren', 'Thomas', 'Henrik', 'Christian', 'Martin', 'Anders', 'Morten', 'Jesper', 'Niels', 'Jens', 'Hans', 'Rasmus', 'Kasper', 'Frederik', 'Mikkel', 'Jonas', 'Simon']
DANISH_FIRST_FEMALE = ['Anne', 'Kirsten', 'Mette', 'Hanne', 'Anna', 'Susanne', 'Lene', 'Marianne', 'Camilla', 'Lone', 'Rikke', 'Louise', 'Sofie', 'Maria', 'Trine', 'Charlotte', 'Julie', 'Emma', 'Laura', 'Sara']
DANISH_LAST = ['Nielsen', 'Jensen', 'Hansen', 'Pedersen', 'Andersen', 'Christensen', 'Larsen', 'Sørensen', 'Rasmussen', 'Jørgensen', 'Petersen', 'Madsen', 'Kristensen', 'Olsen', 'Thomsen', 'Poulsen', 'Johansen', 'Mortensen', 'Møller', 'Berg']

FINNISH_FIRST_MALE = ['Mikko', 'Jukka', 'Matti', 'Antti', 'Juha', 'Petri', 'Jari', 'Timo', 'Kari', 'Pekka', 'Sami', 'Ville', 'Teemu', 'Tuomas', 'Lauri', 'Markus', 'Aleksi', 'Eero', 'Heikki', 'Ilkka']
FINNISH_FIRST_FEMALE = ['Maria', 'Emilia', 'Sofia', 'Johanna', 'Anna', 'Elina', 'Laura', 'Hanna', 'Riikka', 'Tiina', 'Sanna', 'Minna', 'Päivi', 'Jaana', 'Sari', 'Katja', 'Anu', 'Kirsi', 'Outi', 'Niina']
FINNISH_LAST = ['Korhonen', 'Virtanen', 'Mäkinen', 'Nieminen', 'Mäkelä', 'Hämäläinen', 'Laine', 'Heikkinen', 'Koskinen', 'Järvinen', 'Lehtonen', 'Lehtinen', 'Saarinen', 'Salminen', 'Heinonen', 'Niemi', 'Heikkilä', 'Kinnunen', 'Salonen', 'Turunen']

GERMAN_FIRST_MALE = ['Thomas', 'Michael', 'Andreas', 'Stefan', 'Christian', 'Markus', 'Daniel', 'Martin', 'Frank', 'Peter', 'Matthias', 'Alexander', 'Jan', 'Tobias', 'Jens', 'Sebastian', 'Tim', 'Florian', 'Lukas', 'Felix']
GERMAN_FIRST_FEMALE = ['Maria', 'Anna', 'Julia', 'Laura', 'Sarah', 'Lisa', 'Katharina', 'Sandra', 'Nicole', 'Sabine', 'Stefanie', 'Monika', 'Petra', 'Andrea', 'Claudia', 'Christina', 'Melanie', 'Jennifer', 'Daniela', 'Nina']
GERMAN_LAST = ['Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann', 'Koch', 'Bauer', 'Richter', 'Klein', 'Wolf', 'Schröder', 'Neumann', 'Schwarz', 'Zimmermann', 'Braun']

# Organization structure
COUNTRIES = {
    'Norge': {'weight': 0.35, 'cities': ['Oslo', 'Bergen', 'Trondheim', 'Stavanger'], 'currency_factor': 1.0,
              'first_male': NORWEGIAN_FIRST_MALE, 'first_female': NORWEGIAN_FIRST_FEMALE, 'last': NORWEGIAN_LAST},
    'Sverige': {'weight': 0.25, 'cities': ['Stockholm', 'Göteborg', 'Malmö'], 'currency_factor': 0.95,
                'first_male': SWEDISH_FIRST_MALE, 'first_female': SWEDISH_FIRST_FEMALE, 'last': SWEDISH_LAST},
    'Danmark': {'weight': 0.15, 'cities': ['København', 'Aarhus', 'Odense'], 'currency_factor': 0.98,
                'first_male': DANISH_FIRST_MALE, 'first_female': DANISH_FIRST_FEMALE, 'last': DANISH_LAST},
    'Finland': {'weight': 0.10, 'cities': ['Helsinki', 'Tampere', 'Turku'], 'currency_factor': 0.92,
                'first_male': FINNISH_FIRST_MALE, 'first_female': FINNISH_FIRST_FEMALE, 'last': FINNISH_LAST},
    'Tyskland': {'weight': 0.15, 'cities': ['Berlin', 'München', 'Hamburg', 'Frankfurt'], 'currency_factor': 0.88,
                 'first_male': GERMAN_FIRST_MALE, 'first_female': GERMAN_FIRST_FEMALE, 'last': GERMAN_LAST}
}

DEPARTMENTS = {
    'Engineering': {'weight': 0.25, 'turnover_factor': 1.2, 'salary_factor': 1.15},
    'Sales': {'weight': 0.18, 'turnover_factor': 1.4, 'salary_factor': 1.05},
    'Customer Support': {'weight': 0.15, 'turnover_factor': 1.5, 'salary_factor': 0.85},
    'Operations': {'weight': 0.12, 'turnover_factor': 0.9, 'salary_factor': 0.95},
    'Finance': {'weight': 0.08, 'turnover_factor': 0.8, 'salary_factor': 1.0},
    'HR': {'weight': 0.06, 'turnover_factor': 0.7, 'salary_factor': 0.92},
    'Marketing': {'weight': 0.08, 'turnover_factor': 1.1, 'salary_factor': 1.0},
    'R&D': {'weight': 0.08, 'turnover_factor': 0.85, 'salary_factor': 1.2}
}

SENIORITY_LEVELS = {
    'Junior': {'weight': 0.20, 'salary_range': (450000, 550000), 'years_exp': (0, 2)},
    'Mid': {'weight': 0.35, 'salary_range': (550000, 750000), 'years_exp': (2, 5)},
    'Senior': {'weight': 0.25, 'salary_range': (750000, 950000), 'years_exp': (5, 10)},
    'Lead': {'weight': 0.12, 'salary_range': (900000, 1200000), 'years_exp': (7, 15)},
    'Director': {'weight': 0.06, 'salary_range': (1100000, 1500000), 'years_exp': (10, 20)},
    'VP': {'weight': 0.015, 'salary_range': (1400000, 1900000), 'years_exp': (15, 25)},
    'C-Level': {'weight': 0.005, 'salary_range': (1800000, 2500000), 'years_exp': (18, 30)}
}

JOB_FAMILIES = ['Individual Contributor', 'Specialist', 'Management', 'Executive']

JOB_TITLES = {
    'Engineering': {
        'Junior': ['Junior Developer', 'Junior Engineer'],
        'Mid': ['Software Developer', 'Engineer', 'DevOps Engineer'],
        'Senior': ['Senior Developer', 'Senior Engineer', 'Tech Lead'],
        'Lead': ['Principal Engineer', 'Engineering Lead', 'Architect'],
        'Director': ['Engineering Director'],
        'VP': ['VP Engineering'],
        'C-Level': ['CTO']
    },
    'Sales': {
        'Junior': ['Sales Development Rep', 'Inside Sales Rep'],
        'Mid': ['Account Executive', 'Sales Representative'],
        'Senior': ['Senior Account Executive', 'Enterprise Sales Rep'],
        'Lead': ['Sales Lead', 'Team Lead Sales'],
        'Director': ['Sales Director', 'Regional Sales Director'],
        'VP': ['VP Sales'],
        'C-Level': ['CRO']
    },
    'Customer Support': {
        'Junior': ['Support Agent', 'Customer Service Rep'],
        'Mid': ['Support Specialist', 'Technical Support'],
        'Senior': ['Senior Support Specialist', 'Support Lead'],
        'Lead': ['Support Team Lead', 'Customer Success Manager'],
        'Director': ['Support Director'],
        'VP': ['VP Customer Success'],
        'C-Level': ['CCO']
    },
    'Operations': {
        'Junior': ['Operations Coordinator', 'Operations Assistant'],
        'Mid': ['Operations Specialist', 'Project Coordinator'],
        'Senior': ['Senior Operations Specialist', 'Project Manager'],
        'Lead': ['Operations Lead', 'Senior Project Manager'],
        'Director': ['Operations Director'],
        'VP': ['VP Operations'],
        'C-Level': ['COO']
    },
    'Finance': {
        'Junior': ['Finance Analyst', 'Accounting Assistant'],
        'Mid': ['Financial Analyst', 'Accountant'],
        'Senior': ['Senior Financial Analyst', 'Senior Accountant'],
        'Lead': ['Finance Lead', 'Controller'],
        'Director': ['Finance Director'],
        'VP': ['VP Finance'],
        'C-Level': ['CFO']
    },
    'HR': {
        'Junior': ['HR Coordinator', 'Recruitment Coordinator'],
        'Mid': ['HR Specialist', 'Recruiter', 'HR Business Partner'],
        'Senior': ['Senior HR Specialist', 'Senior Recruiter'],
        'Lead': ['HR Lead', 'Talent Acquisition Lead'],
        'Director': ['HR Director'],
        'VP': ['VP People'],
        'C-Level': ['CHRO']
    },
    'Marketing': {
        'Junior': ['Marketing Coordinator', 'Content Assistant'],
        'Mid': ['Marketing Specialist', 'Content Writer', 'Digital Marketer'],
        'Senior': ['Senior Marketing Specialist', 'Brand Manager'],
        'Lead': ['Marketing Lead', 'Product Marketing Manager'],
        'Director': ['Marketing Director'],
        'VP': ['VP Marketing'],
        'C-Level': ['CMO']
    },
    'R&D': {
        'Junior': ['Research Assistant', 'Junior Researcher'],
        'Mid': ['Researcher', 'Data Scientist'],
        'Senior': ['Senior Researcher', 'Senior Data Scientist'],
        'Lead': ['Research Lead', 'Principal Scientist'],
        'Director': ['R&D Director'],
        'VP': ['VP R&D'],
        'C-Level': ['Chief Science Officer']
    }
}

def weighted_choice(options_dict, key='weight'):
    """Make a weighted random choice from a dictionary"""
    options = list(options_dict.keys())
    weights = [options_dict[o][key] for o in options]
    return random.choices(options, weights=weights, k=1)[0]

def generate_name(country_data, gender):
    """Generate a random name based on country"""
    if gender == 'M':
        first = random.choice(country_data['first_male'])
    else:
        first = random.choice(country_data['first_female'])
    last = random.choice(country_data['last'])
    return f"{first} {last}"

def generate_employees():
    """Generate employee data"""
    employees = []

    # Track managers for org structure
    managers_by_dept_country = {}

    for i in range(NUM_EMPLOYEES):
        emp_id = f"EMP-{str(i+1).zfill(5)}"

        # Basic demographics
        country = weighted_choice(COUNTRIES)
        country_data = COUNTRIES[country]
        city = random.choice(country_data['cities'])

        gender = random.choices(['M', 'F', 'Other'], weights=[0.52, 0.46, 0.02])[0]
        name = generate_name(country_data, gender if gender != 'Other' else random.choice(['M', 'F']))

        # Department and role
        department = weighted_choice(DEPARTMENTS)
        seniority = weighted_choice(SENIORITY_LEVELS)

        # Adjust gender distribution for senior roles (reflecting current reality for storyline)
        if seniority in ['Director', 'VP', 'C-Level'] and gender == 'F':
            if random.random() < 0.3:  # 30% chance to bump down
                seniority = 'Lead' if seniority == 'Director' else 'Senior'

        job_titles = JOB_TITLES[department][seniority]
        job_title = random.choice(job_titles)

        # Job family based on seniority
        if seniority in ['C-Level', 'VP']:
            job_family = 'Executive'
        elif seniority in ['Director', 'Lead']:
            job_family = 'Management'
        elif 'Specialist' in job_title or 'Analyst' in job_title:
            job_family = 'Specialist'
        else:
            job_family = 'Individual Contributor'

        # Tenure and dates
        min_years, max_years = SENIORITY_LEVELS[seniority]['years_exp']
        tenure_years = max(0.1, np.random.normal((min_years + max_years) / 2, 1.5))
        tenure_years = min(tenure_years, (CURRENT_DATE - START_DATE).days / 365)

        hire_date = CURRENT_DATE - timedelta(days=int(tenure_years * 365))
        if hire_date < START_DATE:
            hire_date = START_DATE + timedelta(days=random.randint(0, 365))
            tenure_years = (CURRENT_DATE - hire_date).days / 365

        # Termination (some employees have left)
        is_terminated = random.random() < 0.12  # ~12% have left
        termination_date = None
        if is_terminated:
            days_employed = int(tenure_years * 365)
            termination_date = hire_date + timedelta(days=random.randint(30, max(31, days_employed)))
            if termination_date > CURRENT_DATE:
                termination_date = CURRENT_DATE - timedelta(days=random.randint(1, 180))

        # Salary
        base_min, base_max = SENIORITY_LEVELS[seniority]['salary_range']
        dept_factor = DEPARTMENTS[department]['salary_factor']
        country_factor = country_data['currency_factor']

        salary_mid = (base_min + base_max) / 2 * dept_factor * country_factor
        salary = np.random.normal(salary_mid, salary_mid * 0.1)
        salary = round(salary / 1000) * 1000  # Round to nearest 1000

        # Salary bands
        band_min = round(base_min * dept_factor * country_factor / 1000) * 1000
        band_max = round(base_max * dept_factor * country_factor / 1000) * 1000

        # Age
        age_offset = SENIORITY_LEVELS[seniority]['years_exp'][0] + 22
        age = max(22, min(65, int(np.random.normal(age_offset + 5, 5))))
        if age < 25:
            age_group = '<25'
        elif age < 35:
            age_group = '25-34'
        elif age < 45:
            age_group = '35-44'
        elif age < 55:
            age_group = '45-54'
        else:
            age_group = '55+'

        # Performance and engagement
        # Create some variance - Engineering in Germany has issues
        base_performance = 3.5
        base_engagement = 7.0

        if department == 'Engineering' and country == 'Tyskland':
            base_engagement -= 1.5  # Storyline: Engineering Germany has engagement issues
        if department == 'Customer Support':
            base_engagement -= 0.8  # Storyline: Support burnout
        if department == 'Sales' and seniority == 'Junior':
            base_performance -= 0.3  # Storyline: Sales onboarding issues

        performance_rating = max(1, min(5, int(round(np.random.normal(base_performance, 0.8)))))
        engagement_score = max(1, min(10, round(np.random.normal(base_engagement, 1.5), 1)))

        # Flight risk
        flight_risk_score = 0
        if engagement_score < 6:
            flight_risk_score += 2
        if performance_rating >= 4 and tenure_years > 3:
            # High performers stuck
            last_promo_years = random.uniform(1, tenure_years)
            if last_promo_years > 2:
                flight_risk_score += 2
        if salary < salary_mid * 0.9:
            flight_risk_score += 1
        if department == 'Engineering' and country in ['Norge', 'Sverige']:
            flight_risk_score += 1  # Hot market

        if flight_risk_score >= 3:
            flight_risk = 'High'
        elif flight_risk_score >= 1:
            flight_risk = 'Medium'
        else:
            flight_risk = 'Low'

        # Last promotion
        if tenure_years > 1:
            last_promo_days = random.randint(180, int(tenure_years * 365))
            last_promotion_date = hire_date + timedelta(days=last_promo_days)
            if last_promotion_date > CURRENT_DATE:
                last_promotion_date = None
        else:
            last_promotion_date = None

        # Internal moves
        internal_moves = 0
        if tenure_years > 2:
            internal_moves = random.choices([0, 1, 2, 3], weights=[0.6, 0.25, 0.1, 0.05])[0]

        # Training hours
        training_hours = max(0, np.random.normal(35, 20))
        if department == 'R&D':
            training_hours += 15
        if seniority in ['Junior', 'Mid']:
            training_hours += 10

        # Manager assignment
        manager_id = None
        if seniority not in ['C-Level', 'VP', 'Director']:
            key = (department, country)
            if key not in managers_by_dept_country:
                managers_by_dept_country[key] = []
            if managers_by_dept_country[key]:
                manager_id = random.choice(managers_by_dept_country[key])

        # Store potential managers
        if seniority in ['Director', 'Lead', 'VP']:
            key = (department, country)
            if key not in managers_by_dept_country:
                managers_by_dept_country[key] = []
            managers_by_dept_country[key].append(emp_id)

        employees.append({
            'employee_id': emp_id,
            'name': name,
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'termination_date': termination_date.strftime('%Y-%m-%d') if termination_date else None,
            'department': department,
            'country': country,
            'location_city': city,
            'job_family': job_family,
            'job_title': job_title,
            'seniority_level': seniority,
            'manager_id': manager_id,
            'salary': salary,
            'salary_band_min': band_min,
            'salary_band_max': band_max,
            'gender': gender,
            'age_group': age_group,
            'tenure_years': round(tenure_years, 1),
            'performance_rating': performance_rating,
            'engagement_score': engagement_score,
            'flight_risk': flight_risk,
            'last_promotion_date': last_promotion_date.strftime('%Y-%m-%d') if last_promotion_date else None,
            'internal_moves': internal_moves,
            'training_hours_ytd': round(training_hours, 1)
        })

    return pd.DataFrame(employees)

def generate_sick_leave(employees_df):
    """Generate sick leave records"""
    sick_records = []

    active_employees = employees_df[employees_df['termination_date'].isna()]

    for _, emp in active_employees.iterrows():
        # Generate monthly sick leave for 2024
        for month in range(1, 13):
            # Base sick days
            base_sick_days = 0.8

            # Department factors
            if emp['department'] == 'Customer Support':
                base_sick_days += 0.5  # Higher stress
            if emp['department'] == 'Operations':
                base_sick_days += 0.3

            # Country factors (realistic sick leave patterns)
            if emp['country'] == 'Norge':
                base_sick_days *= 1.3  # Higher sick leave culture
            if emp['country'] == 'Tyskland':
                base_sick_days *= 1.2

            # Engagement correlation
            if emp['engagement_score'] < 6:
                base_sick_days *= 1.4

            # Winter months higher
            if month in [1, 2, 11, 12]:
                base_sick_days *= 1.3

            sick_days = max(0, np.random.exponential(base_sick_days))

            if sick_days > 0:
                sick_type = 'Long-term' if sick_days > 5 else 'Short-term'
                sick_records.append({
                    'employee_id': emp['employee_id'],
                    'year': 2024,
                    'month': month,
                    'sick_days': round(sick_days, 1),
                    'sick_leave_type': sick_type
                })

    return pd.DataFrame(sick_records)

def generate_recruitment(employees_df):
    """Generate recruitment data"""
    recruitment_records = []

    # Get hired employees
    hired = employees_df[employees_df['hire_date'] >= '2022-01-01']

    for idx, (_, emp) in enumerate(hired.iterrows()):
        req_id = f"REQ-{str(idx+1).zfill(5)}"

        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')

        # Time to fill varies by role
        base_days = 35
        if emp['seniority_level'] in ['Senior', 'Lead']:
            base_days = 50
        if emp['seniority_level'] in ['Director', 'VP', 'C-Level']:
            base_days = 75
        if emp['department'] == 'Engineering':
            base_days += 15  # Harder to fill
        if emp['country'] == 'Finland':
            base_days += 10  # Smaller talent pool

        days_to_fill = max(14, int(np.random.normal(base_days, 15)))

        open_date = hire_date - timedelta(days=days_to_fill)

        # Candidates
        candidates_screened = random.randint(20, 150)
        candidates_interviewed = random.randint(3, min(15, candidates_screened))

        # Source
        if emp['internal_moves'] > 0:
            source = 'Internal'
        else:
            source = random.choices(
                ['LinkedIn', 'Referral', 'Agency', 'Job Board', 'Internal'],
                weights=[0.35, 0.25, 0.15, 0.20, 0.05]
            )[0]

        recruitment_records.append({
            'requisition_id': req_id,
            'department': emp['department'],
            'country': emp['country'],
            'job_family': emp['job_family'],
            'seniority_level': emp['seniority_level'],
            'open_date': open_date.strftime('%Y-%m-%d'),
            'close_date': hire_date.strftime('%Y-%m-%d'),
            'days_to_fill': days_to_fill,
            'candidates_screened': candidates_screened,
            'candidates_interviewed': candidates_interviewed,
            'hired_employee_id': emp['employee_id'],
            'source': source
        })

    return pd.DataFrame(recruitment_records)

def generate_terminations(employees_df):
    """Generate termination details"""
    termination_records = []

    terminated = employees_df[employees_df['termination_date'].notna()]

    for _, emp in terminated.iterrows():
        # Reason based on performance and engagement
        if emp['performance_rating'] <= 2:
            reason = random.choices(['Involuntary', 'Voluntary'], weights=[0.7, 0.3])[0]
        elif emp['engagement_score'] < 5:
            reason = 'Voluntary'
        elif emp['tenure_years'] > 25 and emp['age_group'] == '55+':
            reason = 'Retirement'
        else:
            reason = random.choices(['Voluntary', 'Involuntary', 'Retirement'],
                                   weights=[0.75, 0.20, 0.05])[0]

        # Exit survey (if voluntary)
        exit_score = None
        if reason == 'Voluntary':
            exit_score = round(np.random.normal(5.5, 2), 1)
            exit_score = max(1, min(10, exit_score))

        # Rehire eligible
        rehire_eligible = reason != 'Involuntary' and (exit_score is None or exit_score > 4)

        # Replacement cost (1.5-2x salary for most, more for senior)
        multiplier = 1.5
        if emp['seniority_level'] in ['Senior', 'Lead']:
            multiplier = 2.0
        if emp['seniority_level'] in ['Director', 'VP', 'C-Level']:
            multiplier = 2.5

        replacement_cost = emp['salary'] * multiplier

        termination_records.append({
            'employee_id': emp['employee_id'],
            'termination_date': emp['termination_date'],
            'termination_reason': reason,
            'exit_survey_score': exit_score,
            'rehire_eligible': rehire_eligible,
            'last_salary': emp['salary'],
            'tenure_at_exit': emp['tenure_years'],
            'replacement_cost': round(replacement_cost, 0)
        })

    return pd.DataFrame(termination_records)

if __name__ == "__main__":
    print("Generating synthetic HR data...")

    # Generate all datasets
    print("1. Generating employees...")
    employees_df = generate_employees()

    print("2. Generating sick leave records...")
    sick_leave_df = generate_sick_leave(employees_df)

    print("3. Generating recruitment data...")
    recruitment_df = generate_recruitment(employees_df)

    print("4. Generating termination records...")
    terminations_df = generate_terminations(employees_df)

    # Save to CSV
    output_dir = '/sessions/optimistic-nifty-knuth/mnt/Claude Coding/hr-analytics-dashboard/data'
    import os
    os.makedirs(output_dir, exist_ok=True)

    employees_df.to_csv(f'{output_dir}/employees.csv', index=False)
    sick_leave_df.to_csv(f'{output_dir}/sick_leave.csv', index=False)
    recruitment_df.to_csv(f'{output_dir}/recruitment.csv', index=False)
    terminations_df.to_csv(f'{output_dir}/terminations.csv', index=False)

    print(f"\nData generation complete!")
    print(f"- Employees: {len(employees_df)} records")
    print(f"- Sick leave: {len(sick_leave_df)} records")
    print(f"- Recruitment: {len(recruitment_df)} records")
    print(f"- Terminations: {len(terminations_df)} records")

    # Summary stats
    active = employees_df[employees_df['termination_date'].isna()]
    print(f"\nActive employees: {len(active)}")
    print(f"Countries: {active['country'].value_counts().to_dict()}")
    print(f"Departments: {active['department'].value_counts().to_dict()}")
