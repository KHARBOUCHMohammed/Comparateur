import pandas as pd
import sys

file_path = sys.argv[1]
data = pd.read_csv(file_path)
data.to_excel(file_path.replace('.csv', '.xlsx'), index=False)
