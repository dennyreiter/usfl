#!/usr/bin/python3

import sys
import json
import re

from usfl_team_yaml import *


def slugify(text: str) -> str:
    """Slugify a given text."""
    RE_SLUGIFY = re.compile(r'[^a-z0-9_]+')
    text = text.lower()
    text = text.replace(" ", "_")
    text = RE_SLUGIFY.sub("", text)
    return text

def sed_replace(dict,text):
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

if len(sys.argv) != 2:
    print("I need to have a team name")
    exit(2)
else:
    req = sys.argv[1]

with open("usfl_divisions.json", "r") as read_file:
    divisions = json.load(read_file)

with open("usfl_teams.json", "r") as read_file:
    teams = json.load(read_file)

result = list(filter(lambda team: req.lower() in team['name'].lower(), teams))
result += list(filter(lambda team: req.lower() in team['region'].lower(), teams))
result += list(filter(lambda team: req.lower() in team['abbrev'].lower(), teams))

if len(result) > 1:
    print("I found multiple matches. Please be more specific.")
    for team in result:
        print(f"{team['region']} {team['name']} ({team['abbrev']})")
    exit(2)

team = result[0]
friendlyname = team['region']+" "+team['name']
teamname = slugify(friendlyname)

sed_dict = {
        "__TEAM_ID__" : str(team['tid']),
        "__TEAM_NAME__" : teamname,
        "__FRIENDLY_NAME__" : friendlyname,
        "__TEAM_ABBREV__" : team['abbrev'],
        "__TEAM_PICTURE__" : team['imgURLSmall'],
        "__TEAM_LOGO__" : team['imgURL'],
        "__TEAM_CONFERENCE__": divisions[team['did']]['name'],
}

yaml_out = sed_replace(sed_dict,sensor_yaml)
print(yaml_out)

filename = teamname + ".yaml"
file1 = open(filename, "w")
file1.write(yaml_out)
file1.close
