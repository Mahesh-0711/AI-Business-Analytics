from fastapi import APIRouter, HTTPException, Depends

from app.data_manager import data_manager
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/charts")
def get_charts(current_user=Depends(get_current_user)):

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data()

    charts = {}

    # Sales by Region
    if "Region" in df.columns and "Sales" in df.columns:

        region_sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .to_dict()
        )

        charts["sales_by_region"] = {
            "labels": list(region_sales.keys()),
            "values": [float(v) for v in region_sales.values()]
        }

    # Sales by Category
    if "Category" in df.columns and "Sales" in df.columns:

        category_sales = (
            df.groupby("Category")["Sales"]
            .sum()
            .to_dict()
        )

        charts["sales_by_category"] = {
            "labels": list(category_sales.keys()),
            "values": [float(v) for v in category_sales.values()]
        }

    # Profit by Category
    if "Category" in df.columns and "Profit" in df.columns:

        profit = (
            df.groupby("Category")["Profit"]
            .sum()
            .to_dict()
        )

        charts["profit_by_category"] = {
            "labels": list(profit.keys()),
            "values": [float(v) for v in profit.values()]
        }

    # Monthly Sales
    if "Order Date" in df.columns and "Sales" in df.columns:

        temp = df.copy()

        temp["Order Date"] = (
            temp["Order Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (
            temp.groupby("Order Date")["Sales"]
            .sum()
            .to_dict()
        )

        charts["monthly_sales"] = {
            "labels": list(monthly.keys()),
            "values": [float(v) for v in monthly.values()]
        }

    return charts