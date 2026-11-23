from pathlib import Path
import pandas as pd
import pytest
ROOT = Path(__file__).resolve().parents[1]
@pytest.fixture(scope="session")
def raw():
    return pd.read_csv(ROOT / "retail_customer_sales_dataset.csv")
@pytest.fixture(scope="session")
def cleaned():
    return pd.read_csv(ROOT / "data" / "retail_customer_sales_cleaned.csv")
