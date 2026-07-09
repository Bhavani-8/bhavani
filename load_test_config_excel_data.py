import ujson as json
import pandas as pd
import os

def load_test_config_excel_data():
    df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='test_details')
    print(f'Test Details:\n{df}')

    module_to_test = {}
    df = df[df['execution'] == 'y']
    print(f'Test Cases:\n{df}')

    for _, row in df.iterrows():
        module = row['module_to_test'].strip()
        if not module:
            continue
        test_types = []
        positive_execution = str(row.get('positive_execution', 'n')).strip().lower()
        negative_execution = str(row.get('negative_execution', 'n')).strip().lower()
        if positive_execution == 'y':
            test_types.append('positive')

        if negative_execution == 'y':
            test_types.append('negative')
        module_to_test.setdefault(module, [])
        for t in test_types:
            if t not in module_to_test[module]:
                module_to_test[module].append(t)
    
    final_test_data = json.dumps({"module_to_test": module_to_test,}, indent=4)
    print(final_test_data)
    return {
        "module_to_test": module_to_test
    }