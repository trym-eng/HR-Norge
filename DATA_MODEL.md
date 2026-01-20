# HR Analytics Dashboard - Datamodell og KPI-er

## Datamodell

### Hovedtabell: `employees.csv`
| Felt | Type | Beskrivelse |
|------|------|-------------|
| employee_id | string | Unik ID (EMP-XXXXX) |
| name | string | Fullt navn (syntetisk) |
| hire_date | date | Ansettelsesdato |
| termination_date | date | Sluttdato (null hvis aktiv) |
| department | string | Avdeling (Sales, Engineering, HR, Finance, Operations, Marketing, R&D, Customer Support) |
| country | string | Land (Norge, Sverige, Danmark, Finland, Tyskland) |
| location_city | string | By |
| job_family | string | Rollefamilie (Management, Individual Contributor, Specialist, Executive) |
| job_title | string | Stillingstittel |
| seniority_level | string | Junior, Mid, Senior, Lead, Director, VP, C-Level |
| manager_id | string | Leder-ID |
| salary | float | Årslønn (lokal valuta) |
| salary_band_min | float | Minimum i lønnsband |
| salary_band_max | float | Maksimum i lønnsband |
| gender | string | M/F/Other (for aggregert diversity) |
| age_group | string | <25, 25-34, 35-44, 45-54, 55+ |
| tenure_years | float | Ansiennitet |
| performance_rating | int | 1-5 skala |
| engagement_score | float | 1-10 skala |
| flight_risk | string | Low, Medium, High |
| last_promotion_date | date | Siste forfremmelse |
| internal_moves | int | Antall interne bytter |
| training_hours_ytd | float | Opplæringstimer i år |

### Tabell 2: `sick_leave.csv`
| Felt | Type | Beskrivelse |
|------|------|-------------|
| employee_id | string | Koblingsnøkkel |
| year | int | År |
| month | int | Måned |
| sick_days | float | Sykedager |
| sick_leave_type | string | Short-term, Long-term |

### Tabell 3: `recruitment.csv`
| Felt | Type | Beskrivelse |
|------|------|-------------|
| requisition_id | string | Rekrutteringsprosjekt-ID |
| department | string | Avdeling |
| country | string | Land |
| job_family | string | Rollefamilie |
| seniority_level | string | Senioritetsnivå |
| open_date | date | Dato utlysning åpnet |
| close_date | date | Dato stilling fylt |
| days_to_fill | int | Dager brukt |
| candidates_screened | int | Antall screenet |
| candidates_interviewed | int | Antall intervjuet |
| hired_employee_id | string | Ansatt som fikk jobben |
| source | string | Kilde (Internal, LinkedIn, Referral, Agency, Job Board) |

### Tabell 4: `terminations.csv`
| Felt | Type | Beskrivelse |
|------|------|-------------|
| employee_id | string | Ansatt-ID |
| termination_date | date | Sluttdato |
| termination_reason | string | Voluntary, Involuntary, Retirement |
| exit_survey_score | float | 1-10 |
| rehire_eligible | bool | Kan reansettes |
| last_salary | float | Siste lønn |
| tenure_at_exit | float | Ansiennitet ved avgang |
| replacement_cost | float | Estimert erstatningskostnad |

---

## KPI-er som beregnes

### Workforce KPIs
| KPI | Formel | Mål |
|-----|--------|-----|
| **Headcount** | Antall aktive ansatte | Organisasjonsstørrelse |
| **Headcount Growth** | (HC nå - HC forrige periode) / HC forrige periode | Vekstrate |
| **Average Tenure** | Sum(tenure) / headcount | Stabilitet |
| **Span of Control** | Antall direct reports per leder | Lederkapasitet |

### Turnover & Retention KPIs
| KPI | Formel | Benchmark |
|-----|--------|-----------|
| **Annual Turnover Rate** | (Avganger / Gjennomsnittlig HC) × 100 | <15% |
| **Voluntary Turnover** | (Frivillige avganger / HC) × 100 | <10% |
| **Regretted Turnover** | Høytytende som slutter | <5% |
| **90-day Turnover** | Sluttet innen 90 dager | <5% |
| **Cost of Attrition** | Sum(replacement_cost) | Minimere |

### Recruitment KPIs
| KPI | Formel | Benchmark |
|-----|--------|-----------|
| **Time to Hire** | Gjennomsnitt days_to_fill | <45 dager |
| **Cost per Hire** | Total rekrutteringskost / ansettelser | Bransjeavhengig |
| **Quality of Hire** | Performance etter 1 år | >3.5 rating |
| **Source Effectiveness** | % ansettelser per kilde | Optimalisere mix |

### Absence KPIs
| KPI | Formel | Benchmark |
|-----|--------|-----------|
| **Sickness Absence Rate** | (Sykedager / Arbeidsdager) × 100 | <4% |
| **Long-term Sick Leave %** | Langvarig / Total sykefravær | <30% |
| **Bradford Factor** | S² × D (S=perioder, D=dager) | <250 |

### Mobility & Development KPIs
| KPI | Formel | Benchmark |
|-----|--------|-----------|
| **Internal Mobility Rate** | Interne bytter / HC | >10% |
| **Promotion Rate** | Forfremmelser / HC | 8-12% |
| **Training Hours per Employee** | Total timer / HC | >40 timer |

### Diversity KPIs (aggregert)
| KPI | Formel | Mål |
|-----|--------|-----|
| **Gender Balance** | % per kjønn per nivå | 40-60% |
| **Age Distribution** | % per aldersgruppe | Balansert |
| **Management Diversity** | % representasjon i ledelse | Reflektere arbeidsstyrke |

### Compensation KPIs
| KPI | Formel | Benchmark |
|-----|--------|-----------|
| **Compa-Ratio** | Faktisk lønn / Midtpunkt i band | 0.9-1.1 |
| **Pay Equity Gap** | Lønnsforskjell mellom grupper | <3% |
| **Salary Band Penetration** | Posisjon i lønnsband | Normaldistribuert |

---

## Red Flags (automatiske varsler)

1. **Høy turnover i segment** - >20% årlig turnover
2. **Lang time-to-hire** - >60 dager
3. **Høyt sykefravær** - >6% i avdeling
4. **Lønnsavvik** - Compa-ratio <0.85 eller >1.15
5. **Lav engagement** - Score <6 i gruppe
6. **Flight risk clustering** - >25% høy risiko i team
7. **Span of control** - >12 direct reports
8. **Diversity gap** - <30% underrepresentert gruppe i ledelse
9. **Stagnering** - >3 år siden forfremmelse med høy ytelse
10. **Onboarding-turnover** - >10% slutter innen 90 dager
