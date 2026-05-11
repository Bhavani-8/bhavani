import re
task_field_dictionary = {}
task_field_validation_dictionary = {}

def task_value_store(field, value):
    global task_field_dictionary
    task_field_dictionary[field] = value

def task_value_validation_store(field, value):
    global task_field_dictionary
    task_field_validation_dictionary[field] = value

def validate_file(file):
    pattern = r'^[\w,\s-]+\.[a-zA-Z0-9]{1,6}$'
    return bool(re.fullmatch(pattern, file))

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.fullmatch(pattern, email))