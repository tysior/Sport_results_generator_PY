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


class FootballTeam(Team):
    off_potential = 0.0
    def_potential = 0.0
    goal_keeper = 0.0


class FootballGenerator(Generator):
    def get_team_info(self, team_name):
        team = FootballTeam()
        team.name = team_name['team']['tname']
        team.goal_keeper = 0.0
        for key in team_name['team']['players']:
            player = self.get_player_info(team_name['team']['players'][key])
            team.players.append(player)
            if player.position == 'goal_keeper':
                team.goal_keeper = player.goal_keeping
            team.off_potential += player.off_skill
            team.def_potential += player.def_skill
        return team

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
        player.nationality = 'Polish'
        return player

    def update_player_info(self, player):
        pl_json = {}
        return pl_json

    def run_match(self, team1, team2):
        teams = [team1, team2]
        i = 0
        while i < 45:
            attacking_team = random.randint(0, 1)
            defensive_team = 1 if attacking_team == 0 else 0
            attack = teams[attacking_team].off_potential + random.randint(0, 10)
            defense = teams[defensive_team].def_potential + random.randint(0, 10)
            if attack > defense:
                gk = teams[defensive_team].goal_keeper * random.randint(0, 10)
                if attack > gk:
                    teams[attacking_team].team_score += 1
                    player_idx = random.randint(0, 4)
                    teams[attacking_team].players[player_idx].goals_in_match += 1
                i += 1
            else:
                i += 1

        print('team: %s strzelil %d bramek' % (teams[0].name, teams[0].team_score))
        print('team: %s strzelil %d bramek' % (teams[1].name, teams[1].team_score))
