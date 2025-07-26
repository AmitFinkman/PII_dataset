import json
import re
from faker import Faker
from faker.providers import BaseProvider
import pandas as pd
from datetime import datetime, timedelta
import random

# Custom provider for medical-specific data
class MedicalProvider(BaseProvider):
    """Custom Faker provider for medical organization data"""
    
    def __init__(self, generator):
        super().__init__(generator)
        
        # Department-specific medications mapping for realistic relationships
        self.dept_medications = {
            'Cardiology': ['Lisinopril', 'Metoprolol', 'Atorvastatin', 'Amlodipine', 'Losartan', 'Carvedilol', 'Warfarin', 'Clopidogrel'],
            'Neurology': ['Levetiracetam', 'Gabapentin', 'Donepezil', 'Carbidopa-Levodopa', 'Topiramate', 'Lamotrigine', 'Phenytoin'],
            'Orthopedics': ['Ibuprofen', 'Naproxen', 'Celecoxib', 'Tramadol', 'Meloxicam', 'Diclofenac', 'Prednisone'],
            'Pediatrics': ['Amoxicillin', 'Azithromycin', 'Albuterol', 'Fluticasone', 'Acetaminophen', 'Ibuprofen', 'Prednisolone'],
            'Emergency Medicine': ['Morphine', 'Epinephrine', 'Atropine', 'Naloxone', 'Lorazepam', 'Fentanyl', 'Midazolam'],
            'Internal Medicine': ['Metformin', 'Omeprazole', 'Simvastatin', 'Hydrochlorothiazide', 'Levothyroxine', 'Sertraline'],
            'Psychiatry': ['Sertraline', 'Fluoxetine', 'Escitalopram', 'Risperidone', 'Quetiapine', 'Lithium', 'Clonazepam'],
            'Radiology': ['Iodinated contrast', 'Gadolinium', 'Barium sulfate', 'Lorazepam', 'Diphenhydramine'],
            'Oncology': ['Doxorubicin', 'Cisplatin', 'Paclitaxel', 'Carboplatin', 'Methotrexate', 'Cyclophosphamide'],
            'Endocrinology': ['Metformin', 'Insulin', 'Levothyroxine', 'Glipizide', 'Pioglitazone', 'Empagliflozin'],
            'Pulmonology': ['Albuterol', 'Fluticasone', 'Montelukast', 'Tiotropium', 'Prednisone', 'Azithromycin'],
            'Gastroenterology': ['Omeprazole', 'Mesalamine', 'Infliximab', 'Adalimumab', 'Lactulose', 'Rifaximin']
        }
        
        # Department-specific diagnosis codes
        self.dept_diagnoses = {
            'Cardiology': ['I21.9', 'I25.10', 'I50.9', 'I10', 'I48.91', 'I35.0', 'I42.9'],
            'Neurology': ['G93.1', 'G40.909', 'F03.90', 'G20', 'G35', 'G43.909', 'G47.00'],
            'Orthopedics': ['M79.18', 'S72.001A', 'M25.511', 'M17.12', 'M48.06', 'S83.511A'],
            'Pediatrics': ['J06.9', 'K59.00', 'J45.9', 'L20.9', 'R50.9', 'Z00.121'],
            'Emergency Medicine': ['R06.02', 'R50.9', 'S06.0X0A', 'T39.1X1A', 'Z87.891'],
            'Internal Medicine': ['E11.9', 'I10', 'K21.9', 'E78.5', 'E03.9', 'F32.9'],
            'Psychiatry': ['F32.9', 'F41.1', 'F84.0', 'F20.9', 'F31.9', 'F43.10'],
            'Radiology': ['Z51.0', 'R93.1', 'Z12.31', 'R91.1'],
            'Oncology': ['C78.00', 'C50.911', 'C25.9', 'Z51.11', 'C34.10'],
            'Endocrinology': ['E11.9', 'E03.9', 'E66.9', 'E78.5', 'E10.9'],
            'Pulmonology': ['J44.1', 'J45.9', 'J18.9', 'J84.10', 'Z87.891'],
            'Gastroenterology': ['K21.9', 'K50.90', 'K72.90', 'K92.2', 'K59.00']
        }
        
        # Common email domains
        self.email_domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'icloud.com', 'aol.com']
        
        # Expanded department list
        self.departments = list(self.dept_medications.keys())
        
        # Ethnicity and cultural diversity
        self.ethnicities = ['Caucasian', 'African American', 'Hispanic/Latino', 'Asian', 'Native American', 'Pacific Islander', 'Mixed']
        
        # Insurance providers
        self.insurance_providers = ['Blue Cross Blue Shield', 'UnitedHealthcare', 'Anthem', 'Aetna', 'Cigna', 'Humana', 'Kaiser Permanente', 'Medicare', 'Medicaid']
    
    def medical_record_number(self):
        """Generate a medical record number"""
        return f"MRN-{self.random_int(100000, 999999)}"
    
    def insurance_id(self):
        """Generate an insurance ID"""
        return f"INS-{self.random_int(1000000, 9999999)}"
    
    def department_name(self):
        """Generate medical department names"""
        return self.random_element(self.departments)
    
    def medication_for_department(self, department):
        """Generate medication based on department"""
        if department in self.dept_medications:
            return self.random_element(self.dept_medications[department])
        return self.random_element(self.dept_medications['Internal Medicine'])
    
    def diagnosis_for_department(self, department):
        """Generate diagnosis code based on department"""
        if department in self.dept_diagnoses:
            return self.random_element(self.dept_diagnoses[department])
        return self.random_element(self.dept_diagnoses['Internal Medicine'])
    
    def create_realistic_email(self, first_name, last_name):
        """Create realistic email based on person's name"""
        domain = self.random_element(self.email_domains)
        
        # Different email formats
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
    
    def ethnicity(self):
        """Generate ethnicity"""
        return self.random_element(self.ethnicities)
    
    def insurance_provider(self):
        """Generate insurance provider"""
        return self.random_element(self.insurance_providers)
    
    def emergency_contact_relationship(self):
        """Generate emergency contact relationship"""
        relationships = ['Spouse', 'Parent', 'Child', 'Sibling', 'Friend', 'Other Family']
        return self.random_element(relationships)
    
    def severity_level(self):
        """Generate condition severity"""
        levels = ['Mild', 'Moderate', 'Severe', 'Critical']
        return self.random_element(levels)
    
    def hospital_type(self):
        """Generate hospital types for variety"""
        types = ['Medical Center', 'General Hospital', 'Regional Hospital', 'University Hospital', 'Community Hospital', 'Specialty Center']
        return self.random_element(types)

