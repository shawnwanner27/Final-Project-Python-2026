import json

import customtkinter as ctk




def write_json(data):
    with open("stats.json", "w") as file:
        json.dump(data, file, indent=4)

def read_json():
    try:
        with open("stats.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def to_dict(self):
    return self.__dict__




class PlayerGameStats:
    def __init__(self, name, team, date):
        self.name = name.upper()
        self.team = team.upper()
        self.date = date

        self.atBats = 0
        self.hits = 0
        self.walks = 0
        self.strikeouts = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.homeRuns = 0

        self.pitchCount = 0
        self.pitchingStrikeouts = 0
        self.pitchingWalks = 0
        self.pitchingHits = 0

    def to_dict(self):
        return self.__dict__


class Player:
    def __init__(self, name, team):
        self.name = name.upper()
        self.team = team.upper()
        self.games = []

    def add_game(self, game_stats):
        self.games.append(game_stats.to_dict())

    def to_dict(self):
        return {
            "name": self.name,
            "team": self.team,
            "games": self.games
        }


class Game:
    def __init__(self, date, home_team, away_team):
        self.date = date
        self.homeTeam = home_team.upper()
        self.awayTeam = away_team.upper()
        self.homeScore = 0
        self.awayScore = 0

    def to_dict(self):
        return self.__dict__


