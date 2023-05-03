import requests
from ratelimiter import RateLimiter
from re import match

import logging

from slippi.slippi_user import SlippiUser

logger = logging.Logger(f'andross.{__name__}')

query_max = """
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
    id
    ratingOrdinal
    ratingUpdateCount
    wins
    losses
    dailyGlobalPlacement
    dailyRegionalPlacement
    continent
    characters {
      id
      character
      gameCount
      __typename
    }
    __typename
  }
  __typename
}
query AccountManagementPageQuery($cc: String!, $uid: String!) {
  getUser(fbUid: $uid) {
    ...userProfilePage
    __typename
  }
  getConnectCode(code: $cc) {
    user {
      ...userProfilePage
      __typename
    }
    __typename
  }
}

"""

query_min = """
                fragment userProfilePage on User {
                    displayName
                    connectCode {
                        code
                        __typename
                    }
                    rankedNetplayProfile {
                        id
                        ratingOrdinal
                        ratingUpdateCount
                        wins
                        losses
                        dailyGlobalPlacement
                        dailyRegionalPlacement
                        continent
                        characters {
                            id
                            character
                            gameCount
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


class SlippiRankedAPI:
    def __init__(self):
        self._limiter = RateLimiter(max_calls=1, period=1)

    @staticmethod
    def is_valid_connect_code(connect_code: str) -> bool:
        return True if (match(r"^(?=.{3,9}$)[a-zA-Z]{1,7}#[0-9]{1,7}$", connect_code)) else False

    @staticmethod
    def _get_player_data(self, connect_code: str, is_max: bool = False):

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
        return response.json()

    def get_player_data_throttled(self, connect_code: str, is_max: bool = False):
        with self._limiter:
            return self._get_player_data(self, connect_code, is_max)

    def get_player_ranked_data(self, connect_code: str, is_max: bool = False) -> SlippiUser | None:
        logger.info(f'get_player_ranked_data: {connect_code}')
        player_data = self.get_player_data_throttled(connect_code, is_max)

        logger.debug(f'player_data: {logger}')
        if not player_data or not player_data['data']['getConnectCode']:
            return

        return SlippiUser(player_data)

    def does_exist(self, connect_code: str) -> bool:
        results = self.get_player_data_throttled(connect_code)

        if not results or not results['data']['getConnectCode']:
            return False

        return True
