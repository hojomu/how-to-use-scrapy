import pandas as pd

import msoffcrypto
from io import BytesIO

from openpyxl import load_workbook


# Load the Excel file
file_path = 'C:/Users/PC-ESN-D0147/Desktop/2024 의공/인튜이티브_240716.xlsx'
password = 'messe123$%'

decrypted = BytesIO()
with open(file_path, 'rb') as f:
    file = msoffcrypto.OfficeFile(f)
    file.load_key(password=password)
    file.decrypt(decrypted)

df = pd.read_excel(decrypted, sheet_name=None)

# Assuming the relevant data is in the first sheet and in the column T
sheet_name = list(df.keys())[0]  # get the name of the first sheet
data = df[sheet_name]

# Convert the 'keyword' column to datetime
data['스캔시간'] = pd.to_datetime(data['스캔시간'], errors='coerce')

# # Apply the adjustments: +5 days and -10 hours 30 minutes
# data['스캔시간2'] = data['스캔시간'] + pd.DateOffset(months=5) + pd.DateOffset(days=27) + pd.Timedelta(hours=2, minutes=48)
data['스캔시간2'] = data['스캔시간'] + pd.Timedelta(hours=1)

data['스캔시간2'] = data['스캔시간2'].dt.strftime('%m/%d/%Y %H:%M:%S')

# # Save the adjusted data back to the Excel file
data.to_excel(file_path, index=False)
