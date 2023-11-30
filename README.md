![Logo Image](logo.png)

## Table Of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Authors & Contributers](#authors)

## Getting Started
Check out [BotetteUI](https://github.com/Fantaxico/botetteUI) it is a useful UI tool for more readable and direct access. 

### Installation
Install dependencies [tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

Install Botette with pip

```bash
  pip install botette
```


    
## Usage
Start the bot by calling main.py
```bash
python ./main.py
```
In order to make changes to the behavior of the code, use [BotetteUI](https://github.com/Fantaxico/botetteUI) or adapt the `config.json` yourself.

#### Example config.json
```json
{
  "Targets": [
    {
      "Name": "Charmander",
      "PriorityBall": {
        "Name": "Great Ball"
      }
    }
  ],
  "MoveToUse": "1",
  "RunningDirection": "Left/Right",
  "RunningInvert": false,
  "RunningRandomness": 3,
  "HuntingMode": true,
  "FleeFromFights": false,
  "UserNotifications": {
    "IsAnonymous": false,
    "OnBlazeRadar": true,
    "OnDisconnect": true,
    "OnCatchAttempt": true,
    "OnWisperMessage": true,
    "OnFriendRequest": true,
    "OnAdminPin": true,
    "OnBallCount": true
  },
  "DiscordUserId": "",
  "Debug": false,
  "TickChatter": 10,
  "TickWatcher": 7
}
```

#### Field documentation

| Field | Options     | Description                |
| :-------- | :------- | :------------------------- |
| `Targets` | `[]` | List of Pokemon you want to hunt |
| `PriorityBall.Name` | `Great Ball \| Ultra Ball \| Master Ball` | Prioritizing this option while hunting |
| `MoveToUse` | `1,2,3,4` | Uses the selected move in battle |
| `RunningDirection` | `Left/Right \| Up/Down`| Direction to run |
| `RunningInvert` | `true \| false`| Changes e.g. Left/Right -> Right/Left |
| `RunningRandomness` | `1 - 5`| 10%-50% chance to skip the next step |
| `HuntingMode` | `true \| false`| Hunt Pokemon in Targets list or on Blaze Radar popup |
| `FleeFromFights` | `true \| false`| Flee from fights instead of fighting |
| `DiscordUserId` | `Your Discord UserID in Botette Discord`| Used for tagged notifications |
| `Debug` | `true \| false`| Shows some more information |
| `TickChatter` | `1 - 10`| Refresh rate of the chat image recognition |
| `TickWatcher` | `1 - 10`| Refresh rate of the popup image recognition |

## Roadmap

- Add fishing bot

- A teleport checker

## Authors & Contributers

- [@Fantaxico](https://github.com/Fantaxico)


