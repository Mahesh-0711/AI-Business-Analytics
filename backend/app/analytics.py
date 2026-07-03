import pandas as pd


# ==========================================
# Load Dataset
# ==========================================
def load_dataset(filepath):
    """
    Load CSV or Excel dataset with automatic encoding detection.
    """

    if filepath.endswith(".csv"):

        encodings = [
            "utf-8",
            "utf-8-sig",
            "cp1252",
            "latin1",
            "ISO-8859-1"
        ]

        df = None

        for encoding in encodings:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                print(f"Loaded CSV using {encoding} encoding.")
                break
            except UnicodeDecodeError:
                continue

        if df is None:
            raise ValueError(
                "Unable to read CSV. Unsupported encoding."
            )

    elif filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath)

    else:
        raise ValueError("Unsupported file format")

    # ---------------------------------------
    # Clean column names
    # ---------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\u00A0", " ", regex=False)
    )

    # ---------------------------------------
    # Automatically convert date columns
    # ---------------------------------------

    for col in df.columns:

        if "date" in col.lower():

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                dayfirst=False
            )

    # ---------------------------------------
    # Convert numeric columns
    # ---------------------------------------

    numeric_cols = [
        "Sales",
        "Profit",
        "Quantity",
        "Discount"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("$", "", regex=False)
            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


# ==========================================
# Clean Dataset
# ==========================================
def clean_data(df):

    df = df.drop_duplicates()

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].ffill()

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
        kpis["Total Sales"] = round(float(df["Sales"].sum()), 2)
        kpis["Average Sale"] = round(float(df["Sales"].mean()), 2)

    if "Profit" in df.columns:
        kpis["Total Profit"] = round(float(df["Profit"].sum()), 2)

    if "Quantity" in df.columns:
        kpis["Total Quantity"] = int(df["Quantity"].sum())

    if "Discount" in df.columns:
        kpis["Average Discount"] = round(
            float(df["Discount"].mean()),
            2
        )

    if "Order ID" in df.columns:
        kpis["Total Orders"] = int(df["Order ID"].nunique())

    return kpis


# ==========================================
# AI Business Insights
# ==========================================
def generate_insights(df):

    insights = []

    if "Sales" in df.columns:

        insights.append(
            f"Total Sales: ₹{df['Sales'].sum():,.2f}"
        )

    if "Profit" in df.columns:

        if df["Profit"].sum() > 0:
            insights.append(
                "Overall business is profitable."
            )
        else:
            insights.append(
                "Overall business is operating at a loss."
            )

    if "Region" in df.columns and "Sales" in df.columns:

        best_region = (
            df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        insights.append(
            f"Top-performing region: {best_region}"
        )

    if "Category" in df.columns and "Sales" in df.columns:

        top_category = (
            df.groupby("Category")["Sales"]
            .sum()
            .idxmax()
        )

        insights.append(
            f"Best-selling category: {top_category}"
        )

    return insights