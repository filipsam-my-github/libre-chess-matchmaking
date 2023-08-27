from copy import deepcopy
import numpy as np
import pygame,sys, math,random
from flask import Flask, jsonify

import colorama
colorama.init()



id_to_get=0
with open("zawodnicy.txt", 'r', encoding='utf-8') as file:
    players = []
    
    for i, player in enumerate(file):
        for_read={"line":[],"string":"","local_line":list(player)}
        for j in player.strip():
            if " "==j  and for_read["string"] != "":
                for_read["line"].append(deepcopy(for_read["string"]))
                for_read["string"]=""
                continue
                
            for_read["string"]+=j
            
            if j==player.strip()[-1] and for_read["string"] != "":
                for_read["line"].append(deepcopy(for_read["string"]))
                for_read["string"]=""
                
        players.append(deepcopy(for_read["line"]))
        
file.close()
names=[]

for number,player in enumerate(players):
    name_and_surname=["",""]
    matrix=np.zeros(len(player[0]))
    for liter_number in range(len(player[0])):
        try:
            name_and_surname[int(matrix[liter_number])]+=player[0][liter_number]
            if player[0][int(liter_number)+1].isupper():
                matrix+=1
        except:
            break
    players[number]=[deepcopy(name_and_surname),player[1],0,id_to_get,[],0]
    id_to_get+=1
    

power_dictionary={"5":1200,"4":1400,"3":1600,"2":1800,"1":2000,
                  "I":2200,"K":2400,"M":2400,"WCM":2000,"CM":2200,
                  "WFM":2100,"FM":2300,"WIM":2250,"IM":2450,"WGM":2450,"GM":2600,"6":100,"7":0,"arekZajac":2300}

def next_round(players):

    sorted_players = sorted(players, key=lambda x: (x[2], x[5], power_dictionary[x[1]]))

    unmatched_players = sorted_players[:]

    matched_players = []
    
    while len(unmatched_players) > 0:
        player = unmatched_players.pop(0)
        

        closest_player = None
        closest_distance = float("inf")
        for potential_opponent in unmatched_players:
            
            skip=False
            for games_data in player[4]:
                if games_data==potential_opponent[3]:
                    skip=True
                    break
            if skip:
                continue 
            
            distance = abs(potential_opponent[2] - player[2]) + abs((potential_opponent[5] - player[5])/10) + abs((power_dictionary[potential_opponent[1]]-power_dictionary[player[1]])/(power_dictionary["GM"]))
           
            if distance < closest_distance:

                closest_player = potential_opponent
                closest_distance = distance

        try:
            unmatched_players.remove(closest_player)
            matched_players.append((player[3], closest_player[3]))
        except:
            if len(unmatched_players)==1:
                matched_players.append(("puza",unmatched_players.pop(0)))
                unmatched_players=[]
    return matched_players


def found_player(target_id):
    global players
    
    for i in range(len(players)):
        if players[i][-3] == target_id:
            return i
        
    return False
            
