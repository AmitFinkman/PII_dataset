import pandas as pd
import random
import json
from datetime import datetime
from faker import Faker
import re

class MedicalPromptGenerator:
    """Generate realistic medical/healthcare employer prompts for LLM with PII detection labels"""
    
    def __init__(self, csv_file_path):
        """Initialize with medical dataset"""
        self.fake = Faker()
        Faker.seed(42)
        
        # Load the medical dataset
        print(f"Loading medical dataset from {csv_file_path}...")
        self.df = pd.read_csv(csv_file_path)
        print(f"Loaded {len(self.df)} patient records")
        
        # Define prompt templates with PII (True cases) - Single Patient
        self.single_patient_templates = [
            # Patient Care Templates
            "Review the treatment plan for patient {patient_name} (MRN: {medical_record_number})",
            "What medications should we prescribe for {patient_name} with diagnosis {diagnosis_code}?",
            "Schedule a follow-up appointment for {patient_name} (Phone: {phone}) in {department}",
            "Check the allergy information for patient {patient_name} (DOB: {date_of_birth})",
            "Review lab results for {patient_name} (MRN: {medical_record_number}) regarding {medication} treatment",
            "Contact {patient_name} at {email} about their upcoming procedure",
            "Prepare discharge instructions for {patient_name} (Blood Type: {blood_type})",
            "Update insurance information for {patient_name} with {insurance_provider} (ID: {insurance_id})",
            
            # Medical Records Templates
            "Pull the medical history for patient {patient_name} (SSN: {ssn})",
            "Transfer records for {patient_name} from {hospital_name} to another facility",
            "Review the {condition_severity} condition of {patient_name} in {department}",
            "Access the emergency contact {emergency_contact_name} ({emergency_contact_phone}) for patient {patient_name}",
            "Update the address for patient {patient_name} to {address}",
            "Verify insurance coverage for {patient_name} (Insurance ID: {insurance_id})",
            
            # Provider Communication Templates
            "Send consultation request to Dr. {provider_name} for patient {patient_name}",
            "Email {provider_email} about {patient_name}'s medication {medication} side effects",
            "Schedule surgery for {patient_name} (MRN: {medical_record_number}) with Dr. {provider_name}",
            "Request second opinion for {patient_name} (Age: {age}) regarding {diagnosis_code}",
            
            # Administrative Templates
            "Process billing for {patient_name} (Insurance: {insurance_provider}, ID: {insurance_id})",
            "Generate medical certificate for {patient_name} (SSN: {ssn}) for work absence",
            "Create referral letter for {patient_name} to {department} specialist",
            "Document {patient_name}'s emergency contact as {emergency_contact_name} ({emergency_contact_relationship})",
            "Update patient {patient_name}'s ethnicity as {ethnicity} in system",
            
            # Emergency/Urgent Templates
            "Emergency admission for {patient_name} (Blood Type: {blood_type}) to {department}",
            "Call emergency contact {emergency_contact_name} at {emergency_contact_phone} for {patient_name}",
            "Rush blood work for {patient_name} (MRN: {medical_record_number}) due to {medication} reaction",
            "Immediate consultation needed for {patient_name} (Phone: {phone}) in {hospital_name}",
            
            # Research/Quality Templates
            "Include {patient_name} (Age: {age}, Ethnicity: {ethnicity}) in {department} research study",
            "Analyze treatment outcomes for {patient_name} with {diagnosis_code} and {medication}",
            "Review quality metrics for {patient_name}'s care in {hospital_name}",
            "Document patient satisfaction for {patient_name} (Email: {email})",
            
            # Pharmacy Templates
            "Verify prescription for {patient_name} (MRN: {medical_record_number}): {medication}",
            "Check drug interactions for {patient_name} with current medication {medication}",
            "Refill authorization needed for {patient_name} (Phone: {phone}) for {medication}",
            "Review allergy list for {patient_name}: {allergies} before dispensing {medication}",
        ]
        
        # Define prompt templates with multiple patients
        self.multi_patient_templates = [
            # Comparative Analysis
            "Compare treatment outcomes between {patient_name_1} (MRN: {medical_record_number_1}) and {patient_name_2} (MRN: {medical_record_number_2})",
            "Review similar cases: {patient_name_1} (Age: {age_1}) and {patient_name_2} (Age: {age_2}) both with {diagnosis_code_1}",
            "Schedule group therapy session for {patient_name_1} ({phone_1}) and {patient_name_2} ({phone_2})",
            "Compare blood work results for {patient_name_1} (Blood Type: {blood_type_1}) and {patient_name_2} (Blood Type: {blood_type_2})",
            
            # Family/Related Care
            "Process family admission: {patient_name_1} (SSN: {ssn_1}) and {patient_name_2} (SSN: {ssn_2})",
            "Contact emergency contacts: {emergency_contact_name_1} for {patient_name_1} and {emergency_contact_name_2} for {patient_name_2}",
            "Review shared insurance coverage for {patient_name_1} and {patient_name_2} under {insurance_provider_1}",
            
            # Batch Processing
            "Send appointment reminders to {patient_name_1} ({email_1}) and {patient_name_2} ({email_2})",
            "Process discharges for {patient_name_1} (MRN: {medical_record_number_1}) and {patient_name_2} (MRN: {medical_record_number_2})",
            "Update medication lists for {patient_name_1}: {medication_1} and {patient_name_2}: {medication_2}",
            
            # Research Cohorts
            "Include patients {patient_name_1} ({ethnicity_1}) and {patient_name_2} ({ethnicity_2}) in diabetes study",
            "Compare {department_1} and {department_2} outcomes for {patient_name_1} and {patient_name_2}",
            "Analyze demographics: {patient_name_1} (Age: {age_1}, {ethnicity_1}) vs {patient_name_2} (Age: {age_2}, {ethnicity_2})",
            
            # Quality Assurance
            "Review care coordination between {provider_name_1} for {patient_name_1} and {provider_name_2} for {patient_name_2}",
            "Assess treatment compliance for {patient_name_1} and {patient_name_2} on similar medications",
        ]
        
        # Combine all PII templates
        self.pii_prompt_templates = self.single_patient_templates + self.multi_patient_templates
        
        # Define prompt templates without PII (False cases)
        self.non_pii_prompt_templates = [
            # Clinical Guidelines
            "What are the latest treatment protocols for diabetes management?",
            "Review infection control policies for the cardiology department",
            "What are the medication dosage guidelines for elderly patients?",
            "Update the emergency response procedures for cardiac arrest",
            "What are the best practices for patient discharge planning?",
            "Review pain management protocols for post-surgical patients",
            "What documentation is required for controlled substance prescriptions?",
            "Create standard operating procedures for blood transfusions",
            
            # Quality & Safety
            "Analyze readmission rates across all departments this quarter",
            "What are the top causes of medication errors in our facility?",
            "Review patient satisfaction scores for nursing staff",
            "How can we reduce average length of stay in the ICU?",
            "What safety protocols should be implemented for MRI procedures?",
            "Analyze trends in hospital-acquired infections",
            "What are the requirements for Joint Commission accreditation?",
            "Review incident reports for falls prevention strategies",
            
            # Training & Education
            "Develop training modules for new nursing staff orientation",
            "What continuing education is required for medical assistants?",
            "Create simulation scenarios for emergency department training",
            "What are the latest guidelines for hand hygiene compliance?",
            "Design workshops on cultural competency in healthcare",
            "What training is needed for new electronic health record system?",
            "Create educational materials for patient medication compliance",
            "Develop competency assessments for critical care nurses",
            
            # Operations & Management
            "Optimize scheduling efficiency for the radiology department",
            "What equipment maintenance schedules should we follow?",
            "How can we improve patient flow in the emergency department?",
            "What staffing ratios are required for different units?",
            "Review cost-effectiveness of surgical supplies procurement",
            "What are the capacity planning needs for the coming year?",
            "How should we prioritize capital equipment requests?",
            "Analyze utilization rates for operating rooms",
            
            # Technology & Innovation
            "What features should our new patient portal include?",
            "How can artificial intelligence improve diagnostic accuracy?",
            "What cybersecurity measures are needed for patient data?",
            "Evaluate different electronic prescribing systems",
            "What mobile health applications should we recommend?",
            "How can we implement telemedicine services effectively?",
            "What data analytics tools would improve patient outcomes?",
            "Review options for automated medication dispensing systems",
            
            # Regulatory & Compliance
            "What are the current HIPAA privacy requirements?",
            "Review Medicare documentation requirements for billing",
            "What infection control measures are mandated by state health department?",
            "How do we ensure compliance with controlled substance regulations?",
            "What quality metrics must be reported to CMS?",
            "Review requirements for clinical trial documentation",
            "What are the updated Joint Commission safety goals?",
            "How should we prepare for state licensing inspections?",
            
            # Research & Development
            "What clinical trials are currently recruiting participants?",
            "How can we improve evidence-based practice implementation?",
            "What outcomes research would benefit our patient population?",
            "How should we structure our institutional review board?",
            "What biomarkers show promise for early disease detection?",
            "How can we participate in national quality improvement initiatives?",
            "What partnerships would enhance our research capabilities?",
            "How do we balance research activities with clinical care?",
            
            # Public Health & Community
            "What preventive care services should we offer in the community?",
            "How can we improve vaccination rates in our service area?",
            "What health education programs would benefit local schools?",
            "How should we respond to seasonal flu outbreaks?",
            "What partnerships would improve access to care for underserved populations?",
            "How can we support healthy lifestyle initiatives in the community?",
            "What emergency preparedness plans do we need for natural disasters?",
            "How should we address social determinants of health in our programs?"
        ]
    
    def extract_patient_data(self, row):
        """Extract clean patient data from a dataframe row"""
        return {
            'record_id': row['record_id'],
            'patient_name': row['patient_name'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'date_of_birth': row['date_of_birth'],
            'age': row['age'],
            'ethnicity': row['ethnicity'],
            'blood_type': row['blood_type'],
            'ssn': row['ssn'],
            'address': row['address'],
            'phone': row['phone'],
            'email': row['email'],
            'medical_record_number': row['medical_record_number'],
            'insurance_provider': row['insurance_provider'],
            'insurance_id': row['insurance_id'],
            'department': row['department'],
            'provider_name': row['provider_name'],
            'provider_email': row['provider_email'],
            'hospital_name': row['hospital_name'],
            'hospital_type': row['hospital_type'],
            'hospital_address': row['hospital_address'],
            'hospital_phone': row['hospital_phone'],
            'admission_date': row['admission_date'],
            'diagnosis_code': row['diagnosis_code'],
            'condition_severity': row['condition_severity'],
            'medication': row['medication'],
            'allergies': row['allergies'] if pd.notna(row['allergies']) and row['allergies'] != '[]' else 'None',
            'emergency_contact_name': row['emergency_contact_name'],
            'emergency_contact_relationship': row['emergency_contact_relationship'],
            'emergency_contact_phone': row['emergency_contact_phone'],
            'emergency_contact_email': row['emergency_contact_email'],
        }
    
    def generate_pii_prompt(self):
        """Generate a prompt containing PII data"""
        # Randomly choose between single and multi-patient templates (70% single, 30% multi)
        use_multi_patient = random.random() < 0.3
        
        if use_multi_patient:
            return self.generate_multi_patient_prompt()
        else:
            return self.generate_single_patient_prompt()
    
    def generate_single_patient_prompt(self):
        """Generate a prompt with one patient's PII"""
        # Select random patient record
        random_row = self.df.sample(n=1).iloc[0]
        patient_data = self.extract_patient_data(random_row)
        
        # Select random single-patient template
        template = random.choice(self.single_patient_templates)
        
        # Fill template with patient data
        try:
            prompt = template.format(**patient_data)
            return prompt, True, [patient_data['record_id']]
        except KeyError as e:
            # Fallback if template has missing field
            fallback_template = "Review the medical record for patient {patient_name} (MRN: {medical_record_number})"
            prompt = fallback_template.format(**patient_data)
            return prompt, True, [patient_data['record_id']]
    
    def generate_multi_patient_prompt(self):
        """Generate a prompt with multiple patients' PII"""
        # Select two random patient records
        random_rows = self.df.sample(n=2)
        patient_1 = self.extract_patient_data(random_rows.iloc[0])
        patient_2 = self.extract_patient_data(random_rows.iloc[1])
        
        # Create combined data with _1 and _2 suffixes
        combined_data = {}
        for key, value in patient_1.items():
            combined_data[f"{key}_1"] = value
        for key, value in patient_2.items():
            combined_data[f"{key}_2"] = value
        
        # Select random multi-patient template
        template = random.choice(self.multi_patient_templates)
        
        # Fill template with combined patient data
        try:
            prompt = template.format(**combined_data)
            return prompt, True, [patient_1['record_id'], patient_2['record_id']]
        except KeyError as e:
            # Fallback if template has missing field
            fallback_template = "Compare medical records for {patient_name_1} (MRN: {medical_record_number_1}) and {patient_name_2} (MRN: {medical_record_number_2})"
            prompt = fallback_template.format(**combined_data)
            return prompt, True, [patient_1['record_id'], patient_2['record_id']]
    
    def generate_non_pii_prompt(self):
        """Generate a prompt without PII data"""
        template = random.choice(self.non_pii_prompt_templates)
        return template, False, None
    
    def has_pii_content(self, prompt):
        """Double-check if prompt actually contains PII"""
        pii_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'MRN-\d{6}',  # Medical Record Number
            r'INS-\d{7}',  # Insurance ID
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{3}-\d{3}-\d{4}\b',  # Phone
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Names (basic pattern)
        ]
        
        for pattern in pii_patterns:
            if re.search(pattern, prompt):
                return True
        return False
    
    def generate_dataset(self, total_prompts=1000, pii_ratio=0.5):
        """Generate the complete medical prompt dataset"""
        print(f"Generating {total_prompts} medical employer prompts...")
        
        dataset = []
        pii_prompts_target = int(total_prompts * pii_ratio)
        non_pii_prompts_target = total_prompts - pii_prompts_target
        
        # Generate PII prompts
        print(f"Generating {pii_prompts_target} prompts with PII...")
        for i in range(pii_prompts_target):
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{pii_prompts_target} PII prompts...")
            
            prompt, contains_pii, patient_ids = self.generate_pii_prompt()
            
            # Verify it actually contains PII
            verified_pii = self.has_pii_content(prompt)
            
            record = {
                'prompt_id': f"pii_{i+1:04d}",
                'prompt': prompt,
                'contains_pii': contains_pii,
                'verified_pii': verified_pii,
                'prompt_type': 'with_pii',
                'source_patient_id': patient_ids,
                'num_patients': len(patient_ids)
            }
            dataset.append(record)
        
        # Generate non-PII prompts
        print(f"Generating {non_pii_prompts_target} prompts without PII...")
        for i in range(non_pii_prompts_target):
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{non_pii_prompts_target} non-PII prompts...")
            
            prompt, contains_pii, patient_data = self.generate_non_pii_prompt()
            
            # Verify it doesn't contain PII
            verified_pii = self.has_pii_content(prompt)
            
            record = {
                'prompt_id': f"nopii_{i+1:04d}",
                'prompt': prompt,
                'contains_pii': contains_pii,
                'verified_pii': verified_pii,
                'prompt_type': 'without_pii',
                'source_patient_id': [],
                'num_patients': 0
            }
            dataset.append(record)
        
        # Shuffle the dataset
        random.shuffle(dataset)
        
        # Add final indices
        for i, record in enumerate(dataset):
            record['final_index'] = i + 1
        
        return dataset
    
    def save_dataset(self, dataset, filename_prefix='employer_prompts_medical'):
        """Save the medical prompt dataset"""
        
        # Save as JSON (no timestamp)
        json_filename = f"{filename_prefix}.json"
        with open(json_filename, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"Dataset saved as JSON: {json_filename}")
        
        # Save as CSV
        df = pd.DataFrame(dataset)
        csv_filename = f"{filename_prefix}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dataset saved as CSV: {csv_filename}")
        
        # Generate analysis report
        self.generate_analysis_report(dataset, f"{filename_prefix}_analysis.txt")
        
        return json_filename, csv_filename
    
    def generate_analysis_report(self, dataset, filename):
        """Generate analysis report of the medical prompt dataset"""
        total_prompts = len(dataset)
        pii_prompts = sum(1 for item in dataset if item['contains_pii'])
        non_pii_prompts = total_prompts - pii_prompts
        
        # Verification analysis
        correctly_labeled_pii = sum(1 for item in dataset if item['contains_pii'] == item['verified_pii'])
        mislabeled = total_prompts - correctly_labeled_pii
        
        # Multi-patient analysis
        multi_patient_prompts = sum(1 for item in dataset if item['num_patients'] > 1)
        single_patient_prompts = sum(1 for item in dataset if item['num_patients'] == 1)
        
        with open(filename, 'w') as f:
            f.write("MEDICAL/HEALTHCARE PROMPT DATASET - ANALYSIS REPORT\n")
            f.write("="*65 + "\n\n")
            f.write(f"Total Prompts Generated: {total_prompts}\n")
            f.write(f"Prompts with PII: {pii_prompts} ({pii_prompts/total_prompts*100:.1f}%)\n")
            f.write(f"Prompts without PII: {non_pii_prompts} ({non_pii_prompts/total_prompts*100:.1f}%)\n\n")
            
            f.write("PATIENT COVERAGE:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Single Patient Prompts: {single_patient_prompts} ({single_patient_prompts/total_prompts*100:.1f}%)\n")
            f.write(f"Multi-Patient Prompts: {multi_patient_prompts} ({multi_patient_prompts/total_prompts*100:.1f}%)\n\n")
            
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
            
            f.write("MEDICAL DATASET FEATURES:\n")
            f.write("=" * 25 + "\n")
            f.write("✓ Healthcare-specific employer queries for medical LLM use cases\n")
            f.write("✓ Patient care, clinical, and administrative scenarios\n")
            f.write("✓ Single and multi-patient prompt variations\n")
            f.write("✓ HIPAA-relevant PII detection training data\n")
            f.write("✓ Medical record numbers, insurance IDs, and clinical data\n")
            f.write("✓ Emergency contact and provider communication scenarios\n")
            f.write("✓ Comprehensive medical workflow coverage\n")
        
        print(f"Medical analysis report saved: {filename}")

