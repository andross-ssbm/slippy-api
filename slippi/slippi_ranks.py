from dataclasses import dataclass

from slippi.custom_logging import CustomFormatter

logger = CustomFormatter().get_logger()


@dataclass
class Rank:
    lower_bound: float
    upper_bound: float
    rank_name: str


class GrandMaster(Rank):
    rank_name = 'Grandmaster'


grand_master = GrandMaster(lower_bound=2191.75, upper_bound=float('inf'), rank_name='Grandmaster')
rank_list = [
    Rank(0, 765.42, 'Bronze 1'),
    Rank(765.43, 913.71, 'Bronze 2'),
    Rank(913.72, 1054.86, 'Bronze 3'),
    Rank(1054.87, 1188.87, 'Silver 1'),
    Rank(1188.88, 1315.74, 'Silver 2'),
    Rank(1315.75, 1435.47, 'Silver 3'),
    Rank(1435.48, 1548.06, 'Gold 1'),
    Rank(1548.07, 1653.51, 'Gold 2'),
    Rank(1653.52, 1751.82, 'Gold 3'),
    Rank(1751.83, 1842.99, 'Platinum 1'),
    Rank(1843, 1927.02, 'Platinum 2'),
    Rank(1927.03, 2003.91, 'Platinum 3'),
    Rank(2003.92, 2073.66, 'Diamond 1'),
    Rank(2073.67, 2136.27, 'Diamond 2'),
    Rank(2136.28, 2191.74, 'Diamond 3'),
    Rank(2191.75, 2274.99, 'Master 1'),
    Rank(2275, 2350, 'Master 2'),
    Rank(2350, float('inf'), 'Master 3')
]


def get_rank(elo: float, daily_regional_placement: int = None, daily_global_placement: int = None):
    logger.info(f'get_rank: {elo}, {daily_regional_placement}, {daily_global_placement}')
    if daily_regional_placement or daily_global_placement:
        return grand_master.rank_name

    for rank in rank_list:
        if rank.lower_bound <= elo < rank.upper_bound:
            return rank.rank_name

    # If score is greater than the upper bound of the last rank, return the highest rank
    return rank_list[-1].rank_name
