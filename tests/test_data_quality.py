def test_dataset_is_not_empty(raw):
    assert len(raw) > 0

def test_expected_columns(raw):
    assert {"Transaction_ID", "Sales", "Profit", "Region", "Age"}.issubset(raw.columns)

def test_duplicate_count(raw):
    assert raw.duplicated().sum() == 55

def test_missing_values_present(raw):
    assert raw.isna().sum().sum() > 0

def test_cleaned_has_no_exact_duplicates(cleaned):
    assert cleaned.duplicated().sum() == 0

def test_cleaned_not_larger_than_raw(raw, cleaned):
    assert len(cleaned) <= len(raw)
