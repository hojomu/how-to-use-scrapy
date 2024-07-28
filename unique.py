import os
import pandas as pd
import json
import argparse

parser = argparse.ArgumentParser(description="Process some files.")
parser.add_argument('subject', type=str, help='The subject name')
args = parser.parse_args()

# 현재 파일 경로 출력
current_file_path = os.path.abspath(__file__)
print(current_file_path)

subject = args.subject

results_path = r'C:\pythonproject\ScrapyFW\ScrapyFW\results'
input_path = os.path.join(results_path, f'{subject}', f'{subject}.json')

with open(input_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

initial_count = len(df)

df_unique = df.drop_duplicates(subset=['name','roadAddress'])

final_count = len(df_unique)

output_path = os.path.join(results_path, f'{subject}', f'{subject}_unique.json')
df_unique.to_json(output_path, orient='records', lines=False, force_ascii=False, indent=4)

print(f"중복 제거 전 레코드 수: {initial_count}")
print(f"중복 제거 후 레코드 수: {final_count}")
print(f"JSON 파일이 저장되었습니다: {output_path}")