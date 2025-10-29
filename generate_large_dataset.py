#!/usr/bin/env python3
"""
Generate a large CSV dataset for PoisonProof AI testing
"""

import csv
import random
from datetime import datetime, timedelta
import numpy as np

# Configuration
NUM_EMPLOYEES = 1000
DEPARTMENTS = ['Engineering', 'Marketing', 'HR', 'Sales', 'Management', 'Finance', 'Operations', 'IT', 'Legal', 'Research']
LOCATIONS = ['California', 'New York', 'Texas', 'Florida', 'Illinois', 'Washington', 'Arizona', 'Colorado', 'Nevada', 'Oregon', 'Georgia', 'Virginia', 'Ohio', 'Pennsylvania', 'North Carolina', 'Michigan', 'New Jersey', 'Massachusetts', 'Tennessee', 'Indiana']
EDUCATION_LEVELS = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD', 'MBA']
CERTIFICATIONS = [
    'AWS Certified', 'Google Analytics', 'PMP Certified', 'SHRM-CP', 'Salesforce Admin',
    'HubSpot Certified', 'CISSP', 'PHR Certified', 'Certified Sales Pro', 'Kubernetes Admin',
    'Content Marketing', 'Advanced Sales', 'SHRM-SCP', 'Docker Certified', 'Six Sigma Black',
    'Azure Certified', 'Enterprise Sales', 'Digital Marketing', 'Security+', 'Compensation Pro',
    'Leadership Cert', 'Brand Strategy', 'Sales Leadership', 'Employee Relations', 'Channel Partner',
    'Social Media', 'DevOps Expert', 'Talent Acquisition', 'B2B Sales', 'Marketing Analytics',
    'Cloud Architect', 'HR Generalist', 'Inside Sales', 'Email Marketing', 'Full Stack Dev',
    'Organizational Dev', 'Enterprise Account', 'Content Creation', 'Operations Mgmt', 'QA Specialist',
    'Regional Sales', 'AI Marketing', 'Strategic HR', 'Mobile Dev', 'PR Specialist',
    'Sales Strategy', 'Benefits Admin', 'Data Engineer', 'Marketing Intern', 'Key Account Mgr',
    'Learning & Dev', 'Junior Developer', 'Product Marketing', 'Sales Director', 'Recruiter',
    'Tech Lead', 'Campaign Manager', 'Business Dev', 'None'
]

MANAGER_IDS = ['M001', 'M002', 'M003', 'M004', 'M005', 'M006', 'M007', 'M008', 'M009', 'M010', 'CEO', 'CTO', 'CFO', 'COO']
SECURITY_LEVELS = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']

# First and last names for realistic employee names
FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth',
    'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Christopher', 'Karen',
    'Charles', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Dorothy', 'Mark', 'Sandra',
    'Donald', 'Donna', 'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle',
    'Kenneth', 'Laura', 'Kevin', 'Sarah', 'Brian', 'Kimberly', 'George', 'Deborah', 'Timothy', 'Dorothy',
    'Ronald', 'Lisa', 'Jason', 'Nancy', 'Edward', 'Karen', 'Jeffrey', 'Betty', 'Ryan', 'Helen',
    'Jacob', 'Sandra', 'Gary', 'Donna', 'Nicholas', 'Carol', 'Eric', 'Ruth', 'Jonathan', 'Sharon',
    'Stephen', 'Michelle', 'Larry', 'Laura', 'Justin', 'Sarah', 'Scott', 'Kimberly', 'Brandon', 'Deborah',
    'Benjamin', 'Jessica', 'Samuel', 'Shirley', 'Gregory', 'Cynthia', 'Alexander', 'Angela', 'Patrick', 'Melissa',
    'Frank', 'Brenda', 'Raymond', 'Emma', 'Jack', 'Olivia', 'Dennis', 'Katherine', 'Jerry', 'Amy',
    'Tyler', 'Anna', 'Aaron', 'Rebecca', 'Jose', 'Virginia', 'Henry', 'Kathleen', 'Adam', 'Pamela',
    'Douglas', 'Martha', 'Nathan', 'Debra', 'Peter', 'Rachel', 'Zachary', 'Carolyn', 'Kyle', 'Janet'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
    'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
    'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
    'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes',
    'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper',
    'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson',
    'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes',
    'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long', 'Ross', 'Foster', 'Jimenez'
]

