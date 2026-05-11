import ujson as json
import subprocess
import os
import pandas as pd
from pathlib import Path

# def load_test_config():
#     with open('data/test_data.json') as f:
#         return json.load(f)
from setup_logger import setup_logger
from load_test_config_excel_data import load_test_config_excel_data

logger = setup_logger()

# def load_test_config_excel_data():
#     df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='test_details')
#     print(f'Excel data loaded:\n{df}')

#     browser = str(df.iloc[0]['browser']).strip()
#     # website = str(df.iloc[0]['website']).strip()
#     # Build module_to_test dict
#     module_to_test = {}
#     df = df[df['execution'] == 'y']
#     print(f'Excel data loaded:\n{df}')

#     for _, row in df.iterrows():
#         module = row['module_to_test'].strip()
#         if not module:
#             continue
#         test_types = []
#         if row['positive_execution'] == 'y':
#             test_types.append('positive')
#         if row['negative_execution'] == 'y':
#             test_types.append('negative')
#         module_to_test.setdefault(module, [])
#         for t in test_types:
#             if t not in module_to_test[module]:
#                 module_to_test[module].append(t)
    
#     final_test_data = json.dumps({"browser": browser,
#                         "module_to_test": module_to_test
#                     }, indent=4)
#     print(final_test_data)
#     return {
#         "browser": browser,
#         "module_to_test": module_to_test
#     }


def run_pytest(marker):
    print(f"🚀 Running pytest for marker: {marker}")
    command = f'pytest -m "{marker}" --alluredir=reports/allure-results'
    # subprocess.run(command, shell=True, check=True)
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"⚠️ Test run for marker '{marker}' exited with code {result.returncode}")

def generate_allure_report():
    print("📊 Generating Allure report...")
    command = 'allure generate reports/allure-results --clean -o reports/allure-report'
    subprocess.run(command, shell=True, check=True)

def customize_allure_title():
    print("🎨 Customizing Allure report title...")

    # 1. Update <title> in index.html
    title_file_path = 'reports/allure-report/index.html'
    if os.path.exists(title_file_path):
        with open(title_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated_content = content.replace(
            '<title>Allure Report</title>', 
            '<title>Compliance Sutra Report</title>'
        )

        with open(title_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print("✅ Browser tab title updated.")
    else:
        print("❌ index.html not found.")

    # 2. Update report heading in summary.json
    heading_file_path = 'reports/allure-report/widgets/summary.json'
    if os.path.exists(heading_file_path):
        with open(heading_file_path, 'r', encoding='utf-8') as file:
            summary_json = file.read()

        updated_summary = summary_json.replace(
            'Allure Report', 
            'Compliance Sutra Report'
        )

        with open(heading_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_summary)

        print("✅ Main heading in summary.json updated.")
    else:
        print("❌ summary.json not found.")
    
    # 3. Update report heading in summary.json
    sidebar_file_path = 'reports/allure-report/app.js'
    if os.path.exists(sidebar_file_path):
        with open(sidebar_file_path, 'r', encoding='utf-8') as file:
            sidebar_js = file.read()

        updated_head = sidebar_js.replace(
            'Allure</span>', 
            'CS</span>'
        )

        with open(sidebar_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_head)

        print("✅ Sidebar heading in app.js updated.")
    else:
        print("❌ app.js not found.")


def show_report():
    print("📊 Opening Allure report...")
    command = 'allure open reports/allure-report'
    subprocess.run(command, shell=True, check=True)

def main():
    # config = load_test_config()
    report_dir = Path('reports')
    if report_dir.exists():
        pass
    else:
        report_dir.mkdir(parents=True, exist_ok=True)
        print(f"'{report_dir}' directory created")
    config = load_test_config_excel_data()
    modules = config.get("module_to_test", {})
    # modules = config_df[['modules', 'test_type']].to_dict(orient='records')[0]

    # Case 1: When "module_to_test" is a string like "smoke" or "regression"
    if isinstance(modules, str):
        run_pytest(modules)

    # Case 2: When it's a dictionary like {"login": ["positive", "negative"]}
    elif isinstance(modules, dict):
        for module_name, test_types in modules.items():
            if not test_types or any(str(t).lower() == "all" for t in test_types):
                run_pytest(module_name)
            else:
                for test_type in test_types:
                    run_pytest(f"{module_name} and {test_type}")

    else:
        print("❌ Invalid format in test_case_selector.xlsx for 'module_to_test'.")

    generate_allure_report()
    customize_allure_title()
    show_report()

if __name__ == "__main__":
    main()
