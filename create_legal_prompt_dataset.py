import json
import re
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

class LegalPromptGenerator:
    def __init__(self, seed=42):
        """Initialize the legal prompt generator"""
        self.fake = Faker()
        Faker.seed(seed)
        
        # PII type definitions for legal prompts
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
            'BILLING_RATE': r'\$\d+\.\d{2}',
            'SETTLEMENT_AMOUNT': r'\$\d+,?\d*\.\d{2}',
            'COURT_JURISDICTION': r'\b\w+\s+(District Court|Supreme Court|Superior Court|Circuit Court|Municipal Court|Family Court|Probate Court)\b',
            'LAW_SCHOOL': r'\b\w+\s+Law\s+School\b',
            'LEGAL_DOCUMENT': r'\b(Articles of Incorporation|Merger Agreement|Motion to Dismiss|Plea Agreement|Complaint|Settlement Agreement|Divorce Petition|Purchase Agreement)\b'
        }
        
        # Legal domain data for realistic prompts
        self.practice_areas = [
            'Corporate Law', 'Criminal Defense', 'Personal Injury', 'Family Law', 'Real Estate',
            'Employment Law', 'Intellectual Property', 'Immigration', 'Bankruptcy', 'Tax Law',
            'Estate Planning', 'Environmental Law', 'Securities Law', 'Healthcare Law'
        ]
        
        self.case_types = {
            'Corporate Law': ['Merger & Acquisition', 'Corporate Governance', 'Securities', 'Contract Dispute'],
            'Criminal Defense': ['Felony Defense', 'Misdemeanor Defense', 'DUI/DWI', 'White Collar Crime'],
            'Personal Injury': ['Auto Accident', 'Medical Malpractice', 'Slip and Fall', 'Product Liability'],
            'Family Law': ['Divorce', 'Child Custody', 'Adoption', 'Prenuptial Agreement'],
            'Real Estate': ['Property Purchase', 'Zoning Dispute', 'Title Issues', 'Landlord-Tenant'],
            'Employment Law': ['Wrongful Termination', 'Discrimination', 'Wage Dispute', 'Contract Negotiation'],
            'Intellectual Property': ['Patent Application', 'Trademark Registration', 'Copyright Infringement'],
            'Immigration': ['Visa Application', 'Green Card', 'Asylum Case', 'Deportation Defense']
        }
        
        self.client_types = ['Individual', 'Small Business', 'Corporation', 'Government Entity', 'Non-Profit']
        self.case_statuses = ['Active', 'Pending Discovery', 'In Mediation', 'Settlement Negotiations', 'Trial Preparation', 'On Appeal', 'Closed - Settled', 'Closed - Dismissed']
        self.legal_documents = ['Motion to Dismiss', 'Complaint', 'Settlement Agreement', 'Divorce Petition', 'Purchase Agreement', 'Employment Contract', 'Patent Application']
        self.court_jurisdictions = ['U.S. District Court SDNY', 'New York Supreme Court', 'California Superior Court', 'U.S. Court of Appeals 9th Circuit']
        
        # Common legal professional roles and tasks
        self.legal_roles = [
            'Attorney', 'Partner', 'Associate', 'Paralegal', 'Legal Assistant', 'Case Manager',
            'Litigation Support', 'Legal Secretary', 'Research Attorney', 'Compliance Officer'
        ]
        
        # Prompt templates with PII (50% will contain PII)
        self.pii_prompt_templates = [
            # Client-specific prompts with names
            "Review the case file for {client_name} regarding their {case_type} matter",
            "Prepare settlement documents for {client_name} (Case: {case_number})",
            "Schedule a deposition for {client_name} at {phone} by {date}",
            "Update billing records for {client_name} - {hours} hours at ${billing_rate}/hour",
            "Send case status update to {client_name} at {email}",
            "Draft motion for {client_name} in {court_jurisdiction}",
            "Contact {client_name} ({phone}) regarding settlement offer of ${settlement_amount}",
            "File documents for {client_name} in case {case_number}",
            "Review discovery materials for {client_name}'s {case_type} case",
            "Prepare witness list for {client_name} vs {opposing_party}",
            
            # Attorney-specific prompts with names
            "Forward case materials to attorney {attorney_name} at {attorney_email}",
            "Schedule meeting between {client_name} and {attorney_name}",
            "Review {attorney_name}'s billing for case {case_number}",
            "Update {attorney_name} on settlement negotiations for {client_name}",
            "Send case files to {attorney_name} (Bar: {bar_number})",
            
            # Case-specific prompts with identifiers
            "Update status for case {case_number} in {court_jurisdiction}",
            "Review docket {docket_number} for upcoming hearings",
            "File motion in case {case_number} by {date}",
            "Prepare settlement agreement for case {case_number} - amount ${settlement_amount}",
            "Review discovery timeline for case {case_number}",
            
            # Document-specific prompts
            "Draft {legal_document} for {client_name}",
            "Review {legal_document} filed in case {case_number}",
            "Prepare {legal_document} for {court_jurisdiction}",
            
            # Billing and financial prompts
            "Process payment of ${settlement_amount} for {client_name}",
            "Generate invoice for {client_name} - {hours} hours at ${billing_rate}/hour",
            "Review billing dispute for case {case_number}",
            "Calculate settlement distribution for {client_name}",
            
            # Contact and communication prompts
            "Email {client_name} at {email} regarding court date",
            "Call {client_name} at {phone} about settlement terms",
            "Send documents to {attorney_email} for review",
            "Contact opposing counsel {opposing_counsel} regarding discovery",
            
            # Multi-entity prompts
            "Coordinate between {client_name} and {attorney_name} for case {case_number}",
            "Schedule conference call with {client_name}, {attorney_name}, and opposing counsel",
            "Review conflict check between {client_name} and {opposing_party}",
            "Prepare joint motion for {client_name} and co-defendant {co_defendant}",
            
            # Administrative prompts with PII
            "Update contact information for {client_name} - new phone {phone}",
            "Process address change for {client_name} to {address}",
            "Update emergency contact for {client_name} to {emergency_contact}",
            "Review client intake form for {client_name} (DOB: {date_of_birth})",
            
            # Court and jurisdiction specific
            "File appeal in {court_jurisdiction} for case {case_number}",
            "Request hearing date in {court_jurisdiction} for {client_name}",
            "Review local rules for {court_jurisdiction}",
            "Submit documents to clerk in {court_jurisdiction}",
            
            # Settlement and negotiation
            "Present settlement offer of ${settlement_amount} to {client_name}",
            "Counter-offer ${settlement_amount} in case {case_number}",
            "Review settlement terms for {client_name} vs {opposing_party}",
            "Prepare settlement statement for ${settlement_amount} distribution"
        ]
        
        # Non-PII prompt templates (general legal work)
        self.non_pii_prompt_templates = [
            # General practice management
            "What are the filing deadlines for motions to dismiss?",
            "Review recent changes to discovery rules",
            "Update practice management software",
            "Schedule staff meeting for next week",
            "Order office supplies for legal department",
            "Review insurance coverage for professional liability",
            
            # Legal research and training
            "Research recent precedents in employment law",
            "Prepare training materials on new privacy regulations",
            "Review changes to court rules and procedures",
            "Update legal research database subscriptions",
            "Compile recent case law updates for monthly newsletter",
            "Research ethical guidelines for client communications",
            
            # Business development
            "Develop marketing materials for practice areas",
            "Plan networking event for legal professionals",
            "Update firm website with recent achievements",
            "Prepare presentation for industry conference",
            "Review competitor analysis for services offered",
            "Create social media content for firm",
            
            # Administrative and operational
            "Implement new document management system",
            "Review vendor contracts for office services",
            "Update employee handbook with recent policies",
            "Schedule annual technology audit",
            "Plan continuing education requirements",
            "Review budget projections for next quarter",
            
            # Compliance and risk management
            "Conduct annual compliance training",
            "Review data security protocols",
            "Update conflict of interest procedures",
            "Implement new client intake procedures",
            "Review professional liability policies",
            "Update privacy policy for client data",
            
            # Legal process and procedure
            "What is the standard timeline for discovery in civil cases?",
            "How do we handle expedited motions?",
            "What are the requirements for expert witness disclosure?",
            "How should we organize case files for complex litigation?",
            "What is the protocol for emergency filings?",
            "How do we handle client confidentiality in team cases?",
            
            # Technology and tools
            "Evaluate new legal research platforms",
            "Implement e-filing system improvements",
            "Review video conferencing options for client meetings",
            "Update case management software",
            "Train staff on new billing software",
            "Research AI tools for document review",
            
            # Financial and billing (general)
            "What are industry standard billing rates for associates?",
            "How do we structure contingency fee agreements?",
            "Review collection procedures for unpaid invoices",
            "Implement new billing code structure",
            "Analyze profitability by practice area",
            "Review expense policies for case costs",
            
            # Professional development
            "Identify continuing education opportunities",
            "Plan mentorship program for junior attorneys",
            "Research bar association committee participation",
            "Develop expertise in emerging legal areas",
            "Plan skills development workshops",
            "Review performance evaluation procedures",
            
            # Court and legal system
            "What are the local rules for electronic filing?",
            "How do different jurisdictions handle discovery disputes?",
            "What is the appeals process timeline?",
            "How do we request expedited hearings?",
            "What are the requirements for pro hac vice admission?",
            "How do we handle conflicts in scheduling between courts?",
            
            # Client service (general)
            "Improve client communication procedures",
            "Develop client feedback collection system",
            "Create informational materials about legal processes",
            "Plan client appreciation events",
            "Implement client portal for document sharing",
            "Develop FAQ for common legal questions",
            
            # Quality control and improvement
            "Review quality assurance procedures for document drafting",
            "Implement peer review process for briefs",
            "Develop checklists for common legal procedures",
            "Analyze case outcomes for process improvement",
            "Create templates for routine legal documents",
            "Review and update firm policies annually"
        ]
    
    def generate_fake_legal_data(self):
        """Generate fake legal data for use in prompts"""
        return {
            'client_name': self.fake.name(),
            'attorney_name': self.fake.name(),
            'opposing_party': self.fake.name(),
            'opposing_counsel': self.fake.name(),
            'co_defendant': self.fake.name(),
            'emergency_contact': self.fake.name(),
            'case_number': f"CV-{random.randint(2020, 2024)}-{random.randint(1000, 9999)}",
            'docket_number': f"DC-{random.randint(100000, 999999)}",
            'bar_number': f"{random.choice(['NY', 'CA', 'TX', 'FL', 'IL'])}-{random.randint(100000, 999999)}",
            'phone': self.fake.phone_number(),
            'email': self.fake.email(),
            'attorney_email': f"{self.fake.first_name().lower()}.{self.fake.last_name().lower()}@lawfirm.com",
            'address': self.fake.address().replace('\n', ', '),
            'date': self.fake.date_between(start_date='today', end_date='+30d').strftime('%m/%d/%Y'),
            'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%m/%d/%Y'),
            'case_type': random.choice([case for cases in self.case_types.values() for case in cases]),
            'practice_area': random.choice(self.practice_areas),
            'court_jurisdiction': random.choice(self.court_jurisdictions),
            'legal_document': random.choice(self.legal_documents),
            'billing_rate': f"{random.randint(150, 1000)}.00",
            'settlement_amount': f"{random.randint(1000, 1000000):,}.00",
            'hours': random.randint(1, 100),
            'client_type': random.choice(self.client_types),
            'case_status': random.choice(self.case_statuses)
        }
    
    def create_pii_prompt(self):
        """Create a prompt that contains PII"""
        template = random.choice(self.pii_prompt_templates)
        fake_data = self.generate_fake_legal_data()
        
        # Fill in the template with fake data
        try:
            prompt = template.format(**fake_data)
        except KeyError as e:
            # If a key is missing, use a fallback
            missing_key = str(e).strip("'")
            fake_data[missing_key] = "PLACEHOLDER"
            prompt = template.format(**fake_data)
        
        return prompt
    
    def create_non_pii_prompt(self):
        """Create a prompt that does not contain PII"""
        return random.choice(self.non_pii_prompt_templates)
    
    def find_pii_in_prompt(self, prompt_text):
        """Find PII types and their indices in a prompt"""
        pii_findings = []
        
        for pii_type, pattern in self.pii_types.items():
            matches = re.finditer(pattern, prompt_text, re.IGNORECASE)
            for match in matches:
                pii_findings.append({
                    'pii_type': pii_type,
                    'value': match.group(),
                    'start_index': match.start(),
                    'end_index': match.end()
                })
        
        return pii_findings
    
    def verify_pii_presence(self, prompt_text, expected_contains_pii):
        """Verify that PII detection matches expected result"""
        pii_findings = self.find_pii_in_prompt(prompt_text)
        actual_contains_pii = len(pii_findings) > 0
        
        return {
            'matches_expectation': actual_contains_pii == expected_contains_pii,
            'expected': expected_contains_pii,
            'actual': actual_contains_pii,
            'pii_findings': pii_findings
        }
    
    def extract_source_entities(self, prompt_text, pii_findings):
        """Extract which legal entities (clients/attorneys/cases) are referenced"""
        entities = []
        
        # Look for person names
        person_names = [finding for finding in pii_findings if finding['pii_type'] == 'PERSON_NAME']
        for name_finding in person_names:
            entities.append({
                'entity_type': 'person',
                'entity_value': name_finding['value'],
                'context': 'legal_participant'
            })
        
        # Look for case numbers
        case_numbers = [finding for finding in pii_findings if finding['pii_type'] == 'CASE_NUMBER']
        for case_finding in case_numbers:
            entities.append({
                'entity_type': 'case',
                'entity_value': case_finding['value'],
                'context': 'legal_case'
            })
        
        # Look for emails
        emails = [finding for finding in pii_findings if finding['pii_type'] == 'EMAIL']
        for email_finding in emails:
            entities.append({
                'entity_type': 'contact',
                'entity_value': email_finding['value'],
                'context': 'communication'
            })
        
        return entities
    
    def generate_prompt_record(self, target_contains_pii=None):
        """Generate a single prompt record with legal context"""
        # Decide if this prompt should contain PII
        if target_contains_pii is None:
            contains_pii = random.choice([True, False])
        else:
            contains_pii = target_contains_pii
        
        # Generate the appropriate type of prompt
        if contains_pii:
            prompt_text = self.create_pii_prompt()
            prompt_category = "Legal Professional Query with PII"
        else:
            prompt_text = self.create_non_pii_prompt()
            prompt_category = "Legal Professional Query without PII"
        
        # Find PII in the prompt
        pii_findings = self.find_pii_in_prompt(prompt_text)
        actual_contains_pii = len(pii_findings) > 0
        
        # Verify PII detection
        verification = self.verify_pii_presence(prompt_text, contains_pii)
        
        # Extract source entities
        source_entities = self.extract_source_entities(prompt_text, pii_findings)
        
        # Determine professional context
        role_context = random.choice(self.legal_roles)
        practice_area_context = random.choice(self.practice_areas)
        
        # Create record
        record = {
            'prompt_id': self.fake.uuid4(),
            'prompt': prompt_text,
            'contains_pii': actual_contains_pii,
            'intended_pii': contains_pii,
            'verification_passed': verification['matches_expectation'],
            'prompt_category': prompt_category,
            'role_context': role_context,
            'practice_area_context': practice_area_context,
            'pii_findings': pii_findings,
            'pii_count': len(pii_findings),
            'unique_pii_types': list(set([finding['pii_type'] for finding in pii_findings])),
            'source_entities': source_entities,
            'entity_count': len(source_entities),
            'prompt_length': len(prompt_text),
            'generated_timestamp': datetime.now().isoformat()
        }
        
        return record
    
    def generate_dataset(self, num_prompts=1000, pii_ratio=0.5):
        """Generate a complete legal prompt dataset"""
        print(f"Generating {num_prompts} legal professional prompts...")
        print(f"Target PII ratio: {pii_ratio*100}% with PII, {(1-pii_ratio)*100}% without PII")
        
        records = []
        num_pii_prompts = int(num_prompts * pii_ratio)
        num_non_pii_prompts = num_prompts - num_pii_prompts
        
        # Generate PII-containing prompts
        print(f"Generating {num_pii_prompts} prompts with PII...")
        for i in range(num_pii_prompts):
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{num_pii_prompts} PII prompts...")
            
            record = self.generate_prompt_record(target_contains_pii=True)
            records.append(record)
        
        # Generate non-PII prompts
        print(f"Generating {num_non_pii_prompts} prompts without PII...")
        for i in range(num_non_pii_prompts):
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{num_non_pii_prompts} non-PII prompts...")
            
            record = self.generate_prompt_record(target_contains_pii=False)
            records.append(record)
        
        # Shuffle the records
        random.shuffle(records)
        
        # Add final numbering
        for i, record in enumerate(records):
            record['prompt_number'] = i + 1
        
        return records
    
    def save_dataset(self, records, filename_prefix='employer_prompts_legal'):
        """Save the prompt dataset in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create prompts_for_llm directory if it doesn't exist
        import os
        if not os.path.exists('prompts_for_llm'):
            os.makedirs('prompts_for_llm')
        
        # Save as JSON
        json_filename = f"prompts_for_llm/{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(records, f, indent=2, default=str)
        print(f"Dataset saved as JSON: {json_filename}")
        
        # Save as CSV (flattened version)
        csv_records = []
        for record in records:
            csv_record = record.copy()
            csv_record['pii_findings'] = json.dumps(record['pii_findings'])
            csv_record['unique_pii_types'] = ', '.join(record['unique_pii_types'])
            csv_record['source_entities'] = json.dumps(record['source_entities'])
            csv_records.append(csv_record)
        
        df = pd.DataFrame(csv_records)
        csv_filename = f"prompts_for_llm/{filename_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dataset saved as CSV: {csv_filename}")
        
        # Generate analysis report
        self.generate_analysis_report(records, f"prompts_for_llm/{filename_prefix}_analysis_{timestamp}.txt")
        
        return json_filename, csv_filename
    
    def generate_analysis_report(self, records, filename):
        """Generate a comprehensive analysis report"""
        pii_type_counts = {}
        total_pii_instances = 0
        verification_passed = 0
        
        for record in records:
            if record['verification_passed']:
                verification_passed += 1
            
            for finding in record['pii_findings']:
                pii_type = finding['pii_type']
                pii_type_counts[pii_type] = pii_type_counts.get(pii_type, 0) + 1
                total_pii_instances += 1
        
        # Collect statistics
        pii_prompts = [r for r in records if r['contains_pii']]
        non_pii_prompts = [r for r in records if not r['contains_pii']]
        role_contexts = [r['role_context'] for r in records]
        practice_areas = [r['practice_area_context'] for r in records]
        
        with open(filename, 'w') as f:
            f.write("LEGAL PROFESSIONAL PROMPTS - COMPREHENSIVE ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Total Prompts Generated: {len(records)}\n")
            f.write(f"Prompts with PII: {len(pii_prompts)} ({len(pii_prompts)/len(records)*100:.1f}%)\n")
            f.write(f"Prompts without PII: {len(non_pii_prompts)} ({len(non_pii_prompts)/len(records)*100:.1f}%)\n")
            f.write(f"Verification Success Rate: {verification_passed/len(records)*100:.1f}%\n")
            f.write(f"Total PII Instances: {total_pii_instances}\n")
            f.write(f"Average PII per PII-containing Prompt: {total_pii_instances/len(pii_prompts):.2f}\n\n")
            
            f.write("PII Type Distribution:\n")
            f.write("-" * 30 + "\n")
            for pii_type, count in sorted(pii_type_counts.items()):
                percentage = (count / total_pii_instances) * 100 if total_pii_instances > 0 else 0
                f.write(f"{pii_type}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nROLE CONTEXT DISTRIBUTION:\n")
            f.write("=" * 30 + "\n")
            for role in set(role_contexts):
                count = role_contexts.count(role)
                percentage = (count / len(records)) * 100
                f.write(f"{role}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nPRACTICE AREA DISTRIBUTION:\n")
            f.write("=" * 30 + "\n")
            for area in set(practice_areas):
                count = practice_areas.count(area)
                percentage = (count / len(records)) * 100
                f.write(f"{area}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nDATASET FEATURES:\n")
            f.write("=" * 20 + "\n")
            f.write(f"✓ Realistic legal professional scenarios\n")
            f.write(f"✓ Practice area-specific context\n")
            f.write(f"✓ Role-based prompt generation\n")
            f.write(f"✓ Comprehensive PII detection ({len(self.pii_types)} types)\n")
            f.write(f"✓ Multi-entity prompt support\n")
            f.write(f"✓ Verification and quality control\n")
            f.write(f"✓ Source entity tracking\n")
            
            f.write(f"\nSAMPLE PROMPTS:\n")
            f.write("=" * 15 + "\n")
            f.write("WITH PII:\n")
            for i, record in enumerate([r for r in records if r['contains_pii']][:5]):
                f.write(f"{i+1}. {record['prompt']}\n")
                f.write(f"   PII Types: {', '.join(record['unique_pii_types'])}\n\n")
            
            f.write("WITHOUT PII:\n")
            for i, record in enumerate([r for r in records if not r['contains_pii']][:5]):
                f.write(f"{i+1}. {record['prompt']}\n\n")
            
            f.write(f"\nQUALITY METRICS:\n")
            f.write("=" * 20 + "\n")
            prompt_lengths = [r['prompt_length'] for r in records]
            entity_counts = [r['entity_count'] for r in records if r['entity_count'] > 0]
            
            f.write(f"Average Prompt Length: {sum(prompt_lengths)/len(prompt_lengths):.1f} characters\n")
            f.write(f"Shortest Prompt: {min(prompt_lengths)} characters\n")
            f.write(f"Longest Prompt: {max(prompt_lengths)} characters\n")
            if entity_counts:
                f.write(f"Average Entities per Multi-entity Prompt: {sum(entity_counts)/len(entity_counts):.2f}\n")
            f.write(f"Multi-entity Prompts: {len(entity_counts)} ({len(entity_counts)/len(records)*100:.1f}%)\n")
        
        print(f"Legal prompt analysis report saved: {filename}")

def main():
    """Main function to generate the legal prompt dataset"""
    print("Legal Professional Prompt Dataset Generator")
    print("="*50)
    print("Features:")
    print("✓ Practice area-specific legal scenarios")
    print("✓ Role-based prompt generation")
    print("✓ Comprehensive PII detection and labeling")
    print("✓ Multi-entity prompt support")
    print("✓ Verification and quality control")
    print("✓ Source entity tracking")
    print()
    
    # Initialize generator
    generator = LegalPromptGenerator(seed=42)
    
    # Generate dataset
    num_prompts = 1000
    records = generator.generate_dataset(num_prompts, pii_ratio=0.5)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(records)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(records)} legal professional prompts")
    print(f"Files created: {json_file}, {csv_file}")
    
    # Display statistics
    pii_prompts = [r for r in records if r['contains_pii']]
    non_pii_prompts = [r for r in records if not r['contains_pii']]
    verification_passed = sum(1 for r in records if r['verification_passed'])
    
    print(f"\nDataset Statistics:")
    print("-" * 30)
    print(f"Total Prompts: {len(records)}")
    print(f"With PII: {len(pii_prompts)} ({len(pii_prompts)/len(records)*100:.1f}%)")
    print(f"Without PII: {len(non_pii_prompts)} ({len(non_pii_prompts)/len(records)*100:.1f}%)")
    print(f"Verification Success Rate: {verification_passed/len(records)*100:.1f}%")
    
    # Display sample prompts
    print(f"\nSample Prompts:")
    print("-" * 30)
    print("WITH PII:")
    for i, record in enumerate(pii_prompts[:3]):
        print(f"{i+1}. {record['prompt']}")
        print(f"   PII Types: {', '.join(record['unique_pii_types'])}")
        print()
    
    print("WITHOUT PII:")
    for i, record in enumerate(non_pii_prompts[:3]):
        print(f"{i+1}. {record['prompt']}")
        print()

if __name__ == "__main__":
    main() 