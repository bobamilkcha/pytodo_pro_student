import pytest
from helpers import is_valid_password


def test_tc_bb_bva_f01_01_seven_char_password():
    """TC-BB-BVA-F01-01: 7-character password (just below minimum boundary) must be rejected."""
    assert is_valid_password("Pass123") is False


@pytest.mark.regression
def test_tc_bb_bva_f01_02_eight_char_password():
    """TC-BB-BVA-F01-02 (Defect D-004): 8-character password (exact boundary) must be accepted."""
    assert is_valid_password("Pass1234") is True


def test_tc_bb_bva_f01_03_nine_char_password():
    """TC-BB-BVA-F01-03: 9-character password (just above boundary) must be accepted."""
    assert is_valid_password("Pass12345") is True