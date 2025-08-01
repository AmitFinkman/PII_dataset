import json
import re
from faker import Faker
from faker.providers import BaseProvider
import pandas as pd
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Custom provider for legal services data
class LegalProvider(BaseProvider):
    """Custom Faker provider for legal services data"""
    
    def __init__(self, generator):
        super().__init__(generator)
        
        # Practice area specific case types
        self.practice_area_cases = {
            'Corporate Law': ['Merger & Acquisition', 'Corporate Governance', 'Securities', 'Contract Dispute', 'Compliance Review', 'IPO Preparation'],
            'Criminal Defense': ['Felony Defense', 'Misdemeanor Defense', 'DUI/DWI', 'White Collar Crime', 'Appeals', 'Plea Negotiation'],
            'Personal Injury': ['Auto Accident', 'Medical Malpractice', 'Slip and Fall', 'Product Liability', 'Workers Compensation', 'Wrongful Death'],
            'Family Law': ['Divorce', 'Child Custody', 'Adoption', 'Prenuptial Agreement', 'Domestic Violence', 'Child Support'],
            'Real Estate': ['Property Purchase', 'Zoning Dispute', 'Title Issues', 'Landlord-Tenant', 'Construction Contract', 'Property Development'],
            'Employment Law': ['Wrongful Termination', 'Discrimination', 'Wage Dispute', 'Contract Negotiation', 'Harassment', 'Union Relations'],
            'Intellectual Property': ['Patent Application', 'Trademark Registration', 'Copyright Infringement', 'Trade Secret', 'Licensing Agreement', 'IP Litigation'],
            'Immigration': ['Visa Application', 'Green Card', 'Asylum Case', 'Deportation Defense', 'Citizenship', 'Family Reunification'],
            'Bankruptcy': ['Chapter 7 Filing', 'Chapter 11 Reorganization', 'Chapter 13 Payment Plan', 'Debt Negotiation', 'Asset Protection', 'Creditor Rights'],
            'Tax Law': ['Tax Audit Defense', 'Tax Planning', 'IRS Dispute', 'Estate Tax', 'Business Tax', 'Tax Court Appeal'],
            'Estate Planning': ['Will Preparation', 'Trust Formation', 'Probate', 'Estate Administration', 'Power of Attorney', 'Healthcare Directive'],
            'Environmental Law': ['EPA Compliance', 'Environmental Impact', 'Pollution Cleanup', 'Regulatory Violation', 'Land Use', 'Toxic Tort']
        }
        
        # Client type to legal service relationships
        self.client_service_mapping = {
            'Individual': ['Personal Injury', 'Family Law', 'Criminal Defense', 'Immigration', 'Bankruptcy', 'Estate Planning'],
            'Small Business': ['Corporate Law', 'Employment Law', 'Real Estate', 'Tax Law', 'Intellectual Property', 'Contract Dispute'],
            'Corporation': ['Corporate Law', 'Employment Law', 'Intellectual Property', 'Tax Law', 'Environmental Law', 'Securities'],
            'Government Entity': ['Administrative Law', 'Public Policy', 'Regulatory Compliance', 'Municipal Law', 'Constitutional Law'],
            'Non-Profit': ['Corporate Governance', 'Tax Law', 'Employment Law', 'Regulatory Compliance', 'Grant Law']
        }
        
        # Case complexity to billing structure
        self.complexity_billing = {
            'Simple': {'hourly_rate_range': (150, 250), 'estimated_hours': (5, 20), 'flat_fee_option': True},
            'Moderate': {'hourly_rate_range': (250, 400), 'estimated_hours': (20, 100), 'flat_fee_option': True},
            'Complex': {'hourly_rate_range': (400, 650), 'estimated_hours': (100, 500), 'flat_fee_option': False},
            'Highly Complex': {'hourly_rate_range': (650, 1000), 'estimated_hours': (500, 2000), 'flat_fee_option': False}
        }
        
        # Attorney specializations
        self.attorney_specializations = [
            'Corporate Law', 'Criminal Defense', 'Personal Injury', 'Family Law', 'Real Estate',
            'Employment Law', 'Intellectual Property', 'Immigration', 'Bankruptcy', 'Tax Law',
            'Estate Planning', 'Environmental Law', 'Securities Law', 'Healthcare Law', 'Aviation Law'
        ]
        
        # Court jurisdictions by region
        self.court_jurisdictions = {
            'Federal': ['U.S. District Court SDNY', 'U.S. District Court NDCA', 'U.S. District Court DDC', 'U.S. Court of Appeals 9th Circuit'],
            'State': ['New York Supreme Court', 'California Superior Court', 'Texas District Court', 'Florida Circuit Court'],
            'Local': ['Manhattan Family Court', 'Los Angeles Municipal Court', 'Cook County Circuit Court', 'Wayne County Probate Court']
        }
        
        # Law firm types and structures
        self.firm_types = [
            'Solo Practice', 'Small Firm (2-10)', 'Mid-Size Firm (11-50)', 'Large Firm (51-200)', 
            'Big Law (200+)', 'Boutique Firm', 'Government Legal Office', 'Corporate Legal Department'
        ]
        
        # Legal document types by practice area
        self.legal_documents = {
            'Corporate Law': ['Articles of Incorporation', 'Merger Agreement', 'Stock Purchase Agreement', 'Board Resolution'],
            'Criminal Defense': ['Motion to Dismiss', 'Plea Agreement', 'Sentencing Memorandum', 'Appeal Brief'],
            'Personal Injury': ['Complaint', 'Settlement Agreement', 'Medical Records Release', 'Expert Witness Report'],
            'Family Law': ['Divorce Petition', 'Custody Agreement', 'Prenuptial Agreement', 'Support Order'],
            'Real Estate': ['Purchase Agreement', 'Deed', 'Title Report', 'Lease Agreement'],
            'Employment Law': ['Employment Contract', 'Severance Agreement', 'Non-Compete Agreement', 'EEOC Complaint']
        }
        
        # Case status options
        self.case_statuses = [
            'Active', 'Pending Discovery', 'In Mediation', 'Settlement Negotiations', 
            'Trial Preparation', 'On Appeal', 'Closed - Settled', 'Closed - Dismissed', 'Closed - Judgment'
        ]
        
        # Legal fee structures
        self.fee_structures = [
            'Hourly', 'Flat Fee', 'Contingency', 'Retainer + Hourly', 'Success Fee', 'Pro Bono'
        ]
        
        # Professional credentials
        self.credentials = [
            'JD', 'LLM', 'MBA', 'CPA', 'Certified Mediator', 'Board Certified Specialist'
        ]
        
        # Law schools (for attorney education)
        self.law_schools = [
            'Harvard Law School', 'Yale Law School', 'Stanford Law School', 'Columbia Law School',
            'NYU Law School', 'Georgetown Law', 'Northwestern Law', 'UCLA Law School',
            'University of Michigan Law', 'Boston University Law', 'George Washington Law'
        ]
        
        # Common email domains for legal professionals
        self.legal_email_domains = ['lawfirm.com', 'legal.com', 'attorney.com', 'counsel.com', 'partners.com']
        self.client_email_domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'icloud.com', 'company.com']
        
        # Demographics
        self.practice_areas = list(self.practice_area_cases.keys())
        self.client_types = list(self.client_service_mapping.keys())
        self.complexities = list(self.complexity_billing.keys())
        self.jurisdiction_types = list(self.court_jurisdictions.keys())
    
    def case_number(self):
        """Generate realistic case number"""
        year = random.randint(2020, 2024)
        sequence = random.randint(1000, 9999)
        return f"CV-{year}-{sequence}"
    
    def docket_number(self):
        """Generate court docket number"""
        return f"DC-{random.randint(100000, 999999)}"
    
    def bar_number(self):
        """Generate attorney bar number"""
        state_code = random.choice(['NY', 'CA', 'TX', 'FL', 'IL'])
        number = random.randint(100000, 999999)
        return f"{state_code}-{number}"
    
    def practice_area(self):
        """Generate practice area"""
        return self.random_element(self.practice_areas)
    
    def client_type(self):
        """Generate client type"""
        return self.random_element(self.client_types)
    
    def case_complexity(self):
        """Generate case complexity"""
        return self.random_element(self.complexities)
    
    def jurisdiction_type(self):
        """Generate jurisdiction type"""
        return self.random_element(self.jurisdiction_types)
    
    def court_jurisdiction(self, jurisdiction_type):
        """Generate court jurisdiction for type"""
        if jurisdiction_type in self.court_jurisdictions:
            return self.random_element(self.court_jurisdictions[jurisdiction_type])
        return self.random_element(self.court_jurisdictions['State'])
    
    def case_types_for_practice_area(self, practice_area):
        """Generate case types based on practice area"""
        if practice_area in self.practice_area_cases:
            available_cases = self.practice_area_cases[practice_area]
            num_cases = self.random_int(1, min(3, len(available_cases)))
            return self.random_elements(available_cases, length=num_cases, unique=True)
        return ['General Legal Matter']
    
    def billing_rate_for_complexity(self, complexity):
        """Generate billing rate based on complexity"""
        if complexity in self.complexity_billing:
            rate_range = self.complexity_billing[complexity]['hourly_rate_range']
            return random.randint(rate_range[0], rate_range[1])
        return random.randint(200, 400)
    
    def estimated_hours_for_complexity(self, complexity):
        """Generate estimated hours based on complexity"""
        if complexity in self.complexity_billing:
            hour_range = self.complexity_billing[complexity]['estimated_hours']
            return random.randint(hour_range[0], hour_range[1])
        return random.randint(10, 50)
    
    def legal_document_for_practice_area(self, practice_area):
        """Generate legal document based on practice area"""
        if practice_area in self.legal_documents:
            return self.random_element(self.legal_documents[practice_area])
        return 'Legal Document'
    
    def attorney_specialization(self):
        """Generate attorney specialization"""
        return self.random_element(self.attorney_specializations)
    
    def firm_type(self):
        """Generate law firm type"""
        return self.random_element(self.firm_types)
    
    def case_status(self):
        """Generate case status"""
        return self.random_element(self.case_statuses)
    
    def fee_structure(self):
        """Generate fee structure"""
        return self.random_element(self.fee_structures)
    
    def professional_credential(self):
        """Generate professional credential"""
        return self.random_element(self.credentials)
    
    def law_school(self):
        """Generate law school"""
        return self.random_element(self.law_schools)
    
    def create_legal_email(self, first_name, last_name, is_attorney=True):
        """Create realistic email based on person's name and role"""
        if is_attorney:
            domain = self.random_element(self.legal_email_domains)
        else:
            domain = self.random_element(self.client_email_domains)
        
        formats = [
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}{last_name.lower()}",
            f"{first_name[0].lower()}{last_name.lower()}",
            f"{first_name.lower()}{last_name[0].lower()}",
            f"{first_name.lower()}.{last_name.lower()}{self.random_int(1, 99)}",
            f"{first_name.lower()}{self.random_int(1, 999)}"
        ]
        
        username = self.random_element(formats)
        return f"{username}@{domain}"
    
    def settlement_amount(self):
        """Generate settlement amount"""
        return round(random.uniform(1000.00, 10000000.00), 2)
    
    def court_filing_fee(self):
        """Generate court filing fee"""
        return round(random.uniform(50.00, 2000.00), 2)

