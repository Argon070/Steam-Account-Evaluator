import os
import requests
from datetime import datetime

# Every time on startup cd local_repos/Steam-Account-Evaluator/Steam_Account_Evaluator\ Code
# source venv/bin/activate
# export STEAM_API_KEY=your_new_key
# python SteamAPI.py
# firefox output.html

API_KEY = os.environ["STEAM_API_KEY"]
STEAM_ID = "76561198664533834"

PLAYER_SUMMARIES_URL = (
    "https://api.steampowered.com/ISteamUser/"
    "GetPlayerSummaries/v0002/"
)

OWNED_GAMES_URL = (
    "https://api.steampowered.com/IPlayerService/"
    "GetOwnedGames/v0001/"
)


def get_json(url, params):
    response = requests.get(url, params=params, timeout=20)
    return response.json()


# 1. Get Steam profile information
player_data = get_json(
    PLAYER_SUMMARIES_URL,
    {
        "key": API_KEY,
        "steamids": STEAM_ID
    }
)

players = player_data.get("response", {}).get("players", [])
player = players[0] if players else {}

steamAccountName = player.get("personaname", "Unknown")
avatarURL = player.get("avatarfull", "")
createdTimestamp = player.get("timecreated")

timeCreated = (
    datetime.fromtimestamp(createdTimestamp).strftime("%d.%m.%Y")
    if createdTimestamp
    else "Unknown"
)

# 2. Get owned games
game_data = get_json(
    OWNED_GAMES_URL,
    {
        "key": API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True,
        "include_played_free_games": True
    }
)

games = game_data.get("response", {}).get("games", [])

# 3. Calculate total playtime
ownedGames = len(games)

totalPlaytime = sum(
    game.get("playtime_forever", 0)
    for game in games
)

totalHours = round(totalPlaytime / 60, 2)


# NEW: rank A-F
def get_rank(hours):
    for limit, rank in [(5000, "A"), (2000, "B"), (1000, "C"), (500, "D"), (100, "E")]:
        if hours >= limit:
            return rank
    return "F"


playerRank = get_rank(totalHours)

# 4. Get the five most-played games
top5Games = sorted(
    games,
    key=lambda game: game.get("playtime_forever", 0),
    reverse=True
)[:5]

# 5. Store each game separately
top1Game = top5Games[0] if len(top5Games) > 0 else None
top2Game = top5Games[1] if len(top5Games) > 1 else None
top3Game = top5Games[2] if len(top5Games) > 2 else None
top4Game = top5Games[3] if len(top5Games) > 3 else None
top5Game = top5Games[4] if len(top5Games) > 4 else None

# 6. Pass data to index.html
from jinja2 import Template

with open("index.html", "r", encoding="utf-8") as file:
    html = file.read()

html = Template(html).render(
    steamAccountName=steamAccountName,
    avatarURL=avatarURL,
    timeCreated=timeCreated,
    ownedGames=ownedGames,
    totalHours=totalHours,
    playerRank=playerRank,
    top1Game=top1Game,
    top2Game=top2Game,
    top3Game=top3Game,
    top4Game=top4Game,
    top5Game=top5Game
)

with open("output.html", "w", encoding="utf-8") as file:
    file.write(html)

print("Done: open output.html in your browser")
