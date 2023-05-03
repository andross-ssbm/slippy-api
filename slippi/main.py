from slippi.slippi_api import SlippiRankedAPI

import argparse

slippi_api = SlippiRankedAPI()


def main():
    parser = argparse.ArgumentParser(description='Slippi API')
    parser.add_argument('connect_codes', nargs='+', help='List of connect codes, separated by a space.')

    args = parser.parse_args()

    return_list = [slippi_api.get_player_ranked_data(code, True) for code in args.connect_codes]

    for player in return_list:
        print(player)


if __name__ == '__main__':
    main()
