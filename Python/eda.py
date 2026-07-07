import pandas as pd

file = pd.read_csv("../Dataset/raw/raw_stock_data.csv")
#print(file.head())
#print(file.info())
#print(file.describe())
file['Date'] = pd.to_datetime(file['Date'])
grp = file.groupby("Company")
comp_close_avg = grp["Close"].mean().sort_values(ascending=False)     #Arrange avg close values in descending
#print(comp_close_avg)

highest_ret = ((grp["Close"].last()-grp["Close"].first())/grp["Close"].first())*100
highest_ret = highest_ret.sort_values(ascending=False)
highest_ret = highest_ret.rename("Return")
#print(highest_ret)                                                    #Prints highest return annually

avg_trade_vol = grp["Volume"].mean().sort_values(ascending=False)
#print(avg_trade_vol)                                                  #Average trading volume

sort_by_sect = file.groupby("Company")["Sector"].first()              #Sector wise group
perf_table = pd.concat([sort_by_sect,highest_ret], axis=1)
better_perf = perf_table.groupby("Sector")["Return"].mean().sort_values(ascending=False)
#print(better_perf)                                                    #Performance Sector wise

print(f"Total rows: {len(file)}")
print(f"total columns: {file.shape[1]}")
print(f"Companies ({file['Company'].nunique()})")                     #Total no. of companies
#print(file['Company'].unique())
file["Daily Return"] = ((file["Close"]-file["Open"])
                        /file["Open"])*100

volatility = grp["Daily Return"].std()
print(volatility)                                                     #Riskiest Company

best_trade_row = file.loc[file["Daily Return"].idxmax()]
print("\n===== Biggest One-Day Gain =====")
print(f"Company      : {best_trade_row['Company']}")
print(f"Date         : {best_trade_row['Date'].date()}")
print(f"Daily Return : {best_trade_row['Daily Return']:.2f}%")

worst_trade_row = file.loc[file["Daily Return"].idxmin()]
print("\n===== Biggest One-Day Loss =====")
print(f"Company      : {worst_trade_row['Company']}")
print(f"Date         : {worst_trade_row['Date'].date()}")
print(f"Daily Return : {worst_trade_row['Daily Return']:.2f}%")

print("Date Range:")                                                  #Get the starting and ending date
print(f"From {file['Date'].min().date()}")
print(f"To {file['Date'].max().date()}")

company_summary = pd.DataFrame()
company_summary["Sector"] = sort_by_sect
company_summary["Average Close"] = comp_close_avg
company_summary["Return"] = highest_ret
company_summary["Average Volume"] = avg_trade_vol
company_summary["Volatility"] = volatility
company_summary = company_summary.reset_index()

print(company_summary.head(5))
company_summary.to_csv("../Dataset/cleaned/company_summary.csv",index=False)

sector_summary = pd.DataFrame()
sector_summary["Average Return"] = better_perf.round(2)
sector_summary["Average Volume"] = company_summary.groupby("Sector")["Average Volume"].mean().round(0)
sector_summary = sector_summary.reset_index()

print(sector_summary.head(5))
sector_summary.to_csv("../Dataset/cleaned/sector_summary.csv",index=False)
