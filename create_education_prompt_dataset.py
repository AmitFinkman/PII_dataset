import json
import re
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

class EducationPromptGenerator:
    def __init__(self, seed=42):
        """Initialize the education prompt generator"""
        self.fake = Faker()
        Faker.seed(seed)
        
        # PII type definitions for education prompts
        self.pii_types = {
            'PERSON_NAME': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b\d{3}-\d{3}-\d{4}\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'ADDRESS': r'\d+\s+\w+\s+\w+',
            'DATE_OF_BIRTH': r'\b\d{2}/\d{2}/\d{4}\b',
            'STUDENT_ID': r'\bSTU\d{6}\b',
            'PARENT_ID': r'\bPAR\d{6}\b',
            'TEACHER_ID': r'\bTCH\d{5}\b',
            'ZIP_CODE': r'\b\d{5}\b',
            'GPA': r'\b[0-4]\.\d{1,2}\b',
            'ACADEMIC_YEAR': r'\b\d{4}-\d{4}\b',
            'SEMESTER': r'\b(Fall|Spring|Summer)\b',
            'ASSESSMENT_SCORE': r'\b\d{1,3}%\b',
            'ATTENDANCE_RATE': r'\b\d{1,3}%\b',
            'INSTITUTION_NAME': r'\b\w+\s+(Elementary|Middle School|High School|Community College|University)\b'
        }
        
        # Education domain data for realistic prompts
        self.grade_levels = [
            'Elementary (K-5)', 'Middle School (6-8)', 'High School (9-12)', 
            'College Undergraduate', 'Graduate'
        ]
        
        self.courses = {
            'Elementary (K-5)': ['Mathematics', 'Reading', 'Science', 'Social Studies', 'Art', 'Physical Education'],
            'Middle School (6-8)': ['Pre-Algebra', 'English Language Arts', 'Life Science', 'World History', 'Spanish'],
            'High School (9-12)': ['Algebra II', 'Biology', 'Chemistry', 'AP English', 'AP History', 'Calculus'],
            'College Undergraduate': ['Calculus', 'Statistics', 'Psychology', 'Business Administration', 'Computer Science'],
            'Graduate': ['Advanced Statistics', 'Research Methods', 'Thesis Preparation', 'Clinical Practice']
        }
        
        self.student_types = ['Regular Education', 'Special Education', 'Gifted and Talented', 'English Language Learner', 'At-Risk']
        self.performance_levels = ['Excellent (3.8-4.0)', 'Good (3.0-3.7)', 'Average (2.5-2.9)', 'Below Average (2.0-2.4)', 'Poor (Below 2.0)']
        self.institution_levels = ['Elementary School', 'Middle School', 'High School', 'Community College', 'University']
        self.staff_roles = ['Teacher', 'Principal', 'Counselor', 'Special Education Coordinator', 'Department Head', 'Librarian']
        self.assessments = ['SAT', 'ACT', 'State Testing', 'AP Exams', 'Final Exams', 'Standardized Tests']
        self.interventions = ['Academic Support', 'Tutoring', 'IEP Services', 'Behavioral Support', 'Gifted Program']
        
        # Common educational professional roles and tasks
        self.educational_roles = [
            'Teacher', 'Principal', 'Vice Principal', 'Counselor', 'Registrar', 'Academic Advisor',
            'Special Education Coordinator', 'Department Head', 'Curriculum Coordinator', 'Student Services'
        ]
        
        # Prompt templates with PII (50% will contain PII)
        self.pii_prompt_templates = [
            # Student-specific prompts with names
            "Review academic progress for {student_name} in {course} class",
            "Update contact information for {student_name} (Student ID: {student_id})",
            "Schedule parent conference for {student_name} with {parent_name} at {phone}",
            "Send progress report to {parent_name} at {parent_email} for {student_name}",
            "Assign {student_name} to {intervention} program based on GPA of {gpa}",
            "Contact {emergency_contact} at {emergency_phone} regarding {student_name}",
            "Update IEP for {student_name} (ID: {student_id}) for {academic_year}",
            "Schedule assessment for {student_name} in {assessment_type}",
            "Review attendance record for {student_name} - current rate: {attendance_rate}",
            "Enroll {student_name} in {course} for {semester} semester",
            
            # Parent/Guardian-specific prompts
            "Email {parent_name} at {parent_email} about {student_name}'s academic performance",
            "Call {parent_name} ({phone}) regarding {student_name}'s behavior incident",
            "Send home assignment details to {parent_email} for {student_name}",
            "Update emergency contact from {old_contact} to {new_contact} for {student_name}",
            "Schedule meeting between {parent_name} and {teacher_name} about {student_name}",
            
            # Teacher-specific prompts with names
            "Assign {teacher_name} to teach {course} in {semester}",
            "Review lesson plans submitted by {teacher_name} for {course}",
            "Schedule observation for {teacher_name} (ID: {teacher_id}) in {classroom}",
            "Send professional development materials to {teacher_email}",
            "Update grade book access for {teacher_name} (Teacher ID: {teacher_id})",
            
            # Academic record prompts
            "Generate transcript for {student_name} (Student ID: {student_id}) for {academic_year}",
            "Update GPA calculation for {student_name} - current GPA: {gpa}",
            "Review graduation requirements for {student_name} in {grade_level}",
            "Process grade change request for {student_name} in {course}",
            "Calculate class rank for {student_name} based on {gpa} GPA",
            
            # Assessment and testing prompts
            "Register {student_name} for {assessment_type} scheduled on {test_date}",
            "Review {assessment_type} scores for {student_name}: {score}%",
            "Submit accommodation request for {student_name} (ID: {student_id}) for {assessment_type}",
            "Generate assessment report for {student_name} showing {score}% performance",
            
            # Attendance and behavioral prompts
            "Document attendance issue for {student_name} - absence on {date}",
            "Review tardiness pattern for {student_name} (current rate: {attendance_rate})",
            "Schedule behavioral intervention meeting for {student_name} with {counselor_name}",
            "Update disciplinary record for {student_name} regarding {incident_type}",
            
            # Special services prompts
            "Develop IEP goals for {student_name} in collaboration with {special_ed_teacher}",
            "Schedule speech therapy session for {student_name} with {therapist_name}",
            "Review 504 plan for {student_name} (Student ID: {student_id})",
            "Coordinate special education services for {student_name} with {service_provider}",
            
            # Communication and coordination prompts
            "Forward grade reports to {counselor_name} for students in {intervention} program",
            "Share student progress data with {department_head} for {course} analysis",
            "Coordinate with {teacher_name} regarding {student_name}'s accommodations",
            "Update {principal_name} on academic intervention outcomes for {student_name}",
            
            # Multi-entity prompts
            "Organize meeting between {student_name}, {parent_name}, and {teacher_name}",
            "Coordinate services for {student_name} involving {teacher_name} and {counselor_name}",
            "Review team meeting notes for {student_name} with {parent_name} and {special_ed_coordinator}",
            "Schedule transition planning for {student_name} with {current_teacher} and {next_teacher}",
            
            # Administrative prompts with PII
            "Process enrollment for {student_name} (DOB: {date_of_birth}) in {grade_level}",
            "Update student records for {student_name} with new address: {address}",
            "Verify immunization records for {student_name} (Student ID: {student_id})",
            "Generate emergency contact list including {parent_name} ({phone}) for {student_name}",
            
            # Academic planning prompts
            "Create course schedule for {student_name} in {grade_level} for {academic_year}",
            "Review college readiness for {student_name} with {gpa} GPA",
            "Plan academic support for {student_name} based on {assessment_type} score of {score}%",
            "Coordinate graduation requirements review for {student_name}",
            
            # Technology and systems
            "Reset password for {student_name} (Student ID: {student_id}) in learning management system",
            "Grant system access to {teacher_name} (Teacher ID: {teacher_id}) for {course}",
            "Update student information system with new data for {student_name}",
            "Generate login credentials for {parent_name} to access {student_name}'s grades",
            
            # Financial and billing (for higher education)
            "Process tuition payment for {student_name} (Student ID: {student_id}) for {semester}",
            "Review financial aid eligibility for {student_name} based on {academic_performance}",
            "Send billing statement to {parent_email} for {student_name}'s account",
            "Update scholarship information for {student_name} with {gpa} GPA"
        ]
        
        # Non-PII prompt templates (general educational work)
        self.non_pii_prompt_templates = [
            # Curriculum and instruction
            "Review new curriculum standards for mathematics department",
            "Develop lesson plan templates for science courses",
            "Update assessment rubrics for English language arts",
            "Plan professional development on differentiated instruction",
            "Research best practices for project-based learning",
            "Evaluate textbook options for social studies curriculum",
            
            # Administrative and policy
            "Draft new attendance policy for student handbook",
            "Review graduation requirements for next academic year",
            "Update emergency procedures for campus safety",
            "Plan faculty meeting agenda for next week",
            "Develop budget proposal for educational technology",
            "Create schedule for standardized testing periods",
            
            # Professional development and training
            "Organize workshop on classroom management strategies",
            "Plan training session on new grading software",
            "Research conference opportunities for staff development",
            "Develop mentoring program for new teachers",
            "Create professional learning communities for departments",
            "Schedule training on special education laws and compliance",
            
            # Student support services
            "Evaluate effectiveness of tutoring programs",
            "Develop mental health resources for students",
            "Plan college readiness workshops for families",
            "Create anti-bullying intervention strategies",
            "Research social-emotional learning curricula",
            "Design peer mentoring program structure",
            
            # Technology and systems
            "Evaluate learning management system options",
            "Plan technology integration training for faculty",
            "Research digital citizenship curriculum",
            "Update data privacy policies for student information",
            "Implement new student information system",
            "Design online learning best practices guide",
            
            # Assessment and evaluation
            "Analyze school-wide assessment data trends",
            "Develop benchmark assessment schedule",
            "Research alternative assessment methods",
            "Plan data analysis training for teachers",
            "Create assessment accommodation procedures",
            "Evaluate standardized test preparation strategies",
            
            # Community and parent engagement
            "Plan back-to-school night presentation format",
            "Develop volunteer program for community members",
            "Create communication strategy for school initiatives",
            "Design family engagement activities calendar",
            "Plan fundraising events for school programs",
            "Organize community partnership opportunities",
            
            # Facilities and operations
            "Schedule maintenance for classroom technology",
            "Plan cafeteria menu for dietary requirements",
            "Coordinate transportation routes for efficiency",
            "Design classroom layout for collaborative learning",
            "Plan emergency drill schedules and procedures",
            "Evaluate campus security systems and protocols",
            
            # Special programs and services
            "Develop criteria for gifted education program",
            "Plan summer enrichment program offerings",
            "Research after-school program options",
            "Design intervention strategies for struggling learners",
            "Create English language learner support framework",
            "Plan transition services for students with disabilities",
            
            # Data analysis and reporting
            "Generate report on graduation rate trends",
            "Analyze attendance patterns by grade level",
            "Review academic achievement gap data",
            "Prepare presentation on school performance metrics",
            "Research demographic trends affecting enrollment",
            "Create dashboard for tracking student progress indicators",
            
            # Quality improvement
            "Conduct survey on classroom environment effectiveness",
            "Review feedback from parent-teacher conferences",
            "Evaluate peer observation program outcomes",
            "Analyze effectiveness of intervention programs",
            "Research evidence-based teaching strategies",
            "Plan accreditation preparation activities",
            
            # Legal and compliance
            "Review compliance with federal education regulations",
            "Update procedures for student records management",
            "Research requirements for student privacy protection",
            "Plan training on Title IX compliance",
            "Review special education legal requirements",
            "Update policies for student discipline procedures"
        ]
    
    def generate_fake_education_data(self):
        """Generate fake education data for use in prompts"""
        return {
            'student_name': self.fake.name(),
            'parent_name': self.fake.name(),
            'teacher_name': self.fake.name(),
            'counselor_name': self.fake.name(),
            'principal_name': self.fake.name(),
            'department_head': self.fake.name(),
            'special_ed_teacher': self.fake.name(),
            'therapist_name': self.fake.name(),
            'special_ed_coordinator': self.fake.name(),
            'service_provider': self.fake.name(),
            'current_teacher': self.fake.name(),
            'next_teacher': self.fake.name(),
            'emergency_contact': self.fake.name(),
            'old_contact': self.fake.name(),
            'new_contact': self.fake.name(),
            'student_id': f"STU{random.randint(100000, 999999)}",
            'parent_id': f"PAR{random.randint(100000, 999999)}",
            'teacher_id': f"TCH{random.randint(10000, 99999)}",
            'phone': self.fake.phone_number(),
            'emergency_phone': self.fake.phone_number(),
            'parent_email': self.fake.email(),
            'teacher_email': f"{self.fake.first_name().lower()}.{self.fake.last_name().lower()}@university.edu",
            'address': self.fake.address().replace('\n', ', '),
            'date': self.fake.date_between(start_date='today', end_date='+30d').strftime('%m/%d/%Y'),
            'test_date': self.fake.date_between(start_date='today', end_date='+60d').strftime('%m/%d/%Y'),
            'date_of_birth': self.fake.date_of_birth(minimum_age=5, maximum_age=25).strftime('%m/%d/%Y'),
            'course': random.choice([course for courses in self.courses.values() for course in courses]),
            'grade_level': random.choice(self.grade_levels),
            'student_type': random.choice(self.student_types),
            'performance_level': random.choice(self.performance_levels),
            'institution_level': random.choice(self.institution_levels),
            'staff_role': random.choice(self.staff_roles),
            'assessment_type': random.choice(self.assessments),
            'intervention': random.choice(self.interventions),
            'gpa': f"{random.uniform(1.0, 4.0):.2f}",
            'score': random.randint(60, 100),
            'attendance_rate': f"{random.randint(75, 100)}%",
            'academic_year': f"{random.randint(2023, 2025)}-{random.randint(2024, 2026)}",
            'semester': random.choice(['Fall', 'Spring', 'Summer']),
            'classroom': f"Room {random.randint(100, 999)}",
            'incident_type': random.choice(['Tardiness', 'Absence', 'Behavioral Issue', 'Academic Concern']),
            'academic_performance': random.choice(['Excellent', 'Good', 'Needs Improvement'])
        }
    
    def create_pii_prompt(self):
        """Create a prompt that contains PII"""
        template = random.choice(self.pii_prompt_templates)
        fake_data = self.generate_fake_education_data()
        
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
        """Extract which educational entities (students/parents/teachers) are referenced"""
        entities = []
        
        # Look for person names
        person_names = [finding for finding in pii_findings if finding['pii_type'] == 'PERSON_NAME']
        for name_finding in person_names:
            entities.append({
                'entity_type': 'person',
                'entity_value': name_finding['value'],
                'context': 'educational_participant'
            })
        
        # Look for student IDs
        student_ids = [finding for finding in pii_findings if finding['pii_type'] == 'STUDENT_ID']
        for student_finding in student_ids:
            entities.append({
                'entity_type': 'student',
                'entity_value': student_finding['value'],
                'context': 'student_record'
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
        """Generate a single prompt record with educational context"""
        # Decide if this prompt should contain PII
        if target_contains_pii is None:
            contains_pii = random.choice([True, False])
        else:
            contains_pii = target_contains_pii
        
        # Generate the appropriate type of prompt
        if contains_pii:
            prompt_text = self.create_pii_prompt()
            prompt_category = "Educational Professional Query with PII"
        else:
            prompt_text = self.create_non_pii_prompt()
            prompt_category = "Educational Professional Query without PII"
        
        # Find PII in the prompt
        pii_findings = self.find_pii_in_prompt(prompt_text)
        actual_contains_pii = len(pii_findings) > 0
        
        # Verify PII detection
        verification = self.verify_pii_presence(prompt_text, contains_pii)
        
        # Extract source entities
        source_entities = self.extract_source_entities(prompt_text, pii_findings)
        
        # Determine professional context
        role_context = random.choice(self.educational_roles)
        grade_level_context = random.choice(self.grade_levels)
        
        # Create record
        record = {
            'prompt_id': self.fake.uuid4(),
            'prompt': prompt_text,
            'contains_pii': actual_contains_pii,
            'intended_pii': contains_pii,
            'verification_passed': verification['matches_expectation'],
            'prompt_category': prompt_category,
            'role_context': role_context,
            'grade_level_context': grade_level_context,
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
        """Generate a complete education prompt dataset"""
        print(f"Generating {num_prompts} educational professional prompts...")
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
    
    def save_dataset(self, records, filename_prefix='employer_prompts_education'):
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
        grade_levels = [r['grade_level_context'] for r in records]
        
        with open(filename, 'w') as f:
            f.write("EDUCATION PROFESSIONAL PROMPTS - COMPREHENSIVE ANALYSIS REPORT\n")
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
            
            f.write(f"\nGRADE LEVEL DISTRIBUTION:\n")
            f.write("=" * 30 + "\n")
            for level in set(grade_levels):
                count = grade_levels.count(level)
                percentage = (count / len(records)) * 100
                f.write(f"{level}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nDATASET FEATURES:\n")
            f.write("=" * 20 + "\n")
            f.write(f"✓ Realistic educational professional scenarios\n")
            f.write(f"✓ Grade level-specific context\n")
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
        
        print(f"Education prompt analysis report saved: {filename}")

def main():
    """Main function to generate the education prompt dataset"""
    print("Education Professional Prompt Dataset Generator")
    print("="*55)
    print("Features:")
    print("✓ Grade level-specific educational scenarios")
    print("✓ Role-based prompt generation")
    print("✓ Comprehensive PII detection and labeling")
    print("✓ Multi-entity prompt support")
    print("✓ Verification and quality control")
    print("✓ Source entity tracking")
    print()
    
    # Initialize generator
    generator = EducationPromptGenerator(seed=42)
    
    # Generate dataset
    num_prompts = 1000
    records = generator.generate_dataset(num_prompts, pii_ratio=0.5)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(records)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(records)} education professional prompts")
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