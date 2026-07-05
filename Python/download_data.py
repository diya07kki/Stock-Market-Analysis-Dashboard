import yfinance as yf
import pandas as pd

companies = pd.read_excel("../Dataset/companies.xlsx")
all_data = []

for _,row in companies.iterrows():
    print(f"Downloading data for {row["Company"]}..")
    data = yf.download(row["Ticker"],period="2y",interval="1d")
    data.columns = data.columns.get_level_values(0)
    #print(data.columns)
    data["Company"] = row["Company"]
    data["Sector"] = row["Sector"]

    all_data.append(data)

comp_data = pd.concat(all_data)
comp_data = comp_data.reset_index()

print(comp_data[comp_data["Close"].isna()])

comp_data.to_csv("../Dataset/raw/raw_stock_data.csv",index=False)