def main():
    """Main function to generate medical employer prompt dataset"""
    print("Medical/Healthcare Prompt Dataset Generator for PII Detection")
    print("="*65)
    print("Purpose: Generate realistic healthcare employer prompts with PII labels")
    print("Use Case: Training LLMs to detect PII in medical/clinical queries")
    print()
    
    # Initialize generator with the CSV file
    csv_file = "medical/medical_org_dataset_20250726_151340.csv"
    try:
        generator = MedicalPromptGenerator(csv_file)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        print("Please ensure the medical dataset CSV file exists.")
        return
    
    # Generate dataset
    total_prompts = 1000
    print(f"Generating {total_prompts} medical employer prompts...")
    dataset = generator.generate_dataset(total_prompts=total_prompts, pii_ratio=0.5)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(dataset)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(dataset)} medical employer prompts")
    print(f"Files created: {json_file}, {csv_file}")
    
    # Show sample results
    pii_samples = [item for item in dataset if item['contains_pii']][:3]
    non_pii_samples = [item for item in dataset if not item['contains_pii']][:3]
    
    print(f"\nSample Medical Prompts WITH PII:")
    print("-" * 50)
    for i, sample in enumerate(pii_samples, 1):
        print(f"{i}. {sample['prompt']}")
        print()
    
    print(f"Sample Medical Prompts WITHOUT PII:")
    print("-" * 50)
    for i, sample in enumerate(non_pii_samples, 1):
        print(f"{i}. {sample['prompt']}")
        print()
    
    # Summary statistics
    total = len(dataset)
    with_pii = sum(1 for item in dataset if item['contains_pii'])
    without_pii = total - with_pii
    multi_patient = sum(1 for item in dataset if item['num_patients'] > 1)
    
    print(f"Final Statistics:")
    print(f"Total prompts: {total}")
    print(f"With PII: {with_pii} ({with_pii/total*100:.1f}%)")
    print(f"Without PII: {without_pii} ({without_pii/total*100:.1f}%)")
    print(f"Multi-patient prompts: {multi_patient} ({multi_patient/total*100:.1f}%)")

if __name__ == "__main__":
    main() 