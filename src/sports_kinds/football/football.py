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

from src.common.sports_generator_commons import Player, Team, Generator


class FootballPlayer(Player):
    off_skill = 0.0
    def_skill = 0.0
    matches = 0
    goals = 0
    goals_in_match = 0


class FootballTeam(Team):
    off_potential = 0.0
    def_potential = 0.0


class FootballGenerator(Generator):
    def get_team_info(self, team_name):
        team = FootballTeam()
        team.name = team_name['team']['tname']
        for key in team_name['team']['players']:
            player = self.get_player_info(team_name['team']['players'][key])
            team.players.append(player)
            team.off_potential += player.off_skill
            team.def_potential += player.def_skill
        return team

    def get_player_info(self, player_json):
        player = FootballPlayer()
        player.name = player_json['name']
        player.DoB = player_json['DoB']
        player.def_skill = player_json['def_skill']
        player.off_skill = player_json['off_skill']
        player.matches = player_json['matches']
        player.goals = player_json['goals']
        player.goals_in_match = 0
        player.nationality = 'Polish'
        return player

    def update_player_info(self, player):
        pl_json = {}
        return pl_json
