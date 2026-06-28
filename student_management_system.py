import csv
import json
import logging
import os
import re

# 1. LOGGING CONFIGURATION
logging.basicConfig(
    filename="student_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 2. CUSTOM EXCEPTIONS
class StudentNotFoundError(Exception):
    """Exception raised when a student registration number does not exist."""
    def __init__(self, reg_num, message="Student record not found"):
        self.reg_num = reg_num
        self.message = f"{message}: {reg_num}"
        super().__init__(self.message)


class DuplicateStudentError(Exception):
    """Exception raised when attempting to add an existing student."""
    def __init__(self, reg_num, message="Student registration number already exists"):
        self.reg_num = reg_num
        self.message = f"{message}: {reg_num}"
        super().__init__(self.message)

# 3. DATA MANAGER CLASS
class StudentDataManager:
    def __init__(self, csv_file="students.csv", json_file="students.json"):
        self.csv_file = csv_file
        self.json_file = json_file
        self.csv_headers = ["Registration Number", "Name"]
        self._initialize_files()

    def _initialize_files(self):
        """Creates the data files with proper headers/structures if they don't exist."""
        try:
            if not os.path.exists(self.csv_file):
                with open(self.csv_file, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.csv_headers)
                logging.info(f"Initialized empty CSV file: {self.csv_file}")

            if not os.path.exists(self.json_file):
                with open(self.json_file, mode='w', encoding='utf-8') as f:
                    json.dump({}, f)
                logging.info(f"Initialized empty JSON file: {self.json_file}")
        except Exception as e:
            logging.critical(f"Failed to initialize data files: {e}")
            print(f"Critical System Error: Could not initialize storage. {e}")
            exit(1)

    def load_records(self):
        """Reads CSV and JSON files and merges them into a unified dictionary."""
        records = {}
        try:
            # Load basic info from CSV
            with open(self.csv_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    reg = row["Registration Number"]
                    records[reg] = {
                        "name": row["Name"],
                        "address": "",
                        "contact": "",
                        "program": ""
                    }
            
            # Load detailed info from JSON
            with open(self.json_file, mode='r', encoding='utf-8') as f:
                json_data = json.load(f)
                for reg, details in json_data.items():
                    if reg in records:
                        records[reg].update(details)
            
            return records
        except Exception as e:
            logging.error(f"Error loading student records: {e}")
            raise e

    def save_records(self, records):
        """Splits data and saves it back to both CSV and JSON synchronously."""
        try:
            # Save to CSV
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.csv_headers)
                for reg, data in records.items():
                    writer.writerow([reg, data["name"]])

            # Save to JSON
            json_data = {
                reg: {
                    "address": data["address"],
                    "contact": data["contact"],
                    "program": data["program"]
                } for reg, data in records.items()
            }
            with open(self.json_file, mode='w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)

            logging.info("Student records synchronized and saved successfully.")
        except Exception as e:
            logging.error(f"Error saving student records: {e}")
            raise e

# 4. INPUT VALIDATORS
def get_validated_input(prompt, pattern, error_msg):
    """Generic regex validator wrapper for user inputs."""
    while True:
        user_input = input(prompt).strip()
        if re.match(pattern, user_input):
            return user_input
        print(f"Invalid input! {error_msg}")


def get_student_input(existing_regs, is_update=False):
    """Collects and validates comprehensive student details."""
    reg_pattern = r"^STU\d{3}$"  # Example format: STU001
    phone_pattern = r"^\+?\d{9,15}$"
    
    if not is_update:
        reg_num = get_validated_input(
            "Enter Registration Number (Format: STU001): ", 
            reg_pattern, "Must match 'STU' followed by 3 digits."
        )
        if reg_num in existing_regs:
            raise DuplicateStudentError(reg_num)
    else:
        reg_num = None

    name = get_validated_input("Enter Full Name: ", r"^[A-Za-z\s]{2,50}$", "2-50 alphabetic characters required.")
    address = input("Enter Address: ").strip()
    contact = get_validated_input("Enter Contact Number: ", phone_pattern, "Provide a valid phone number (9-15 digits).")
    program = input("Enter Academic Program: ").strip()

    return reg_num, {"name": name, "address": address, "contact": contact, "program": program}

# 5. CORE CRUD OPERATIONS
def add_student(db):
    print("\n--- Add New Student ---")
    try:
        records = db.load_records()
        reg_num, details = get_student_input(records.keys(), is_update=False)
        records[reg_num] = details
        db.save_records(records)
        print(f"Success: Student {reg_num} added successfully.")
        logging.info(f"Admin action: Added student {reg_num}")
    except DuplicateStudentError as dse:
        print(f"Operation Failed: {dse}")
        logging.warning(f"Failed Add Attempt: {dse}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Add Operation Complete.")


def view_all_students(db):
    print("\n--- All Student Records ---")
    try:
        records = db.load_records()
        if not records:
            print("No student records found.")
            return
            
        print(f"{'Reg Num':<10} | {'Name':<20} | {'Program':<15} | {'Contact':<15} | {'Address'}")
        print("-" * 80)
        for reg, data in records.items():
            print(f"{reg:<10} | {data['name']:<20} | {data['program']:<15} | {data['contact']:<15} | {data['address']}")
        logging.info("Admin action: Viewed all student records.")
    except Exception as e:
        print(f"Could not load records: {e}")


def search_student(db):
    print("\n--- Search Student ---")
    try:
        reg_num = input("Enter Registration Number to search: ").strip()
        records = db.load_records()
        
        if reg_num not in records:
            raise StudentNotFoundError(reg_num)
            
        student = records[reg_num]
        print(f"\nRecord Found for {reg_num}:")
        print(f"Name:    {student['name']}")
        print(f"Program: {student['program']}")
        print(f"Contact: {student['contact']}")
        print(f"Address: {student['address']}")
        logging.info(f"Admin action: Searched for student {reg_num}")
    except StudentNotFoundError as snfe:
        print(snfe)
        logging.warning(f"Failed Search: {snfe}")


def update_student(db):
    print("\n--- Update Student Details ---")
    try:
        reg_num = input("Enter Registration Number to update: ").strip()
        records = db.load_records()
        
        if reg_num not in records:
            raise StudentNotFoundError(reg_num)
            
        print("Enter new details below:")
        _, updated_details = get_student_input(records.keys(), is_update=True)
        
        records[reg_num] = updated_details
        db.save_records(records)
        print(f"Success: Student {reg_num} updated successfully.")
        logging.info(f"Admin action: Updated student {reg_num}")
    except StudentNotFoundError as snfe:
        print(snfe)
        logging.warning(f"Failed Update Attempt: {snfe}")
    except Exception as e:
        print(f"An unexpected error occurred during update: {e}")


def delete_student(db):
    print("\n--- Delete Student Record ---")
    try:
        reg_num = input("Enter Registration Number to delete: ").strip()
        records = db.load_records()
        
        if reg_num not in records:
            raise StudentNotFoundError(reg_num)
            
        confirm = input(f"Are you sure you want to delete {reg_num}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            del records[reg_num]
            db.save_records(records)
            print(f"Success: Student {reg_num} permanently deleted.")
            logging.info(f"Admin action: Deleted student {reg_num}")
        else:
            print("Deletion canceled.")
    except StudentNotFoundError as snfe:
        print(snfe)
        logging.warning(f"Failed Deletion Attempt: {snfe}")

# 6. MAIN SYSTEM LOOP
def main():
    db = StudentDataManager()
    logging.info("System Session Started.")
    
    while True:
        print(" STUDENT RECORD MANAGEMENT SYSTEM")
        print("1. Add a New Student")
        print("2. View All Students")
        print("3. Search Student by Reg Number")
        print("4. Update Student Details")
        print("5. Delete a Student Record")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            add_student(db)
        elif choice == '2':
            view_all_students(db)
        elif choice == '3':
            search_student(db)
        elif choice == '4':
            update_student(db)
        elif choice == '5':
            delete_student(db)
        elif choice == '6':
            print("\nExiting system. Goodbye!")
            logging.info("System Session Closed Normally.")
            break
        else:
            print("Invalid choice! Please select an option between 1 and 6.")
            logging.warning(f"User entered invalid menu choice: '{choice}'")

if __name__ == "__main__":
    main()