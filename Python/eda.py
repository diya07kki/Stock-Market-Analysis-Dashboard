import pandas as pd

file = pd.read_csv("../Dataset/raw/raw_stock_data.csv")
#print(file.head())
#print(file.info())
#print(file.describe())
file['Date'] = pd.to_datetime(file['Date'])
grp = file.groupby("Companies")
comp_close_avg = grp["Close"].mean().sort_values(ascending=False)     #Arrange avg close values in ascending
print(comp_close_avg)

highest_ret = ((grp["Close"].last-grp["Close"].first)/grp["Close"].first)*100
highest_ret = highest_ret.sort_values(ascending=False)
highest_ret = highest_ret.rename("Return")
print(highest_ret)                                                    #Prints highest return annually

avg_trade_vol = grp["Volume"].mean().sort_values(ascending=False)
print(avg_trade_vol)                                                  #Average trading volume

sort_by_sect = file.groupby("Company")["Sector"].first()              #Sector wise group
perf_table = pd.concat([sort_by_sect,highest_ret], axis=1)
better_perf = perf_table.groupby("Sector")["Return"].mean().sort_values(ascending=False)
print(better_perf)                                                    #Performance Sector wise

print(f"Total rows: {len(file)}")
print(f"total columns: {file.shape[1]}")
print(f"Companies ({file['Company'].nunique()})")                     #Total no. of companies
#print(file['Company'].unique())

print(f"Companies ({file['Sector'].nunique()})")                      #Total no. of sectors
#print(file['Sector'].unique())

print("Date Range:")                                                  #Get the starting and ending date
print(f"From {file['Date'].min().date()}")
print(f"To {file['Date'].max().date()}")