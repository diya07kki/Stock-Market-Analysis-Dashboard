import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEANED_FILE = ROOT / "Dataset" / "cleaned" / "stock_data_cleaned.csv"

file = pd.read_csv(CLEANED_FILE)

print(file.head())
print(file.columns.tolist())
print(file.shape)

file["Date"] = pd.to_datetime(file["Date"])
print("Date range:", file["Date"].min(), "to", file["Date"].max())
print("Missing values:\n", file.isna().sum())
print("Duplicate rows:", file.duplicated().sum())
print(
    "Duplicate company-date records:",
    file.duplicated(subset=["Company", "Date"]).sum()
)

print("\nRecords per company:")
print(file.groupby("Company").size())

print("\nInvalid prices:")
print((file[["Open", "High", "Low", "Close"]] <= 0).sum())


# Sort chronologically within each company
file = file.sort_values(["Company", "Date"]).copy()

grp = file.groupby("Company", sort=False)

# Average closing price
comp_close_avg = grp["Close"].mean()

# Return across the available period
first_close = grp["Close"].first()
last_close = grp["Close"].last()

period_return = (
    (last_close - first_close) / first_close
) * 100

highest_ret = period_return.sort_values(ascending=False)
highest_ret = highest_ret.rename("Return")

# Create a company-level period return summary
returns_summary = period_return.rename("Period Return (%)").reset_index()

print("\nCompany Period Returns:")
print(returns_summary.sort_values(
    "Period Return (%)", ascending=False
).round(2))

# Save the summary for Excel
returns_summary.to_csv(
    "Dataset/cleaned/company_returns.csv",
    index=False
)

# Calculate day-to-day percentage returns
file["Daily Return"] = (
    file.groupby("Company")["Close"].pct_change() * 100
)
# Investigate ITC's largest daily loss
itc_check = file[
    (file["Company"] == "ITC") &
    (file["Date"].between("2025-12-29", "2026-01-05"))
].copy()

print("\n===== ITC Price Check =====")
print(
    itc_check[
        ["Date", "Open", "High", "Low", "Close", "Volume", "Daily Return"]
    ].to_string(index=False)
)

# Calculate volatility for each company
volatility = file.groupby("Company")["Daily Return"].std()

# Calculate average trading volume
avg_trade_vol = file.groupby("Company")["Volume"].mean()

# Get each company's sector
sort_by_sect = file.groupby("Company")["Sector"].first()

# Calculate average return by sector
perf_table = pd.concat([sort_by_sect, highest_ret], axis=1)
better_perf = (
    perf_table.groupby("Sector")["Return"]
    .mean()
    .sort_values(ascending=False)
)


# Display overall dataset information
print(f"Total rows: {len(file)}")
print(f"Total columns: {file.shape[1]}")
print(f"Companies: {file['Company'].nunique()}")

# Biggest daily gain and loss
best_trade_row = file.loc[file["Daily Return"].idxmax()]
worst_trade_row = file.loc[file["Daily Return"].idxmin()]

print("\n===== Biggest One-Day Gain =====")
print(f"Company: {best_trade_row['Company']}")
print(f"Date: {best_trade_row['Date'].date()}")
print(f"Daily Return: {best_trade_row['Daily Return']:.2f}%")

print("\n===== Biggest One-Day Loss =====")
print(f"Company: {worst_trade_row['Company']}")
print(f"Date: {worst_trade_row['Date'].date()}")
print(f"Daily Return: {worst_trade_row['Daily Return']:.2f}%")

# Create company summary
company_summary = pd.DataFrame({
    "Sector": sort_by_sect,
    "Average Close": comp_close_avg,
    "Return": period_return,
    "Average Volume": avg_trade_vol,
    "Volatility": volatility
})

company_summary = company_summary.reset_index()
company_summary.to_csv(
    "Dataset/cleaned/company_summary.csv", index=False
)

print("\nCompany Summary:")
print(company_summary.head())

# Create sector summary
sector_summary = pd.DataFrame({
    "Average Return": better_perf,
    "Average Volume": company_summary.groupby("Sector")[
        "Average Volume"
    ].mean()
}).round(2)

sector_summary = sector_summary.reset_index()
sector_summary.to_csv(
    "Dataset/cleaned/sector_summary.csv", index=False
)

print("\nSector Summary:")
print(sector_summary)
