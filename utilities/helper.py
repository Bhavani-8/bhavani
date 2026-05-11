# success = False
# print(f'{'Success' if success else 'Failure'}')

import json

# test_case_list = []
# with open('test_case_selector.json', 'r') as f:
#     test_case_details = json.load(f)
#     positive_case_details = test_case_details['login_test_cases']
#     for i in range(len(positive_case_details)):
#         test_case_list.append(tuple((positive_case_details[i]['username'], positive_case_details[i]['password'], positive_case_details[i]['expected_success'])))

# print(test_case_list)


# task_list1 = {'title': 'Piyush', 'age': '18', 'gender': 'male'}
# task_list2 = {'title': 'Piyush', 'gender': 'male', 'age': '18'}

# if task_list1 == task_list2:
#     print("True")
# else:
#     print("False")

# string = 'ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt'
# print(len(string))
# print(string.capitalize())

# from plyer import notification

# notification.notify(
#     title="Test Completed",
#     message="End Time and Due Date set successfully!",
#     timeout=3  # seconds
# )

# import tkinter as tk
# from threading import Timer

# def show_toast(message):
#     root = tk.Tk()
#     root.overrideredirect(1)
#     root.geometry("300x50+1000+40")  # Adjust position and size
#     tk.Label(root, text=message, bg="black", fg="white", font=("Helvetica", 12)).pack(fill="both", expand=True)
#     Timer(5.0, root.destroy).start()  # Auto close after 3 seconds
#     root.mainloop()

# show_toast("Test case passed successfully!")

# import re

# emails = ["piyush@example.com", "invalid_email@", "test.user@domain.co", "user@site"]
# files = ["test.001", "test.docx", "test.pdf", "no_ext"]


# def validate_files(file):
#     pattern = r'^[\w,\s-]+\.[a-zA-Z0-9]{1,6}$'
#     return bool(re.fullmatch(pattern, file))

# def validate_email(email):
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return bool(re.fullmatch(pattern, email))

# for email in emails:
#     if validate_email(email):
#         print(f"✅ Valid: {email}")
#     else:
#         print(f"❌ Invalid: {email}")

# print('-' * 50)

# for file in files:
#     if validate_files(file):
#         print(f"✅ Valid: {file}")
#     else:
#         print(f"❌ Invalid: {file}")


# if int('4.00'):
#     print("True") 
# else: 
#     print("False")

# string = "//div[@class='frequency-weeks']//span[text()='day']"
# print(string.replace('day', 'Monday'))