def read_input():
    with open("input.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        
    print(lines)
    
    file.close()
    return lines

def gifting(match_making,match_resultss):
    match_results=match_resultss[::-1]
    global players
    for number,mach in enumerate(match_making):
        print(number)
        if mach[0]=="puza":
            print("...",mach[1][2],"...")
            players[found_player(mach[1][3])][2]+=1
            continue
        elif mach[0] != players[found_player(mach[0])][3]:
            players[found_player(mach[0])][4].append(mach[0])
            players[found_player(mach[1])][4].append(mach[1])
        elif mach[1] != players[found_player(mach[0])][3]:
            print(players[found_player(mach[0])])
            players[found_player(mach[0])][4].append(mach[1])
            players[found_player(mach[1])][4].append(mach[0])

        print(mach,"a",match_results,number)
        
        
        if match_results[number] =="1":
            print(match_results[number],players[found_player(mach[1])],players[found_player(mach[1])],"0")
            pass
            players[found_player(mach[0])][2]+=1
            
        elif match_results[number] == "0":
            print(match_results[number],players[found_player(mach[1])],players[found_player(mach[1])],"0")
            pass
            players[found_player(mach[1])][2]+=1

        elif match_results[number]=="r":
            players[found_player(mach[0])][2]+=0.5
            players[found_player(mach[1])][2]+=0.5
            

        players[found_player(mach[0])][5]+=power_dictionary[str(players[mach[1]][1])]/power_dictionary["GM"]
        players[found_player(mach[1])][5]+=power_dictionary[str(players[mach[0]][1])]/power_dictionary["GM"]
    
def end_draw():
    global players
    for i in range(5):
        print()
        
    for place,player in enumerate(sorted(players, key=lambda x: (-x[2], -x[5], -power_dictionary[x[1]]))):
        print(f"{player[0][0]} {player[0][1]} ma miejsce {place+1} ma punktow {player[2]}")
def draw(meachs):
    for i in range(5):
        print()
        
    print(meachs)
    
    print("                  Biale            ||                Czarne")
    for numer,meach in enumerate(meachs[::-1]):
        try:
            if players[found_player(meach[0])][2]=="Pa":
                print(f"palze ma: {players[found_player(meach[1])][2]}, {players[found_player(meach[1])][0][0]}")
            elif players[found_player(meach[1])][2]=="Pa":
                print(f"palze ma: {players[found_player(meach[0])][2]}, {players[found_player(meach[0])][0][0]}")
            else:
                print(f"szachownica {numer+1}: punkty Bialego {players[found_player(meach[0])][2]}, {players[found_player(meach[0])][0][0]} {players[found_player(meach[0])][0][1]}  : {players[found_player(meach[1])][0][0]} {players[found_player(meach[1])][0][1]}, punkty Czarnego {players[found_player(meach[1])][2]}")
        
        except:
            print(f"palze ma: {meach[1][0][0]} {meach[1][0][1]}")
round=0

pygame.font.init()
pygame.init()

pygame.display.set_caption("Free Turnamments")

screen = pygame.display.set_mode((500,400))
#players=[[['Piotr', 'Glebioski'], '4', 1, 0, [0], 0.038461538461538464], [['Adrian', 'Zielonka'], '6', 0, 1, [2], 0.038461538461538464], [['Michal', 'Selweskiuk'], '6', 1, 2, [], 0.038461538461538464], [['Wiktor', 'Wakulewicz'], '6', 1, 3, [4], 0.038461538461538464], [['Kacper', 'Rudzki'], '6', 0, 4, [], 0.038461538461538464], [['Krystian', 'Jarzabkowski'], '6', 1, 5, [7], 0.038461538461538464], [['Mikolej', 'Lesik'], '4', 0, 6, [9], 0.5384615384615384], [['Bartosz', 'Naumiuk'], '6', 0, 7, [], 0.038461538461538464], [['Milosz', 'Juskiewicz'], '6', 0, 8, [10], 0.038461538461538464], [['Krzysztof', 'Golebioski'], '4', 1, 9, [], 0.5384615384615384], [['Karol', 'Dajda'], '6', 1, 10, [], 0.038461538461538464], [['Jan', 'Golebioski'], '6', 1, 11, [12], 0.038461538461538464], [['Marcin', 'Tarasiuk'], '6', 0, 12, [], 0.038461538461538464], [['Marciniuk', 'Kacper'], '6', 1, 13, [14], 0.038461538461538464], [['Wiktor', 'Pikula'], '6', 0, 14, [], 0.038461538461538464], [['Zuk', 'Bartosz'], '6', 0, 15, [0], 0.5384615384615384],[['Wojtek', 'Niedzielko'], '6', 0, 16, [], 0.5384615384615384]]
class Botton:
    def __init__(self,event,x_cord,y_cord,width,height,txt="",clolors={"up":(77.9,77.9,77.9),"down":(40,40,40)}) -> object:
        self.rect=pygame.Rect(x_cord,y_cord,width,height)
        
        self.txt=txt
        self.clolors=clolors
        
        self.press="up"
        self.event=["",event,True]
    def tick(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.event[0]=self.event[1]
            self.press="down"
    def draw(self,screen):
        pygame.draw.rect(screen, self.clolors[self.press], self.rect, width=0)
        screen.blit(pygame.font.Font.render(pygame.font.SysFont("papyrus",math.floor(self.rect.height*0.6)),f"{self.txt}",True,(0, 0, 0)),(self.rect.x,self.rect.y))


matched_players=0

game_number=0
run=True
bottons=[]

bottons.append(Botton("wprowadz wyniki",30,80,180,40,txt="wprowadz wyniki"))
bottons.append(Botton("kojazenia",30,30,100,40,txt="kojazenia"))
print(players)
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            for botton in bottons:
                botton.tick()
   
    screen.fill((255,255,255))
    screen.blit(pygame.font.Font.render(pygame.font.SysFont("papyrus",math.floor(30*0.6)),f"jest runda:{game_number}",True,(0, 0, 0)),(30*0.6*1.2*len(f"jest runda:{game_number}"),30))
    
    for botton in bottons:
        botton.draw(screen)
        if botton.event[0]=="kojazenia":
            try :
                if matched_players!=next_round(players):
                    
                    game_number+=1
                    matched_players = next_round(players)
                    
                    if type(matched_players)!= object:
                        draw(matched_players)
                    else:
                        pass
                        next_round(players)
                    for i_botton in bottons:
                        if i_botton.event[0]=="wprowadz wyniki" and i_botton.event[2]==False:
                            i_botton.event[2]=True
                            i_botton.event[0]=""
                            i_botton.press="up"    
            except:
                
                game_number+=1
                matched_players = next_round(players)
                
                if type(matched_players)!= object:
                    draw(matched_players)
                else:
                    pass
                    next_round(players)
                for i_botton in bottons:
                    if i_botton.event[0]=="wprowadz wyniki" and i_botton.event[2]==False:
                        i_botton.event[2]=True
                        i_botton.event[0]=""
                        i_botton.press="up" 
                                           
            if botton.event[2]:
                print("Wprowadz Wyniki")
                botton.event[2]=False
                
            if matched_players==next_round(players) and botton.event[2]:
                print(colorama.Fore.RED +"Wyniki nie zostaly wprowadzone !!! (sprawdz czy zapisales plik z wynikami partji) !!!",colorama.Style.RESET_ALL)
                botton.event[2]=True
                botton.event[0]=""
                botton.press="up"
        if botton.event[0]=="wprowadz wyniki":
            
            if botton.event[2]:
                print("wyniki wprowadzone !!!")
                gifting(matched_players,read_input())
                end_draw()
                print(players)
                botton.event[2]=False
                i_botton.event[0]=""
                i_botton.press="up"
                for i_botton in bottons:
                    if i_botton.event[0]=="kojazenia" and i_botton.event[2]==False:
                        i_botton.event[2]=True
                        i_botton.event[0]=""
                        i_botton.press="up"
    pygame.display.update()    

