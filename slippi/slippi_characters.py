from slippi.custom_logging import CustomFormatter

logger = CustomFormatter().get_logger()

slippi_character_url = 'https://slippi.gg/images/characters/stock-icon-?-0.png'


SlippiCharacterId = {
    'DONKEY_KONG': 0,  # Mapped to 255 in database
    'CAPTAIN_FALCON': 1,
    'FOX': 2,
    'GAME_AND_WATCH': 3,
    'KIRBY': 4,
    'BOWSER': 5,
    'LINK': 6,
    'LUIGI': 7,
    'MARIO': 8,
    'MARTH': 9,
    'MEWTWO': 10,
    'NESS': 11,
    'PEACH': 12,
    'PIKACHU': 13,
    'ICE_CLIMBERS': 14,
    'JIGGLYPUFF': 15,
    'SAMUS': 16,
    'YOSHI': 17,
    'ZELDA': 18,
    'SHEIK': 19,
    'FALCO': 20,
    'YOUNG_LINK': 21,
    'DR_MARIO': 22,
    'ROY': 23,
    'PICHU': 24,
    'GANONDORF': 25,
    'None': 256
}


SlippiCharacterColors = {
    'DONKEY_KONG': '#2f1003',
    'CAPTAIN_FALCON': '#353c5e',
    'FOX': '#ffb242',
    'GAME_AND_WATCH': '#000000',
    'KIRBY': '#ffbed8',
    'BOWSER': '#376218',
    'LINK': '#073f07',
    'LUIGI': '#10b91a',
    'MARIO': '#ff1d1c',
    'MARTH': '#2f3955',
    'MEWTWO': '#734c60',
    'NESS': '#f9ca58',
    'PEACH': '#ff5488',
    'PIKACHU': '#ffff00',
    'ICE_CLIMBERS': '#8a63ff',
    'JIGGLYPUFF': '#ffd6f0',
    'SAMUS': '#da490c',
    'YOSHI': '#008000',
    'ZELDA': '#f9d9e6',
    'SHEIK': '#4846db',
    'FALCO': '#494fd6',
    'YOUNG_LINK': '#009e01',
    'DR_MARIO': '#d1cfc9',
    'ROY': '#962000',
    'PICHU': '#ffff1b',
    'GANONDORF': '#91763e',
}


def get_key_from_value(value, dict):
    for key, val in dict.items():
        if val == value:
            return key
    return None


def get_character_name(char_id: int) -> str:
    logger.info(f'get_character_name: {char_id}')
    if char_id == 255:
        char_id = 0
    return get_key_from_value(char_id, SlippiCharacterId)


def get_character_id(name: str, dk_claus: bool = False) -> int:
    logger.info(f'get_character_id: {name}')
    character_id = SlippiCharacterId.get(name)
    if dk_claus and character_id == 0:
        character_id = 255
    return character_id


def get_character_url(name: str) -> str:
    logger.info(f'get_character_url: {name}')
    return slippi_character_url.replace('?', str(get_character_id(name)))
