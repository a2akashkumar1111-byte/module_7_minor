import json
import os

class StudentRecordError(Exception):
    pass

# Auto-create sample input if not exists - so files will always be created
if not os.path.exists("students_input.json"):
    sample = [
        {"student_id": "S101", "name": "Aman", "department": "CSE", "marks": [78, 65, 88]},
        {"student_id": "S102", "name": "Riya", "department": "CSE", "marks": [35, 72]},
        {"student_id": "S103", "department": "CSE", "marks": [90, 80, 70]},
        {"student_id": "S101", "name": "Rahul", "department": "ECE", "marks": [60, 60, 60]},
        {"student_id": "S104", "name": "Neha", "department": "CSE", "marks": [101, 20, 30]}
    ]
    with open("students_input.json", 'w', encoding='utf-8') as f:
        json.dump(sample, f, indent=4)
    print("Created sample students_input.json")

students_valid = {}
errors = []
accepted = 0
rejected = 0
input_file = "students_input.json"

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"File not found: {input_file}")
    exit()
except PermissionError:
    print(f"No permission: {input_file}")
    exit()
except OSError as e:
    print(f"OS error: {e}")
    exit()
except json.JSONDecodeError as e:
    print(f"JSON malformed: {e}")
    exit()
else:
    print(f"Import started: {input_file}")

    for i in range(len(data)):
        rec = data[i]
        try:
            if type(rec) != dict:
                raise TypeError("record must be a dict")
            
            sid = rec['student_id']
            name = rec['name']
            dept = rec['department']
            marks = rec['marks']

            if sid == "" or name == "" or dept == "":
                raise ValueError("fields cannot be empty")

            if type(marks) != list:
                raise TypeError("marks must be a list")
            
            if len(marks) != 3:
                raise StudentRecordError("marks must contain exactly 3 values between 0 and 100")

            for m in marks:
                if type(m) == bool:
                    raise StudentRecordError("marks must contain exactly 3 values between 0 and 100")
                if type(m) != int and type(m) != float:
                    raise TypeError("marks must be numbers")
                if m < 0 or m > 100:
                    raise StudentRecordError("marks must contain exactly 3 values between 0 and 100")

            if sid in students_valid:
                raise StudentRecordError(f"duplicate ID {sid}")

        except KeyError as e:
            msg = f"Rejected record {i+1}: missing required field {e}"
            print(msg)
            errors.append(msg)
            rejected = rejected + 1
        except TypeError as e:
            msg = f"Rejected record {i+1}: {e}"
            print(msg)
            errors.append(msg)
            rejected = rejected + 1
        except ValueError as e:
            msg = f"Rejected record {i+1}: {e}"
            print(msg)
            errors.append(msg)
            rejected = rejected + 1
        except StudentRecordError as e:
            msg = f"Rejected record {i+1}: {e}"
            print(msg)
            errors.append(msg)
            rejected = rejected + 1
        else:
            students_valid[sid] = rec
            print(f"Accepted: {sid} - {name}")
            accepted = accepted + 1

    # This part will now ALWAYS run and create files
    with open("students_valid.json", 'w', encoding='utf-8') as f:
        json.dump(students_valid, f, indent=4)

    with open("import_errors.txt", 'w', encoding='utf-8') as f:
        for e in errors:
            f.write(e + "\n")

    print("Import completed.")
    print(f"Accepted records: {accepted}")
    print(f"Rejected records: {rejected}")
    print("Valid output: students_valid.json")
    print("Error log: import_errors.txt")