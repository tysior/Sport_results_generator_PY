# Copyright [2017] [Patryk Matyjasek]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import random
import time

from src.common.sports_generator_commons import Player, Team, Generator
from src.sports_kinds.volleyball.db import insert_match_info


class VolleyballPlayer(Player):
    # skills
    service = 0.0
    attack = 0.0
    block = 0.0
    defence = 0.0
    # skills progress
    service_progress = 0
    attack_progress = 0
    block_progress = 0
    defence_progress = 0
    # global statistics
    matches = 0
    points = 0
    blocks = 0
    attacks = 0
    succ_att = 0
    serves = 0
    aces = 0
    # match statistics
    points_in_match = 0
    blocks_in_match = 0
    attacks_in_match = 0
    succ_att_in_match = 0
    serves_in_match = 0
    aces_in_match = 0
    # form
    form = 0
    injury = False


class VolleyballTeam(Team):
    name = ""
    sets = 0
    score = 0
    scores = []
    defence = 0
    players = []
    players_in_match = []


class VolleyballGenerator(Generator):
    def get_team_info(self, team_name, names):
        pass

    def get_player_info(self, player_json):
        pass

    def update_player_info(self, player):
        player.matches += 1
        player.points += player.points_in_match
        player.blocks += player.blocks_in_match
        player.attacks += player.attacks_in_match
        player.succ_att += player.succ_att_in_match
        player.serves += player.serves_in_match
        player.aces += player.aces_in_match
        player.points_in_match = 0
        player.blocks_in_match = 0
        player.attacks_in_match = 0
        player.succ_att_in_match = 0
        player.serves_in_match = 0
        player.aces_in_match = 0

    def get_block(self, team):
        a = random.randint(0, 5)
        b = random.randint(0, 5)
        c = random.randint(0, 5)
        if a != b and b != c and a != c:
            block = team.players[a].block + team.players[b].block + team.players[c].block
        elif a != b and b != c and a == c:
            block = team.players[a].block + team.players[b].block
        elif a == b and b != c and a != c:
            block = team.players[a].block + team.players[c].block
        elif a == b and b != c and a != c:
            block = team.players[b].block + team.players[c].block
        else:
            block = team.players[a].block
        block_json = {"player_a": a,
                      "player_b": b,
                      "player_c": c,
                      "block": block}
        return block_json

    def run_match(self, team1, team2):
        team1.players_in_match = random.sample(team1.players, 6)
        team2.players_in_match = random.sample(team2.players, 6)
        serve_out = 3
        teams = [team1, team2]
        team_serve = random.randint(0,1)
        if team_serve == 0:
            team_interception = 1
        else:
            team_interception = 0
        player_serv = 0
        teams[0].sets = 0
        teams[1].sets = 0
        teams[0].scores = []
        teams[1].scores = []
        teams[0].defence = 0
        teams[1].defence = 0
        match_str = "rozpoczyna sie mecz pomiedzy {} a {}\n".format(teams[0].name, teams[1].name)
        while not(teams[0].sets == 3 or teams[1].sets == 3):
            match_str += "zaczyna sie set numer {}\n".format(teams[0].sets + teams[1].sets + 1)
            teams[0].score = 0
            teams[1].score = 0
            while not(((teams[0].score >= 15) or (teams[1].score >= 15)) and (abs(teams[0].score - teams[1].score) >= 2)):
                if player_serv > 5:
                    player_serv = 0
                point = False
                match_str += "zagrywa {}\n".format(teams[team_serve].players_in_match[player_serv].name)
                defense = 0
                for player in teams[team_interception].players_in_match:
                    defense += player.defence
                serve = random.randint(0, 20) + random.randint(0, 6) * teams[team_serve].players_in_match[player_serv].service
                if serve < serve_out:
                    match_str += "{} zagrywa w aut, punkt dla {}\n".format(teams[team_serve].players_in_match[player_serv].name, teams[team_interception].name)
                    teams[team_interception].score += 1
                    teams[team_serve].players_in_match[player_serv].serves_in_match += 1
                    team_serve, team_interception = self.change_team(team_serve, team_interception)
                elif serve > 2 * defense or random.randint(0, 1000) == 1000:
                    match_str += "As serwisowy {}, punkt dla {}\n".format(teams[team_serve].players_in_match[player_serv].name, teams[team_serve].name)
                    teams[team_serve].players_in_match[player_serv].serves_in_match += 1
                    teams[team_serve].players_in_match[player_serv].aces_in_match += 1
                    teams[team_serve].players_in_match[player_serv].points_in_match += 1
                    teams[team_serve].score += 1
                else:
                    d = 0
                    teams[team_serve].players_in_match[player_serv].serves_in_match += 1
                    while not point:
                        teams[team_interception].defence += 1
                        match_str += "zepol {} przyjmuje\n".format(teams[team_interception].name)
                        att_player = random.randint(0,5)
                        block = self.get_block(teams[team_serve])
                        attack = teams[team_interception].players_in_match[att_player].attack
                        match_str += "atakuje {}\n".format(teams[team_interception].players_in_match[att_player].name)
                        att_ratio = random.randint(0,20)/10
                        block_ratio = random.randint(0,20)/10
                        if (attack * att_ratio) > (block["block"] * block_ratio):
                            match_str += "udany atak {}, punkt dla {}\n".format(
                                teams[team_interception].players_in_match[att_player].name,
                                teams[team_interception].name)
                            teams[team_interception].players_in_match[att_player].attacks_in_match += 1
                            teams[team_interception].players_in_match[att_player].succ_att_in_match += 1
                            teams[team_interception].players_in_match[att_player].points_in_match += 1
                            teams[team_interception].score += 1
                            team_serve, team_interception = self.change_team(team_serve, team_interception)
                            point = True
                            if d % 2 == 0:
                                player_serv += 1
                        elif (block["block"] * block_ratio) > (2 * att_ratio * attack):
                            match_str += "{} zostaje zablokowany przez {}, punkt dla {}\n".format(
                                teams[team_interception].players_in_match[att_player].name,
                                teams[team_serve].players_in_match[block["player_a"]].name,
                                teams[team_serve].name)
                            teams[team_interception].players_in_match[att_player].attacks_in_match += 1
                            teams[team_serve].players_in_match[block["player_a"]].blocks_in_match += 1
                            teams[team_serve].players_in_match[block["player_a"]].points_in_match += 1
                            teams[team_serve].score += 1
                            point = True
                            if d % 2 == 1:
                                player_serv += 1
                        else:
                            match_str += "atak {} zatrzymany, kontra\n".format(teams[team_interception].players_in_match[att_player].name)
                            team_serve, team_interception = self.change_team(team_serve, team_interception)
                            d += 1
            if teams[0].score > teams[1].score:
                teams[0].sets += 1
            else:
                teams[1].sets += 1
            teams[0].scores.append(teams[0].score)
            teams[1].scores.append(teams[1].score)
        # insert_match_info(teams[0], teams[1], match_str)
        self.post_match(teams[0], teams[1])
        print(teams[0].name, " - ", teams[1].name, teams[0].sets, teams[1].sets, teams[0].scores, teams[1].scores)
        self.print_post_match_info(teams[0])
        self.print_post_match_info(teams[1])

    def change_team(self, team_serve, team_interception):
        if team_serve == 0:
            team_serve = 1
            team_interception = 0
        elif team_serve == 1:
            team_serve = 0
            team_interception = 1
        return team_serve, team_interception

    def set_progress(self, player, defence, win=False):
        if win:
            player.service_progress += 10
            player.attack_progress += 10
            player.block_progress += 5
            player.defence_progress += 10
        player.service_progress += player.serves_in_match
        player.service_progress += 2 * player.aces_in_match
        player.attack_progress += player.attacks_in_match
        player.attack_progress += 2 * player.succ_att_in_match
        player.block_progress += player.blocks_in_match
        player.defence_progress += defence

    def update_attributes(self, player, win=False):
        if win:
            player.service += 0.1
            player.attack += 0.1
            player.block += 0.1
            player.defence += 0.1
        else:
            player.service += 0.05
            player.attack += 0.05
            player.block += 0.05
            player.defence += 0.05
        player.service += random.randint(-1, 1)/10
        player.attack += random.randint(-1, 1)/10
        player.block += random.randint(-1, 1)/10
        player.defence += random.randint(-1, 1)/10
        if player.service_progress >= 100:
            player.service += 0.1
            player.service_progress -= 100
        if player.attack_progress >= 100:
            player.attack += 0.1
            player.attack_progress -= 100
        if player.block_progress >= 50:
            player.block += 0.1
            player.block_progress -= 50
        if player.defence_progress >= 400:
            player.defence += 0.1
            player.defence_progress -= 400

    def post_match(self, team1, team2):
        if team1.score > team2.score:
            for player in team1.players_in_match:
                self.set_progress(player, team1.defence, True)
                self.update_attributes(player, True)
                self.update_player_info(player)
            for player in team2.players_in_match:
                self.set_progress(player, team1.defence, False)
                self.update_attributes(player, False)
                self.update_player_info(player)
        else:
            for player in team2.players_in_match:
                self.set_progress(player, team1.defence, True)
                self.update_attributes(player, True)
                self.update_player_info(player)
            for player in team1.players_in_match:
                self.set_progress(player, team1.defence, False)
                self.update_attributes(player, False)
                self.update_player_info(player)

    def print_post_match_info(self, team):
        print(team.name)
        print(team.sets)
        print(team.scores)
        for player in team.players:
            print(player.name, player.matches, player.points, player.blocks, player.attacks, player.succ_att,
                  player.serves,
                  player.aces, player.attack, player.service, player.defence, player.block, player.service_progress,
                  player.attack_progress, player.block_progress, player.defence_progress)
