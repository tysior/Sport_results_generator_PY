# Copyright [2015] [Patryk Matyjasek]
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

from src.common.sports_generator_commons import Player, Team, Generator


class FootballPlayer(Player):
    off_skill = 0.0
    def_skill = 0.0
    goal_keeping = 0.0
    position = ''
    matches = 0
    goals = 0
    goals_in_match = 0

    def update_player_info(self, player):
        pl_json = {}
        return pl_json


class FootballTeam(Team):
    off_potential = 0.0
    def_potential = 0.0
    goal_keeper = 0.0
    saves = 0


class FootballGenerator(Generator):
    def get_team_info(self, team_name, names):
        team = FootballTeam()
        team.name = team_name['team']['tname']
        team.goal_keeper = 0.0
        for key in team_name['team']['players']:
            player = self.get_player_info(team_name['team']['players'][key])
            if player.name in names:
                team.players.append(player)
                if player.position == 'goal_keeper':
                    team.goal_keeper = player.goal_keeping
                team.off_potential += player.off_skill
                team.def_potential += player.def_skill
        return team

    # def get_eleven(self, team, names):
    #     eleven = []
    #     for idx, player in enumerate(team.players):
    #         if player.name in names:
    #             eleven.append(player)
    #     team.players = eleven
    #     return team

    def get_player_info(self, player_json):
        player = FootballPlayer()
        player.name = player_json['name']
        player.DoB = player_json['DoB']
        player.def_skill = player_json['def_skill']
        player.off_skill = player_json['off_skill']
        player.goal_keeping = player_json['goal_keeping']
        player.position = player_json['position']
        player.matches = player_json['matches']
        player.goals = player_json['goals']
        player.goals_in_match = 0
        player.nationality = 'Polish' #player_json['nationality']
        return player

    def run_half_match(self, start, end, teams):
        i = start
        txt = ''
        while i < end:
            attacking_team = random.randint(0, 1)
            defensive_team = 1 if attacking_team == 0 else 0
            attack = (teams[attacking_team].off_potential + random.randint(0, 10))/random.randint(1, 10)
            defense = (teams[defensive_team].def_potential + random.randint(0, 10))/random.randint(1, 5)
            if attack > defense:
                gk = teams[defensive_team].goal_keeper * random.randint(0, 10)
                if attack > gk:
                    teams[attacking_team].team_score += 1
                    # player_idx = random.randint(0, 10)
                    scorrers = []
                    for player in teams[attacking_team].players:
                        if player.position == 'goal_keeper':
                            a = random.randint(0, 100)
                            if a > 90:
                                scorrers.append(player.name)
                        elif player.position == 'defender':
                            scorrers.append(player.name)
                        elif player.position == 'midfielder':
                            scorrers.append(player.name)
                            scorrers.append(player.name)
                        elif player.position == 'attacker':
                            scorrers.append(player.name)
                            scorrers.append(player.name)
                            scorrers.append(player.name)
                            scorrers.append(player.name)
                            if player.off_skill > 4:
                                scorrers.append(player.name)
                                scorrers.append(player.name)
                                scorrers.append(player.name)
                                scorrers.append(player.name)
                                scorrers.append(player.name)
                                scorrers.append(player.name)
                                scorrers.append(player.name)
                                scorrers.append(player.name)
                    scorer = random.choice(scorrers)
                    txt += 'minuta: ' + str(i + 1) + ': ' + scorer + ' ' + teams[attacking_team].name + '\n'
                    # print(scorer)
                    for player in teams[attacking_team].players:
                        if player.name == scorer:
                            player.goals_in_match += 1
                else:
                    teams[defensive_team].saves += 1
                i += 1 #TODO: change it to random value?
                # i += random.randint(0, 45)
            else:

                i += 1 #TODO: change it to random value?
                # i += random.randint(0, 45)
        return txt
        # return teams

    def update_win_skills(self, team):
        updated = {}
        updated['team'] = {}
        updated['team']['tname'] = team.name
        updated['team']['players'] = {}
        for idx, player in enumerate(team.players):
            updated['team']['players'][str(idx)] = {}
            updated['team']['players'][str(idx)]["name"] = player.name
            updated['team']['players'][str(idx)]["DoB"] = player.DoB
            updated['team']['players'][str(idx)]["off_skill"] = player.off_skill + 0.1
            updated['team']['players'][str(idx)]["def_skill"] = player.def_skill + 0.1
            updated['team']['players'][str(idx)]["goal_keeping"] = player.goal_keeping
            updated['team']['players'][str(idx)]["position"] = player.position
            updated['team']['players'][str(idx)]["matches"] = player.matches + 1
            updated['team']['players'][str(idx)]["goals"] = player.goals + player.goals_in_match
            if player.position == 'goal_keeper':
                updated['team']['players'][str(idx)]["goal_keeping"] = player.goal_keeping + 0.1
        filename = team.name
        f = open(filename, 'w')
        f.write(str(updated))

    def update_lose_skills(self, team):
        updated = {}
        updated['team'] = {}
        updated['team']['tname'] = team.name
        updated['team']['players'] = {}
        for idx, player in enumerate(team.players):
            updated['team']['players'][str(idx)] = {}
            updated['team']['players'][str(idx)]["name"] = player.name
            updated['team']['players'][str(idx)]["DoB"] = player.DoB
            updated['team']['players'][str(idx)]["off_skill"] = player.off_skill + 0.05
            updated['team']['players'][str(idx)]["def_skill"] = player.def_skill + 0.05
            updated['team']['players'][str(idx)]["goal_keeping"] = player.goal_keeping
            updated['team']['players'][str(idx)]["position"] = player.position
            updated['team']['players'][str(idx)]["matches"] = player.matches + 1
            updated['team']['players'][str(idx)]["goals"] = player.goals + player.goals_in_match
            if player.position == 'goal_keeper':
                updated['team']['players'][str(idx)]["goal_keeping"] = player.goal_keeping + 0.05
        filename = team.name
        f = open(filename, 'w')
        f.write(str(updated))

    def update_skills(self, team1, team2):
        if team1.team_score > team2.team_score:
            self.update_win_skills(team1)
            self.update_lose_skills(team2)
        elif team1.team_score < team2.team_score:
            self.update_win_skills(team2)
            self.update_lose_skills(team1)
        else:
            self.update_win_skills(team1)
            self.update_win_skills(team2)

    def run_match(self, team1, team2):
        teams = [team1, team2]
        tx = ''
        tx += self.run_half_match(0, 45, teams)
        # print('team: %s strzelil %d bramek' % (teams[0].name, teams[0].team_score))
        # print('team: %s strzelil %d bramek' % (teams[1].name, teams[1].team_score))
        tx += self.run_half_match(46, 90, teams)
        # print('team: %s strzelil %d bramek' % (teams[0].name, teams[0].team_score))
        # print('team: %s strzelil %d bramek' % (teams[1].name, teams[1].team_score))
        filename = teams[0].name + '_vs_' + teams[1].name
        f = open(filename, 'w')
        f.write(teams[0].name + ' ' + str(teams[0].team_score) + ' - ' + str(teams[1].team_score) + ' ' + teams[1].name
                + '\n')
        for team in teams:
            for player in team.players:
                wr = player.position + ': ' + player.name + ': ' + str(player.goals_in_match) + '\n'
                f.write(wr)
            f.write('===============\n')
        f.write(tx)
        f.write('obrony: ' + teams[0].name + ' ' + str(teams[0].saves) + ' - ' + str(teams[1].saves) + ' '
                + teams[1].name + '\n')
        f.write(teams[0].name + ',' + str(teams[0].team_score) + ',' + teams[1].name + ',' + str(teams[1].team_score))
        f.close()
