# slippy-api

## Overview

slippy-api is a simple wrapper for slippi.gg's GraphQL API.


## Installation

`pip install slippy-api` 

## Usage

```python
from slippi.slippi_api import SlippiRankedAPI

# Initialize the SlippiRankedAPI class
slippi_api = SlippiRankedAPI()

# Show slippi users data
slippi_user = slippi_api.get_player_ranked_date('so#0', True)
print(slippi_user)

```

## License

This library is licensed under the MIT License. See the [LICENSE](https://github.com/andross-ssbm/slippy-api/blob/master/LICENSE) file for more information.

----------