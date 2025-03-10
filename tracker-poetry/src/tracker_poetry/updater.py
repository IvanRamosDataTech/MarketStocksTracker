import sqlquery
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)


print("==== Updating Database with Excel portfolio sheet .... =====")

ppr_snapshot = pd.read_excel("Portafolio Indizado_Patrimonial.xlsx", sheet_name="Indizado PPR", header=4)

print(ppr_shapshot.head(20))