import pandas as pd

def format_region(col: tuple[str, str]):
    """Return a clean display name for a (country, province) column."""
    country, province = col
    if not province or str(province).lower() == "nan" or province.strip() == "" or province == country:
        return country
    return f"{country} - {province}"

def summary_stats(df: pd.DataFrame, countries: list[tuple[str, str]]):
    """Build summary stats for selected countries or provinces."""
    summary = {"Region": [], "Total Cases": [], "Peak Cases": [], "Peak Date": []}

    for col in countries:
        series = pd.to_numeric(df[col], errors="coerce")

        total = series.sum(skipna=True)
        peak = series.max(skipna=True)
        peak_idx = series.idxmax() if peak > 0 else None

        summary["Region"].append(format_region(col))
        summary["Total Cases"].append(int(total) if pd.notna(total) else 0)
        summary["Peak Cases"].append(int(peak) if pd.notna(peak) else 0)
        summary["Peak Date"].append(
            df.loc[peak_idx, ("Date", "")].strftime("%Y-%m-%d") if peak_idx is not None else "N/A"
        )

    return pd.DataFrame(summary)

def global_cases(df: pd.DataFrame) -> pd.DataFrame:
    """Add GlobalCases column = sum of all numeric columns by row."""
    numeric_df = df.drop(columns=[("Date", "")], axis=1, errors="ignore")
    df[("GlobalCases", "")] = numeric_df.sum(axis=1, numeric_only=True)
    return df