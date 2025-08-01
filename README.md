# PII Detection Datasets Framework

## Overview

A comprehensive framework for generating realistic fake datasets and employer prompt datasets specifically designed for training and evaluating **Personally Identifiable Information (PII) detection** in Large Language Models (LLMs). This project addresses the critical need for privacy-preserving AI systems in business environments.

## Purpose & Motivation

Modern organizations increasingly rely on LLMs for business operations, but these models must be trained to recognize and appropriately handle sensitive data. This framework provides:

- **Training Data** for PII detection algorithms
- **Evaluation Benchmarks** for privacy-preserving LLM systems  
- **Compliance Testing** for GDPR, HIPAA, and other privacy regulations
- **Research Foundation** for privacy-preserving AI development

## Project Structure

```
datset/
├── README.md                                    # This file
├── PII_Detection_Datasets_Summary.txt           # Comprehensive project documentation
├── domain_ideas_reference.md                    # Additional domain expansion ideas
│
├── 💰 FINANCIAL SERVICES DOMAIN
├── create_financial_dataset.py                  # Financial customer data generator
├── create_prompt_dataset.py                     # Financial employer prompt generator
├── financial_dataset_*.csv                      # Generated financial customer data
├── employer_prompts_finance_*.csv               # Generated financial prompts with PII labels
├── finance/
│   ├── financial_dataset.csv                    # Financial source data
│   ├── financial_dataset.json                   # Financial source data (JSON)
│   └── financial_dataset_summary.txt            # Detailed column explanations
│
├── 🏥 HEALTHCARE/MEDICAL DOMAIN
├── create_dataset.py                            # Medical patient data generator  
├── create_medical_prompt_dataset.py             # Medical employer prompt generator
├── employer_prompts_medical.csv                 # Generated medical prompts with PII labels
├── medical/
│   ├── medical_org_dataset_*.csv                # Medical source data
│   ├── medical_org_dataset_*.json               # Medical source data (JSON)
│   └── medical_org_dataset_summary.txt          # Detailed column explanations
│
├── ⚖️ LEGAL SERVICES DOMAIN
├── create_legal_dataset.py                      # Legal case data generator
├── create_legal_prompt_dataset.py               # Legal employer prompt generator
├── employer_prompts_legal.csv                   # Generated legal prompts with PII labels
├── legal/
│   ├── legal_dataset_*.csv                      # Legal source data
│   ├── legal_dataset_*.json                     # Legal source data (JSON)
│   └── legal_dataset_summary_*.txt              # Detailed column explanations
│
├── 🎓 EDUCATION SERVICES DOMAIN
├── create_education_dataset.py                  # Student record data generator
├── create_education_prompt_dataset.py           # Education employer prompt generator
├── employer_prompts_education.csv               # Generated education prompts with PII labels
├── education/
│   ├── education_dataset_*.csv                  # Education source data
│   ├── education_dataset_*.json                 # Education source data (JSON)
│   └── education_dataset_summary_*.txt          # Detailed column explanations
│
└── 📊 ANALYSIS & REPORTS
    ├── *_analysis.txt                           # Statistical analysis reports
    └── *_summary_*.txt                          # Comprehensive summaries
```

## Core Components

### 1. **Source Dataset Generators**
Generate realistic fake customer/patient/case/student records with sophisticated relationships:

- **Financial Services** (`create_financial_dataset.py`): 500 bank customers with income-based account types
- **Healthcare/Medical** (`create_dataset.py`): 500 patients with department-specific medications
- **Legal Services** (`create_legal_dataset.py`): 500 legal cases with practice area-based case types
- **Education Services** (`create_education_dataset.py`): 500 student records with grade level-based courses

### 2. **Prompt Dataset Generators**  
Create realistic employer queries for LLM training:

- **Financial Prompts** (`create_prompt_dataset.py`): 1000 banking/finance queries
- **Medical Prompts** (`create_medical_prompt_dataset.py`): 1000 healthcare queries
- **Legal Prompts** (`create_legal_prompt_dataset.py`): 1000 legal professional queries
- **Education Prompts** (`create_education_prompt_dataset.py`): 1000 educational professional queries

### 3. **PII Detection & Labeling**
Comprehensive PII identification with exact indices:

- **Financial Domain**: 17 PII types (SSNs, account numbers, credit scores, etc.)
- **Medical Domain**: 18 PII types (medical records, blood types, diagnoses, etc.)
- **Legal Domain**: 21 PII types (case numbers, bar numbers, court jurisdictions, etc.)
- **Education Domain**: 22 PII types (student IDs, GPAs, parent contacts, etc.)


## Dataset Overview

### Financial Services Dataset
```
Records: 500 customers
Columns: 35 attributes per customer
PII Types: 17 financial-specific types
Relationships: Income ↔ Account types, Credit ↔ Products
```

**Key Features:**
- Realistic income-based account progression
- Credit score product eligibility matching  
- Regional branch assignments
- Name-based email generation

### Healthcare/Medical Dataset
```
Records: 500 patients  
Columns: 35 attributes per patient
PII Types: 18 healthcare-specific types
Relationships: Department ↔ Medications, Demographics ↔ Conditions
```

**Key Features:**
- Department-specific medication prescribing
- Realistic medical condition distributions
- Emergency contact relationships
- HIPAA-relevant PII coverage

### Legal Services Dataset
```
Records: 500 legal cases  
Columns: 42 attributes per case
PII Types: 21 legal-specific types
Relationships: Practice area ↔ Case types, Complexity ↔ Billing rates
```

**Key Features:**
- Practice area-based case type relationships
- Case complexity billing rate matching
- Attorney specialization alignment
- Court jurisdiction assignments
- Realistic legal document patterns
- Bar number and credential tracking

### Education Services Dataset
```
Records: 500 student records  
Columns: 45 attributes per student
PII Types: 22 education-specific types
Relationships: Grade level ↔ Courses, Performance ↔ Interventions
```

**Key Features:**
- Grade level-based course relationships
- Performance level intervention matching
- Student type service alignment
- Institution level course offerings
- Realistic academic progression patterns
- Parent/guardian contact management
- Educational staff role assignments

### Employer Prompt Datasets
```
Financial Prompts: 1000 labeled queries (50% PII, 50% non-PII)
Medical Prompts: 1000 labeled queries (50% PII, 50% non-PII)
Legal Prompts: 1000 labeled queries (50% PII, 50% non-PII)
Education Prompts: 1000 labeled queries (50% PII, 50% non-PII)
Multi-entity Support: ~30% prompts involve multiple customers/patients/cases/students
```
