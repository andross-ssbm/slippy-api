from dataclasses import dataclass, field
from .custom_logging import CustomFormatter

from .slippi_ranks import get_rank
from .slippi_characters import get_character_id, get_character_url

logger = CustomFormatter().get_logger()


@dataclass
class Characters:
    """Represents a character with its ID, name, and game count."""
    character: str = ''
    game_count: int = 0

    def get_character_icon_url(self):
        """Get the URL of the character's icon."""
        return get_character_url(self.character)

    def get_true_character_id(self):
        """Get the true character ID, accounting for special cases."""
        return get_character_id(self.character)

    def __eq__(self, other):
        """Check if two Characters instances are equal."""
        return self.character == other.character and self.game_count == other.game_count


@dataclass
class RankedNetplayProfile:
    """Represents a ranked netplay profile with its ID, rating, win/loss counts, placements, and character data."""
    id: str = None
    rating_mu: float = None
    rating_sigma: float = None
    rating_ordinal: float = 1100
    rating_update_count: int = None
    wins: int = 0
    losses: int = 0
    daily_global_placement = None
    daily_regional_placement = None
    continent: str = None
    characters: list[Characters] = field(default_factory=list)


@dataclass
class SubscriptionStatus:
    """Represents the subscription status with its active state and level."""
    active: bool = False
    level: str = 'NONE'
    gift: bool = False


@dataclass
class SlippiUser:
    """Represents a Slippi user with their display name, connect code, subscription status, and ranked netplay profile."""
    display_name: str = ''
    connect_code: str = ''
    sub_status: SubscriptionStatus = SubscriptionStatus()
    ranked_profile: RankedNetplayProfile = RankedNetplayProfile()

    def __init__(self, slippi_data: dict):
        """Initialize the SlippiUser object based on the provided Slippi data.

        Args:
            slippi_data (dict): The Slippi data containing the user information.
        """
        logger.info('SlippiUser created')

        # Check if dict exists correctly
        if not slippi_data['data']['getUser']['connectCode']['code']:
            return

        # Create local variables to use later
        user_data = slippi_data['data']['getUser']
        ranked_data = user_data['rankedNetplayProfile']

        # Assign nothing if user_data not present
        if not user_data:
            return

        # Assign values from user
        self.display_name = user_data['displayName']
        self.connect_code = user_data['connectCode']['code']

        # Assign values from activeSubscription
        if 'activeSubscription' in user_data:
            sub_data = user_data['activeSubscription']
            self.sub_status = SubscriptionStatus(
                level=sub_data['level'],
                gift=bool(sub_data['hasGiftSub']),
                active=True if sub_data['level'] != 'NONE' else False
            )

        # Loop through characters in rankedNetplayProfile to generate Characters list
        characters_list = []
        for character in ranked_data['characters']:
            if character:
                characters_list.append(
                    Characters(
                        character=character['character'],
                        game_count=character['gameCount'])
                )

        self.ranked_profile = RankedNetplayProfile(
            id=ranked_data['id'],
            rating_mu=ranked_data['ratingMu'],
            rating_sigma=ranked_data['ratingSigma'],
            rating_ordinal=ranked_data['ratingOrdinal'],
            rating_update_count=ranked_data['ratingUpdateCount'],
            wins=ranked_data['wins'] or 0,
            losses=ranked_data['losses'] or 0,
            continent=ranked_data['continent'] or 'NONE',
            characters=characters_list
        )
        self.ranked_profile.daily_global_placement = ranked_data['dailyGlobalPlacement'] or 0
        self.ranked_profile.daily_regional_placement = ranked_data['dailyRegionalPlacement'] or 0

    def get_rank(self) -> str:
        """Get the rank of the Slippi user based on their ranked profile.

        Returns:
            str: The name of the rank.
        """
        # Check if they've played their placement games, or else return 'None'
        if (self.ranked_profile.wins + self.ranked_profile.losses) < 5:
            return 'None' if not self.ranked_profile.wins and self.ranked_profile.losses else 'Pending'
        return get_rank(self.ranked_profile.rating_ordinal,
                        self.ranked_profile.daily_global_placement)

    def get_user_profile_page(self) -> str:
        """Get the URL of the user's profile page.

        Returns:
            str: The URL of the user's profile page.
        """
        return f'https://slippi.gg/user/{self.connect_code.replace("#", "-")}'

    def get_main_character(self) -> Characters:
        """Get the main character of the Slippi user based on game count.

        Returns:
            Characters: The character with the highest game count.
        """
        character_to_return = None
        highest_game_count = 0
        for guy in self.ranked_profile.characters:
            if guy.game_count > highest_game_count:
                highest_game_count = guy.game_count
                character_to_return = guy

        return character_to_return
