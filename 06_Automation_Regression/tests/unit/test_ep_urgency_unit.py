from datetime import date, timedelta
import pytest
from helpers import compute_urgency

FIXED_TODAY = date(2026, 11, 10)


def test_tc_bb_006_no_due_date_none_and_empty():
    """TC-BB-006 / TC-WB-F14-01, 02: None and empty due date return 'No due date'."""
    assert compute_urgency(None, today=FIXED_TODAY) == "No due date"
    assert compute_urgency("", today=FIXED_TODAY) == "No due date"


def test_tc_bb_007_past_due_date_overdue():
    """TC-BB-007 / TC-WB-F14-03: Past due date returns 'Overdue'."""
    assert compute_urgency("2026-11-09", today=FIXED_TODAY) == "Overdue"


@pytest.mark.regression
def test_tc_bb_008_due_today_urgency():
    """TC-BB-008 / TC-WB-F14-04 (Defect D-001): Task due today must return 'Due Today'."""
    assert compute_urgency("2026-11-10", today=FIXED_TODAY) == "Due Today"


def test_tc_bb_009_near_future_due_soon():
    """TC-BB-009 / TC-WB-F14-05, 06: Due date 1 or 2 days ahead returns 'Due Soon'."""
    assert compute_urgency("2026-11-11", today=FIXED_TODAY) == "Due Soon"
    assert compute_urgency("2026-11-12", today=FIXED_TODAY) == "Due Soon"


def test_tc_bb_010_far_future_upcoming():
    """TC-BB-010 / TC-WB-F14-07, 08: Due date 3+ days ahead returns 'Upcoming'."""
    assert compute_urgency("2026-11-13", today=FIXED_TODAY) == "Upcoming"
    future_default = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    assert compute_urgency(future_default) == "Upcoming"


def test_tc_wb_f14_09_invalid_date_format_raises_value_error():
    """TC-WB-F14-09: Malformed due date string raises ValueError."""
    for bad_date in ["04-11-2026", "abc", "2026-02-30", " "]:
        with pytest.raises(ValueError):
            compute_urgency(bad_date, today=FIXED_TODAY)