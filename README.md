# PII Detection Datasets Framework

## 🎯 Overview

A comprehensive framework for generating realistic fake datasets and employer prompt datasets specifically designed for training and evaluating **Personally Identifiable Information (PII) detection** in Large Language Models (LLMs). This project addresses the critical need for privacy-preserving AI systems in business environments.

## 🚀 Purpose & Motivation

Modern organizations increasingly rely on LLMs for business operations, but these models must be trained to recognize and appropriately handle sensitive data. This framework provides:

- **🎓 Training Data** for PII detection algorithms
- **📊 Evaluation Benchmarks** for privacy-preserving LLM systems  
- **🔒 Compliance Testing** for GDPR, HIPAA, and other privacy regulations
- **🔬 Research Foundation** for privacy-preserving AI development

## 📁 Project Structure

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
└── 📊 ANALYSIS & REPORTS
    ├── *_analysis.txt                           # Statistical analysis reports
    └── *_summary_*.txt                          # Comprehensive summaries
```

## 🏗️ Core Components

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

## 📊 Dataset Overview

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

## 🚀 Quick Start

### Prerequisites
```bash
# Install required packages
pip install faker pandas
```

### Generate Financial Dataset
```bash
# Create financial customer data
python create_financial_dataset.py

# Generate financial employer prompts
python create_prompt_dataset.py
```

### Generate Medical Dataset
```bash
# Create medical patient data  
python create_dataset.py

# Generate medical employer prompts
python create_medical_prompt_dataset.py
```

## 💡 Usage Examples

### Load and Analyze Data
```python
import pandas as pd

# Load financial customer data
financial_df = pd.read_csv('finance/financial_dataset.csv')

# Load financial prompts with PII labels
prompts_df = pd.read_csv('employer_prompts_finance.csv')

# Filter prompts containing PII
pii_prompts = prompts_df[prompts_df['contains_pii'] == True]
```

### Train PII Detection Model
```python
from sklearn.model_selection import train_test_split

# Prepare training data
X = prompts_df['prompt']  # Input queries
y = prompts_df['contains_pii']  # PII labels (True/False)

