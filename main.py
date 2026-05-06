import json
#import customtkinter as ctk


class Player:
    def __init__(self, name, team):
        self.name = name.upper()
        self.team = team.upper()
        self.games = []

    def addGame(self, stats):
        self.games.append(stats)

    def getTotals(self):
        totals = {
            "atBats": 0,
            "hits": 0,
            "walks": 0,
            "strikeouts": 0,
            "singles": 0,
            "doubles": 0,
            "triples": 0,
            "homeRuns": 0,
            "pitchCount": 0,
            "pitchingStrikes": 0,
            "pitchingBalls": 0,
            "pitchingHits": 0}

        for game in self.games:
            for x in totals:
                totals[x] += game.get(x, 0)
        return totals


class League:
    def __init__(self):
        self.teams = {}
        self.players = {}
        self.games = []
        self.load()

    def load(self):
        try:
            with open("stats.json", "r") as file:
                data = json.load(file)
                self.teams = data["teams"]
                self.games = data["games"]

                for name, x in data["players"].items():
                    y = Player(name, x["team"])
                    y.games = x["games"]
                    self.players[name] = y
        except:
            pass


    def save(self):
        data = {
            "teams": self.teams,
            "players": {},
            "games": self.games}

        for name, x in self.players.items():
            data["players"][name] = {
                "team": x.team,
                "games": x.games}

        with open("stats.json", "w") as file:
            json.dump(data, file, indent=4)






def createTeam(league):
    name = input("Enter team name: ").upper()

    if name in league.teams:
        print("Team already exists.")
        return

    league.teams[name] = []
    print("Team created.")


def createPlayer(league):
    name = input("Enter player name: ").upper()
    team = input("Enter team: ").upper()

    if team not in league.teams:
        print("Team does not exist.")
        return

    player = Player(name, team)
    league.players[name] = player
    league.teams[team].append(name)
    print("Player created.")


def addGame(league):
    game = {
        "date": input("Date (mm/dd/yyyy): "),
        "homeTeam": input("Home team: ").upper(),
        "awayTeam": input("Away team: ").upper(),
        "homeScore": int(input("Home score: ")),
        "awayScore": int(input("Away score: ")),
        "playerStats": []}

    numPlayers = int(input("How many player entries? "))
    for x in range(numPlayers):
        name = input("Player name: ").upper()

        stats = {
            "atBats": int(input("At bats: ")),
            "hits": int(input("Hits: ")),
            "walks": int(input("Walks: ")),
            "strikeouts": int(input("Strikeouts: ")),
            "singles": int(input("Singles: ")),
            "doubles": int(input("Doubles: ")),
            "triples": int(input("Triples: ")),
            "homeRuns": int(input("Home runs: ")),

            "pitchCount": int(input("Pitch count: ")),
            "pitchingStrikes": int(input("Pitching strikes: ")),
            "pitchingBalls": int(input("Pitching balls: ")),
            "pitchingHits": int(input("Hits allowed: "))}

        game["playerStats"].append({"name": name, **stats})
        if name in league.players:
            league.players[name].addGame(stats)
        else:
            print(f"Warning: {name} not found.")

    league.games.append(game)
    print("Game added.")


def battingAvg(x):
    return x["hits"] / x["atBats"] if x["atBats"] else 0

def onBasePercent(x):
    denominator = x["atBats"] + x["walks"]
    return (x["hits"] + x["walks"]) / denominator if denominator else 0

def strikeoutPercent(x):
    return x["strikeouts"] / x["atBats"] if x["atBats"] else 0

def walkPercent(x):
    return x["walks"] / x["atBats"] if x["atBats"] else 0

def pitchingStrikesPercent(x):
    return x["pitchingStrikes"] / x["pitchCount"] if x["pitchCount"] else 0

def pitchingWalkPercent(x):
    return x["pitchingBalls"] / x["pitchCount"] if x["pitchCount"] else 0




#need to add the team stats next