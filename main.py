import json

import customtkinter as ctk

class Player:
    def __init__(self, name, team):
        self.name = name.upper()
        self.team = team.upper()
        self.games = []

    def add_game(self, stats):
        self.games.append(stats)

    def get_totals(self):
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
            with open("stats.json", "r") as f:
                data = json.load(f)

                self.teams = data["teams"]
                self.games = data["games"]

                for name, pdata in data["players"].items():
                    p = Player(name, pdata["team"])
                    p.games = pdata["games"]
                    self.players[name] = p

        except:
            pass

    def save(self):
        data = {
            "teams": self.teams,
            "players": {},
            "games": self.games
        }

        for name, p in self.players.items():
            data["players"][name] = {
                "team": p.team,
                "games": p.games
            }

        with open("stats.json", "w") as f:
            json.dump(data, f, indent=4)