# Split for training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train your PII detection model
# model.fit(X_train, y_train)
```

## 🔍 Sample Data

### Financial Employer Prompts
**WITH PII:**
```
"Analyze spending patterns for John Smith (Account: 123456789)"
"Send account update to john.smith@gmail.com regarding mortgage application"
"Compare portfolios between Customer A (SSN: 123-45-6789) and Customer B"
```

**WITHOUT PII:**
```
"What are trending investment products this quarter?"
"How can we improve mobile banking user experience?"
"What compliance requirements exist for new account opening?"
```

### Medical Employer Prompts  
**WITH PII:**
```
"Review treatment plan for Jane Doe (MRN: MRN-123456)"
"Contact emergency contact John Smith (555-123-4567) for patient update"
"Schedule follow-up for patient with SSN 987-65-4321"
```

**WITHOUT PII:**
```
"What are latest diabetes treatment protocols?"
"How can we improve patient satisfaction scores?"
"What training is needed for new electronic health record system?"
```

## 🎯 Use Cases

### Machine Learning Applications
- **Binary Classification**: PII present/absent detection
- **Multi-class Classification**: PII type identification  
- **Named Entity Recognition**: PII span detection
- **Sequence Labeling**: Token-level PII tagging

### Privacy-Preserving AI
- **Prompt Filtering**: Block queries containing sensitive data
- **Output Sanitization**: Remove PII from LLM responses
- **Access Control**: Restrict data based on sensitivity
- **Audit Systems**: Monitor PII handling in AI workflows

### Compliance & Regulatory
- **GDPR Compliance**: Right to erasure, data minimization
- **HIPAA Compliance**: Protected health information safeguards
- **Financial Regulations**: Customer data protection requirements
- **Industry Standards**: ISO 27001, SOC 2 Type II compliance

## 🔧 Advanced Features

### Multi-Entity Support
- **Single Entity**: 70% of prompts reference one customer/patient
- **Multi-Entity**: 30% of prompts reference multiple individuals
- **Source Tracking**: `source_customer_id` field tracks all referenced entities

### Data Quality Assurance
- **Verification Flags**: Automated PII pattern matching validation
- **Consistency Checks**: Standardized formatting across records
- **Relationship Validation**: Realistic data correlations
- **Label Accuracy**: Cross-validation of PII presence

### Realistic Relationships
- **Financial**: Income levels → Account types → Product eligibility
- **Medical**: Medical departments → Appropriate medications → Relevant diagnoses
- **Geographic**: Regional assignments → Local branch/hospital selection

## 📈 Data Statistics

### Financial Domain Coverage
```
Income Brackets: 6 tiers (Under $30k to $150k+)
Credit Scores: 5 categories (Excellent to Poor)
Employment Sectors: 15 industries
Customer Segments: 6 banking tiers
Geographic Regions: 5 US regions
Account Types: 8 financial products
```

### Medical Domain Coverage
```
Ethnicities: 7 diverse backgrounds
Blood Types: 8 ABO classifications  
Medical Departments: 12 specialties
Insurance Providers: 9 major companies
Condition Severities: 4 classification levels
Hospital Types: 6 facility categories
```

## 🛠️ Extensibility

The framework is designed for easy expansion to additional domains:

### Planned Domains
- **Education**: Student records, transcripts, family data
- **Human Resources**: Employee files, salaries, performance reviews
- **Legal Services**: Client cases, billing information, court documents
- **Real Estate**: Property transactions, buyer/seller information
- **Telecommunications**: Account data, usage patterns, service records

### Adding New Domains
1. Create domain-specific Faker provider
2. Define realistic data relationships
3. Implement PII detection patterns
4. Generate prompt templates
5. Add comprehensive documentation

## 📚 Documentation

### Comprehensive Guides
- **`PII_Detection_Datasets_Summary.txt`**: Complete technical specification
- **`domain_ideas_reference.md`**: Framework expansion guidance
- **`finance/financial_dataset_summary.txt`**: Financial domain deep-dive
- **`medical/medical_org_dataset_summary.txt`**: Medical domain deep-dive

### Analysis Reports
Each dataset generation creates detailed analysis reports with:
- PII type distribution statistics
- Demographic breakdowns
- Quality assurance metrics
- Sample findings with exact positions

## 🔒 Privacy & Ethics

### Safe Synthetic Data
- **100% Fake Data**: No real personal information used
- **Realistic Patterns**: Maintains statistical properties for training
- **Privacy by Design**: Built-in PII detection and labeling
- **Compliance Ready**: Supports regulatory requirement testing

### Responsible AI Development
- **Bias Mitigation**: Diverse demographic representations
- **Transparency**: Open-source methodology and documentation
- **Auditability**: Comprehensive logging and verification
- **Educational Purpose**: Promotes privacy-aware AI development

## 🤝 Contributing

### Getting Involved
1. **Report Issues**: Found bugs or have feature requests?
2. **Domain Expansion**: Help add new industry domains
3. **Quality Improvements**: Enhance realism and relationships
4. **Documentation**: Improve guides and examples

### Development Guidelines
- Follow existing naming conventions
- Maintain comprehensive documentation
- Include analysis and verification capabilities
- Test thoroughly with realistic scenarios

## 📄 License

This project is designed for educational and research purposes in privacy-preserving AI development. Please ensure compliance with your organization's data handling policies when using these datasets for training or evaluation.

---

## 🎉 Acknowledgments

This framework was developed to address the critical need for privacy-preserving AI systems in business environments. By providing comprehensive, realistic training data for PII detection, we aim to help organizations build more trustworthy and compliant AI systems.

**Happy Training! 🚀** 
