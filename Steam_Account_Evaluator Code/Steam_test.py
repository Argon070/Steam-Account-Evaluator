import requests
from datetime import datetime
API_KEY = "24E7BD7E4595E0A0E554C5B4E3CE72F3"
STEAM_ID = "76561198664533834"

PLAYER_SUMMARIES_URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
OWNED_GAMES_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
totalPlaytime = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"

player_params = {
    "key": API_KEY,
    "steamids": STEAM_ID
}

game_params = {
    "key": API_KEY,
    "steamid": STEAM_ID
}

# Player Summaries
response = requests.get(PLAYER_SUMMARIES_URL, params=player_params)
data = response.json()

steamAccountName = data["response"]["players"][0]["personaname"]
timeCreated = data["response"]["players"][0]["timecreated"]
timeCreated = datetime.fromtimestamp(timeCreated)

#playtime
response2 = requests.get(totalPlaytime, params=game_params)
data = response2.json()

totalPlaytime = data["response"]["playtime_forever"]

# Owned Games
response = requests.get(OWNED_GAMES_URL, params=game_params)
data = response.json()

ownedGames = data["response"]["game_count"]

print(steamAccountName, ownedGames, timeCreated, totalPlaytime)