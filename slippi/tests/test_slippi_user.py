import pytest
from slippi.slippi_user import SlippiUser

test_data = {
    "data": {
        "getConnectCode": {
            "user": {
                "displayName": "Bramus",
                "connectCode": {
                    "code": "BRAZ#13",
                    "__typename": "ConnectCode"
                },
                "rankedNetplayProfile": {
                    "id": "0x22d4a6",
                    "ratingOrdinal": 2232.203952,
                    "ratingUpdateCount": 164,
                    "wins": 98,
                    "losses": 66,
                    "dailyGlobalPlacement": None,
                    "dailyRegionalPlacement": None,
                    "continent": "NORTH_AMERICA",
                    "characters": [
                        {
                            "id": "0x262263",
                            "character": "MARTH",
                            "gameCount": 106,
                            "__typename": "CharacterUsage"
                        },
                        {
                            "id": "0x268531",
                            "character": "FOX",
                            "gameCount": 291,
                            "__typename": "CharacterUsage"
                        },
                        {
                            "id": "0x39a923",
                            "character": "SHEIK",
                            "gameCount": 1,
                            "__typename": "CharacterUsage"
                        }
                    ],
                    "__typename": "NetplayProfile"
                },
                "__typename": "User"
            },
            "__typename": "ConnectCode"
        }
    }
}

test_data2 = {
    "data": {
        "getConnectCode": {
            "user": {
                "displayName": "IDCrisis",
                "connectCode": {
                    "code": "IDCR#192",
                    "__typename": "ConnectCode"
                },
                "rankedNetplayProfile": {
                    "id": "0x6feaa8",
                    "ratingOrdinal": 1100,
                    "ratingUpdateCount": 0,
                    "wins": None,
                    "losses": None,
                    "dailyGlobalPlacement": None,
                    "dailyRegionalPlacement": None,
                    "continent": None,
                    "characters": [],
                    "__typename": "NetplayProfile"
                },
                "__typename": "User"
            },
            "__typename": "ConnectCode"
        }
    }
}

test_data3 = {
    "data": {
        "getConnectCode": None
    }
}


@pytest.fixture
def user_from_data():
    def make_user(data):
        return SlippiUser(data)

    return make_user


def test_slippi_user_with_data_1(user_from_data):
    user = user_from_data(test_data)
    assert user.display_name == 'Bramus'
    assert user.connect_code == 'BRAZ#13'
    assert user.ranked_profile.id == 2282662
    assert user.ranked_profile.rating_ordinal == 2232.203952
    assert user.ranked_profile.rating_update_count == 164
    assert user.ranked_profile.wins == 98
    assert user.ranked_profile.losses == 66
    assert user.ranked_profile.continent == 'NORTH_AMERICA'
    assert len(user.ranked_profile.characters) == 3
    assert user.ranked_profile.characters[0].id == '0x262263'
    assert user.ranked_profile.characters[0].character == 'MARTH'
    assert user.ranked_profile.characters[0].game_count == 106


def test_slippi_user_with_data_2(user_from_data):
    user = user_from_data(test_data2)
    assert user.display_name == 'IDCrisis'
    assert user.connect_code == 'IDCR#192'
    assert user.ranked_profile.id == 7334568
    assert user.ranked_profile.rating_ordinal == 1100
    assert user.ranked_profile.rating_update_count == 0
    assert user.ranked_profile.wins == 0
    assert user.ranked_profile.losses == 0
    assert user.ranked_profile.continent == 'NONE'
    assert len(user.ranked_profile.characters) == 0


def test_slippi_user_with_data_3(user_from_data):
    user = user_from_data(test_data3)
    assert user.display_name == ''
    assert user.connect_code == ''
    assert user.ranked_profile.id is None
    assert user.ranked_profile.rating_ordinal == 1100
    assert user.ranked_profile.rating_update_count is None
    assert user.ranked_profile.wins == 0
    assert user.ranked_profile.losses == 0
    assert user.ranked_profile.continent is None
    assert len(user.ranked_profile.characters) == 0
