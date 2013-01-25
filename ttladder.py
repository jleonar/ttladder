from trueskill import *
import pickle
import pprint
import os
import operator
from easygui import *
import sys
import uuid


def loadMatches():
    if os.path.exists("matches.pkl"):
        pkl_file = open('matches.pkl', 'rb')
        mydict2 = pickle.load(pkl_file)
        pkl_file.close()
        return mydict2
    else:
        return dict()
        
def writeMatches():
    output = open('matches.pkl', 'wb')
    pickle.dump(matches, output)
    output.close()
    
def reloadMatches():
    writeMatches()
    matches=loadMatches()
    for i in matches.values():
        print i 
        

def loadPickle():
    if os.path.exists("myfile.pkl"):
        pkl_file = open('myfile.pkl', 'rb')
        mydict2 = pickle.load(pkl_file)
        pkl_file.close()
        return mydict2
    else:
        return dict()

def writePickle():
    output = open('myfile.pkl', 'wb')
    pickle.dump(players, output)
    output.close()

def reloadPickle():
    writePickle()
    players = loadPickle()


def validatePlayers(w,l):
    if w and l not in players:
        if w == None:
            return None, None
        msgbox("Invalid Players")
        w,l = enterGameUI()
        
    return w,l       

def addMatch(w,l):
    id = uuid.uuid4()
    matches[id]=[w,l]
    reloadMatches()
    
def addPlayer(player):
    email = player.email
    players[email]=player
    reloadPickle()
    
def listPlayers():
    for key, value in players.iteritems() :        
        print key

def getRankings():
    temp="Rankings:\n\n\n\n\n"
    for player in (reversed(sorted(players.values(), key=operator.attrgetter('trueskill.mu')))):
        temp = str(temp)+str("Score: " + str(int(round(player.trueskill.mu))) + "     Name: "+ player.name+"\n")
    return temp

    
def match(w, l):
    winner = players[w].trueskill
    loser = players[l].trueskill
    w1, l1 = rate_1vs1(winner, loser)
    players[w].trueskill=w1
    players[l].trueskill=l1
    return w,l,players[w].trueskill,players[l].trueskill

def enterGameUI(u):
    if u=="game":
        pl = []
        for player in players.values():
            pl.append(player.email)
        choices=multchoicebox("Enter Match","Pick two players",pl)
        if choices!=None and len(choices)==2:
            choice=choicebox("Match","Select the winner",choices)
            if (choice==choices[0]):
                return [choice,choices[1]]
            else:
                return [choice,choices[0]]
        elif choices!=None:
            msgbox("Only pick two players")
            choices = enterGameUI("game")
        else:
            return None
    elif u=="matchup":
        pl = []
        for player in players.values():
            pl.append(player.email)
        choices=multchoicebox("Enter Matchup","Pick two players",pl)
        if choices!=None and len(choices)==2:
            val = quality(choices[0],choices[1])
            if val > .6:
                msgbox(choices[0] +" versus "+choices[1]+" is a good matchup")
            else:
                msgbox("This match may be unfair!")
        elif choices!=None:
            msgbox("Only pick two players")
            choices = enterGameUI("matchup")
        else:
            return None


def displaySkillUI():
    msg ="Select the player"
    title = "Players"
    choices = []
    for player in (players.values()):
        choices.append(player.email)
    choice = choicebox(msg, title, choices)
    if choice !=None:
        msgbox(players[choice].trueskill)
    
    
    
     
def addPlayerUI():
    msg         = "Add New Player"
    title       = "Enter Player Info"
    fieldNames  = ["Name","Username"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)
    while 1:  # do forever, until we find acceptable values and break out
        if fieldValues == None: 
            break
        errmsg = ""

            # look for errors in the returned values
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        if errmsg == "": 
            break # no problems found
        else:
            # show the box again, with the errmsg as the message    
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    if fieldValues==None:
        return None,None
    return fieldValues[0].lower(), fieldValues[1].lower()
    
    
def quality(w, l):
    winner = players[w].trueskill
    loser = players[l].trueskill
    return quality_1vs1(winner, loser)
    
class ppplayer:
    def __init__(self, name, email, ts):
        self.name = name
        self.email = email
        self.trueskill = ts
        self.mu=ts.mu
    def getName():
        return name
    def getEmail():
        return email
    def getTrueSkill():
        return trueskill
    def setTrueSkill(ts):
        self.trueskill=ts
        self.mu=ts.mu
    
        

players= loadPickle()
matches= loadMatches()
choice=None
while choice!="Quit":
    msg =getRankings()
    title = "Table Tennis Ladder"
    choices = ["Add new player", "Enter a completed game", "Display player's trueskill","Matchup quality", "Quit"]
    choice = choicebox(msg, title, choices)
    if choice == "Add new player":
        nm,usr = addPlayerUI()
        flag=False
        if(usr!=None and nm!=None):
            while flag==False and usr in players:
                msgbox("User Already Exists")
                nm,usr = addPlayerUI()
                if usr==None:
                    flag=True
        if nm!=None:
            player = ppplayer(nm,usr,Rating())
            addPlayer(player)
        reloadPickle()
    if choice == "Display player's trueskill":
        displaySkillUI()
        
    if choice == "Enter a completed game":
        returnval = enterGameUI("game")
        winner=None
        loser=None
        if returnval!=None:
            winner=returnval[0]
            loser=returnval[1]
        if winner!=None and loser != None:
            winner,loser,players[winner].trueskill,players[loser].trueskill = match(winner,loser)
            addMatch(winner,loser)
        reloadPickle()
        
    if choice == "Matchup quality":
        enterGameUI("matchup")
            
        

reloadPickle()
