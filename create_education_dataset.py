import json
import re
from faker import Faker
from faker.providers import BaseProvider
import pandas as pd
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Custom provider for education services data
class EducationProvider(BaseProvider):
    """Custom Faker provider for education services data"""
    
    def __init__(self, generator):
        super().__init__(generator)
        
        # Grade level specific course offerings
        self.grade_level_courses = {
            'Elementary (K-5)': ['Mathematics', 'Reading', 'Science', 'Social Studies', 'Art', 'Physical Education', 'Music'],
            'Middle School (6-8)': ['Pre-Algebra', 'Algebra I', 'English Language Arts', 'Life Science', 'World History', 'Spanish', 'Band', 'Physical Education'],
            'High School (9-12)': ['Algebra II', 'Geometry', 'Biology', 'Chemistry', 'Physics', 'AP English', 'AP History', 'Calculus', 'Foreign Languages', 'Computer Science'],
            'College Undergraduate': ['Calculus', 'Statistics', 'Biology', 'Chemistry', 'Psychology', 'Sociology', 'Literature', 'Business Administration', 'Computer Science'],
            'Graduate': ['Advanced Statistics', 'Research Methods', 'Thesis Preparation', 'Advanced Theory', 'Clinical Practice', 'Dissertation Research']
        }
        
        # Academic performance to intervention mapping
        self.performance_interventions = {
            'Excellent (3.8-4.0)': ['Gifted Program', 'Advanced Placement', 'Honor Society', 'Academic Scholarships'],
            'Good (3.0-3.7)': ['Study Groups', 'Academic Clubs', 'College Prep', 'Tutoring'],
            'Average (2.5-2.9)': ['Study Skills Training', 'Academic Support', 'Progress Monitoring', 'Peer Tutoring'],
            'Below Average (2.0-2.4)': ['Intensive Tutoring', 'Academic Intervention', 'Progress Plans', 'Parent Conferences'],
            'Poor (Below 2.0)': ['Academic Probation', 'Remedial Classes', 'Credit Recovery', 'Alternative Programs']
        }
        
        # Student type to services mapping
        self.student_services = {
            'Regular Education': ['Standard Curriculum', 'Extracurricular Activities', 'College Counseling', 'Career Guidance'],
            'Special Education': ['IEP Services', 'Resource Room', 'Speech Therapy', 'Occupational Therapy', 'Behavioral Support'],
            'Gifted and Talented': ['Enrichment Programs', 'Advanced Courses', 'Independent Study', 'Academic Competitions'],
            'English Language Learner': ['ESL Classes', 'Bilingual Support', 'Language Assessment', 'Cultural Integration'],
            'At-Risk': ['Mentoring Programs', 'Counseling Services', 'Academic Support', 'Social Services Referral']
        }
        
        # Educational institutions by level
        self.institution_types = {
            'Elementary School': ['Lincoln Elementary', 'Washington Elementary', 'Roosevelt Elementary', 'Jefferson Elementary'],
            'Middle School': ['Central Middle School', 'Eastside Middle School', 'Westfield Middle School', 'Riverside Middle School'],
            'High School': ['Central High School', 'North High School', 'South High School', 'West High School'],
            'Community College': ['City Community College', 'Regional Community College', 'Technical College', 'Junior College'],
            'University': ['State University', 'Regional University', 'Technical University', 'Community University']
        }
        
        # Academic departments by institution level
        self.academic_departments = {
            'Elementary School': ['Primary Education', 'Special Education', 'Art & Music', 'Physical Education'],
            'Middle School': ['Mathematics', 'Language Arts', 'Science', 'Social Studies', 'Special Education', 'Arts'],
            'High School': ['Mathematics', 'English', 'Science', 'Social Studies', 'Foreign Languages', 'Arts', 'Physical Education', 'Special Education'],
            'Community College': ['Liberal Arts', 'Sciences', 'Business', 'Technical Education', 'Health Sciences', 'Continuing Education'],
            'University': ['College of Arts & Sciences', 'School of Business', 'School of Engineering', 'School of Education', 'School of Medicine', 'Graduate School']
        }
        
        # Assessment types by grade level
        self.assessments = {
            'Elementary (K-5)': ['Reading Assessment', 'Math Benchmark', 'State Testing', 'Portfolio Review'],
            'Middle School (6-8)': ['Standardized Tests', 'Course Exams', 'Project Assessments', 'State Testing'],
            'High School (9-12)': ['SAT', 'ACT', 'AP Exams', 'Final Exams', 'State Testing', 'College Placement'],
            'College Undergraduate': ['Midterm Exams', 'Final Exams', 'Research Projects', 'Internship Evaluation'],
            'Graduate': ['Comprehensive Exams', 'Thesis Defense', 'Research Evaluation', 'Practicum Assessment']
        }
        
        # Extracurricular activities by level
        self.extracurriculars = {
            'Elementary (K-5)': ['Art Club', 'Chess Club', 'Student Council', 'Safety Patrol', 'Choir'],
            'Middle School (6-8)': ['Drama Club', 'Science Club', 'Student Government', 'Sports Teams', 'Band'],
            'High School (9-12)': ['Football', 'Basketball', 'Drama Club', 'National Honor Society', 'Debate Team', 'Band', 'Student Government'],
            'College Undergraduate': ['Greek Life', 'Student Organizations', 'Intramural Sports', 'Academic Clubs', 'Volunteer Groups'],
            'Graduate': ['Research Groups', 'Professional Organizations', 'Teaching Assistantships', 'Conference Presentations']
        }
        
        # Common email domains for educational institutions
        self.edu_email_domains = ['university.edu', 'college.edu', 'school.edu', 'academy.edu', 'institute.edu']
        self.parent_email_domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'icloud.com']
        
        # Educational staff roles
        self.staff_roles = [
            'Teacher', 'Principal', 'Vice Principal', 'Counselor', 'Special Education Coordinator',
            'Department Head', 'Librarian', 'Nurse', 'Social Worker', 'Psychologist', 'Speech Therapist'
        ]
        
        # Parent/Guardian relationships
        self.guardian_relationships = ['Mother', 'Father', 'Guardian', 'Grandmother', 'Grandfather', 'Stepmother', 'Stepfather', 'Foster Parent']
        
        # Attendance status options
        self.attendance_statuses = ['Excellent', 'Good', 'Fair', 'Poor', 'Chronic Absenteeism']
        
        # Disciplinary actions
        self.disciplinary_actions = ['Warning', 'Detention', 'In-School Suspension', 'Out-of-School Suspension', 'Parent Conference', 'Behavioral Contract']
        
        # Demographics
        self.grade_levels = list(self.grade_level_courses.keys())
        self.performance_levels = list(self.performance_interventions.keys())
        self.student_types = list(self.student_services.keys())
        self.institution_levels = list(self.institution_types.keys())
    
    def student_id(self):
        """Generate realistic student ID number"""
        return f"STU{random.randint(100000, 999999)}"
    
    def parent_id(self):
        """Generate parent/guardian ID"""
        return f"PAR{random.randint(100000, 999999)}"
    
    def teacher_id(self):
        """Generate teacher ID"""
        return f"TCH{random.randint(10000, 99999)}"
    
    def grade_level(self):
        """Generate grade level"""
        return self.random_element(self.grade_levels)
    
    def performance_level(self):
        """Generate academic performance level"""
        return self.random_element(self.performance_levels)
    
    def student_type(self):
        """Generate student type"""
        return self.random_element(self.student_types)
    
    def institution_level(self):
        """Generate institution level"""
        return self.random_element(self.institution_levels)
    
    def institution_name(self, level):
        """Generate institution name for level"""
        if level in self.institution_types:
            return self.random_element(self.institution_types[level])
        return self.random_element(self.institution_types['High School'])
    
    def academic_department(self, level):
        """Generate academic department for institution level"""
        if level in self.academic_departments:
            return self.random_element(self.academic_departments[level])
        return self.random_element(self.academic_departments['High School'])
    
    def courses_for_grade_level(self, grade_level):
        """Generate courses based on grade level"""
        if grade_level in self.grade_level_courses:
            available_courses = self.grade_level_courses[grade_level]
            num_courses = self.random_int(3, min(7, len(available_courses)))
            return self.random_elements(available_courses, length=num_courses, unique=True)
        return ['General Studies']
    
    def interventions_for_performance(self, performance_level):
        """Generate interventions based on performance"""
        if performance_level in self.performance_interventions:
            available_interventions = self.performance_interventions[performance_level]
            num_interventions = self.random_int(1, min(3, len(available_interventions)))
            return self.random_elements(available_interventions, length=num_interventions, unique=True)
        return ['Standard Support']
    
    def services_for_student_type(self, student_type):
        """Generate services based on student type"""
        if student_type in self.student_services:
            available_services = self.student_services[student_type]
            num_services = self.random_int(2, min(4, len(available_services)))
            return self.random_elements(available_services, length=num_services, unique=True)
        return ['Standard Services']
    
    def assessments_for_grade_level(self, grade_level):
        """Generate assessments based on grade level"""
        if grade_level in self.assessments:
            return self.random_element(self.assessments[grade_level])
        return 'Standard Assessment'
    
    def extracurricular_for_grade_level(self, grade_level):
        """Generate extracurricular activity based on grade level"""
        if grade_level in self.extracurriculars:
            return self.random_element(self.extracurriculars[grade_level])
        return 'Student Activities'
    
    def staff_role(self):
        """Generate staff role"""
        return self.random_element(self.staff_roles)
    
    def guardian_relationship(self):
        """Generate guardian relationship"""
        return self.random_element(self.guardian_relationships)
    
    def attendance_status(self):
        """Generate attendance status"""
        return self.random_element(self.attendance_statuses)
    
    def disciplinary_action(self):
        """Generate disciplinary action"""
        return self.random_element(self.disciplinary_actions)
    
    def gpa(self, performance_level):
        """Generate GPA based on performance level"""
        if 'Excellent' in performance_level:
            return round(random.uniform(3.8, 4.0), 2)
        elif 'Good' in performance_level:
            return round(random.uniform(3.0, 3.7), 2)
        elif 'Average' in performance_level:
            return round(random.uniform(2.5, 2.9), 2)
        elif 'Below Average' in performance_level:
            return round(random.uniform(2.0, 2.4), 2)
        else:  # Poor
            return round(random.uniform(1.0, 1.9), 2)
    
    def create_educational_email(self, first_name, last_name, is_staff=False):
        """Create realistic email based on person's name and role"""
        if is_staff:
            domain = self.random_element(self.edu_email_domains)
        else:
            domain = self.random_element(self.parent_email_domains)
        
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
    
    def academic_year(self):
        """Generate academic year"""
        current_year = datetime.now().year
        return f"{current_year}-{current_year + 1}"
    
    def semester(self):
        """Generate semester"""
        return random.choice(['Fall', 'Spring', 'Summer'])

