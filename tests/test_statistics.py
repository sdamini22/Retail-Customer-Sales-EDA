import pandas as pd

def test_sales_numeric(raw):
    assert pd.api.types.is_numeric_dtype(raw["Sales"])

def test_profit_numeric(raw):
    assert pd.api.types.is_numeric_dtype(raw["Profit"])

def test_sales_total_matches_sum(raw):
    assert abs(raw.groupby("Region", dropna=False)["Sales"].sum().sum() - raw["Sales"].sum()) < 0.01

def test_count_by_region(raw):
    assert raw.groupby("Region", dropna=False).size().sum() == len(raw)

def test_median_between_min_max(raw):
    assert raw["Sales"].min() <= raw["Sales"].median() <= raw["Sales"].max()