class MedicalDatasetGenerator:
    def __init__(self, seed=42):
        """Initialize the medical dataset generator"""
        self.fake = Faker()
        self.fake.add_provider(MedicalProvider)
        Faker.seed(seed)
        
        # Build dynamic medication pattern from all department medications
        all_medications = []
        for dept_meds in self.fake.dept_medications.values():
            all_medications.extend(dept_meds)
        unique_medications = list(set(all_medications))
        medication_pattern = r'\b(' + '|'.join(re.escape(med) for med in unique_medications) + r')\b'
        
        # PII type definitions
        self.pii_types = {
            'PERSON_NAME': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b\d{3}-\d{3}-\d{4}\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'ADDRESS': r'\d+\s+\w+\s+\w+',
            'DATE_OF_BIRTH': r'\b\d{2}/\d{2}/\d{4}\b',
            'MEDICAL_RECORD_NUMBER': r'MRN-\d{6}',
            'INSURANCE_ID': r'INS-\d{7}',
            'ZIP_CODE': r'\b\d{5}\b',
            'BLOOD_TYPE': r'\b[ABO][\+\-]|AB[\+\-]\b',
            'ETHNICITY': r'\b(Caucasian|African American|Hispanic/Latino|Asian|Native American|Pacific Islander|Mixed)\b',
            'INSURANCE_PROVIDER': r'\b(Blue Cross Blue Shield|UnitedHealthcare|Anthem|Aetna|Cigna|Humana|Kaiser Permanente|Medicare|Medicaid)\b',
            'MEDICATION_NAME': medication_pattern,
            'DIAGNOSIS_CODE': r'\b[A-Z]\d{2}\.\d+[A-Z]?\b',
            'DEPARTMENT': r'\b(Cardiology|Neurology|Orthopedics|Pediatrics|Emergency Medicine|Internal Medicine|Psychiatry|Radiology|Oncology|Endocrinology|Pulmonology|Gastroenterology)\b',
            'SEVERITY_LEVEL': r'\b(Mild|Moderate|Severe|Critical)\b',
            'ALLERGY': r'\b(Penicillin|Peanuts|Shellfish|Latex|Iodine|None Known)\b',
            'RELATIONSHIP': r'\b(Spouse|Parent|Child|Sibling|Friend|Other Family)\b'
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
    
    def generate_patient_record(self):
        """Generate a single patient record with medical organization data"""
        # Generate basic patient information
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        
        # Generate dates
        birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=90)
        admission_date = self.fake.date_between(start_date='-2y', end_date='today')
        
        # Generate contact information with realistic email
        email = self.fake.create_realistic_email(first_name, last_name)
        phone = self.fake.phone_number()
        address = self.fake.address().replace('\n', ', ')
        
        # Generate diverse patient data
        ethnicity = self.fake.ethnicity()
        insurance_provider = self.fake.insurance_provider()
        
        # Generate medical information with department relationships
        department = self.fake.department_name()
        medication = self.fake.medication_for_department(department)
        diagnosis = self.fake.diagnosis_for_department(department)
        severity = self.fake.severity_level()
        
        # Generate medical IDs
        mrn = self.fake.medical_record_number()
        insurance_id = self.fake.insurance_id()
        
        # Generate provider information with realistic email
        provider_first = self.fake.first_name()
        provider_last = self.fake.last_name()
        provider_name = f"Dr. {provider_first} {provider_last}"
        provider_email = self.fake.create_realistic_email(provider_first, provider_last)
        
        # Generate emergency contact
        emergency_first = self.fake.first_name()
        emergency_last = self.fake.last_name()
        emergency_name = f"{emergency_first} {emergency_last}"
        emergency_relationship = self.fake.emergency_contact_relationship()
        emergency_phone = self.fake.phone_number()
        emergency_email = self.fake.create_realistic_email(emergency_first, emergency_last)
        
        # Generate organization information
        hospital_type = self.fake.hospital_type()
        hospital_name = f"{self.fake.city()} {hospital_type}"
        hospital_address = self.fake.address().replace('\n', ', ')
        hospital_phone = self.fake.phone_number()
        
        # Additional medical details
        allergies = self.fake.random_elements(['Penicillin', 'Peanuts', 'Shellfish', 'Latex', 'Iodine', 'None Known'], length=self.fake.random_int(0, 2))
        blood_type = self.fake.random_element(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
        
        # Create comprehensive medical record text
        record_text = f"""
PATIENT RECORD - {hospital_name}
Hospital Phone: {hospital_phone}

PATIENT INFORMATION:
Name: {full_name}
Date of Birth: {birth_date.strftime('%m/%d/%Y')}
SSN: {self.fake.ssn()}
Ethnicity: {ethnicity}
Blood Type: {blood_type}
Address: {address}
Phone: {phone}
Email: {email}
Medical Record Number: {mrn}

INSURANCE INFORMATION:
Provider: {insurance_provider}
Insurance ID: {insurance_id}

MEDICAL INFORMATION:
Department: {department}
Attending Physician: {provider_name}
Physician Email: {provider_email}
Admission Date: {admission_date.strftime('%m/%d/%Y')}
Primary Diagnosis: {diagnosis}
Condition Severity: {severity}
Current Medication: {medication}
Known Allergies: {', '.join(allergies) if allergies else 'None Known'}

EMERGENCY CONTACT:
Name: {emergency_name}
Relationship: {emergency_relationship}
Phone: {emergency_phone}
Email: {emergency_email}

HOSPITAL INFORMATION:
Facility: {hospital_name}
Address: {hospital_address}
Phone: {hospital_phone}

CLINICAL NOTES:
Patient {full_name} was admitted to {department} on {admission_date.strftime('%m/%d/%Y')} under the care of {provider_name}.
Current treatment includes {medication} for {diagnosis} with {severity.lower()} severity.
Contact information on file: {phone} and {email}.
Emergency contact: {emergency_name} ({emergency_relationship}) - {emergency_phone}, {emergency_email}.
Insurance coverage through {insurance_provider} (ID: {insurance_id}).
Patient ethnicity: {ethnicity}, Blood type: {blood_type}.
Known allergies: {', '.join(allergies) if allergies else 'None'}.
        """.strip()
        
        # Find PII in the record
        pii_findings = self.find_pii_in_text(record_text)
        
        # Create structured record
        record = {
            'record_id': self.fake.uuid4(),
            'patient_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': birth_date.strftime('%m/%d/%Y'),
            'age': (datetime.now().date() - birth_date).days // 365,
            'ethnicity': ethnicity,
            'blood_type': blood_type,
            'ssn': self.fake.ssn(),
            'address': address,
            'phone': phone,
            'email': email,
            'medical_record_number': mrn,
            'insurance_provider': insurance_provider,
            'insurance_id': insurance_id,
            'department': department,
            'provider_name': provider_name,
            'provider_email': provider_email,
            'hospital_name': hospital_name,
            'hospital_type': hospital_type,
            'hospital_address': hospital_address,
            'hospital_phone': hospital_phone,
            'admission_date': admission_date.strftime('%m/%d/%Y'),
            'diagnosis_code': diagnosis,
            'condition_severity': severity,
            'medication': medication,
            'allergies': allergies,
            'emergency_contact_name': emergency_name,
            'emergency_contact_relationship': emergency_relationship,
            'emergency_contact_phone': emergency_phone,
            'emergency_contact_email': emergency_email,
            'full_record_text': record_text,
            'pii_findings': pii_findings,
            'pii_count': len(pii_findings),
            'unique_pii_types': list(set([finding['pii_type'] for finding in pii_findings]))
        }
        
        return record
    
    def generate_dataset(self, num_records=1000):
        """Generate a complete medical organization dataset"""
        print(f"Generating {num_records} medical organization records...")
        
        records = []
        for i in range(num_records):
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{num_records} records...")
            
            record = self.generate_patient_record()
            records.append(record)
        
        return records
    
    def save_dataset(self, records, filename_prefix='medical_org_dataset'):
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
            # Convert PII findings to summary
            csv_record['pii_findings'] = json.dumps(record['pii_findings'])
            csv_record['unique_pii_types'] = ', '.join(record['unique_pii_types'])
            csv_records.append(csv_record)
        
        df = pd.DataFrame(csv_records)
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dataset saved as CSV: {csv_filename}")
        
        # Generate summary statistics
        self.generate_summary_report(records, f"{filename_prefix}_summary_{timestamp}.txt")
        
        return json_filename, csv_filename
    
    def generate_summary_report(self, records, filename):
        """Generate a summary report of PII findings"""
        pii_type_counts = {}
        total_pii_instances = 0
        
        for record in records:
            for finding in record['pii_findings']:
                pii_type = finding['pii_type']
                pii_type_counts[pii_type] = pii_type_counts.get(pii_type, 0) + 1
                total_pii_instances += 1
        
        # Collect diversity statistics
        ethnicities = [r['ethnicity'] for r in records]
        departments = [r['department'] for r in records]
        insurance_providers = [r['insurance_provider'] for r in records]
        blood_types = [r['blood_type'] for r in records]
        medications = [r['medication'] for r in records]
        
        with open(filename, 'w') as f:
            f.write("ENHANCED MEDICAL ORGANIZATION DATASET - ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Total Records Generated: {len(records)}\n")
            f.write(f"Total PII Instances Found: {total_pii_instances}\n")
            f.write(f"Average PII per Record: {total_pii_instances/len(records):.2f}\n\n")
            
            f.write("PII Type Distribution:\n")
            f.write("-" * 30 + "\n")
            for pii_type, count in sorted(pii_type_counts.items()):
                percentage = (count / total_pii_instances) * 100
                f.write(f"{pii_type}: {count} ({percentage:.1f}%)\n")
            
            # Diversity statistics
            f.write(f"\nDIVERSITY STATISTICS:\n")
            f.write("=" * 30 + "\n")
            
            f.write(f"\nEthnicity Distribution:\n")
            for ethnicity in set(ethnicities):
                count = ethnicities.count(ethnicity)
                percentage = (count / len(records)) * 100
                f.write(f"  {ethnicity}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nDepartment Distribution:\n")
            for dept in set(departments):
                count = departments.count(dept)
                percentage = (count / len(records)) * 100
                f.write(f"  {dept}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nInsurance Provider Distribution:\n")
            for provider in set(insurance_providers):
                count = insurance_providers.count(provider)
                percentage = (count / len(records)) * 100
                f.write(f"  {provider}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nBlood Type Distribution:\n")
            for blood_type in set(blood_types):
                count = blood_types.count(blood_type)
                percentage = (count / len(records)) * 100
                f.write(f"  {blood_type}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nTop 10 Medications:\n")
            from collections import Counter
            med_counts = Counter(medications)
            for med, count in med_counts.most_common(10):
                percentage = (count / len(records)) * 100
                f.write(f"  {med}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nDATASET FEATURES:\n")
            f.write("=" * 20 + "\n")
            f.write(f"✓ Realistic department-medication relationships\n")
            f.write(f"✓ Name-based emails with common domains\n")
            f.write(f"✓ Diverse patient demographics\n")
            f.write(f"✓ Emergency contacts and detailed medical info\n")
            f.write(f"✓ Comprehensive PII detection ({len(self.pii_types)} types)\n")
            
            f.write(f"\nSample PII Findings from First Record:\n")
            f.write("-" * 40 + "\n")
            if records:
                for finding in records[0]['pii_findings'][:15]:  # Show first 15 findings
                    f.write(f"Type: {finding['pii_type']}, Value: {finding['value']}, "
                           f"Position: {finding['start_index']}-{finding['end_index']}\n")
        
        print(f"Comprehensive summary report saved: {filename}")

def main():
    """Main function to generate the medical organization dataset"""
    print("Enhanced Medical Organization Dataset Generator")
    print("=============================================")
    print("Features:")
    print("✓ Realistic department-medication relationships")
    print("✓ Name-based emails with common domains")
    print("✓ Diverse patient demographics")
    print("✓ Emergency contacts and detailed medical info")
    print("✓ Comprehensive PII detection and indexing")
    print()
    
    # Initialize generator
    generator = MedicalDatasetGenerator(seed=42)
    
    # Generate dataset
    num_records = 500  # Adjust as needed
    records = generator.generate_dataset(num_records)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(records)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(records)} medical organization records")
    print(f"Files created: {json_file}, {csv_file}")
    
    # Display sample record with enhanced details
    print(f"\nSample Record (first record):")
    print("-" * 60)
    sample = records[0]
    print(f"Patient: {sample['patient_name']} ({sample['ethnicity']}, {sample['blood_type']})")
    print(f"Email: {sample['email']} (name-based)")
    print(f"Hospital: {sample['hospital_name']}")
    print(f"Department: {sample['department']}")
    print(f"Medication: {sample['medication']} (department-matched)")
    print(f"Diagnosis: {sample['diagnosis_code']} ({sample['condition_severity']})")
    print(f"Provider: {sample['provider_name']}")
    print(f"Provider Email: {sample['provider_email']} (name-based)")
    print(f"Insurance: {sample['insurance_provider']}")
    print(f"Emergency Contact: {sample['emergency_contact_name']} ({sample['emergency_contact_relationship']})")
    print(f"PII Types Found: {', '.join(sample['unique_pii_types'])}")
    print(f"Total PII Count: {sample['pii_count']}")
    
    print(f"\nSample Record Text (first 400 chars):")
    print(sample['full_record_text'][:400] + "...")
    
    # Show department-medication relationships
    print(f"\nDepartment-Medication Relationship Examples:")
    print("-" * 50)
    dept_examples = {}
    for record in records[:10]:  # First 10 records
        dept = record['department']
        med = record['medication']
        if dept not in dept_examples:
            dept_examples[dept] = med
    
    for dept, med in dept_examples.items():
        print(f"{dept}: {med}")
    
    # Show email variety
    print(f"\nEmail Variety Examples:")
    print("-" * 30)
    for i, record in enumerate(records[:8]):
        print(f"{record['patient_name']}: {record['email']}")
    
    print(f"\nDataset contains {len(set(r['department'] for r in records))} different departments")
    print(f"Dataset contains {len(set(r['ethnicity'] for r in records))} different ethnicities")
    print(f"Dataset contains {len(set(r['insurance_provider'] for r in records))} different insurance providers")

if __name__ == "__main__":
    main()