import pandas as pd
import random
import json
from datetime import datetime
from faker import Faker
import re

class EmployerPromptGenerator:
    """Generate realistic employer prompts for LLM with PII detection labels"""
    
    def __init__(self, csv_file_path):
        """Initialize with financial dataset"""
        self.fake = Faker()
        Faker.seed(42)
        
        # Load the financial dataset
        print(f"Loading financial dataset from {csv_file_path}...")
        self.df = pd.read_csv(csv_file_path)
        print(f"Loaded {len(self.df)} customer records")
        
        # Define prompt templates with PII (True cases) - Single Customer
        self.single_customer_templates = [
            # Customer Analysis Templates
            "Analyze the spending patterns for customer {customer_name} (Account: {account_number})",
            "What's the credit risk assessment for {customer_name} with SSN {ssn}?",
            "Review the transaction history for account number {account_number} belonging to {customer_name}",
            "Can you pull up the financial profile for {email}?",
            "Generate a credit report summary for {customer_name} at {address}",
            "What are the investment recommendations for customer {customer_name} in the {employment_sector} sector?",
            "Create a loan pre-approval letter for {customer_name} (Phone: {phone})",
            "Review the account activity for {customer_name} in our {bank_branch} branch",
            
            # Customer Service Templates  
            "Send a follow-up email to {email} regarding their {recent_transaction_type} transaction",
            "Call {customer_name} at {phone} about their overdue payment",
            "Draft a personalized investment proposal for {customer_name} based on their {risk_profile} risk profile",
            "Schedule a meeting with {customer_name} (SSN: {ssn}) to discuss their mortgage application",
            "Send account statements to {customer_name} at {address}",
            "Contact {customer_name} ({email}) about upgrading their {primary_account_type} account",
            
            # Risk Assessment Templates
            "Evaluate the creditworthiness of {customer_name} with income bracket {income_bracket}",
            "What's the fraud risk for recent transactions on account {account_number}?",
            "Review the loan application for {customer_name} (DOB: {date_of_birth})",
            "Assess the default probability for customer {ssn} based on their payment history",
            "Check if {customer_name} at {address} meets our investment criteria",
            
            # Marketing Templates
            "Create a targeted marketing campaign for {customer_name} in the {employment_sector} industry",
            "Send a credit card offer to {email} for someone with {credit_score_category} credit",
            "Draft a personalized retirement planning email for {customer_name} (Age: {age})",
            "Target investment products to {customer_name} based on their {customer_segment} profile",
            
            # Compliance Templates
            "Verify the identity of {customer_name} using SSN {ssn} and DOB {date_of_birth}",
            "Run a background check on {customer_name} at {address} for loan approval",
            "Confirm the employment details for {customer_name} in {employment_sector}",
            "Validate the contact information: {phone} and {email} for {customer_name}",
            
            # Account Management Templates
            "Update the address for {customer_name} (Account: {account_number}) to {address}",
            "Process a wire transfer from account {account_number} for {customer_name}",
            "Close the {primary_account_type} account for {customer_name} (SSN: {ssn})",
            "Transfer funds between accounts for {customer_name} at {bank_branch}",
            "Set up automatic payments for {customer_name} ({email}) for their {loan_purpose} loan",
            
            # Advisory Templates
            "Prepare investment advice for {customer_name} with ${recent_transaction_amount} available",
            "What tax implications should {customer_name} (SSN: {ssn}) consider for their investments?",
            "Create a financial plan for {customer_name} in {region} region",
            "Advise {customer_name} on refinancing their loan amount of ${loan_amount}",
            
            # Reporting Templates
            "Generate a customer portfolio report for {customer_name} (ID: {customer_id})",
            "Create a transaction summary for {customer_name} covering their {recent_transaction_date} activity",
            "Prepare a year-end tax document for {customer_name} at {email}",
            "Compile all accounts for {customer_name}: {account_types}",
        ]
        
        # Define prompt templates with multiple customers
        self.multi_customer_templates = [
            # Comparative Analysis
            "Compare the investment portfolios between {customer_name_1} (Account: {account_number_1}) and {customer_name_2} (Account: {account_number_2})",
            "Analyze credit risk differences between {customer_name_1} (SSN: {ssn_1}) and {customer_name_2} (SSN: {ssn_2})",
            "Review transaction patterns for customers {customer_name_1} ({email_1}) and {customer_name_2} ({email_2})",
            "Cross-reference accounts {account_number_1} for {customer_name_1} and {account_number_2} for {customer_name_2}",
            
            # Relationship Analysis
            "Check if {customer_name_1} at {address_1} and {customer_name_2} at {address_2} are related customers",
            "Verify joint account holders: {customer_name_1} (SSN: {ssn_1}) and {customer_name_2} (SSN: {ssn_2})",
            "Review shared transactions between {customer_name_1} ({phone_1}) and {customer_name_2} ({phone_2})",
            
            # Batch Processing
            "Process loan applications for {customer_name_1} (DOB: {date_of_birth_1}) and {customer_name_2} (DOB: {date_of_birth_2})",
            "Send account updates to {customer_name_1} ({email_1}) and {customer_name_2} ({email_2})",
            "Generate investment reports for {customer_name_1} and {customer_name_2} in {employment_sector_1} and {employment_sector_2} sectors",
            
            # Risk Assessment
            "Evaluate fraud risk for connected accounts: {customer_name_1} (Account: {account_number_1}) and {customer_name_2} (Account: {account_number_2})",
            "Review credit applications from {customer_name_1} ({ssn_1}) and {customer_name_2} ({ssn_2})",
            
            # Customer Service
            "Schedule meetings with {customer_name_1} ({phone_1}) and {customer_name_2} ({phone_2}) for portfolio review",
            "Update contact information for {customer_name_1} at {address_1} and {customer_name_2} at {address_2}",
            "Send personalized offers to {customer_name_1} ({email_1}) and {customer_name_2} ({email_2}) based on their profiles",
        ]
        
        # Combine all PII templates
        self.pii_prompt_templates = self.single_customer_templates + self.multi_customer_templates
        
        # Define prompt templates without PII (False cases)
        self.non_pii_prompt_templates = [
            # General Analytics
            "What are the trending investment products this quarter?",
            "Analyze overall customer satisfaction scores across all branches",
            "What's the average loan approval rate for the healthcare sector?",
            "How do credit card usage patterns vary by region?",
            "What are the most popular account types for new customers?",
            "Generate a report on transaction volume trends by day of week",
            "Compare investment performance across different risk profiles",
            "What's the correlation between employment sector and account types?",
            
            # Process & Policy
            "Create a standard procedure for loan application processing",
            "What are the compliance requirements for new account opening?",
            "Generate a template for customer onboarding emails",
            "What documentation is needed for mortgage pre-approval?",
            "Create a checklist for account closure procedures",
            "Draft a policy for handling customer complaints",
            "What are the KYC requirements for business accounts?",
            "Generate guidelines for credit limit increases",
            
            # Market Research
            "What products should we offer to compete with other banks?",
            "Analyze market trends in the fintech space",
            "How can we improve our mobile banking features?",
            "What are customer expectations for digital services?",
            "Research best practices for customer retention",
            "What are the emerging trends in investment products?",
            "How do interest rate changes affect customer behavior?",
            "What cybersecurity measures should we implement?",
            
            # Training & Education
            "Create training materials for new financial advisors",
            "What are the latest regulations in consumer banking?",
            "Generate a guide for explaining investment risks to customers",
            "How should staff handle sensitive customer information?",
            "Create FAQ responses for common customer questions",
            "What soft skills are important for customer service representatives?",
            "Design a workshop on fraud detection techniques",
            "Develop scenarios for customer interaction training",
            
            # Product Development
            "What features should our new mobile app include?",
            "How can we simplify the loan application process?",
            "What rewards program would appeal to millennials?",
            "Design a savings product for college students",
            "How can we make investment advice more accessible?",
            "What digital tools would help small business customers?",
            "Create a framework for personalized financial recommendations",
            "What partnerships could enhance our service offerings?",
            
            # Operations
            "How can we reduce wait times at branch locations?",
            "What metrics should we track for customer service quality?",
            "How can we optimize our call center operations?",
            "What's the best schedule for system maintenance windows?",
            "How should we prioritize feature requests from customers?",
            "What backup procedures should we have for data protection?",
            "How can we streamline the account verification process?",
            "What quality assurance measures should we implement?",
            
            # Strategy & Planning
            "What markets should we expand into next year?",
            "How should we position ourselves against digital-only banks?",
            "What's our strategy for acquiring younger customers?",
            "How can we increase profitability while maintaining service quality?",
            "What partnerships would support our growth goals?",
            "How should we adapt to changing regulatory requirements?",
            "What technology investments should we prioritize?",
            "How can we improve operational efficiency across departments?"
        ]
    
    def extract_customer_data(self, row):
        """Extract clean customer data from a dataframe row"""
        return {
            'customer_id': row['customer_id'],
            'customer_name': row['customer_name'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'date_of_birth': row['date_of_birth'],
            'age': row['age'],
            'ssn': row['ssn'],
            'address': row['address'],
            'phone': row['phone'],
            'email': row['email'],
            'employment_sector': row['employment_sector'],
            'income_bracket': row['income_bracket'],
            'credit_score_category': row['credit_score_category'],
            'risk_profile': row['risk_profile'],
            'customer_segment': row['customer_segment'],
            'relationship_length': row['relationship_length'],
            'region': row['region'],
            'bank_branch': row['bank_branch'],
            'account_types': row['account_types'],
            'primary_account_type': row['primary_account_type'],
            'account_number': row['account_number'],
            'routing_number': row['routing_number'],
            'credit_card_number': row['credit_card_number'] if pd.notna(row['credit_card_number']) else 'Not Available',
            'recent_transaction_type': row['recent_transaction_type'],
            'recent_transaction_amount': row['recent_transaction_amount'],
            'recent_transaction_date': row['recent_transaction_date'],
            'investment_product': row['investment_product'] if pd.notna(row['investment_product']) else 'Not Available',
            'loan_purpose': row['loan_purpose'] if pd.notna(row['loan_purpose']) else 'Not Available',
            'loan_amount': row['loan_amount'] if pd.notna(row['loan_amount']) else 'Not Available',
            'advisor_name': row['advisor_name'],
            'advisor_email': row['advisor_email'],
        }
    
    def generate_pii_prompt(self):
        """Generate a prompt containing PII data"""
        # Randomly choose between single and multi-customer templates (70% single, 30% multi)
        use_multi_customer = random.random() < 0.3
        
        if use_multi_customer:
            return self.generate_multi_customer_prompt()
        else:
            return self.generate_single_customer_prompt()
    
    def generate_single_customer_prompt(self):
        """Generate a prompt with one customer's PII"""
        # Select random customer record
        random_row = self.df.sample(n=1).iloc[0]
        customer_data = self.extract_customer_data(random_row)
        
        # Select random single-customer template
        template = random.choice(self.single_customer_templates)
        
        # Fill template with customer data
        try:
            prompt = template.format(**customer_data)
            return prompt, True, [customer_data['customer_id']]
        except KeyError as e:
            # Fallback if template has missing field
            fallback_template = "Analyze the account for customer {customer_name} (SSN: {ssn})"
            prompt = fallback_template.format(**customer_data)
            return prompt, True, [customer_data['customer_id']]
    
    def generate_multi_customer_prompt(self):
        """Generate a prompt with multiple customers' PII"""
        # Select two random customer records
        random_rows = self.df.sample(n=2)
        customer_1 = self.extract_customer_data(random_rows.iloc[0])
        customer_2 = self.extract_customer_data(random_rows.iloc[1])
        
        # Create combined data with _1 and _2 suffixes
        combined_data = {}
        for key, value in customer_1.items():
            combined_data[f"{key}_1"] = value
        for key, value in customer_2.items():
            combined_data[f"{key}_2"] = value
        
        # Select random multi-customer template
        template = random.choice(self.multi_customer_templates)
        
        # Fill template with combined customer data
        try:
            prompt = template.format(**combined_data)
            return prompt, True, [customer_1['customer_id'], customer_2['customer_id']]
        except KeyError as e:
            # Fallback if template has missing field
            fallback_template = "Compare accounts for {customer_name_1} (SSN: {ssn_1}) and {customer_name_2} (SSN: {ssn_2})"
            prompt = fallback_template.format(**combined_data)
            return prompt, True, [customer_1['customer_id'], customer_2['customer_id']]
    
    def generate_non_pii_prompt(self):
        """Generate a prompt without PII data"""
        template = random.choice(self.non_pii_prompt_templates)
        return template, False, None
    
    def has_pii_content(self, prompt):
        """Double-check if prompt actually contains PII"""
        pii_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{9,12}\b',  # Account numbers
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{3}-\d{3}-\d{4}\b',  # Phone
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Names (basic pattern)
        ]
        
        for pattern in pii_patterns:
            if re.search(pattern, prompt):
                return True
        return False
    
    def generate_dataset(self, total_prompts=1000, pii_ratio=0.5):
        """Generate the complete prompt dataset"""
        print(f"Generating {total_prompts} employer prompts...")
        
        dataset = []
        pii_prompts_target = int(total_prompts * pii_ratio)
        non_pii_prompts_target = total_prompts - pii_prompts_target
        
        # Generate PII prompts
        print(f"Generating {pii_prompts_target} prompts with PII...")
        for i in range(pii_prompts_target):
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{pii_prompts_target} PII prompts...")
            
            prompt, contains_pii, customer_ids = self.generate_pii_prompt()
            
            # Verify it actually contains PII
            verified_pii = self.has_pii_content(prompt)
            
            record = {
                'prompt_id': f"pii_{i+1:04d}",
                'prompt': prompt,
                'contains_pii': contains_pii,
                'verified_pii': verified_pii,
                'prompt_type': 'with_pii',
                'source_customer_id': customer_ids,
                'num_customers': len(customer_ids)
            }
            dataset.append(record)
        
        # Generate non-PII prompts
        print(f"Generating {non_pii_prompts_target} prompts without PII...")
        for i in range(non_pii_prompts_target):
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{non_pii_prompts_target} non-PII prompts...")
            
            prompt, contains_pii, customer_data = self.generate_non_pii_prompt()
            
            # Verify it doesn't contain PII
            verified_pii = self.has_pii_content(prompt)
            
            record = {
                'prompt_id': f"nopii_{i+1:04d}",
                'prompt': prompt,
                'contains_pii': contains_pii,
                'verified_pii': verified_pii,
                'prompt_type': 'without_pii',
                'source_customer_id': [],
                'num_customers': 0
            }
            dataset.append(record)
        
        # Shuffle the dataset
        random.shuffle(dataset)
        
        # Add final indices
        for i, record in enumerate(dataset):
            record['final_index'] = i + 1
        
        return dataset
    
    def save_dataset(self, dataset, filename_prefix='employer_prompts_finance'):
        """Save the prompt dataset"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as JSON
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"Dataset saved as JSON: {json_filename}")
        
        # Save as CSV
        df = pd.DataFrame(dataset)
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dataset saved as CSV: {csv_filename}")
        
        # Generate analysis report
        self.generate_analysis_report(dataset, f"{filename_prefix}_analysis_{timestamp}.txt")
        
        return json_filename, csv_filename
    
    def generate_analysis_report(self, dataset, filename):
        """Generate analysis report of the prompt dataset"""
        total_prompts = len(dataset)
        pii_prompts = sum(1 for item in dataset if item['contains_pii'])
        non_pii_prompts = total_prompts - pii_prompts
        
        # Verification analysis
        correctly_labeled_pii = sum(1 for item in dataset if item['contains_pii'] == item['verified_pii'])
        mislabeled = total_prompts - correctly_labeled_pii
        
        with open(filename, 'w') as f:
            f.write("EMPLOYER PROMPT DATASET - ANALYSIS REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Total Prompts Generated: {total_prompts}\n")
            f.write(f"Prompts with PII: {pii_prompts} ({pii_prompts/total_prompts*100:.1f}%)\n")
            f.write(f"Prompts without PII: {non_pii_prompts} ({non_pii_prompts/total_prompts*100:.1f}%)\n\n")
            
            f.write("LABEL VERIFICATION:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Correctly Labeled: {correctly_labeled_pii} ({correctly_labeled_pii/total_prompts*100:.1f}%)\n")
            f.write(f"Mislabeled: {mislabeled} ({mislabeled/total_prompts*100:.1f}%)\n\n")
            
            f.write("SAMPLE PROMPTS WITH PII:\n")
            f.write("-" * 30 + "\n")
            pii_samples = [item for item in dataset if item['contains_pii']][:5]
            for i, sample in enumerate(pii_samples, 1):
                f.write(f"{i}. {sample['prompt']}\n\n")
            
            f.write("SAMPLE PROMPTS WITHOUT PII:\n")
            f.write("-" * 30 + "\n")
            non_pii_samples = [item for item in dataset if not item['contains_pii']][:5]
            for i, sample in enumerate(non_pii_samples, 1):
                f.write(f"{i}. {sample['prompt']}\n\n")
            
            f.write("DATASET FEATURES:\n")
            f.write("=" * 20 + "\n")
            f.write("✓ Realistic employer queries for financial LLM use cases\n")
            f.write("✓ Balanced PII vs non-PII distribution\n")
            f.write("✓ Comprehensive coverage of banking scenarios\n")
            f.write("✓ Ground truth labels for PII detection training\n")
            f.write("✓ Verification flags for data quality assurance\n")
            f.write("✓ Source traceability to original customer records\n")
        
        print(f"Analysis report saved: {filename}")

def main():
    """Main function to generate employer prompt dataset"""
    print("Employer Prompt Dataset Generator for PII Detection")
    print("="*55)
    print("Purpose: Generate realistic employer prompts with PII labels")
    print("Use Case: Training LLMs to detect PII in business queries")
    print()
    
    # Initialize generator with the CSV file
    csv_file = "financial_dataset_20250726_155509.csv"
    try:
        generator = EmployerPromptGenerator(csv_file)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        print("Please ensure the financial dataset CSV file exists.")
        return
    
    # Generate dataset
    total_prompts = 1000
    print(f"Generating {total_prompts} employer prompts...")
    dataset = generator.generate_dataset(total_prompts=total_prompts, pii_ratio=0.5)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(dataset)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(dataset)} employer prompts")
    print(f"Files created: {json_file}, {csv_file}")
    
    # Show sample results
    pii_samples = [item for item in dataset if item['contains_pii']][:3]
    non_pii_samples = [item for item in dataset if not item['contains_pii']][:3]
    
    print(f"\nSample Prompts WITH PII:")
    print("-" * 40)
    for i, sample in enumerate(pii_samples, 1):
        print(f"{i}. {sample['prompt']}")
        print()
    
    print(f"Sample Prompts WITHOUT PII:")
    print("-" * 40)
    for i, sample in enumerate(non_pii_samples, 1):
        print(f"{i}. {sample['prompt']}")
        print()
    
    # Summary statistics
    total = len(dataset)
    with_pii = sum(1 for item in dataset if item['contains_pii'])
    without_pii = total - with_pii
    
    print(f"Final Statistics:")
    print(f"Total prompts: {total}")
    print(f"With PII: {with_pii} ({with_pii/total*100:.1f}%)")
    print(f"Without PII: {without_pii} ({without_pii/total*100:.1f}%)")

if __name__ == "__main__":
    main() 