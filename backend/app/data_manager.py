import pandas as pd


class DataManager:
    """
    Stores the currently uploaded dataset in memory.
    """

    def __init__(self):
        self.df = None

    def set_data(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def get_data(self):
        return self.df

    def has_data(self):
        return self.df is not None


# Singleton instance
data_manager = DataManager()