import pandas as pd


# ==========================================
# Load Dataset
# ==========================================
def load_dataset(filepath):
    """
    Load CSV or Excel dataset.
    """

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)

    elif filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath)

    else:
        raise ValueError("Unsupported file format")

    # Convert date columns automatically
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


# ==========================================
# Clean Dataset
# ==========================================
def clean_data(df):
    """
    Remove duplicates and fill missing values.
    """

    df = df.drop_duplicates()

    for col in df.columns:

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())

        # Datetime columns
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].ffill()

        # Text columns
        else:
            df[col] = df[col].fillna("Unknown")

    return df


# ==========================================
# Dataset Summary
# ==========================================
def summary(df):

    return {
        "Rows": int(len(df)),
        "Columns": int(len(df.columns)),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    }


# ==========================================
# KPI Calculation
# ==========================================
def calculate_kpis(df):

    kpis = {}

    if "Sales" in df.columns:
        kpis["Total Sales"] = float(df["Sales"].sum())
        kpis["Average Sale"] = float(df["Sales"].mean())

    if "Profit" in df.columns:
        kpis["Total Profit"] = float(df["Profit"].sum())

    if "Quantity" in df.columns:
        kpis["Total Quantity"] = int(df["Quantity"].sum())

    if "Discount" in df.columns:
        kpis["Average Discount"] = float(df["Discount"].mean())

    if "Order ID" in df.columns:
        kpis["Total Orders"] = int(df["Order ID"].nunique())

    return kpis


# ==========================================
# AI Business Insights
# ==========================================
def generate_insights(df):

    insights = []

    if "Sales" in df.columns:

        total_sales = float(df["Sales"].sum())

        insights.append(
            f"Total Sales generated: ₹{total_sales:,.2f}"
        )

    if "Profit" in df.columns:

        total_profit = float(df["Profit"].sum())

        if total_profit > 0:
            insights.append(
                "Business is currently profitable."
            )
        else:
            insights.append(
                "Business is currently running at a loss."
            )

    if "Region" in df.columns and "Sales" in df.columns:

        region_sales = df.groupby("Region")["Sales"].sum()

        best_region = str(region_sales.idxmax())

        insights.append(
            f"Highest sales were recorded in {best_region} region."
        )

    if "Category" in df.columns and "Sales" in df.columns:

        category_sales = df.groupby("Category")["Sales"].sum()

        top_category = str(category_sales.idxmax())

        insights.append(
            f"Top performing category: {top_category}"
        )

    return insights