class EducationDatasetGenerator:
    def __init__(self, seed=42):
        """Initialize the education dataset generator"""
        self.fake = Faker()
        self.fake.add_provider(EducationProvider)
        Faker.seed(seed)
        
        # Build dynamic patterns for PII detection
        provider = [p for p in self.fake.providers if isinstance(p, EducationProvider)][0]
        all_grade_levels = provider.grade_levels
        all_student_types = provider.student_types
        all_staff_roles = provider.staff_roles
        all_performance_levels = provider.performance_levels
        all_institution_levels = provider.institution_levels
        
        # PII type definitions for education data
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
            'GRADE_LEVEL': r'\b(' + '|'.join([re.escape(level) for level in all_grade_levels]) + r')\b',
            'STUDENT_TYPE': r'\b(' + '|'.join(all_student_types) + r')\b',
            'STAFF_ROLE': r'\b(' + '|'.join(all_staff_roles) + r')\b',
            'PERFORMANCE_LEVEL': r'\b(' + '|'.join([re.escape(level) for level in all_performance_levels]) + r')\b',
            'INSTITUTION_LEVEL': r'\b(' + '|'.join(all_institution_levels) + r')\b',
            'GPA': r'\b[0-4]\.\d{1,2}\b',
            'ACADEMIC_YEAR': r'\b\d{4}-\d{4}\b',
            'SEMESTER': r'\b(Fall|Spring|Summer)\b',
            'ASSESSMENT_SCORE': r'\b\d{1,3}%\b',
            'ATTENDANCE_RATE': r'\b\d{1,3}%\b',
            'INSTITUTION_NAME': r'\b\w+\s+(Elementary|Middle School|High School|Community College|University)\b',
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
    
    def generate_student_record(self):
        """Generate a single student record with educational data"""
        # Generate basic student information
        student_first_name = self.fake.first_name()
        student_last_name = self.fake.last_name()
        student_full_name = f"{student_first_name} {student_last_name}"
        
        # Generate parent/guardian information
        parent1_first_name = self.fake.first_name()
        parent1_last_name = self.fake.last_name()
        parent1_full_name = f"{parent1_first_name} {parent1_last_name}"
        parent1_relationship = self.fake.guardian_relationship()
        
        parent2_first_name = self.fake.first_name()
        parent2_last_name = self.fake.last_name()
        parent2_full_name = f"{parent2_first_name} {parent2_last_name}"
        parent2_relationship = self.fake.guardian_relationship()
        
        # Generate teacher information
        teacher_first_name = self.fake.first_name()
        teacher_last_name = self.fake.last_name()
        teacher_full_name = f"{teacher_first_name} {teacher_last_name}"
        
        # Generate student demographics
        student_birth_date = self.fake.date_of_birth(minimum_age=5, maximum_age=25)
        student_ssn = self.fake.ssn() if random.random() > 0.7 else None  # Not always available
        student_address = self.fake.address().replace('\n', ', ')
        parent1_phone = self.fake.phone_number()
        parent2_phone = self.fake.phone_number()
        parent1_email = self.fake.create_educational_email(parent1_first_name, parent1_last_name, is_staff=False)
        parent2_email = self.fake.create_educational_email(parent2_first_name, parent2_last_name, is_staff=False)
        
        # Generate academic profile
        grade_level = self.fake.grade_level()
        performance_level = self.fake.performance_level()
        student_type = self.fake.student_type()
        institution_level = self.fake.institution_level()
        institution_name = self.fake.institution_name(institution_level)
        academic_department = self.fake.academic_department(institution_level)
        
        # Generate educational IDs
        student_id = self.fake.student_id()
        parent1_id = self.fake.parent_id()
        parent2_id = self.fake.parent_id()
        teacher_id = self.fake.teacher_id()
        
        # Generate academic details
        courses = self.fake.courses_for_grade_level(grade_level)
        primary_course = courses[0] if courses else 'General Studies'
        gpa = self.fake.gpa(performance_level)
        academic_year = self.fake.academic_year()
        semester = self.fake.semester()
        
        # Generate support services
        interventions = self.fake.interventions_for_performance(performance_level)
        services = self.fake.services_for_student_type(student_type)
        
        # Generate teacher and staff details
        teacher_email = self.fake.create_educational_email(teacher_first_name, teacher_last_name, is_staff=True)
        staff_role = self.fake.staff_role()
        
        # Generate academic assessments
        recent_assessment = self.fake.assessments_for_grade_level(grade_level)
        assessment_score = random.randint(60, 100)
        attendance_rate = random.randint(75, 100)
        attendance_status = self.fake.attendance_status()
        
        # Generate extracurricular activities
        extracurricular = self.fake.extracurricular_for_grade_level(grade_level)
        
        # Generate academic dates
        enrollment_date = self.fake.date_between(start_date='-1y', end_date='today')
        last_update_date = self.fake.date_between(start_date=enrollment_date, end_date='today')
        
        # Generate emergency contact (sometimes different from parents)
        emergency_contact = parent1_full_name if random.random() > 0.3 else self.fake.name()
        emergency_phone = parent1_phone if emergency_contact == parent1_full_name else self.fake.phone_number()
        
        # Generate disciplinary information (not always present)
        disciplinary_action = self.fake.disciplinary_action() if random.random() > 0.7 else None
        disciplinary_date = self.fake.date_between(start_date=enrollment_date, end_date='today') if disciplinary_action else None
        
        # Create comprehensive educational record with consistent structure
        record_text = f"""
STUDENT ACADEMIC RECORD - {institution_name.upper()}
Student ID: {student_id} | Academic Year: {academic_year} | Semester: {semester}
Institution: {institution_name} ({institution_level})

STUDENT INFORMATION:
Name: {student_full_name}
Date of Birth: {student_birth_date.strftime('%m/%d/%Y')}
SSN: {student_ssn if student_ssn else 'Not Available'}
Address: {student_address}
Student Type: {student_type}
Grade Level: {grade_level}

PARENT/GUARDIAN INFORMATION:
Primary Contact: {parent1_full_name} ({parent1_relationship})
Phone: {parent1_phone}
Email: {parent1_email}
Parent ID: {parent1_id}

Secondary Contact: {parent2_full_name} ({parent2_relationship})
Phone: {parent2_phone}
Email: {parent2_email}
Parent ID: {parent2_id}

ACADEMIC PROFILE:
Current GPA: {gpa}
Performance Level: {performance_level}
Academic Department: {academic_department}
Primary Course: {primary_course}
All Enrolled Courses: {', '.join(courses)}
Recent Assessment: {recent_assessment}
Assessment Score: {assessment_score}%

TEACHER ASSIGNMENT:
Primary Teacher: {teacher_full_name}
Teacher ID: {teacher_id}
Email: {teacher_email}
Role: {staff_role}
Department: {academic_department}

SUPPORT SERVICES:
Academic Interventions: {', '.join(interventions)}
Student Services: {', '.join(services)}
Extracurricular Activity: {extracurricular}

ATTENDANCE & BEHAVIOR:
Attendance Rate: {attendance_rate}%
Attendance Status: {attendance_status}
Disciplinary Action: {disciplinary_action if disciplinary_action else 'None'}
Disciplinary Date: {disciplinary_date.strftime('%m/%d/%Y') if disciplinary_date else 'Not Applicable'}

EMERGENCY CONTACT:
Name: {emergency_contact}
Phone: {emergency_phone}
Relationship: Primary Contact

ENROLLMENT INFORMATION:
Enrollment Date: {enrollment_date.strftime('%m/%d/%Y')}
Last Update: {last_update_date.strftime('%m/%d/%Y')}
Academic Year: {academic_year}
Current Semester: {semester}

ACADEMIC SUMMARY:
Student {student_full_name} is enrolled in {grade_level} at {institution_name}.
Current GPA: {gpa} (Performance Level: {performance_level})
Primary contact: {parent1_full_name} at {parent1_phone} ({parent1_email})
Teacher: {teacher_full_name} ({teacher_email}) - ID: {teacher_id}
Enrolled courses: {', '.join(courses)}
Recent assessment: {recent_assessment} - Score: {assessment_score}%
Attendance: {attendance_rate}% ({attendance_status})
Support services: {', '.join(services)}
Academic interventions: {', '.join(interventions)}
Emergency contact: {emergency_contact} ({emergency_phone})
        """.strip()
        
        # Find PII in the record
        pii_findings = self.find_pii_in_text(record_text)
        
        # Create structured record
        record = {
            'student_record_id': self.fake.uuid4(),
            'student_id': student_id,
            'student_name': student_full_name,
            'student_first_name': student_first_name,
            'student_last_name': student_last_name,
            'student_date_of_birth': student_birth_date.strftime('%m/%d/%Y'),
            'student_age': (datetime.now().date() - student_birth_date).days // 365,
            'student_ssn': student_ssn,
            'student_address': student_address,
            'student_type': student_type,
            'grade_level': grade_level,
            'performance_level': performance_level,
            'gpa': gpa,
            'academic_year': academic_year,
            'semester': semester,
            'institution_name': institution_name,
            'institution_level': institution_level,
            'academic_department': academic_department,
            'courses': courses,
            'primary_course': primary_course,
            'recent_assessment': recent_assessment,
            'assessment_score': assessment_score,
            'attendance_rate': attendance_rate,
            'attendance_status': attendance_status,
            'parent1_name': parent1_full_name,
            'parent1_first_name': parent1_first_name,
            'parent1_last_name': parent1_last_name,
            'parent1_relationship': parent1_relationship,
            'parent1_phone': parent1_phone,
            'parent1_email': parent1_email,
            'parent1_id': parent1_id,
            'parent2_name': parent2_full_name,
            'parent2_first_name': parent2_first_name,
            'parent2_last_name': parent2_last_name,
            'parent2_relationship': parent2_relationship,
            'parent2_phone': parent2_phone,
            'parent2_email': parent2_email,
            'parent2_id': parent2_id,
            'teacher_name': teacher_full_name,
            'teacher_first_name': teacher_first_name,
            'teacher_last_name': teacher_last_name,
            'teacher_id': teacher_id,
            'teacher_email': teacher_email,
            'staff_role': staff_role,
            'interventions': interventions,
            'services': services,
            'extracurricular': extracurricular,
            'disciplinary_action': disciplinary_action,
            'disciplinary_date': disciplinary_date.strftime('%m/%d/%Y') if disciplinary_date else None,
            'emergency_contact': emergency_contact,
            'emergency_phone': emergency_phone,
            'enrollment_date': enrollment_date.strftime('%m/%d/%Y'),
            'last_update_date': last_update_date.strftime('%m/%d/%Y'),
            'full_record_text': record_text,
            'pii_findings': pii_findings,
            'pii_count': len(pii_findings),
            'unique_pii_types': list(set([finding['pii_type'] for finding in pii_findings]))
        }
        
        return record
    
    def generate_dataset(self, num_records=1000):
        """Generate a complete education services dataset"""
        print(f"Generating {num_records} student education records...")
        
        records = []
        for i in range(num_records):
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{num_records} records...")
            
            record = self.generate_student_record()
            records.append(record)
        
        return records
    
    def save_dataset(self, records, filename_prefix='education_dataset'):
        """Save the dataset in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create education directory if it doesn't exist
        import os
        if not os.path.exists('education'):
            os.makedirs('education')
        
        # Save as JSON
        json_filename = f"education/{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(records, f, indent=2, default=str)
        print(f"Dataset saved as JSON: {json_filename}")
        
        # Save as CSV (flattened version)
        csv_records = []
        for record in records:
            csv_record = record.copy()
            csv_record['pii_findings'] = json.dumps(record['pii_findings'])
            csv_record['unique_pii_types'] = ', '.join(record['unique_pii_types'])
            csv_record['courses'] = ', '.join(record['courses'])
            csv_record['interventions'] = ', '.join(record['interventions'])
            csv_record['services'] = ', '.join(record['services'])
            csv_records.append(csv_record)
        
        df = pd.DataFrame(csv_records)
        csv_filename = f"education/{filename_prefix}_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dataset saved as CSV: {csv_filename}")
        
        # Generate summary statistics
        self.generate_summary_report(records, f"education/{filename_prefix}_summary_{timestamp}.txt")
        
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
        
        # Collect education statistics
        grade_levels = [r['grade_level'] for r in records]
        student_types = [r['student_type'] for r in records]
        performance_levels = [r['performance_level'] for r in records]
        institution_levels = [r['institution_level'] for r in records]
        attendance_statuses = [r['attendance_status'] for r in records]
        
        with open(filename, 'w') as f:
            f.write("EDUCATION SERVICES DATASET - COMPREHENSIVE ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Total Student Records: {len(records)}\n")
            f.write(f"Total PII Instances Found: {total_pii_instances}\n")
            f.write(f"Average PII per Record: {total_pii_instances/len(records):.2f}\n\n")
            
            f.write("PII Type Distribution:\n")
            f.write("-" * 30 + "\n")
            for pii_type, count in sorted(pii_type_counts.items()):
                percentage = (count / total_pii_instances) * 100
                f.write(f"{pii_type}: {count} ({percentage:.1f}%)\n")
            
            # Education demographics
            f.write(f"\nEDUCATION DEMOGRAPHICS:\n")
            f.write("=" * 30 + "\n")
            
            f.write(f"\nGrade Level Distribution:\n")
            for level in set(grade_levels):
                count = grade_levels.count(level)
                percentage = (count / len(records)) * 100
                f.write(f"  {level}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nStudent Type Distribution:\n")
            for student_type in set(student_types):
                count = student_types.count(student_type)
                percentage = (count / len(records)) * 100
                f.write(f"  {student_type}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nPerformance Level Distribution:\n")
            for performance in set(performance_levels):
                count = performance_levels.count(performance)
                percentage = (count / len(records)) * 100
                f.write(f"  {performance}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nInstitution Level Distribution:\n")
            for institution in set(institution_levels):
                count = institution_levels.count(institution)
                percentage = (count / len(records)) * 100
                f.write(f"  {institution}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nAttendance Status Distribution:\n")
            for status in set(attendance_statuses):
                count = attendance_statuses.count(status)
                percentage = (count / len(records)) * 100
                f.write(f"  {status}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nDATASET FEATURES:\n")
            f.write("=" * 20 + "\n")
            f.write(f"✓ Grade level-based course relationships\n")
            f.write(f"✓ Performance level intervention matching\n")
            f.write(f"✓ Student type service alignment\n")
            f.write(f"✓ Institution level course offerings\n")
            f.write(f"✓ Realistic academic progression patterns\n")
            f.write(f"✓ Name-based email generation\n")
            f.write(f"✓ Comprehensive PII detection ({len(self.pii_types)} types)\n")
            
            f.write(f"\nSample PII Findings from First Record:\n")
            f.write("-" * 40 + "\n")
            if records:
                for finding in records[0]['pii_findings'][:20]:
                    f.write(f"Type: {finding['pii_type']}, Value: {finding['value']}, "
                           f"Position: {finding['start_index']}-{finding['end_index']}\n")
        
        print(f"Education services summary report saved: {filename}")

def main():
    """Main function to generate the education services dataset"""
    print("Education Services Dataset Generator")
    print("="*45)
    print("Features:")
    print("✓ Grade level-based course relationships")
    print("✓ Performance level intervention matching")
    print("✓ Student type service alignment")
    print("✓ Institution level course offerings")
    print("✓ Realistic academic progression patterns")
    print("✓ Name-based email generation")
    print("✓ Comprehensive PII detection and indexing")
    print()
    
    # Initialize generator
    generator = EducationDatasetGenerator(seed=42)
    
    # Generate dataset
    num_records = 500
    records = generator.generate_dataset(num_records)
    
    # Save dataset
    json_file, csv_file = generator.save_dataset(records)
    
    print(f"\nDataset generation complete!")
    print(f"Generated {len(records)} student education records")
    print(f"Files created: {json_file}, {csv_file}")
    
    # Display sample record
    print(f"\nSample Record (first record):")
    print("-" * 60)
    sample = records[0]
    print(f"Student: {sample['student_name']} ({sample['student_type']})")
    print(f"Grade Level: {sample['grade_level']} - GPA: {sample['gpa']}")
    print(f"Institution: {sample['institution_name']} ({sample['institution_level']})")
    print(f"Primary Contact: {sample['parent1_name']} ({sample['parent1_relationship']})")
    print(f"Teacher: {sample['teacher_name']} ({sample['staff_role']})")
    print(f"Performance: {sample['performance_level']}")
    print(f"Courses: {', '.join(sample['courses'])}")
    print(f"Attendance: {sample['attendance_rate']}% ({sample['attendance_status']})")
    print(f"PII Types Found: {', '.join(sample['unique_pii_types'])}")
    print(f"Total PII Count: {sample['pii_count']}")
    
    print(f"\nSample Record Text (first 400 chars):")
    print(sample['full_record_text'][:400] + "...")
    
    # Show grade level-course relationships
    print(f"\nGrade Level-Course Relationship Examples:")
    print("-" * 50)
    level_examples = {}
    for record in records[:10]:
        level = record['grade_level']
        courses = ', '.join(record['courses'])
        if level not in level_examples:
            level_examples[level] = courses
    
    for level, courses in level_examples.items():
        print(f"{level}: {courses}")

if __name__ == "__main__":
    main() 