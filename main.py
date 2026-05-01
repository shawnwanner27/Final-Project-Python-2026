import json
import customtkinter as ctk


#ALWAYS USE .UPPER

def write_json(data):
    with open("stats.json", "w") as file:
        json.dump(data, file, indent=4)

def read_json():
    try:
        with open("stats.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None





class Game():
    def __init__(self, date, homeTeam, awayTeam):
        self.date = date
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.


class PlayerStatsPerGame:
    def __init__(self,):