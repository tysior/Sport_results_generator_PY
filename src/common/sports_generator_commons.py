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


class Player:
    # Player Name
    name = ""
    # Player date of birth
    DoB = ""
    # Player nationality
    nationality = ""


class Team:
    # Team name
    name = ""
    # Team players
    players = []
    # Score in match
    team_score = 0

    def __init__(self):
        self.players = []


class Generator:
    def get_team_info(self, team_name):
        pass

    def get_player_info(self, player_json):
        pass

    def update_player_info(self, player):
        pass

    def run_match(self, team1, team2):
        pass
