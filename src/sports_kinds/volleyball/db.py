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
import sqlite3
import os
import json


def insert_match_info(team1, team2, match_str, dbname):
    conn = sqlite3.connect(dbname)
    team1_player_stats = ""
    team2_player_stats = ""
    for player in team1.players_in_match:
        team1_player_stats += str((player.name, player.points_in_match, player.attacks_in_match,
                                  player.succ_att_in_match, player.serves_in_match, player.aces_in_match,
                                  player.blocks_in_match))
    for player in team2.players_in_match:
        team2_player_stats += str((player.name, player.points_in_match, player.attacks_in_match,
                                  player.succ_att_in_match, player.serves_in_match, player.aces_in_match,
                                  player.blocks_in_match))
    score = str(team1.sets) + "-" + str(team2.sets) + str(team1.scores) + str(team2.scores)
    data = (team1.name, team2.name, score, team1_player_stats, team2_player_stats, match_str)
    conn.execute('INSERT INTO `matches` VALUES (?,?,?,?,?,?)', data)
    conn.commit()
    conn.close()

def populate_db(dbname):
    conn = sqlite3.connect(dbname)
    path = 'starting_data'

    for filename in os.listdir(path):
        a = open(path + "\\" + filename, 'r')
        b = a.read()
        a.close()
        c = json.loads(b)

        dbase = "CREATE TABLE `{}` (\
            `Name`	TEXT,\
            `Nationality`	TEXT,\
            `DoB`	TEXT,\
            `Attack`	NUMERIC,\
            `Block`	NUMERIC,\
            `Defence`	NUMERIC,\
            `Serve`	NUMERIC,\
            `Matches`	INTEGER,\
            `Points`	INTEGER,\
            `Attacks`	INTEGER,\
            `SuccAttacks`	INTEGER,\
            `Blocks`	INTEGER,\
            `Serves`	INTEGER,\
            `Aces`	INTEGER,\
            `AttackProgress`	INTEGER,\
            `BlockProgress`	INTEGER,\
            `DefenceProgress`	INTEGER,\
            `ServeProgress`	INTEGER,\
            `Height`	INTEGER,\
            `Weight`	INTEGER,\
            `Clubs`	TEXT,\
            `Injury`	TEXT,\
            `Form`	NUMERIC,\
            `InjuryLeft`	INTEGER\
            );".format(c["team"]["tname"])
        conn.execute(dbase)
        conn.commit()

        for idx in c["team"]["players"]:
            player = (c["team"]["players"][idx]["name"],
                      c["team"]["players"][idx]["DoB"],
                      c["team"]["players"][idx]["nationality"],
                      c["team"]["players"][idx]["height"],
                      c["team"]["players"][idx]["weight"],
                      c["team"]["players"][idx]["service"],
                      c["team"]["players"][idx]["attack"],
                      c["team"]["players"][idx]["block"],
                      c["team"]["players"][idx]["defence"],
                      c["team"]["tname"])
            conn.execute('INSERT INTO `{}`(Name, DoB, Nationality, Height, Weight, Serve, Attack, Block, Defence, Clubs)\
             VALUES (?,?,?,?,?,?,?,?,?,?)'.format(c["team"]["tname"]), player)
            conn.commit()
        conn.close()
