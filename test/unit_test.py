import os
import sys

import pandas as pd
import pytest

sys.path.append(os.path.dirname(__file__))

from src.components.data_load import data_loader, PATH
from src.components.data_transformation import data_cleaning


# ---------- fixtures ----------

@pytest.fixture(scope="module")
def loader():
    """Load real CSVs once per test module."""
    dl = data_loader(PATH)
    dl.load_data()
    return dl


@pytest.fixture(scope="module")
def cleaner():
    """Instantiate data_cleaning and load real data once per test module."""
    dc = data_cleaning()
    dc.load_data()
    return dc


@pytest.fixture
def cleaner_with_synthetic_dupes():
    """Fresh cleaner pre-populated with known duplicates for deterministic tests."""
    dc = data_cleaning()
    dc.cust_data = pd.DataFrame({
        "customer_id": ["C1", "C1", "C2", "C3"],
        "name": ["A", "A", "B", "C"],
    })
    dc.acc_data = pd.DataFrame({
        "account_id": ["ACC1", "ACC2", "ACC2"],
        "balance": [100, 200, 200],
    })
    dc.txn_data = pd.DataFrame({
        "txn_id": ["T1", "T2", "T2", "T3", "T3"],
        "amount": [10, 20, 20, 30, 30],
    })
    return dc


# ---------- data_loader tests ----------

class TestDataLoader:

    def test_three_dataframes_are_loaded(self, loader):
        assert isinstance(loader.cust_data, pd.DataFrame)
        assert isinstance(loader.acc_data, pd.DataFrame)
        assert isinstance(loader.txn_data, pd.DataFrame)

    def test_dataframes_are_not_empty(self, loader):
        assert len(loader.cust_data) > 0, "customers.csv loaded empty"
        assert len(loader.acc_data) > 0, "accounts.csv loaded empty"
        assert len(loader.txn_data) > 0, "transactions.csv loaded empty"

    def test_invalid_path_raises_exception(self):
        bad = data_loader("/nonexistent/path/xyz")
        with pytest.raises(Exception):
            bad.load_data()


# ---------- data_cleaning.load_data tests ----------

class TestDataCleaningLoad:

    def test_load_returns_three_dataframes(self, cleaner):
        assert isinstance(cleaner.cust_data, pd.DataFrame)
        assert isinstance(cleaner.acc_data, pd.DataFrame)
        assert isinstance(cleaner.txn_data, pd.DataFrame)

    def test_dataframes_have_rows(self, cleaner):
        assert len(cleaner.cust_data) > 0
        assert len(cleaner.acc_data) > 0
        assert len(cleaner.txn_data) > 0


# ---------- remove_duplicates tests ----------

class TestRemoveDuplicates:

    def test_synthetic_duplicates_are_removed(self, cleaner_with_synthetic_dupes):
        cust, acc, txn = cleaner_with_synthetic_dupes.remove_duplicates()
        assert len(cust) == 3, "expected 1 duplicate removed from customers"
        assert len(acc) == 2, "expected 1 duplicate removed from accounts"
        assert len(txn) == 3, "expected 2 duplicates removed from transactions"

    def test_no_duplicates_means_no_rows_removed(self):
        dc = data_cleaning()
        dc.cust_data = pd.DataFrame({"id": [1, 2, 3]})
        dc.acc_data = pd.DataFrame({"id": [1, 2]})
        dc.txn_data = pd.DataFrame({"id": [1, 2, 3, 4]})

        cust, acc, txn = dc.remove_duplicates()
        assert len(cust) == 3
        assert len(acc) == 2
        assert len(txn) == 4

    def test_index_is_reset_after_dedup(self):
        dc = data_cleaning()
        dc.cust_data = pd.DataFrame({"id": [1, 1, 2]})
        dc.acc_data = pd.DataFrame({"id": [1]})
        dc.txn_data = pd.DataFrame({"id": [1]})

        cust, _, _ = dc.remove_duplicates()
        assert list(cust.index) == [0, 1]

    def test_real_data_dedup_runs_without_error(self, cleaner):
        cust, acc, txn = cleaner.remove_duplicates()
        assert len(cust) > 0
        assert len(acc) > 0
        assert len(txn) > 0
