
from pathlib import Path

import pandas as pd


# Project paths
ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = ROOT / "Dataset" / "raw" / "raw_stock_data.csv"
CLEANED_DIR = ROOT / "Dataset" / "cleaned"
CLEANED_FILE = CLEANED_DIR / "stock_data_cleaned.csv"

PRICE_COLUMNS = ["Open", "High", "Low", "Close"]


def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_FILE}. "
            "Run download_data.py first."
        )

    df = pd.read_csv(RAW_FILE)
    initial_rows = len(df)

    if df.empty:
        raise ValueError("The raw dataset is empty.")

    # Standardize column names and text fields
    df.columns = df.columns.str.strip()

    required_columns = [
        "Date", "Company", "Sector",
        "Open", "High", "Low", "Close", "Volume"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    for col in ["Company", "Sector"]:
        df[col] = df[col].astype("string").str.strip()

    # Convert dates and numeric fields
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_columns = PRICE_COLUMNS + ["Volume"]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Report missing values before cleaning
    print("Missing values before cleaning:")
    print(df[required_columns].isna().sum())

    # Remove rows missing essential identifiers or closing price
    df = df.dropna(
        subset=["Date", "Company", "Sector", "Close"]
    ).copy()

    df = df[
        df["Company"].ne("") &
        df["Sector"].ne("")
    ].copy()

    # Remove records with non-positive closing prices
    df = df[df["Close"] > 0].copy()

    # Remove duplicate records for the same company and date
    df = df.sort_values(["Company", "Date"])
    df = df.drop_duplicates(
        subset=["Company", "Date"],
        keep="last"
    )

    # Sort the final dataset chronologically
    df = df.sort_values(["Company", "Date"]).reset_index(drop=True)

    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEANED_FILE, index=False)

    print("\nCleaning completed.")
    print(f"Original rows: {initial_rows}")
    print(f"Cleaned rows: {len(df)}")
    print(f"Rows removed: {initial_rows - len(df)}")
    print(f"Remaining duplicate company-date records: "
          f"{df.duplicated(['Company', 'Date']).sum()}")
    print(f"Cleaned dataset saved to: {CLEANED_FILE}")


if __name__ == "__main__":
    main()
