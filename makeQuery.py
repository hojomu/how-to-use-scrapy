import pandas as pd

# 엑셀 파일 읽기
file_path = 'C:/pythonproject/ScrapyFW/ScrapyFW/results/innovationMarket/innovationMarket.xlsx'
df = pd.read_excel(file_path, dtype=str)

# 테이블 생성 쿼리
create_table_query = """
CREATE TABLE TMP_INNOVATION (
    keyword VARCHAR(50),
    name VARCHAR(100),
    item VARCHAR(255),
    businessNum VARCHAR(20),
    address VARCHAR(255),
    zipNo VARCHAR(10),
    tel VARCHAR(20),
    fax VARCHAR(20),
    homepage VARCHAR(255),
    category VARCHAR(50),
    manager VARCHAR(50),
    managerTel VARCHAR(20),
    managerEmail VARCHAR(100)
)
"""

# 데이터 삽입 쿼리 생성
insert_query = f"""
INSERT INTO TMP_INNOVATION (keyword, name, item, businessNum, address, zipNo, tel, fax, homepage, category, manager, managerTel, managerEmail)
VALUES 
"""

# 각 행을 SQL 쿼리로 변환하여 추가
values_list = []
for index, row in df.iterrows():
    values_list.append(
        f"('{row['keyword']}', '{row['name']}', '{row['item']}', '{row['businessNum']}', '{row['address']}', '{row['zipNo']}', "
        f"'{row['tel']}', '{row['fax']}', '{row['homepage']}', '{row['category']}', '{row['manager']}', '{row['managerTel']}', '{row['managerEmail']}')"
    )

insert_query += ",\n".join(values_list) + ";"

print(insert_query)
