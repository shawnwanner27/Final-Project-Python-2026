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
    name = input("Enter Team Name: ").upper()
    if name in league.teams:
        print("Team already exists.")
        return
    league.teams[name] = []
    print("Team created.")
    print("--------------------------------------------------")


def createPlayer(league):
    name = input("Enter Player Name: ").upper()
    team = input("Enter Team: ").upper()
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
        "number": input("Game Number of That Day (1st, 2nd, 3rd): "),
        "homeTeam": input("Home Team: ").upper(),
        "awayTeam": input("Away Team: ").upper(),
        "homeScore": int(input("Home Score: ")),
        "awayScore": int(input("Away Score: ")),
        "playerStats": []}

    numPlayers = int(input("How many player entries? "))
    print("--------------------------------------------------")
    for x in range(numPlayers):
        name = input("Player Name: ").upper()
        stats = {
            "atBats": int(input("At Bats: ")),
            "hits": int(input("Hits: ")),
            "walks": int(input("Walks: ")),
            "strikeouts": int(input("Strikeouts: ")),
            "singles": int(input("Singles: ")),
            "doubles": int(input("Doubles: ")),
            "triples": int(input("Triples: ")),
            "homeRuns": int(input("Home Runs: ")),
            "pitchCount": int(input("Pitch Count: ")),
            "pitchingStrikes": int(input("Pitching Strikes: ")),
            "pitchingBalls": int(input("Pitching Balls: ")),
            "pitchingHits": int(input("Hits Allowed: "))}
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




def editGame(league):
    while True:
        targetDate = input("What day was the game you would like to edit? ")
        targetGameNumber = input("What number game was it that day? ")
        targetGame = "x"

        for game in league.games:
            if game["date"] == targetDate and game["number"] == targetGameNumber:
                targetGame = game
                break
        if targetGame is "x":
            print("Game not found.")
            print("--------------------------------------------------")
            continue

        print(f'{targetGame["awayTeam"]} vs {targetGame["homeTeam"]}')
        print(f'Score: {targetGame["awayScore"]} - {targetGame["homeScore"]}')

        print(targetGame["awayTeam"], "PLAYER STATS:")
        for player in targetGame["playerStats"]:
            if player["name"] in league.players:
                if league.players[player["name"]].team == targetGame["awayTeam"]:
                    print(player)
        print("--------------------------------------------------")

        print(targetGame["homeTeam"], "PLAYER STATS:")
        for player in targetGame["playerStats"]:
            if player["name"] in league.players:
                if league.players[player["name"]].team == targetGame["homeTeam"]:
                    print(player)
        print("--------------------------------------------------")

        correct = input("Is this the correct game? (yes/no): ").upper()
        if correct == "YES":
            break

    playerName = input("Which player's stats would you like to edit? ").upper()
    playerStats = "x"
    for player in targetGame["playerStats"]:
        if player["name"] == playerName:
            playerStats = player
            break
    if playerStats is "x":
        print("Player not found in this game.")
        print("--------------------------------------------------")
        return




########################################################################################################################




def searchStats(league):
    choice = input("Player or Team? ").lower()

    if choice == "player":
        name = input("Player Name: ").upper()
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
        name = input("Team Name: ").upper()
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
    print(f"{choice} ROSTER:")
    for playerName in league.teams[choice]:
        print(playerName)
    print("--------------------------------------------------")




def main():
    league = League()

    while True:
        print("1. Create Team")
        print("2. Create Player")
        print("3. Add Game")
        print("4. Edit Game")
        print("5. Search Stats")
        print("6. Show Rosters")
        print("7. Exit")

        choice = input("Choose: ")
        print("--------------------------------------------------")

        if choice == "1":
            createTeam(league)
        elif choice == "2":
            createPlayer(league)
        elif choice == "3":
            addGame(league)
        elif choice == "4":
            editGame(league)
        elif choice == "5":
            searchStats(league)
        elif choice == "6":
            showRosters(league)
        elif choice == "7":
            league.save()
            print("Saved. Goodbye.")
            print("--------------------------------------------------")
            break
        else:
            print("Invalid choice.")
            print("--------------------------------------------------")

        league.save()


print("--------------------------------------------------")
main()