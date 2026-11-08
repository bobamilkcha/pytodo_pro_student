import pytest
from datetime import datetime, timedelta
from helpers import completed_in_last_n_days

# We use a fixed "now" time so our tests are stable and don't randomly fail tomorrow
NOW = datetime(2026, 11, 8, 12, 0, 0)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def test_completed_within_bounds():
    """Branch: Date is valid, past, and within N days -> True"""
    past_date = (NOW - timedelta(days=3)).strftime(DATE_FORMAT)
    assert completed_in_last_n_days(past_date, 7, now=NOW) is True

def test_completed_older_than_n_days():
    """Branch: age.days < n evaluates to False"""
    old_date = (NOW - timedelta(days=8)).strftime(DATE_FORMAT)
    assert completed_in_last_n_days(old_date, 7, now=NOW) is False

def test_completed_exactly_n_days_ago():
    """Boundary: Reproduces Defect D-005 (exactly 7 days returns False)"""
    exact_date = (NOW - timedelta(days=7)).strftime(DATE_FORMAT)
    assert completed_in_last_n_days(exact_date, 7, now=NOW) is False

def test_completed_in_future():
    """Branch: age.total_seconds() > 0 evaluates to False"""
    future_date = (NOW + timedelta(days=1)).strftime(DATE_FORMAT)
    assert completed_in_last_n_days(future_date, 7, now=NOW) is False

def test_invalid_date_format():
    """Branch: ValueError exception raised on bad string format"""
    with pytest.raises(ValueError):
        completed_in_last_n_days("not-a-real-date", 7, now=NOW)

def test_empty_date():
    """Branch: Handles missing/None date gracefully"""
    assert completed_in_last_n_days(None, 7, now=NOW) is False
    assert completed_in_last_n_days("", 7, now=NOW) is False

def test_completed_default_now():
    """Branch: now is None -> defaults to real datetime.now()"""
    # Create a date exactly 1 day ago from the actual current time
    recent_date = (datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT)
    
    # Call the function WITHOUT the `now` parameter to trigger line 72
    assert completed_in_last_n_days(recent_date, 7) is True    