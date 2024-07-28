import os
import json
import pandas as pd

subject = '2024_케이펫_수원2'

results_path = r'C:\pythonproject\ScrapyFW\ScrapyFW\results'
new_path = os.path.join(results_path, f'{subject}', f'{subject}_unique.json')
old_path = 'test.xlsx'

with open(new_path, 'r', encoding='utf-8') as file:
    new_data = json.load(file)
    print(f"처음 데이터 수 : {len(new_data)}")
    
df_new = pd.DataFrame(new_data)

df_old = pd.read_excel(old_path)
df_old.columns = ['empty', 'region', 'type', 'roadAddress', 'name']
df_old = df_old.drop(columns=['empty'])
df_old = df_old.drop(df_old.index[0])

print(df_new)
print(df_old)

df_filtered = df_new[~df_new.apply(lambda x: ((df_old['roadAddress'] == x['roadAddress']) & (df_old['name'] == x['name'])).any(), axis=1)]

output_path = os.path.join(results_path, f'{subject}', f'{subject}_filtered_unique.json')
df_filtered.to_json(output_path, orient='records', force_ascii=False, indent=4)
    
print(f"중복 항목 제거 후 레코드 수: {len(df_filtered)}")
print(f"필터링된 JSON 파일이 저장되었습니다: {output_path}")