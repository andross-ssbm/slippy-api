from slippi.slippi_characters import get_character_url, get_character_id, \
    SlippiCharacterId, slippi_character_url


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

    return None


def test_get_character_url_and_id():

    for i in range(0, 25):
        character_name = get_key(SlippiCharacterId, i)
        assert get_character_id(character_name) == i
        assert get_character_url(character_name) == slippi_character_url.replace('?', str(i))

    assert not get_character_id('not a character')
    assert get_character_url('not a character') == slippi_character_url.replace('?', str(None))
