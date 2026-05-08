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
    print("--------------------------------------------------")


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
    print("--------------------------------------------------")


def addGame(league):
    game = {
        "date": input("Date (mm/dd/yyyy): "),
        "homeTeam": input("Home team: ").upper(),
        "awayTeam": input("Away team: ").upper(),
        "homeScore": int(input("Home score: ")),
        "awayScore": int(input("Away score: ")),
        "playerStats": []}

    numPlayers = int(input("How many player entries? "))
    print("--------------------------------------------------")
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
        print("--------------------------------------------------")

        game["playerStats"].append({"name": name, **stats})
        if name in league.players:
            league.players[name].addGame(stats)
        else:
            print("Player not found.")
            print("--------------------------------------------------")

    league.games.append(game)
    print("Game added.")
    print("--------------------------------------------------")






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


def teamTotals(league, team):
    totals = {}
    for playerName in league.teams[team]:
        player = league.players[playerName]
        playerTotals = player.getTotals()
        for x, y in playerTotals.items():
            totals[x] = totals.get(x, 0) + y
    return totals


def teamRecord(league, team):
    wins, losses = 0, 0
    for x in league.games:
        if x["homeTeam"] == team:
            wins += x["homeScore"] > x["awayScore"]
            losses += x["homeScore"] < x["awayScore"]
        elif x["awayTeam"] == team:
            wins += x["awayScore"] > x["homeScore"]
            losses += x["awayScore"] < x["homeScore"]
    return wins, losses






def searchStats(league):
    choice = input("Player or Team? ").lower()

    if choice == "player":
        name = input("Player name: ").upper()
        if name not in league.players:
            print("Player not found.")
            print("--------------------------------------------------")
            return

        player = league.players[name]
        stat = player.getTotals()
        print("Batting Average:", round(battingAvg(stat),3))
        print("On Base Percent:", round(onBasePercent(stat),3))
        print("Strikeout Percent:", round(strikeoutPercent(stat),3))
        print("Walk Percent:", round(walkPercent(stat),3))
        print("Singles:", stat["singles"])
        print("Doubles:", stat["doubles"])
        print("Triples:", stat["triples"])
        print("Home Runs:", stat["homeRuns"])
        print("Pitching Strike Percent:", round(pitchingStrikesPercent(stat),3))
        print("Pitching Walk Percent:", round(pitchingWalkPercent(stat),3))
        print("--------------------------------------------------")


    elif choice == "team":
        name = input("Team name: ").upper()
        if name not in league.teams:
            print("Team not found.")
            print("--------------------------------------------------")
            return

        totals = teamTotals(league, name)
        wins, losses = teamRecord(league, name)
        print("Record:", wins, "-", losses)
        print("Win Percent:", wins / (wins + losses) if (wins + losses) else 0)
        print("Team Batting Average:", round(battingAvg(totals),3))
        print("Team On Base Percent:", round(onBasePercent(totals),3))
        print("Team Strikeout Percent:", round(strikeoutPercent(totals),3))
        print("Team Walk Percent:", round(walkPercent(totals),3))
        print("Total Singles:", totals["singles"])
        print("Total Doubles:", totals["doubles"])
        print("Total Triples:", totals["triples"])
        print("Total Home Runs:", totals["homeRuns"])
        print("Pitching Strike Percent:", round(pitchingStrikesPercent(totals),3))
        print("Pitching Walk Percent:", round(pitchingWalkPercent(totals),3))
        print("--------------------------------------------------")


def showRosters(league):
    choice = input("Which team would you like to see? ").upper()
    if choice not in league.teams:
            print("Team not found.")
            print("--------------------------------------------------")
            return
    for x in league.teams if choice == league.teams:
        #####################################################################################################################






def main():
    league = League()

    while True:
        print("1. Create Team")
        print("2. Create Player")
        print("3. Add Game")
        print("4. Search Stats")
        print("5. Show Rosters")
        print("6. Exit")

        choice = input("Choose: ")
        print("--------------------------------------------------")

        if choice == "1":
            createTeam(league)
        elif choice == "2":
            createPlayer(league)
        elif choice == "3":
            addGame(league)
        elif choice == "4":
            searchStats(league)
        elif choice == "5":
            showRosters(league)
        elif choice == "6":
            league.save()
            print("Saved. Goodbye.")
            print("--------------------------------------------------")
            break
        else:
            print("Invalid choice.")
            print("--------------------------------------------------")

        league.save()



main()