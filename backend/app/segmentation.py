from fastapi import APIRouter, HTTPException
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from app.data_manager import data_manager

router = APIRouter()


@router.get("/customer-segmentation")
def customer_segmentation():

    if not data_manager.has_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    df = data_manager.get_data()

    required = ["Customer ID", "Sales"]

    for col in required:
        if col not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"{col} column not found."
            )

    customer = (
        df.groupby("Customer ID")
        .agg(
            TotalSales=("Sales", "sum"),
            Orders=("Order ID", "count"),
            AvgSales=("Sales", "mean")
        )
        .reset_index()
    )

    X = customer[["TotalSales", "Orders", "AvgSales"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    customer["Cluster"] = kmeans.fit_predict(X_scaled)

    descriptions = {
        0: "High Value Customers",
        1: "Regular Customers",
        2: "Low Value Customers"
    }

    summary = {}

    for cluster in sorted(customer["Cluster"].unique()):

        cluster_df = customer[customer["Cluster"] == cluster]

        summary[f"Cluster {cluster}"] = {
            "description": descriptions.get(cluster, "Customer Segment"),
            "customers": int(len(cluster_df)),
            "average_sales": round(
                float(cluster_df["TotalSales"].mean()), 2
            ),
            "average_orders": round(
                float(cluster_df["Orders"].mean()), 2
            )
        }

    return {
        "total_customers": int(len(customer)),
        "segments": summary
    }