from fastapi import APIRouter, HTTPException, Depends
from prophet import Prophet
import pandas as pd

from app.data_manager import data_manager
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/forecast")
def forecast_sales(current_user=Depends(get_current_user)):

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data().copy()

    # Validate required columns
    if "Order Date" not in df.columns or "Sales" not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="Dataset must contain 'Order Date' and 'Sales'."
        )

    # Convert dates
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=["Order Date"])

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="No valid dates found in dataset."
        )

    # Aggregate daily sales
    daily_sales = (
        df.groupby("Order Date")["Sales"]
        .sum()
        .reset_index()
    )

    daily_sales.columns = ["ds", "y"]

    if len(daily_sales) < 2:
        raise HTTPException(
            status_code=400,
            detail="Not enough data for forecasting."
        )

    # Train Prophet
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    model.fit(daily_sales)

    # Forecast next 30 days
    future = model.make_future_dataframe(periods=30)

    forecast = model.predict(future).tail(30)

    return {
        "predicted_total_sales": round(
            float(forecast["yhat"].sum()), 2
        ),
        "forecast": [
            {
                "date": row["ds"].strftime("%Y-%m-%d"),
                "predicted_sales": round(float(row["yhat"]), 2),
                "lower_bound": round(float(row["yhat_lower"]), 2),
                "upper_bound": round(float(row["yhat_upper"]), 2)
            }
            for _, row in forecast.iterrows()
        ]
    }