class LegalDatasetGenerator:
    def __init__(self, seed=42):
        """Initialize the legal dataset generator"""
        self.fake = Faker()
        self.fake.add_provider(LegalProvider)
        Faker.seed(seed)
        
        # Build dynamic patterns for PII detection
        provider = [p for p in self.fake.providers if isinstance(p, LegalProvider)][0]
        all_practice_areas = provider.practice_areas
        all_client_types = provider.client_types
        all_case_statuses = provider.case_statuses
        all_firm_types = provider.firm_types
        all_credentials = provider.credentials
        
        # PII type definitions for legal data
        self.pii_types = {
            'PERSON_NAME': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b\d{3}-\d{3}-\d{4}\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'ADDRESS': r'\d+\s+\w+\s+\w+',
            'DATE_OF_BIRTH': r'\b\d{2}/\d{2}/\d{4}\b',
            'CASE_NUMBER': r'\bCV-\d{4}-\d{4}\b',
            'DOCKET_NUMBER': r'\bDC-\d{6}\b',
            'BAR_NUMBER': r'\b[A-Z]{2}-\d{6}\b',
            'ZIP_CODE': r'\b\d{5}\b',
            'PRACTICE_AREA': r'\b(' + '|'.join(all_practice_areas) + r')\b',
            'CLIENT_TYPE': r'\b(' + '|'.join(all_client_types) + r')\b',
            'CASE_STATUS': r'\b(' + '|'.join(all_case_statuses) + r')\b',
            'FIRM_TYPE': r'\b(' + '|'.join(all_firm_types) + r')\b',
            'CREDENTIAL': r'\b(' + '|'.join(all_credentials) + r')\b',
            'BILLING_RATE': r'\$\d+\.\d{2}',
            'SETTLEMENT_AMOUNT': r'\$\d+,?\d*\.\d{2}',
            'COURT_JURISDICTION': r'\b\w+\s+(District Court|Supreme Court|Superior Court|Circuit Court|Municipal Court|Family Court|Probate Court)\b',
            'LAW_SCHOOL': r'\b\w+\s+Law\s+School\b',
            'LEGAL_DOCUMENT': r'\b(Articles of Incorporation|Merger Agreement|Motion to Dismiss|Plea Agreement|Complaint|Settlement Agreement|Divorce Petition|Purchase Agreement)\b',
            'UNAVAILABLE_FIELD': r'\bNot Available\b'
        }
    
    def find_pii_in_text(self, text):
        """Find PII types and their indices in a text"""
        pii_findings = []
        
        for pii_type, pattern in self.pii_types.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                pii_findings.append({
                    'pii_type': pii_type,
                    'value': match.group(),
                    'start_index': match.start(),
                    'end_index': match.end(),
                    'length': len(match.group())
                })
        
        return pii_findings
    
    def generate_legal_record(self):
        """Generate a single legal case record"""
        # Generate basic client information
        client_first_name = self.fake.first_name()
        client_last_name = self.fake.last_name()
        client_full_name = f"{client_first_name} {client_last_name}"
        
        # Generate attorney information
        attorney_first_name = self.fake.first_name()
        attorney_last_name = self.fake.last_name()
        attorney_full_name = f"{attorney_first_name} {attorney_last_name}"
        
        # Generate client demographics
        client_birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
        client_ssn = self.fake.ssn() if random.random() > 0.3 else None  # Not always available
        client_email = self.fake.create_legal_email(client_first_name, client_last_name, is_attorney=False)
        client_phone = self.fake.phone_number()
        client_address = self.fake.address().replace('\n', ', ')
        
        # Generate legal case profile
        practice_area = self.fake.practice_area()
        client_type = self.fake.client_type()
        case_complexity = self.fake.case_complexity()
        jurisdiction_type = self.fake.jurisdiction_type()
        court_jurisdiction = self.fake.court_jurisdiction(jurisdiction_type)
        
        # Generate case details
        case_number = self.fake.case_number()
        docket_number = self.fake.docket_number()
        case_types = self.fake.case_types_for_practice_area(practice_area)
        primary_case_type = case_types[0] if case_types else 'General Legal Matter'
        case_status = self.fake.case_status()
        
        # Generate attorney details
        attorney_bar_number = self.fake.bar_number()
        attorney_email = self.fake.create_legal_email(attorney_first_name, attorney_last_name, is_attorney=True)
        attorney_specialization = self.fake.attorney_specialization()
        law_school = self.fake.law_school()
        credentials = [self.fake.professional_credential() for _ in range(random.randint(1, 3))]
        years_practiced = random.randint(1, 40)
        
        # Generate firm information
        firm_type = self.fake.firm_type()
        firm_name = f"{self.fake.company()} Law Firm"
        
        # Generate billing information
        billing_rate = self.fake.billing_rate_for_complexity(case_complexity)
        estimated_hours = self.fake.estimated_hours_for_complexity(case_complexity)
        fee_structure = self.fake.fee_structure()
        
        # Generate case dates
        case_opened_date = self.fake.date_between(start_date='-2y', end_date='today')
        last_activity_date = self.fake.date_between(start_date=case_opened_date, end_date='today')
        
        # Generate case financial details
        total_fees_billed = round(billing_rate * estimated_hours * random.uniform(0.3, 1.2), 2)
        settlement_amount = self.fake.settlement_amount() if case_status in ['Closed - Settled'] else None
        court_filing_fee = self.fake.court_filing_fee()
        
        # Generate opposing party (sometimes)
        opposing_party = None
        opposing_counsel = None
        if random.random() > 0.4:  # 60% chance of having opposing party
            opposing_party = self.fake.company() if client_type == 'Individual' else self.fake.name()
            opposing_counsel_first = self.fake.first_name()
            opposing_counsel_last = self.fake.last_name()
            opposing_counsel = f"{opposing_counsel_first} {opposing_counsel_last}"
        
        # Generate recent legal document
        recent_document = self.fake.legal_document_for_practice_area(practice_area)
        document_date = self.fake.date_between(start_date=case_opened_date, end_date='today')
        
        # Create comprehensive legal record with consistent structure
        record_text = f"""
LEGAL CASE RECORD - {firm_name.upper()}
Case Number: {case_number} | Docket: {docket_number}
Court: {court_jurisdiction}

CLIENT INFORMATION:
Name: {client_full_name}
Date of Birth: {client_birth_date.strftime('%m/%d/%Y') if client_birth_date else 'Not Available'}
SSN: {client_ssn if client_ssn else 'Not Available'}
Address: {client_address}
Phone: {client_phone}
Email: {client_email}
Client Type: {client_type}

CASE DETAILS:
Practice Area: {practice_area}
Primary Case Type: {primary_case_type}
All Case Types: {', '.join(case_types)}
Case Complexity: {case_complexity}
Case Status: {case_status}
Case Opened: {case_opened_date.strftime('%m/%d/%Y')}
Last Activity: {last_activity_date.strftime('%m/%d/%Y')}

ATTORNEY INFORMATION:
Name: {attorney_full_name}
Bar Number: {attorney_bar_number}
Email: {attorney_email}
Specialization: {attorney_specialization}
Law School: {law_school}
Years Practiced: {years_practiced}
Credentials: {', '.join(credentials)}

FIRM INFORMATION:
Firm Name: {firm_name}
Firm Type: {firm_type}
Jurisdiction Type: {jurisdiction_type}
Court: {court_jurisdiction}

BILLING & FINANCIAL:
Fee Structure: {fee_structure}
Hourly Rate: ${billing_rate:.2f}
Estimated Hours: {estimated_hours}
Total Fees Billed: ${total_fees_billed:.2f}
Court Filing Fee: ${court_filing_fee:.2f}
Settlement Amount: {f'${settlement_amount:.2f}' if settlement_amount else 'Not Available'}

OPPOSING PARTY:
Opposing Party: {opposing_party if opposing_party else 'Not Available'}
Opposing Counsel: {opposing_counsel if opposing_counsel else 'Not Available'}

RECENT ACTIVITY:
Document Type: {recent_document}
Document Date: {document_date.strftime('%m/%d/%Y')}
Last Update: {last_activity_date.strftime('%m/%d/%Y')}

CASE SUMMARY:
Client {client_full_name} ({client_type}) has retained {attorney_full_name} for {practice_area} matter.
Primary case type: {primary_case_type} (Complexity: {case_complexity})
Case opened on {case_opened_date.strftime('%m/%d/%Y')} in {court_jurisdiction}
Attorney contact: {attorney_email} (Bar: {attorney_bar_number})
Current status: {case_status}
Recent activity: {recent_document} filed on {document_date.strftime('%m/%d/%Y')}
Billing rate: ${billing_rate:.2f}/hour ({fee_structure})
Total fees to date: ${total_fees_billed:.2f}
{f'Settlement reached for ${settlement_amount:.2f}' if settlement_amount else 'Case ongoing'}
        """.strip()
        
        # Find PII in the record
        pii_findings = self.find_pii_in_text(record_text)
        
        # Create structured record
        record = {
            'case_id': self.fake.uuid4(),
            'case_number': case_number,
            'docket_number': docket_number,
            'client_name': client_full_name,
            'client_first_name': client_first_name,
            'client_last_name': client_last_name,
            'client_date_of_birth': client_birth_date.strftime('%m/%d/%Y') if client_birth_date else None,
            'client_age': (datetime.now().date() - client_birth_date).days // 365 if client_birth_date else None,
            'client_ssn': client_ssn,
            'client_address': client_address,
            'client_phone': client_phone,
            'client_email': client_email,
            'client_type': client_type,
            'practice_area': practice_area,
            'case_types': case_types,
            'primary_case_type': primary_case_type,
            'case_complexity': case_complexity,
            'case_status': case_status,
            'case_opened_date': case_opened_date.strftime('%m/%d/%Y'),
            'last_activity_date': last_activity_date.strftime('%m/%d/%Y'),
            'attorney_name': attorney_full_name,
            'attorney_first_name': attorney_first_name,
            'attorney_last_name': attorney_last_name,
            'attorney_bar_number': attorney_bar_number,
            'attorney_email': attorney_email,
            'attorney_specialization': attorney_specialization,
            'law_school': law_school,
            'credentials': credentials,
            'years_practiced': years_practiced,
            'firm_name': firm_name,
            'firm_type': firm_type,
            'jurisdiction_type': jurisdiction_type,
            'court_jurisdiction': court_jurisdiction,
            'fee_structure': fee_structure,
            'billing_rate': billing_rate,
            'estimated_hours': estimated_hours,
            'total_fees_billed': total_fees_billed,
            'court_filing_fee': court_filing_fee,
            'settlement_amount': settlement_amount,
            'opposing_party': opposing_party,
            'opposing_counsel': opposing_counsel,
            'recent_document': recent_document,
            'document_date': document_date.strftime('%m/%d/%Y'),
            'full_record_text': record_text,
            'pii_findings': pii_findings,
            'pii_count': len(pii_findings),
            'unique_pii_types': list(set([finding['pii_type'] for finding in pii_findings]))
        }
        
        return record
    
    def generate_dataset(self, num_records=1000):
        """Generate a complete legal services dataset"""
        print(f"Generating {num_records} legal case records...")
        
        records = []
        for i in range(num_records):
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{num_records} records...")
            
            record = self.generate_legal_record()
            records.append(record)
        
        return records
    
    def save_dataset(self, records, filename_prefix='legal_dataset'):
        """Save the dataset in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create legal directory if it doesn't exist
        import os
        if not os.path.exists('legal'):
            os.makedirs('legal')
        
        # Save as JSON
        json_filename = f"legal/{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(records, f, indent=2, default=str)
        print(f"Dataset saved as JSON: {json_filename}")
        
        # Save as CSV (flattened version)
        csv_records = []
        for record in records:
            csv_record = record.copy()
            csv_record['pii_findings'] = json.dumps(record['pii_findings'])
            csv_record['unique_pii_types'] = ', '.join(record['unique_pii_types'])
            csv_record['case_types'] = ', '.join(record['case_types'])
            csv_record['credentials'] = ', '.join(record['credentials'])
            csv_records.append(csv_record)
        
        df = pd.DataFrame(csv_records)
        csv_filename = f"legal/{filename_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dataset saved as CSV: {csv_filename}")
        
        # Generate summary statistics
        self.generate_summary_report(records, f"legal/{filename_prefix}_summary_{timestamp}.txt")
        
        return json_filename, csv_filename
    
    def generate_summary_report(self, records, filename):
        """Generate a comprehensive summary report"""
        pii_type_counts = {}
        total_pii_instances = 0
        
        for record in records:
            for finding in record['pii_findings']:
                pii_type = finding['pii_type']
                pii_type_counts[pii_type] = pii_type_counts.get(pii_type, 0) + 1
                total_pii_instances += 1
        
        # Collect legal statistics
        practice_areas = [r['practice_area'] for r in records]
        client_types = [r['client_type'] for r in records]
        case_complexities = [r['case_complexity'] for r in records]
        case_statuses = [r['case_status'] for r in records]
        firm_types = [r['firm_type'] for r in records]
        jurisdiction_types = [r['jurisdiction_type'] for r in records]
        
        with open(filename, 'w') as f:
            f.write("LEGAL SERVICES DATASET - COMPREHENSIVE ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Total Legal Case Records: {len(records)}\n")
            f.write(f"Total PII Instances Found: {total_pii_instances}\n")
            f.write(f"Average PII per Record: {total_pii_instances/len(records):.2f}\n\n")
            
            f.write("PII Type Distribution:\n")
            f.write("-" * 30 + "\n")
            for pii_type, count in sorted(pii_type_counts.items()):
                percentage = (count / total_pii_instances) * 100
                f.write(f"{pii_type}: {count} ({percentage:.1f}%)\n")
            
            # Legal demographics
            f.write(f"\nLEGAL CASE DEMOGRAPHICS:\n")
            f.write("=" * 30 + "\n")
            
            f.write(f"\nPractice Area Distribution:\n")
            for area in set(practice_areas):
                count = practice_areas.count(area)
                percentage = (count / len(records)) * 100
                f.write(f"  {area}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nClient Type Distribution:\n")
            for client_type in set(client_types):
                count = client_types.count(client_type)
                percentage = (count / len(records)) * 100
                f.write(f"  {client_type}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nCase Complexity Distribution:\n")
            for complexity in set(case_complexities):
                count = case_complexities.count(complexity)
                percentage = (count / len(records)) * 100
                f.write(f"  {complexity}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nCase Status Distribution:\n")
            for status in set(case_statuses):
                count = case_statuses.count(status)
                percentage = (count / len(records)) * 100
                f.write(f"  {status}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nFirm Type Distribution:\n")
            for firm_type in set(firm_types):
                count = firm_types.count(firm_type)
                percentage = (count / len(records)) * 100
                f.write(f"  {firm_type}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nJurisdiction Type Distribution:\n")
            for jurisdiction in set(jurisdiction_types):
                count = jurisdiction_types.count(jurisdiction)
                percentage = (count / len(records)) * 100
                f.write(f"  {jurisdiction}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nDATASET FEATURES:\n")
            f.write("=" * 20 + "\n")
            f.write(f"✓ Practice area-based case type relationships\n")
            f.write(f"✓ Case complexity billing rate matching\n")
            f.write(f"✓ Attorney specialization alignment\n")
            f.write(f"✓ Court jurisdiction assignments\n")
            f.write(f"✓ Realistic legal document patterns\n")
            f.write(f"✓ Name-based email generation\n")
            f.write(f"✓ Comprehensive PII detection ({len(self.pii_types)} types)\n")
            
            f.write(f"\nSample PII Findings from First Record:\n")
            f.write("-" * 40 + "\n")
            if records:
                for finding in records[0]['pii_findings'][:20]:
                    f.write(f"Type: {finding['pii_type']}, Value: {finding['value']}, "
                           f"Position: {finding['start_index']}-{finding['end_index']}\n")
        
        print(f"Legal services summary report saved: {filename}")

def main():
    """Main function to generate the legal services dataset"""
    print("Legal Services Dataset Generator")
    print("="*40)
    print("Features:")
    print("✓ Practice area-based case type relationships")
    print("✓ Case complexity to billing rate mapping")
    print("✓ Attorney specialization alignment")
    print("✓ Court jurisdiction assignments")
    print("✓ Realistic legal document patterns")
    print("✓ Name-based email generation")
    print("✓ Comprehensive PII detection and indexing")
    print()
    
    # Initialize generator
    generator = LegalDatasetGenerator(seed=42)
    
    # Generate dataset
    num_records = 500
    records = generator.generate_dataset(num_records)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(records)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(records)} legal case records")
    print(f"Files created: {json_file}, {csv_file}")
    
    # Display sample record
    print(f"\nSample Record (first record):")
    print("-" * 60)
    sample = records[0]
    print(f"Client: {sample['client_name']} ({sample['client_type']})")
    print(f"Case: {sample['case_number']} - {sample['primary_case_type']}")
    print(f"Attorney: {sample['attorney_name']} ({sample['attorney_specialization']})")
    print(f"Practice Area: {sample['practice_area']}")
    print(f"Complexity: {sample['case_complexity']} - Rate: ${sample['billing_rate']}/hour")
    print(f"Court: {sample['court_jurisdiction']}")
    print(f"Status: {sample['case_status']}")
    print(f"Firm: {sample['firm_name']} ({sample['firm_type']})")
    print(f"PII Types Found: {', '.join(sample['unique_pii_types'])}")
    print(f"Total PII Count: {sample['pii_count']}")
    
    print(f"\nSample Record Text (first 400 chars):")
    print(sample['full_record_text'][:400] + "...")
    
    # Show practice area-case type relationships
    print(f"\nPractice Area-Case Type Relationship Examples:")
    print("-" * 50)
    area_examples = {}
    for record in records[:10]:
        area = record['practice_area']
        case_types = ', '.join(record['case_types'])
        if area not in area_examples:
            area_examples[area] = case_types
    
    for area, case_types in area_examples.items():
        print(f"{area}: {case_types}")

if __name__ == "__main__":
    main() 