def generate_random_date(start_year=2005, end_year=2024):
    """Generate a random date between start_year and end_year"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

def generate_employee_data(employee_id):
    """Generate data for a single employee"""
    # Basic info
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    age = random.randint(22, 65)
    department = random.choice(DEPARTMENTS)
    location = random.choice(LOCATIONS)
    hire_date = generate_random_date()
    education = random.choice(EDUCATION_LEVELS)
    certification = random.choice(CERTIFICATIONS)
    manager_id = random.choice(MANAGER_IDS)
    security_clearance = random.choice(SECURITY_LEVELS)
    
    # Experience and performance (generally correlated with age)
    years_experience = max(0, age - 22 + random.randint(-3, 3))
    base_performance = min(10.0, max(5.0, 7.0 + (years_experience * 0.1) + random.gauss(0, 1)))
    performance_score = round(base_performance, 1)
    
    # Salary (correlated with experience, department, and performance)
    dept_multiplier = {
        'Engineering': 1.2, 'IT': 1.1, 'Management': 1.5, 'Finance': 1.3,
        'Legal': 1.4, 'Research': 1.1, 'Sales': 1.0, 'Marketing': 0.9,
        'HR': 0.8, 'Operations': 0.9
    }
    
    base_salary = 40000 + (years_experience * 3000) + (performance_score * 5000)
    salary = int(base_salary * dept_multiplier.get(department, 1.0) * random.uniform(0.8, 1.3))
    
    # Other metrics
    project_count = max(1, int(years_experience * 1.5 + random.randint(-2, 5)))
    overtime_hours = random.randint(0, 80)
    satisfaction_rating = round(performance_score + random.gauss(0, 0.5), 1)
    satisfaction_rating = max(3.0, min(10.0, satisfaction_rating))
    
    training_completed = random.randint(5, 50)
    bonus_eligible = random.choice(['Yes', 'No'])
    remote_work_days = random.randint(0, 5)
    health_score = random.randint(65, 100)
    
    return [
        f"E{employee_id:03d}", name, age, salary, department, years_experience,
        performance_score, location, hire_date, education, certification,
        project_count, overtime_hours, satisfaction_rating, manager_id,
        security_clearance, training_completed, bonus_eligible, remote_work_days, health_score
    ]

def inject_anomalies(data, num_anomalies=50):
    """Inject various types of anomalies into the dataset"""
    anomaly_indices = random.sample(range(len(data)), num_anomalies)
    
    for i, idx in enumerate(anomaly_indices):
        anomaly_type = i % 8  # 8 different types of anomalies
        
        if anomaly_type == 0:  # Extremely high salary
            data[idx][3] = random.randint(500000, 2000000)
        elif anomaly_type == 1:  # Negative or extremely low salary
            data[idx][3] = random.randint(-50000, 15000)
        elif anomaly_type == 2:  # Impossible performance score
            data[idx][6] = round(random.uniform(10.5, 15.0), 1)
        elif anomaly_type == 3:  # Extremely low performance
            data[idx][6] = round(random.uniform(0.1, 2.0), 1)
        elif anomaly_type == 4:  # Excessive overtime
            data[idx][12] = random.randint(120, 200)
        elif anomaly_type == 5:  # Age vs experience mismatch
            data[idx][2] = random.randint(20, 25)  # Young age
            data[idx][5] = random.randint(15, 25)  # High experience
        elif anomaly_type == 6:  # Suspicious satisfaction vs performance
            data[idx][6] = round(random.uniform(8.5, 10.0), 1)  # High performance
            data[idx][13] = round(random.uniform(1.0, 3.0), 1)  # Low satisfaction
        elif anomaly_type == 7:  # Health score anomaly
            data[idx][19] = random.randint(10, 35)  # Very low health score
    
    return data

def generate_large_dataset():
    """Generate the complete dataset"""
    print("Generating large employee dataset...")
    
    # Headers
    headers = [
        'employee_id', 'name', 'age', 'salary', 'department', 'years_experience',
        'performance_score', 'location', 'hire_date', 'education_level', 'certifications',
        'project_count', 'overtime_hours', 'satisfaction_rating', 'manager_id',
        'security_clearance', 'training_completed', 'bonus_eligible', 'remote_work_days', 'health_score'
    ]
    
    # Generate employee data
    employee_data = []
    for i in range(1, NUM_EMPLOYEES + 1):
        employee_data.append(generate_employee_data(i))
    
    # Inject anomalies
    employee_data = inject_anomalies(employee_data, num_anomalies=75)  # ~7.5% anomaly rate
    
    # Write to CSV
    filename = 'large_employee_dataset.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(employee_data)
    
    print(f"✅ Generated {filename} with {NUM_EMPLOYEES} employees")
    print(f"📊 Dataset includes ~75 intentional anomalies for testing")
    print(f"📈 20 columns with realistic business data")
    print(f"🔍 Ready for PoisonProof AI analysis!")
    
    return filename

if __name__ == "__main__":
    generate_large_dataset()