from blessed import Terminal
import math
from getch import getch
import random
import urllib.request

oracle_URL = "https://www.linusakesson.net/games/autosokoban/board.php?v=1&seed=";
term = Terminal()
seed = random.randint(0,722222542);
moves = 0;
level = 1;
initialLevel = 1;
pos = {'x':0,'y':0,'n':0}
haveNew = False;
levelData = [];
oldLevelData=[];
history=[];
def cls():
	put(term.home + term.clear);
	put("""                        /                                                      \\
  __ _    _  _          |                                                      |
 (_ / \|// \|_) /\ |\ | |                                                      |
 __)\_/|\\\_/|_)/--\| \| |                                                      |
       by kaylee        |                                                      |
                        |                                                      |
                        |                                                      |
 Seed:                X |                                                      |
 Level:               X |                                                      |
                        |                                                      |
 Moves:               X |                                                      |
                        |                                                      |
 Controls:              |                                                      |
 W: up      U: undo     |                                                      |
 A: left    R: restart  |                                                      |
 S: down    N: new game |                                                      |
 D: right   Q: quit     |                                                      |
 ______________________ |                                                      |
                        |                                                      |
 Special thanks to      |                                                      |
 Linus Akesson for the  |                                                      |
 level gen algorithm    |                                                      |
                        |                                                      |
                        \\                                                      /""");
	drawNumber(7, seed);
	drawNumber(8, level);
	drawNumber(10, moves);

def drawNumber(line, n):
	ndigits = len(str(n));
	put(term.move_xy(7,line) +" "*(16-ndigits)+ str(n));

def put(s):
	print(s,end='',flush=True);

def drawDialog(text):
	padding="    "+" "*len(text)+"    ";
	l1n3="  "+term.reverse+"  "+" "*len(text)+"  "+term.normal+"  ";
	#l1n3="  "+term.reverse+"+-"+"-"*len(text)+"-+"+term.normal+"  ";
	#l2="  "+term.reverse+"+ "+text+" +"+term.normal+"  ";
	l2="  "+term.reverse+"  "+text+"  "+term.normal+"  ";
	xpos = 21 + math.floor((54-len(text))/2);
	put(term.move_xy(xpos, 10) +padding);
	put(term.move_xy(xpos, 11)+l1n3);
	put(term.move_xy(xpos,12)+l2);
	put(term.move_xy(xpos,13)+l1n3);
	put(term.move_xy(xpos,14)+padding);

	put(term.move_xy(0, 25));
	
def loadLevel():
	global moves,seed,level,oldLevelData,levelData,history;
	moves=0;
	request_url = urllib.request.urlopen(oracle_URL+str(seed)+"&level="+str(level));
	# do YOU want to fuck around with an XML parser? didn't think so.
	history=[];
	levelData=list(str(request_url.read())[58:274]);
	setPos();
	drawNumber(8, level);
	drawNumber(10, moves)
	drawRange(0,0,17,11);
	oldLevelData=levelData[:];

def setPos():
	global pos;
	pos['n'] = "".join(levelData).lower().index('m');
	pos['x'] = pos['n'] % 18;
	pos['y'] = math.floor(pos['n']/18);

def drawRange(x1,y1,x2,y2):
	x1=max(x1*3,0);
	x2=min(x2*3,51);
	y1=max(y1*2,0);
	y2=min(y2*2,22);
	for y in range(y1,2+y2):	
		put(term.move_xy(25+x1,y));
		for x in range(25+x1,28+x2):
			put(charAt(x,y));

def charAt(x,y):
	x = x-25;
	y = y;
	block = levelData[math.floor(y/2)*18+math.floor(x/3)]
	if block=="w":
		return ".";
	elif block=="E":
		return term.reverse + " " + term.normal;
	elif block=="o":
		return term.bold+"+-+"[x%3]+term.normal;
	elif block=="O":
		return term.reverse+term.bold+ "+-+"[x%3] +term.normal;
	elif block=="m":
		return term.bold+ " O /|\\"[(y%2)*3+(x%3)]+term.normal;
	elif block=="M":
		return term.reverse+term.bold+ " O /|\\"[(y%2)*3+(x%3)]+term.normal;

		
	else:
		return " "

def undo():
	global pos, levelData, history,moves;
	if moves==0: return;
	moves = moves -1;
	levelData = history.pop();
	drawNumber(10, moves);	
	drawRange(pos['x']-2,pos['y']-2,pos['x']+2,pos['y']+2);
	setPos()

def reset():
	global moves, oldLevelData, levelData,history;
	levelData=oldLevelData[:];
	history=[];
	setPos();
	moves=0;
	drawNumber(10, moves);
	drawRange(0,0,17,11);

def setup():
	cls();
	drawDialog("Generating level...");
	loadLevel();	

