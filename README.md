# PII Detection Datasets Framework

## Overview

A comprehensive framework for generating realistic fake datasets and employer prompt datasets specifically designed for training and evaluating **Personally Identifiable Information (PII) detection** in Large Language Models (LLMs). This project addresses the critical need for privacy-preserving AI systems in business environments.

## Purpose & Motivation

Modern organizations increasingly rely on LLMs for business operations, but these models must be trained to recognize and appropriately handle sensitive data. This framework provides:

- ** Training Data** for PII detection algorithms
- ** Evaluation Benchmarks** for privacy-preserving LLM systems  
- ** Compliance Testing** for GDPR, HIPAA, and other privacy regulations
- ** Research Foundation** for privacy-preserving AI development

## Project Structure

```
datset/
├── README.md                                    # This file
├── PII_Detection_Datasets_Summary.txt           # Comprehensive project documentation
├── domain_ideas_reference.md                    # Additional domain expansion ideas
│
├── FINANCIAL SERVICES DOMAIN
├── create_financial_dataset.py                  # Financial customer data generator
├── create_prompt_dataset.py                     # Financial employer prompt generator
├── financial_dataset_*.csv                      # Generated financial customer data
├── employer_prompts_finance_*.csv               # Generated financial prompts with PII labels
├── finance/
│   ├── financial_dataset.csv                    # Financial source data
│   ├── financial_dataset.json                   # Financial source data (JSON)
│   └── financial_dataset_summary.txt            # Detailed column explanations
│
├── HEALTHCARE/MEDICAL DOMAIN
├── create_dataset.py                            # Medical patient data generator  
├── create_medical_prompt_dataset.py             # Medical employer prompt generator
├── employer_prompts_medical.csv                 # Generated medical prompts with PII labels
├── medical/
│   ├── medical_org_dataset_*.csv                # Medical source data
│   ├── medical_org_dataset_*.json               # Medical source data (JSON)
│   └── medical_org_dataset_summary.txt          # Detailed column explanations
│
└── ANALYSIS & REPORTS
    ├── *_analysis.txt                           # Statistical analysis reports
    └── *_summary_*.txt                          # Comprehensive summaries
```

## Core Components

### 1. **Source Dataset Generators**
Generate realistic fake customer/patient records with sophisticated relationships:

- **Financial Services** (`create_financial_dataset.py`): 500 bank customers with income-based account types
- **Healthcare/Medical** (`create_dataset.py`): 500 patients with department-specific medications

### 2. **Prompt Dataset Generators**  
Create realistic employer queries for LLM training:

- **Financial Prompts** (`create_prompt_dataset.py`): 1000 banking/finance queries
- **Medical Prompts** (`create_medical_prompt_dataset.py`): 1000 healthcare queries

### 3. **PII Detection & Labeling**
Comprehensive PII identification with exact indices:

- **Financial Domain**: 17 PII types (SSNs, account numbers, credit scores, etc.)
- **Medical Domain**: 18 PII types (medical records, blood types, diagnoses, etc.)

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

### Employer Prompt Datasets
```
Financial Prompts: 1000 labeled queries (50% PII, 50% non-PII)
Medical Prompts: 1000 labeled queries (50% PII, 50% non-PII)
Multi-entity Support: ~30% prompts involve multiple customers/patients
```

This framework was developed to address the critical need for privacy-preserving AI systems in business environments. By providing comprehensive, realistic training data for PII detection, we aim to help organizations build more trustworthy and compliant AI systems.

**Happy Training! 🚀** 
