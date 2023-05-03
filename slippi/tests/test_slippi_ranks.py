from decimal import Decimal

from slippi.slippi_ranks import get_rank


def test_get_rank():
    assert get_rank(0) == 'Bronze 1'
    assert get_rank(800) == 'Bronze 2'
    assert get_rank(1000) == 'Bronze 3'
    assert get_rank(1100) == 'Silver 1'
    assert get_rank(1300) == 'Silver 2'
    assert get_rank(1400) == 'Silver 3'
    assert get_rank(1500) == 'Gold 1'
    assert get_rank(1600) == 'Gold 2'
    assert get_rank(1700) == 'Gold 3'
    assert get_rank(1800) == 'Platinum 1'
    assert get_rank(1900) == 'Platinum 2'
    assert get_rank(2000) == 'Platinum 3'
    assert get_rank(2050) == 'Diamond 1'
    assert get_rank(2100) == 'Diamond 2'
    assert get_rank(2150) == 'Diamond 3'
    assert get_rank(2200) == 'Master 1'
    assert get_rank(2300) == 'Master 2'
    assert get_rank(2500) == 'Master 3'
    assert get_rank(2500, 1) == 'Grandmaster'

