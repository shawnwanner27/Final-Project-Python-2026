import json
import customtkinter as ctk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")



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
            "pitchingHits": 0
        }

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




class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.league = League()

        self.title("Daniel's Backyard Wiffleball Database")
        self.geometry("1200x800")

        title = ctk.CTkLabel(
            self,
            text="Daniel's Backyard Wiffleball Database",
            font=("Arial", 28, "bold"))
        title.pack(pady=20)

        buttonFrame = ctk.CTkFrame(self)
        buttonFrame.pack(pady=10)

        ctk.CTkButton(
            buttonFrame,
            text="Create Team",
            command=self.createTeamWindow,
            width=180
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(
            buttonFrame,
            text="Create Player",
            command=self.createPlayerWindow,
            width=180
        ).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(
            buttonFrame,
            text="Add Game",
            command=self.addWindow,
            width=180
        ).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkButton(
            buttonFrame,
            text="Edit Game",
            command=self.editWindow,
            width=180
        ).grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkButton(
            buttonFrame,
            text="Search Stats",
            command=self.searchStatsWindow,
            width=180
        ).grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(
            buttonFrame,
            text="Show Rosters",
            command=self.showRosterWindow,
            width=180
        ).grid(row=1, column=2, padx=10, pady=10)

        self.output = ScrolledText(
            self,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Consolas", 12))
        self.output.pack(fill="both", expand=True, padx=20, pady=20)

        self.log("Welcome to Daniel's Backyard Wiffleball Database!")

        self.protocol("WM_DELETE_WINDOW", self.onClose)



    def log(self, text):
        self.output.insert("end", text + "\n")
        self.output.see("end")


    def createTeamWindow(self):
        window = ctk.CTkToplevel(self)
        window.title("Create Team")
        window.geometry("300x200")

        ctk.CTkLabel(window, text="Team Name").pack(pady=10)
        teamEntry = ctk.CTkEntry(window)
        teamEntry.pack(pady=10)

        def submit():
            name = teamEntry.get().upper()
            if name in self.league.teams:
                messagebox.showerror("Error", "Team already exists.")
                return

            self.league.teams[name] = []
            self.league.save()
            self.log(f"Team created: {name}")
            window.destroy()
        ctk.CTkButton(window, text="Create", command=submit).pack(pady=20)


    def createPlayerWindow(self):
        window = ctk.CTkToplevel(self)
        window.title("Create Player")
        window.geometry("400x300")

        ctk.CTkLabel(window, text="Player Name").pack(pady=5)
        nameEntry = ctk.CTkEntry(window)
        nameEntry.pack(pady=5)

        ctk.CTkLabel(window, text="Team").pack(pady=5)
        teamEntry = ctk.CTkEntry(window)
        teamEntry.pack(pady=5)

        def submit():
            name = nameEntry.get().upper()
            team = teamEntry.get().upper()
            if team not in self.league.teams:
                messagebox.showerror("Error", "Team does not exist.")
                return

            player = Player(name, team)
            self.league.players[name] = player
            self.league.teams[team].append(name)
            self.league.save()
            self.log(f"Player created: {name} ({team})")
            window.destroy()
        ctk.CTkButton(window, text="Create", command=submit).pack(pady=20)


    def addWindow(self):
        window = ctk.CTkToplevel(self)
        window.title("Add Game")
        window.geometry("600x900")
        entries = {}

        fields = [
            "Date (mm/dd/yyyy)",
            "Number (1st,2nd,3rd)",
            "Home Team Name",
            "Away Team Name",
            "Home Team Score",
            "Away Team Score"]

        for field in fields:
            ctk.CTkLabel(window, text=field).pack()
            entry = ctk.CTkEntry(window)
            entry.pack(pady=5)
            entries[field] = entry

        ctk.CTkLabel(
            window,
            text="Player Stats Format:\nName,AtBats,Hits,Walks,StrickOuts,1B,2B,3B,HR,PCount,PStrike,PBall,PHits",
            font=("Arial", 12)
        ).pack(pady=10)

        playerText = ctk.CTkTextbox(window, height=300)
        playerText.pack(fill="both", expand=True, padx=20)

        def submit():
            game = {
                "date": entries["Date (mm/dd/yyyy)"].get(),
                "number": entries["Number (1st,2nd,3rd)"].get(),
                "homeTeam": entries["Home Team Name"].get().upper(),
                "awayTeam": entries["Away Team Name"].get().upper(),
                "homeScore": int(entries["Home Team Score"].get()),
                "awayScore": int(entries["Away Team Score"].get()),
                "playerStats": []}
            lines = playerText.get("1.0", "end").strip().split("\n")

            for line in lines:
                data = line.split(",")
                if len(data) != 13:
                    continue

                name = data[0].upper()
                stats = {
                    "atBats": int(data[1]),
                    "hits": int(data[2]),
                    "walks": int(data[3]),
                    "strikeouts": int(data[4]),
                    "singles": int(data[5]),
                    "doubles": int(data[6]),
                    "triples": int(data[7]),
                    "homeRuns": int(data[8]),
                    "pitchCount": int(data[9]),
                    "pitchingStrikes": int(data[10]),
                    "pitchingBalls": int(data[11]),
                    "pitchingHits": int(data[12])}
                game["playerStats"].append({"name": name, **stats})

                if name in self.league.players:
                    playerGameStats = {
                        "date": game["date"],
                        "number": game["number"],
                        **stats}

                    self.league.players[name].addGame(playerGameStats)
            self.league.games.append(game)
            self.league.save()
            self.log(
                f"Game added: "
                f"{game['awayTeam']} vs {game['homeTeam']}")

            window.destroy()
        ctk.CTkButton(window, text="Add Game", command=submit).pack(pady=20)



    def editWindow(self):
        window = ctk.CTkToplevel(self)
        window.title("Edit Game")
        window.geometry("500x500")

        ctk.CTkLabel(window, text="Game Date (mm/dd/yyyy)").pack()
        dateEntry = ctk.CTkEntry(window)
        dateEntry.pack()

        ctk.CTkLabel(window, text="Game Number (1st,2nd,3rd)").pack()
        numberEntry = ctk.CTkEntry(window)
        numberEntry.pack()

        ctk.CTkLabel(window, text="Player Name").pack()
        playerEntry = ctk.CTkEntry(window)
        playerEntry.pack()

        ctk.CTkLabel(window, text="Stat To Edit").pack()
        statEntry = ctk.CTkEntry(window)
        statEntry.pack()

        ctk.CTkLabel(window, text="New Value").pack()
        valueEntry = ctk.CTkEntry(window)
        valueEntry.pack()

        def submit():
            targetDate = dateEntry.get()
            targetGameNumber = numberEntry.get()
            playerName = playerEntry.get().upper()
            statToEdit = statEntry.get()
            newValue = int(valueEntry.get())

            targetGame = None
            for game in self.league.games:
                if (game["date"] == targetDate and game["number"] == targetGameNumber):
                    targetGame = game
                    break

            if targetGame is None:
                messagebox.showerror("Error", "Game not found.")
                return
            playerStats = None

            for player in targetGame["playerStats"]:
                if player["name"] == playerName:
                    playerStats = player
                    break

            if playerStats is None:
                messagebox.showerror(
                    "Error",
                    "Player not found in game.")
                return

            if statToEdit not in playerStats:
                messagebox.showerror(
                    "Error",
                    "Invalid stat.")
                return
            oldValue = playerStats[statToEdit]
            playerStats[statToEdit] = newValue

            for gameStats in self.league.players[playerName].games:
                if (gameStats["date"] == targetDate and gameStats["number"] == targetGameNumber):
                    gameStats[statToEdit] = newValue
                    break

            self.league.save()
            self.log(
                f"{playerName} | {statToEdit}: "
                f"{oldValue} -> {newValue}")
            window.destroy()
        ctk.CTkButton(window, text="Edit", command=submit).pack(pady=20)


    def searchStatsWindow(self):
        window = ctk.CTkToplevel(self)
        window.title("Search Stats")
        window.geometry("400x300")

        ctk.CTkLabel(window, text="Player or Team").pack()
        typeEntry = ctk.CTkEntry(window)
        typeEntry.pack()

        ctk.CTkLabel(window, text="Name").pack()
        nameEntry = ctk.CTkEntry(window)
        nameEntry.pack()

        def submit():
            choice = typeEntry.get().lower()
            name = nameEntry.get().upper()
            self.log("")

            if choice == "player":
                if name not in self.league.players:
                    self.log("Player not found.")
                    return

                player = self.league.players[name]
                stat = player.getTotals()
                self.log(f"{name} STATS")
                self.log(f"Batting Avg: {round(battingAvg(stat), 3)}")
                self.log(f"OBP: {round(onBasePercent(stat), 3)}")
                self.log(f"Strikeout %: {round(strikeoutPercent(stat), 3)}")
                self.log(f"Walk %: {round(walkPercent(stat), 3)}")
                self.log(f"HRs: {stat['homeRuns']}")

            elif choice == "team":
                if name not in self.league.teams:
                    self.log("Team not found.")
                    return
                totals = teamTotals(self.league, name)
                wins, losses = teamRecord(self.league, name)

                self.log(f"{name} TEAM STATS")
                self.log(f"Record: {wins}-{losses}")
                self.log(
                    f"Batting Avg: "
                    f"{round(battingAvg(totals), 3)}")
                self.log(
                    f"OBP: "
                    f"{round(onBasePercent(totals), 3)}")
            window.destroy()
        ctk.CTkButton(window, text="Search", command=submit).pack(pady=20)


    def showRosterWindow(self):
        window = ctk.CTkToplevel(self)
        window.title("Show Rosters")
        window.geometry("300x300")
        ctk.CTkLabel(window, text="Team Name").pack(pady=10)
        teamEntry = ctk.CTkEntry(window)
        teamEntry.pack(pady=10)

        def submit():
            team = teamEntry.get().upper()
            if team not in self.league.teams:
                self.log("Team not found.")
                return

            self.log(f"{team} ROSTER")
            for player in self.league.teams[team]:
                self.log(player)
            self.log("")
            window.destroy()
        ctk.CTkButton(window, text="Show", command=submit).pack(pady=20)


    def onClose(self):
        self.league.save()
        self.destroy()



app = App()
app.mainloop()