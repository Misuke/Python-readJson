#! /usr/bin/python3.4


# ./refactor.py isldb.json | wc -l
# ./refactor.py isldb.json | cat -n
# ./refactor.py isldb.json result.txt | sort | uniq -c

  
import json
import sys

line = 1

def handleLand(dico):
    print(line, dico["data"]["action"] , file=out_file, end="(")
    print("people=" + str(dico["data"]["parameters"]["people"]) + ")" , file=out_file)

def handleGlimpse_Explorer(dico):
    print(line, dico["data"]["action"] , file=out_file, end="(")
    print(str(dico["data"]["parameters"]["range"]) + "," + dico["data"]["parameters"]["direction"] + ")" , file=out_file, end=" => ")

def handleGlimpse_Engine(dico):
	i = 0
	while i < len(dico["data"]["extras"]["report"]):
		j = 0
		while j < len(dico["data"]["extras"]["report"][i]):
			if (type(dico["data"]["extras"]["report"][i][j]) is list):
				print(str(dico["data"]["extras"]["report"][i][j][0]) + "(" + str(dico["data"]["extras"]["report"][i][j][1]) + ")", file=out_file, end=",")
			else:
				print(str(dico["data"]["extras"]["report"][i][j]), file=out_file, end=",")
			j = j + 1
		print(" | " ,file=out_file, end="")
		i = i + 1
	print(file=out_file)


def handleExplore_Explorer(dico):
    print(line, dico["data"]["action"] , file=out_file, end="(")

def handleExplore_Engine(dico):
	i = 0
	while i < len(dico["data"]["extras"]["resources"]):
		print(dico["data"]["extras"]["resources"][i]["resource"] + "(" + dico["data"]["extras"]["resources"][i]["amount"] + ")",file=out_file, end=",")
		i = i + 1
	print("-)" ,file=out_file)


def handleMove_to(dico):
    print(line, dico["data"]["action"] , file=out_file, end="(")
    print(dico["data"]["parameters"]["direction"] + ")" , file=out_file)

def handleExploit_Explorer(dico):
    print(line, dico["data"]["action"] , file=out_file, end="(")
    print(dico["data"]["parameters"]["resource"] + ")" , file=out_file, end=" => ")

def handleExploit_Engine(dico):
	print(dico["data"]["extras"]["amount"], file=out_file, end=",")
	print(file=out_file)

def handleScout_Explorer(dico):
    print(line, dico["data"]["action"] , file=out_file, end="(")
    print(dico["data"]["parameters"]["direction"] + ")" , file=out_file, end=" => ")

def handleScout_Engine(dico):
	i = 0
	while i < len(dico["data"]["extras"]["resources"]):
		print(dico["data"]["extras"]["resources"][i] ,file=out_file, end=",")
		i = i + 1
	print(file=out_file)



# main --------------------------
in_file = open(sys.argv[1], "r")
#out_file = sys.stdout
out_file = open(sys.argv[2], "w")

json_dict = json.load(in_file)

for info in json_dict:
	# part: EXPLORER
	if "data" in info and "action" in info["data"]: 
		#action : LAND
		if info["data"]["action"] == "land":
			handleLand(info)
			line = line + 1
		#action : GLIMPSE
		if info["data"]["action"] == "glimpse":
			handleGlimpse_Explorer(info)
			line = line + 1
		#action : EXPLORE
		if info["data"]["action"] == "explore":
			handleExplore_Explorer(info)
			line = line + 1
		#action : MOVE_TO
		if info["data"]["action"] == "move_to":
			handleMove_to(info)
			line = line + 1
		#action : EXPLOIT
		if info["data"]["action"] == "exploit":
			handleExploit_Explorer(info)
			line = line + 1
		#action : SCOUT
		if info["data"]["action"] == "scout":
			handleScout_Explorer(info)
			line = line + 1


	# part: EXPLORE_ENGINE
	if ("data" in info and "extras" in info["data"] and "resources" in info["data"]["extras"] and not("altitude" in info["data"]["extras"])):
		handleExplore_Engine(info)
	# part: SCOUT_ENGINE
	if ("data" in info and "extras" in info["data"] and "resources" in info["data"]["extras"] and "altitude" in info["data"]["extras"]):
		handleScout_Engine(info)
	# part: EXPLOIT_ENGINE
	if ("data" in info and "extras" in info["data"] and "amount" in info["data"]["extras"]):
		handleExploit_Engine(info)
	# part: GLIMPSE_ENGINE
	if ("data" in info and "extras" in info["data"] and "report" in info["data"]["extras"]):
		handleGlimpse_Engine(info)