def switch(a,b):
	global levelData;
	curCase = levelData[a].isupper();
	targetCase = levelData[b].isupper();
	tmp = levelData[b];
	if(curCase==targetCase):
		levelData[b] = levelData[a];
		levelData[a] = tmp;
	elif(curCase==0):
		levelData[b] = levelData[a].upper();
		levelData[a] = tmp.lower();
	else:
		levelData[b] = levelData[a].lower();
		levelData[a] = tmp.upper();
		

def tryMove(c):
	global moves, pos, levelData;
	oldData = levelData[:];
	x=pos['x'];
	y=pos['y'];
	n=pos['n'];
	
	if c=="w": #up
		if y==0: return;
		nextPos = n-18;
		nextCell = levelData[nextPos].lower();
		if nextCell == 'w': return;
		if nextCell == 'o':
			if nextPos<18: return;
			nextNextPos = nextPos - 18;
			nextNextCell = levelData[nextNextPos].lower();
			if nextNextCell != 'e': return;
			switch(nextPos, nextNextPos);
			drawRange(x,y-2,x,y-2);
		switch(n, nextPos);
		drawRange(x,y-1,x,y);
		setPos();
	elif c=="a":  #left
		if x==0: return;
		nextPos = n-1;
		nextCell = levelData[nextPos].lower();
		if nextCell == 'w': return;
		if nextCell == 'o':
			if (nextPos%18)<1: return;
			nextNextPos = nextPos - 1;
			nextNextCell = levelData[nextNextPos].lower();
			if nextNextCell != 'e': return;
			switch(nextPos, nextNextPos);
			drawRange(x-2,y,x-2,y);
		switch(n, nextPos);
		drawRange(x-1,y,x,y);
		setPos();
	elif c=="s": #down
		if y==11: return;
		nextPos = n+18;
		nextCell = levelData[nextPos].lower();
		if nextCell == 'w': return;
		if nextCell == 'o':
			if nextPos>(18*11): return;
			nextNextPos = nextPos + 18;
			nextNextCell = levelData[nextNextPos].lower();
			if nextNextCell != 'e': return;
			switch(nextPos, nextNextPos);
			drawRange(x,y+2,x,y+2);
		switch(n, nextPos);
		drawRange(x,y,x,y+1);
		setPos();
	elif c=="d":  #right
		if x==17: return;
		nextPos = n+1;
		nextCell = levelData[nextPos].lower();
		if nextCell == 'w': return;
		if nextCell == 'o':
			if (nextPos%18)==17: return;
			nextNextPos = nextPos + 1;
			nextNextCell = levelData[nextNextPos].lower();
			if nextNextCell != 'e': return;
			switch(nextPos, nextNextPos);
			drawRange(x+2,y,x+2,y);
		switch(n, nextPos);
		drawRange(x,y,x+1,y);
		setPos();
	else:
		return;
	history.append(oldData);
	moves+=1;
	drawNumber(10, moves);
	
def checkWin():
	global levelData;
	return ('E' not in levelData and 'M' not in levelData);	


import time;
def main():
		global level,levelData,seed;
		setup();
		while True:
			c=getch().lower();
			if c=="q":
				drawDialog("Really quit? y/N");
				yn = getch().lower();
				if yn=='y':
					drawDialog("Thank you for playing! :)");
					time.sleep(1);
					return;
				else:
					drawRange(4,4,13,8);
			elif c=="\033":
				getch();
				getch();
			elif c=="n":
				drawDialog("Really start a new game? y/N");
				yn = getch().lower();
				if yn=='y':
					global haveNew;
					haveNew = True;
					return;
				else:
					drawRange(3,4,14,8);
			elif c in "wasd":
				tryMove(c);
				w = checkWin();
				if(w):
					time.sleep(0.2);
					levelData='w'*256;
					drawRange(0,0,17,11);
					drawDialog("You win!!!");
					time.sleep(1);
					level+=1;
					loadLevel();	
			elif c=="r":
				reset();
			elif c=="u":
				undo();
		
try:
	with term.fullscreen():
		while True:
			with term.hidden_cursor():
				main();
			if(haveNew):
				haveNew=False;
				put(term.home() + term.clear());
				print("Setting up new game... ");
				seedTxt = input("Seed [random]: ");
				try:
					level = int(input("Level [1]: "));
				except:
					level = 1;
				level = max(level, 1);
				initialLevel = level;
				if len(seedTxt) == 0:
					seed = random.randint(0,722222542);
				else:
					try:
						seed = int(seedTxt);
					except:
						seed = 666
				
			else:
				break;
except KeyboardInterrupt:
	pass
finally:
	if level>initialLevel:
		print("You beat " + str(level-initialLevel) +" level"+("s" if level>initialLevel+1 else "")+"! Well done.\n")
