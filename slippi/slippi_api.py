import requests
from ratelimiter import RateLimiter
from re import match

import logging

from slippi.custom_logging import CustomFormatter
from slippi.slippi_user import SlippiUser

# Get the logger instance from custom formatter
logger = CustomFormatter().get_logger()

# GraphQL query for maximum player data
query_max = """
fragment profileFieldsV2 on NetplayProfileV2 {
  id
  ratingOrdinal
  ratingUpdateCount
  wins
  losses
  dailyGlobalPlacement
  dailyRegionalPlacement
  continent
  characters {
    character
    gameCount
    __typename
  }
  __typename
}

fragment userProfilePage on User {
  fbUid
  displayName
  connectCode {
    code
    __typename
  }
  status
  activeSubscription {
    level
    hasGiftSub
    __typename
  }
  rankedNetplayProfile {
    ...profileFieldsV2
    __typename
  }
  rankedNetplayProfileHistory {
    ...profileFieldsV2
    season {
      id
      startedAt
      endedAt
      name
      status
      __typename
    }
    __typename
  }
  __typename
}

query AccountManagementPageQuery($cc: String!) {

  getConnectCode(code: $cc) {
    user {
      ...userProfilePage
      __typename
    }
    __typename
  }
}

"""

# GraphQL query for minimum player data
query_min = """
fragment profileFieldsV2 on NetplayProfileV2 {
  id
  ratingOrdinal
  ratingUpdateCount
  wins
  losses
  dailyGlobalPlacement
  dailyRegionalPlacement
  continent
  characters {
    character
    gameCount
    __typename
  }
  __typename
}

fragment userProfilePage on User {
    displayName
    connectCode {
        code
        __typename
    }
    rankedNetplayProfile {
        ..profileFieldsV2
        __typename
    }
    __typename
}
query AccountManagementPageQuery($cc: String!) {
    getConnectCode(code: $cc) {
        user {
            ...userProfilePage
            __typename
        }
        __typename
    }
}
"""


class SlippiRankedAPI:
    def __init__(self):
        # Initialize a rate limiter with maximum 1 call per second
        self._limiter = RateLimiter(max_calls=1, period=1)

    @staticmethod
    def is_valid_connect_code(connect_code: str) -> bool:
        """
        Check if the given connect code is valid.

        Args:
            connect_code (str): The connect code to validate.

        Returns:
            bool: True if the connect code is valid, False otherwise.
        """
        logger.info(f'is_valid_connect_code: {connect_code}')
        return True if (match(r"^(?=.{3,9}$)[a-zA-Z]{1,7}#[0-9]{1,7}$", connect_code)) else False

    @staticmethod
    def _get_player_data(self, connect_code: str, is_max: bool = False):
        """
        Get player data from the Slippi API.

        Args:
            self: The instance of the SlippiRankedAPI class.
            connect_code (str): The connect code of the player.
            is_max (bool): Whether to fetch maximum player data or not.

        Returns:
            dict: The player data in JSON format.
        """
        if not self.is_valid_connect_code(connect_code):
            logger.warning(f'Invalid connect_code: {connect_code}')
            return

        variables = {
            "cc": connect_code.upper(),
            "uid": connect_code.upper()
        }
        payload = {
            "operationName": "AccountManagementPageQuery",
            "query": query_min if not is_max else query_max,
            "variables": variables
        }
        headers = {
            "content-type": "application/json"
        }
        response = requests.post('https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql', json=payload,
                                 headers=headers)
        logger.debug(f'response: {response.json()}')
        return response.json()

    def get_player_data_throttled(self, connect_code: str, is_max: bool = False):
        """
        Get player data with rate limiting.

        Args:
            connect_code (str): The connect code of the player.
            is_max (bool): Whether to fetch maximum player data or not.

        Returns:
            dict: The player data in JSON format.
        """
        with self._limiter:
            return self._get_player_data(self, connect_code, is_max)

    def get_player_ranked_data(self, connect_code: str, is_max: bool = False) -> SlippiUser | None:
        """
        Get ranked player data.

        Args:
            connect_code (str): The connect code of the player.
            is_max (bool): Whether to fetch maximum player data or not.

        Returns:
            SlippiUser | None: An instance of SlippiUser class if player data is available, None otherwise.
        """
        logger.info(f'get_player_ranked_data: {connect_code}')
        player_data = self.get_player_data_throttled(connect_code, is_max)

        logger.debug(f'player_data: {player_data}')
        if not player_data or not player_data['data']['getConnectCode']:
            return

        return SlippiUser(player_data)

    def does_exist(self, connect_code: str) -> bool:
        """
        Check if a player with the given connect code exists.

        Args:
            connect_code (str): The connect code of the player.

        Returns:
            bool: True if the player exists, False otherwise.
        """
        results = self.get_player_data_throttled(connect_code)

        if not results or not results['data']['getConnectCode']:
            return False

        return True
