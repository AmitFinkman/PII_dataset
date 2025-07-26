import json
import re
from faker import Faker
from faker.providers import BaseProvider
import pandas as pd
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Custom provider for financial services data
class FinancialProvider(BaseProvider):
    """Custom Faker provider for financial services data"""
    
    def __init__(self, generator):
        super().__init__(generator)
        
        # Account type specific transaction patterns
        self.account_transactions = {
            'Checking': ['Direct Deposit', 'Debit Purchase', 'ATM Withdrawal', 'Bill Payment', 'Transfer', 'Check Payment'],
            'Savings': ['Interest Payment', 'Transfer In', 'Transfer Out', 'Deposit', 'Withdrawal'],
            'Credit Card': ['Purchase', 'Payment', 'Cash Advance', 'Interest Charge', 'Fee', 'Refund'],
            'Investment': ['Stock Purchase', 'Stock Sale', 'Dividend', 'Bond Purchase', 'Mutual Fund', 'Fee'],
            'Mortgage': ['Payment', 'Interest', 'Escrow', 'Principal', 'Late Fee'],
            'Auto Loan': ['Payment', 'Interest', 'Principal', 'Late Fee', 'Insurance Payment'],
            'Personal Loan': ['Payment', 'Interest', 'Principal', 'Late Fee'],
            'Business': ['Wire Transfer', 'ACH Payment', 'Merchant Deposit', 'Fee', 'Payroll', 'Tax Payment']
        }
        
        # Income bracket to account type relationships
        self.income_account_mapping = {
            'Under $30k': ['Checking', 'Savings'],
            '$30k-$50k': ['Checking', 'Savings', 'Credit Card'],
            '$50k-$75k': ['Checking', 'Savings', 'Credit Card', 'Auto Loan'],
            '$75k-$100k': ['Checking', 'Savings', 'Credit Card', 'Investment', 'Auto Loan'],
            '$100k-$150k': ['Checking', 'Savings', 'Credit Card', 'Investment', 'Mortgage', 'Auto Loan'],
            '$150k+': ['Checking', 'Savings', 'Credit Card', 'Investment', 'Mortgage', 'Personal Loan', 'Business']
        }
        
        # Credit score to product relationships
        self.credit_products = {
            'Excellent (750+)': ['Premium Credit Card', 'Mortgage', 'Personal Loan', 'Business Loan'],
            'Good (700-749)': ['Standard Credit Card', 'Mortgage', 'Auto Loan', 'Personal Loan'],
            'Fair (650-699)': ['Secured Credit Card', 'Auto Loan', 'Personal Loan'],
            'Poor (600-649)': ['Secured Credit Card', 'Payday Loan'],
            'Bad (Below 600)': ['Prepaid Card', 'Payday Loan']
        }
        
        # Employment sectors
        self.employment_sectors = [
            'Technology', 'Healthcare', 'Finance', 'Education', 'Government', 
            'Retail', 'Manufacturing', 'Construction', 'Real Estate', 'Legal',
            'Consulting', 'Non-Profit', 'Entertainment', 'Transportation', 'Energy'
        ]
        
        # Investment types by risk profile
        self.investment_products = {
            'Conservative': ['Savings Account', 'CD', 'Government Bonds', 'Money Market'],
            'Moderate': ['Mutual Funds', 'Corporate Bonds', 'Balanced Portfolio', 'Index Funds'],
            'Aggressive': ['Individual Stocks', 'Options', 'Crypto', 'Growth Funds', 'REITs']
        }
        
        # Bank branches by region
        self.bank_branches = {
            'Northeast': ['New York Main', 'Boston Financial', 'Philadelphia Center', 'Newark Business'],
            'Southeast': ['Atlanta Metro', 'Miami Beach', 'Charlotte Uptown', 'Jacksonville East'],
            'Midwest': ['Chicago Loop', 'Detroit Downtown', 'Minneapolis Central', 'Cleveland Heights'],
            'Southwest': ['Dallas North', 'Houston Energy', 'Austin Tech', 'San Antonio River'],
            'West': ['Los Angeles Beverly', 'San Francisco Financial', 'Seattle Tech', 'Denver Mile High']
        }
        
        # Common email domains for financial customers
        self.email_domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'icloud.com', 'aol.com', 'comcast.net']
        
        # Demographics
        self.income_brackets = list(self.income_account_mapping.keys())
        self.credit_scores = list(self.credit_products.keys())
        self.risk_profiles = list(self.investment_products.keys())
        self.regions = list(self.bank_branches.keys())
    
    def account_number(self):
        """Generate realistic account number"""
        return f"{self.random_int(100000000, 999999999)}"
    
    def routing_number(self):
        """Generate realistic routing number"""
        return f"{self.random_int(100000000, 199999999)}"
    
    def credit_card_number(self):
        """Generate realistic credit card number (fake)"""
        # Visa format: 4xxx-xxxx-xxxx-xxxx
        return f"4{self.random_int(100, 999)}-{self.random_int(1000, 9999)}-{self.random_int(1000, 9999)}-{self.random_int(1000, 9999)}"
    
    def ssn(self):
        """Generate SSN"""
        return f"{self.random_int(100, 999)}-{self.random_int(10, 99)}-{self.random_int(1000, 9999)}"
    
    def income_bracket(self):
        """Generate income bracket"""
        return self.random_element(self.income_brackets)
    
    def credit_score_category(self):
        """Generate credit score category"""
        return self.random_element(self.credit_scores)
    
    def employment_sector(self):
        """Generate employment sector"""
        return self.random_element(self.employment_sectors)
    
    def risk_profile(self):
        """Generate investment risk profile"""
        return self.random_element(self.risk_profiles)
    
    def region(self):
        """Generate region"""
        return self.random_element(self.regions)
    
    def bank_branch(self, region):
        """Generate bank branch for region"""
        if region in self.bank_branches:
            return self.random_element(self.bank_branches[region])
        return self.random_element(self.bank_branches['Northeast'])
    
    def account_types_for_income(self, income_bracket):
        """Generate account types based on income"""
        if income_bracket in self.income_account_mapping:
            available_accounts = self.income_account_mapping[income_bracket]
            num_accounts = self.random_int(1, min(4, len(available_accounts)))
            return self.random_elements(available_accounts, length=num_accounts, unique=True)
        return ['Checking']
    
    def transaction_type_for_account(self, account_type):
        """Generate transaction type based on account"""
        if account_type in self.account_transactions:
            return self.random_element(self.account_transactions[account_type])
        return 'Transaction'
    
    def investment_for_risk_profile(self, risk_profile):
        """Generate investment based on risk profile"""
        if risk_profile in self.investment_products:
            return self.random_element(self.investment_products[risk_profile])
        return 'Savings Account'
    
    def create_realistic_email(self, first_name, last_name):
        """Create realistic email based on person's name"""
        domain = self.random_element(self.email_domains)
        
        formats = [
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}{last_name.lower()}",
            f"{first_name[0].lower()}{last_name.lower()}",
            f"{first_name.lower()}{last_name[0].lower()}",
            f"{first_name.lower()}.{last_name.lower()}{self.random_int(1, 999)}",
            f"{first_name.lower()}{self.random_int(1, 999)}"
        ]
        
        username = self.random_element(formats)
        return f"{username}@{domain}"
    
    def customer_segment(self):
        """Generate customer segment"""
        segments = ['Mass Market', 'Affluent', 'High Net Worth', 'Private Banking', 'Business', 'Small Business']
        return self.random_element(segments)
    
    def relationship_length(self):
        """Generate relationship length with bank"""
        return self.random_int(1, 25)
    
    def loan_purpose(self):
        """Generate loan purpose"""
        purposes = ['Home Purchase', 'Refinance', 'Home Improvement', 'Debt Consolidation', 'Education', 'Business Expansion', 'Equipment Purchase']
        return self.random_element(purposes)

