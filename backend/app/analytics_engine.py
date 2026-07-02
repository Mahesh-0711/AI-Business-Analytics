import pandas as pd


class AnalyticsEngine:

    def __init__(self, df):
        self.df = df.copy()

        if "Order Date" in self.df.columns:
            self.df["Order Date"] = pd.to_datetime(
                self.df["Order Date"],
                errors="coerce"
            )

    # -----------------------
    # KPIs
    # -----------------------

    def total_sales(self):
        return float(self.df["Sales"].sum())

    def total_profit(self):
        return float(self.df["Profit"].sum())

    def total_orders(self):
        return int(self.df["Order ID"].nunique())

    def average_sale(self):
        return float(self.df["Sales"].mean())

    def average_discount(self):
        return float(self.df["Discount"].mean())

    # -----------------------
    # Top Region
    # -----------------------

    def top_region(self):
        region = (
            self.df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        return region.head(5).to_dict()

    # -----------------------
    # Top State
    # -----------------------

    def top_states(self):
        state = (
            self.df.groupby("State")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        return state.head(10).to_dict()

    # -----------------------
    # Top Categories
    # -----------------------

    def category_sales(self):
        category = (
            self.df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        return category.to_dict()

    # -----------------------
    # Top Products
    # -----------------------

    def top_products(self):

        if "Sub-Category" not in self.df.columns:
            return {}

        product = (
            self.df.groupby("Sub-Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        return product.head(10).to_dict()

    # -----------------------
    # Payment Analysis
    # -----------------------

    def payment_analysis(self):

        if "Payment Method" not in self.df.columns:
            return {}

        return self.df["Payment Method"].value_counts().to_dict()

    # -----------------------
    # Monthly Sales
    # -----------------------

    def monthly_sales(self):

        if "Order Date" not in self.df.columns:
            return {}

        temp = self.df.copy()

        temp["Month"] = (
            temp["Order Date"]
            .dt.to_period("M")
            .astype(str)
        )

        sales = (
            temp.groupby("Month")["Sales"]
            .sum()
            .sort_index()
        )

        return sales.to_dict()

    # -----------------------
    # Profit by Region
    # -----------------------

    def profit_by_region(self):

        profit = (
            self.df.groupby("Region")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        return profit.to_dict()

    # -----------------------
    # Discount Analysis
    # -----------------------

    def discount_analysis(self):

        return {
            "average_discount": float(self.df["Discount"].mean()),
            "maximum_discount": float(self.df["Discount"].max()),
            "minimum_discount": float(self.df["Discount"].min())
        }

    # -----------------------
    # Top Customers
    # -----------------------

    def top_customers(self):

        if "Customer Name" not in self.df.columns:
            return {}

        customer = (
            self.df.groupby("Customer Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        return customer.head(10).to_dict()

    # -----------------------
    # Summary
    # -----------------------

    def generate_summary(self):

        return {

            "total_sales": self.total_sales(),

            "total_profit": self.total_profit(),

            "total_orders": self.total_orders(),

            "average_sale": self.average_sale(),

            "average_discount": self.average_discount(),

            "top_regions": self.top_region(),

            "top_states": self.top_states(),

            "category_sales": self.category_sales(),

            "top_products": self.top_products(),

            "payment_analysis": self.payment_analysis(),

            "monthly_sales": self.monthly_sales(),

            "profit_by_region": self.profit_by_region(),

            "discount_analysis": self.discount_analysis(),

            "top_customers": self.top_customers()

        }