class FinancialDatasetGenerator:
    def __init__(self, seed=42):
        """Initialize the financial dataset generator"""
        self.fake = Faker()
        self.fake.add_provider(FinancialProvider)
        Faker.seed(seed)
        
        # Build dynamic patterns for PII detection
        provider = [p for p in self.fake.providers if isinstance(p, FinancialProvider)][0]
        all_sectors = provider.employment_sectors
        all_segments = ['Mass Market', 'Affluent', 'High Net Worth', 'Private Banking', 'Business', 'Small Business']
        all_account_types = list(set([acc for acc_list in provider.income_account_mapping.values() for acc in acc_list]))
        
        # PII type definitions for financial data
        self.pii_types = {
            'PERSON_NAME': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b\d{3}-\d{3}-\d{4}\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'ADDRESS': r'\d+\s+\w+\s+\w+',
            'DATE_OF_BIRTH': r'\b\d{2}/\d{2}/\d{4}\b',
            'ACCOUNT_NUMBER': r'\b\d{9}\b',
            'ROUTING_NUMBER': r'\b1\d{8}\b',
            'CREDIT_CARD': r'\b4\d{3}-\d{4}-\d{4}-\d{4}\b',
            'ZIP_CODE': r'\b\d{5}\b',
            'INCOME_BRACKET': r'\b(\$\d+k-\$\d+k|Under \$\d+k|\$\d+k\+)\b',
            'CREDIT_SCORE': r'\b(Excellent|Good|Fair|Poor|Bad)\s*\(\d+[-\+]*\d*\)\b',
            'EMPLOYMENT_SECTOR': r'\b(' + '|'.join(all_sectors) + r')\b',
            'CUSTOMER_SEGMENT': r'\b(' + '|'.join(all_segments) + r')\b',
            'ACCOUNT_TYPE': r'\b(' + '|'.join(all_account_types) + r')\b',
            'TRANSACTION_AMOUNT': r'\$\d+\.\d{2}',
            'BANK_BRANCH': r'\b\w+\s+(Main|Financial|Center|Business|Metro|Beach|Uptown|East|Loop|Downtown|Central|Heights|North|Energy|Tech|River|Beverly|Mile High)\b',
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
    
    def generate_customer_record(self):
        """Generate a single customer record with financial data"""
        # Generate basic customer information
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        
        # Generate demographics
        birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
        ssn = self.fake.ssn()
        email = self.fake.create_realistic_email(first_name, last_name)
        phone = self.fake.phone_number()
        address = self.fake.address().replace('\n', ', ')
        
        # Generate financial profile
        income_bracket = self.fake.income_bracket()
        credit_score_category = self.fake.credit_score_category()
        employment_sector = self.fake.employment_sector()
        risk_profile = self.fake.risk_profile()
        customer_segment = self.fake.customer_segment()
        relationship_length = self.fake.relationship_length()
        
        # Generate location and branch
        region = self.fake.region()
        bank_branch = self.fake.bank_branch(region)
        
        # Generate accounts based on income
        account_types = self.fake.account_types_for_income(income_bracket)
        primary_account_type = account_types[0] if account_types else 'Checking'
        
        # Generate account details
        account_number = self.fake.account_number()
        routing_number = self.fake.routing_number()
        
        # Generate additional financial products
        if 'Credit Card' in account_types:
            credit_card_number = self.fake.credit_card_number()
        else:
            credit_card_number = None
        
        # Generate recent transaction
        transaction_type = self.fake.transaction_type_for_account(primary_account_type)
        transaction_amount = round(random.uniform(10.00, 5000.00), 2)
        transaction_date = self.fake.date_between(start_date='-30d', end_date='today')
        
        # Generate investment if applicable
        investment_product = None
        if 'Investment' in account_types:
            investment_product = self.fake.investment_for_risk_profile(risk_profile)
        
        # Generate loan details if applicable
        loan_purpose = None
        loan_amount = None
        if any(loan_type in account_types for loan_type in ['Mortgage', 'Auto Loan', 'Personal Loan']):
            loan_purpose = self.fake.loan_purpose()
            loan_amount = round(random.uniform(5000.00, 500000.00), 2)
        
        # Generate advisor information
        advisor_first = self.fake.first_name()
        advisor_last = self.fake.last_name()
        advisor_name = f"{advisor_first} {advisor_last}"
        advisor_email = self.fake.create_realistic_email(advisor_first, advisor_last)
        
        # Create comprehensive financial record with consistent structure
        record_text = f"""
CUSTOMER PROFILE - PREMIER FINANCIAL SERVICES
Branch: {bank_branch} ({region} Region)

PERSONAL INFORMATION:
Name: {full_name}
Date of Birth: {birth_date.strftime('%m/%d/%Y')}
SSN: {ssn}
Address: {address}
Phone: {phone}
Email: {email}
Employment Sector: {employment_sector}

FINANCIAL PROFILE:
Customer Segment: {customer_segment}
Income Bracket: {income_bracket}
Credit Score: {credit_score_category}
Risk Profile: {risk_profile}
Relationship Length: {relationship_length} years

ACCOUNT INFORMATION:
Primary Account Type: {primary_account_type}
Account Number: {account_number}
Routing Number: {routing_number}
All Account Types: {', '.join(account_types)}
Credit Card: {credit_card_number if credit_card_number else 'Not Available'}

RECENT ACTIVITY:
Transaction Type: {transaction_type}
Amount: ${transaction_amount:.2f}
Date: {transaction_date.strftime('%m/%d/%Y')}
Investment Product: {investment_product if investment_product else 'Not Available'}
Loan Purpose: {loan_purpose if loan_purpose else 'Not Available'}
Loan Amount: {f'${loan_amount:.2f}' if loan_amount else 'Not Available'}

RELATIONSHIP MANAGER:
Name: {advisor_name}
Email: {advisor_email}
Branch: {bank_branch}

ACCOUNT SUMMARY:
Customer {full_name} has been with Premier Financial Services for {relationship_length} years.
Primary contact: {phone}, {email}
Current portfolio includes: {', '.join(account_types)}
Risk tolerance: {risk_profile}
Preferred branch: {bank_branch} in {region}
Recent transaction: {transaction_type} for ${transaction_amount:.2f} on {transaction_date.strftime('%m/%d/%Y')}
Account managed by {advisor_name} ({advisor_email})
        """.strip()
        
        # Find PII in the record
        pii_findings = self.find_pii_in_text(record_text)
        
        # Create structured record
        record = {
            'customer_id': self.fake.uuid4(),
            'customer_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': birth_date.strftime('%m/%d/%Y'),
            'age': (datetime.now().date() - birth_date).days // 365,
            'ssn': ssn,
            'address': address,
            'phone': phone,
            'email': email,
            'employment_sector': employment_sector,
            'income_bracket': income_bracket,
            'credit_score_category': credit_score_category,
            'risk_profile': risk_profile,
            'customer_segment': customer_segment,
            'relationship_length': relationship_length,
            'region': region,
            'bank_branch': bank_branch,
            'account_types': account_types,
            'primary_account_type': primary_account_type,
            'account_number': account_number,
            'routing_number': routing_number,
            'credit_card_number': credit_card_number,
            'recent_transaction_type': transaction_type,
            'recent_transaction_amount': transaction_amount,
            'recent_transaction_date': transaction_date.strftime('%m/%d/%Y'),
            'investment_product': investment_product,
            'loan_purpose': loan_purpose,
            'loan_amount': loan_amount,
            'advisor_name': advisor_name,
            'advisor_email': advisor_email,
            'full_record_text': record_text,
            'pii_findings': pii_findings,
            'pii_count': len(pii_findings),
            'unique_pii_types': list(set([finding['pii_type'] for finding in pii_findings]))
        }
        
        return record
    
    def generate_dataset(self, num_records=1000):
        """Generate a complete financial services dataset"""
        print(f"Generating {num_records} financial services customer records...")
        
        records = []
        for i in range(num_records):
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{num_records} records...")
            
            record = self.generate_customer_record()
            records.append(record)
        
        return records
    
    def save_dataset(self, records, filename_prefix='financial_dataset'):
        """Save the dataset in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as JSON
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(records, f, indent=2, default=str)
        print(f"Dataset saved as JSON: {json_filename}")
        
        # Save as CSV (flattened version)
        csv_records = []
        for record in records:
            csv_record = record.copy()
            csv_record['pii_findings'] = json.dumps(record['pii_findings'])
            csv_record['unique_pii_types'] = ', '.join(record['unique_pii_types'])
            csv_record['account_types'] = ', '.join(record['account_types'])
            csv_records.append(csv_record)
        
        df = pd.DataFrame(csv_records)
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dataset saved as CSV: {csv_filename}")
        
        # Generate summary statistics
        self.generate_summary_report(records, f"{filename_prefix}_summary_{timestamp}.txt")
        
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
        
        # Collect financial statistics
        income_brackets = [r['income_bracket'] for r in records]
        credit_scores = [r['credit_score_category'] for r in records]
        employment_sectors = [r['employment_sector'] for r in records]
        customer_segments = [r['customer_segment'] for r in records]
        regions = [r['region'] for r in records]
        
        with open(filename, 'w') as f:
            f.write("FINANCIAL SERVICES DATASET - COMPREHENSIVE ANALYSIS REPORT\n")
            f.write("="*75 + "\n\n")
            f.write(f"Total Customer Records: {len(records)}\n")
            f.write(f"Total PII Instances Found: {total_pii_instances}\n")
            f.write(f"Average PII per Record: {total_pii_instances/len(records):.2f}\n\n")
            
            f.write("PII Type Distribution:\n")
            f.write("-" * 30 + "\n")
            for pii_type, count in sorted(pii_type_counts.items()):
                percentage = (count / total_pii_instances) * 100
                f.write(f"{pii_type}: {count} ({percentage:.1f}%)\n")
            
            # Financial demographics
            f.write(f"\nFINANCIAL DEMOGRAPHICS:\n")
            f.write("=" * 30 + "\n")
            
            f.write(f"\nIncome Distribution:\n")
            for income in set(income_brackets):
                count = income_brackets.count(income)
                percentage = (count / len(records)) * 100
                f.write(f"  {income}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nCredit Score Distribution:\n")
            for score in set(credit_scores):
                count = credit_scores.count(score)
                percentage = (count / len(records)) * 100
                f.write(f"  {score}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nEmployment Sector Distribution:\n")
            for sector in set(employment_sectors):
                count = employment_sectors.count(sector)
                percentage = (count / len(records)) * 100
                f.write(f"  {sector}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nCustomer Segment Distribution:\n")
            for segment in set(customer_segments):
                count = customer_segments.count(segment)
                percentage = (count / len(records)) * 100
                f.write(f"  {segment}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nRegional Distribution:\n")
            for region in set(regions):
                count = regions.count(region)
                percentage = (count / len(records)) * 100
                f.write(f"  {region}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nDATASET FEATURES:\n")
            f.write("=" * 20 + "\n")
            f.write(f"✓ Income-based account type relationships\n")
            f.write(f"✓ Credit score product eligibility matching\n")
            f.write(f"✓ Risk profile investment alignment\n")
            f.write(f"✓ Regional branch assignments\n")
            f.write(f"✓ Realistic transaction patterns\n")
            f.write(f"✓ Name-based email generation\n")
            f.write(f"✓ Comprehensive PII detection ({len(self.pii_types)} types)\n")
            
            f.write(f"\nSample PII Findings from First Record:\n")
            f.write("-" * 40 + "\n")
            if records:
                for finding in records[0]['pii_findings'][:20]:
                    f.write(f"Type: {finding['pii_type']}, Value: {finding['value']}, "
                           f"Position: {finding['start_index']}-{finding['end_index']}\n")
        
        print(f"Financial services summary report saved: {filename}")

def main():
    """Main function to generate the financial services dataset"""
    print("Financial Services Dataset Generator")
    print("="*45)
    print("Features:")
    print("✓ Income-based account type relationships")
    print("✓ Credit score to product eligibility mapping")
    print("✓ Risk profile investment alignment")
    print("✓ Regional branch assignments")
    print("✓ Realistic transaction patterns")
    print("✓ Name-based email generation")
    print("✓ Comprehensive PII detection and indexing")
    print()
    
    # Initialize generator
    generator = FinancialDatasetGenerator(seed=42)
    
    # Generate dataset
    num_records = 500
    records = generator.generate_dataset(num_records)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(records)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(records)} financial customer records")
    print(f"Files created: {json_file}, {csv_file}")
    
    # Display sample record
    print(f"\nSample Record (first record):")
    print("-" * 60)
    sample = records[0]
    print(f"Customer: {sample['customer_name']} ({sample['employment_sector']})")
    print(f"Email: {sample['email']} (name-based)")
    print(f"Income Bracket: {sample['income_bracket']}")
    print(f"Credit Score: {sample['credit_score_category']}")
    print(f"Account Types: {', '.join(sample['account_types'])} (income-matched)")
    print(f"Region: {sample['region']} - Branch: {sample['bank_branch']}")
    print(f"Investment Risk: {sample['risk_profile']}")
    print(f"Advisor: {sample['advisor_name']} ({sample['advisor_email']})")
    print(f"PII Types Found: {', '.join(sample['unique_pii_types'])}")
    print(f"Total PII Count: {sample['pii_count']}")
    
    print(f"\nSample Record Text (first 400 chars):")
    print(sample['full_record_text'][:400] + "...")
    
    # Show income-account relationships
    print(f"\nIncome-Account Relationship Examples:")
    print("-" * 50)
    income_examples = {}
    for record in records[:10]:
        income = record['income_bracket']
        accounts = ', '.join(record['account_types'])
        if income not in income_examples:
            income_examples[income] = accounts
    
    for income, accounts in income_examples.items():
        print(f"{income}: {accounts}")

if __name__ == "__main__":
    main() 