
import json, copy

SCREEN_SIZE = (700,700)
BLOCK_SIZE = (SCREEN_SIZE[0]/10,SCREEN_SIZE[1]/10)
SCALE_FACTOR = (BLOCK_SIZE[0]/16, BLOCK_SIZE[1]/16)

OLD_BUTTON_SYSTEM = False
OLD_PLAY_SYSTEM = False
OLD_LOAD_SYSTEM = False
CHANGE_FILES = True

GAME_NAME = "Numpad Clash | PRE 1.6.1"

import pygame
ANY_KEY = [pygame.K_KP0,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9]

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(f"{GAME_NAME} (Loading...)")
pygame.display.set_icon(pygame.image.load("assets/textures/icon.png"))
clock = pygame.time.Clock()
running = True

jsons_files = {
    "props_blocks":open("assets/blockproperties.json","r"),
    "props_elements":open("assets/blockproperties.json","r"),
    "props_menus":open("assets/menus.json","r"),
    "story_maps":open("assets/maps.json","r"),
    "bonus_maps":open("assets/bonusmaps.json","r"),
    "save_main":open("saves/save0.json","r+"),
    "save_empty":open("saves/empty.json","r")
}

jsons = {}
for i in range(len(list(jsons_files.keys()))):
    if OLD_LOAD_SYSTEM:
        jsons[list(jsons_files.keys())[i]] = json.loads(list(jsons_files.values())[i].read())
    else:
        jsons[list(jsons_files.keys())[i]] = json.load(list(jsons_files.values())[i])

load = {
    "map":{
        "billboards":[],
        "textures":[],
        "elements":[],
        "spawn":{
            "position":[0,0],
            "keys":{"1":"none","2":"m_s","3":"none","4":"m_w","5":"none","6":"m_e","7":"none","8":"m_n","9":"none"},
            "texture":"idle"
        }
    },
    "premap":{
        "name":"This is a bug!!",
        "type":0,
        # 0 Story Mode
        # 1 Bonus
        # 2 Custom
        "index":0
    },
    "menu":{
        "index":1,
        "menu_index":0,
        "buttons":[]
    },
    "player":{
        "position":[0,0],
        "keys":{"1":"none","2":"m_s","3":"none","4":"m_w","5":"none","6":"m_e","7":"none","8":"m_n","9":"none"},
        "texture":"idle"
    },
    "framecount":0
}

def load_texture(texture:str) -> pygame.Surface:
    return pygame.transform.scale_by(
        pygame.image.load(f"{texture}"),
        SCALE_FACTOR # change
    )

def plr_damage():
    pass

def check_collision(pos:tuple[int]) -> bool:
    returner = False

    if pos[0] < 0:
        returner = True
    elif pos[1] < 0:
        returner = True
    elif pos[0] > len(load["map"]["elements"][0][0]) - 1:
        returner = True
    elif pos[1] > len(load["map"]["elements"][0]) - 1:
        returner = True
    else:

        for z in range(len(load["map"]["elements"])):
            if load["map"]["elements"][z][pos[1]][pos[0]] == 1:
                returner = True

    return returner

def plr_move(pos:tuple[int]):
    global load
    if pos == (0,-1):
        load["player"]["texture"] = "move_n"
    elif pos == (1,0):
        load["player"]["texture"] = "move_e"
    elif pos == (0,1):
        load["player"]["texture"] = "move_s"
    elif pos == (-1,0):
        load["player"]["texture"] = "move_w"

    # move and collide and balls
    # nvm no balls
    if check_collision((load["player"]["position"][0] + pos[0],load["player"]["position"][1] + pos[1])):
        pass
    else:
        load["player"]["position"][0] += pos[0]
        load["player"]["position"][1] += pos[1]

def load_map(map) -> None:
    global load
    print("map loaded")
    load["map"] = map
    load["player"] = copy.deepcopy(map["spawn"])
    load["player"]["texture"] = "idle"

def play_map(map,name:str) -> None:
    global load
    if OLD_PLAY_SYSTEM:
        load_map(map)
        change_menu(0)
    else:
        load_map(map)
        load["premap"]["name"] = name
        change_menu(2)

def make_text(text:str,size:int=30,color:tuple[int,int,int]=(0,0,0)) -> pygame.Surface:
    return pygame.font.Font("assets/font.ttf",int(size/1.5)).render(text,True,color)

def change_menu(index:int) -> None:
    global load
    load["menu"]["index"] = index
    load["menu"]["menu_index"] = 0

def press_menubutton(index:int,menu:int) -> None:
    global load, running
    if menu == 1:
        if index == 0:
            change_menu(4)
        elif index == 1:
            change_menu(8)
        elif index == 2:
            change_menu(3)
        elif index == 3:
            running = False
    elif menu == 3:
        if index == 0:
            change_menu(1)
    elif menu == 4:
        if index == 0:
            change_menu(1)
        elif index == 1:
            change_menu(6)
        elif index == 2:
            change_menu(7)
        elif index == 3:
            change_menu(5)
    elif menu == 5:
        if index == 0:
            change_menu(4)
        else:
            load["premap"]["type"] = 2
            load["premap"]["index"] = index-1
            play_map(jsons["save_main"]["maps"][index-1]["map"],jsons["save_main"]["maps"][index-1]["name"])
    elif menu == 6:
        if index == 0:
            change_menu(4)
        else:
            load["premap"]["type"] = 0
            load["premap"]["index"] = index-1
            play_map(jsons["story_maps"][index-1]["map"],jsons["story_maps"][index-1]["name"])
    elif menu == 7:
        if index == 0:
            change_menu(4)
        else:
            load["premap"]["type"] = 1
            load["premap"]["index"] = index-1
            play_map(jsons["bonus_maps"][index-1]["map"],jsons["bonus_maps"][index-1]["name"])
    elif menu == 8:
        if index == 0:
            change_menu(1)
        elif index == 1:
            print("deleting savefile!!")
            jsons["save_main"] = copy.deepcopy(jsons["save_empty"])

def exit_level() -> None:
    if load["premap"]["type"] == 0:
        change_menu(6)
    elif load["premap"]["type"] == 1:
        change_menu(7)
    elif load["premap"]["type"] == 2:
        change_menu(5)


def check_elements() -> None:
    for z in range(len(load["map"]["elements"])):
        if load["map"]["elements"][z] [load["player"]["position"][1]] [load["player"]["position"][0]] == 2:

            print("goal reached!")
            # repletion system
            if load["premap"]["index"] in jsons["save_main"]["completed"][load["premap"]["type"]]:
                print("repleted level!")
            else:
                print("first completion!")
                jsons["save_main"]["completed"][load["premap"]["type"]].append(load["premap"]["index"])

            exit_level()
            return None
    
    return None

def press_key(key:str) -> None:
    if load["player"]["keys"][key] == "none":
        return None
    elif load["player"]["keys"][key] == "m_n":
        plr_move((0,-1))
    elif load["player"]["keys"][key] == "m_e":
        plr_move((1, 0))
    elif load["player"]["keys"][key] == "m_s":
        plr_move((0, 1))
    elif load["player"]["keys"][key] == "m_w":
        plr_move((-1,0))
            
def render_keys() -> None:
    screen.blits([
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["7"]}.png"),[550,550]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["8"]}.png"),[600,550]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["9"]}.png"),[650,550]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["4"]}.png"),[550,600]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["5"]}.png"),[600,600]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["6"]}.png"),[650,600]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["1"]}.png"),[550,650]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["2"]}.png"),[600,650]],
        [load_texture(f"assets/textures/keys/{load["player"]["keys"]["3"]}.png"),[650,650]],
    ])


while running:

    # window title
    pygame.display.set_caption(f"{GAME_NAME} ({jsons["props_menus"][load["menu"]["index"]]["name"]})")

    # tick clock
    clock.tick(60)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if load["menu"]["index"] == 0: # ingame

                # quit to menu
                if event.key == pygame.K_KP0:
                    exit_level()

                # all other keys
                elif event.key == pygame.K_KP1:
                    press_key("1")
                elif event.key == pygame.K_KP2:
                    press_key("2")
                elif event.key == pygame.K_KP3:
                    press_key("3")
                elif event.key == pygame.K_KP4:
                    press_key("4")
                elif event.key == pygame.K_KP5:
                    press_key("5")
                elif event.key == pygame.K_KP6:
                    press_key("6")
                elif event.key == pygame.K_KP7:
                    press_key("7")
                elif event.key == pygame.K_KP8:
                    press_key("8")
                elif event.key == pygame.K_KP9:
                    press_key("9")
            
            elif load["menu"]["index"] == 2: # pre ingame
                if event.key in ANY_KEY:
                    change_menu(0)
            
            elif jsons["props_menus"][load["menu"]["index"]]["button"]: # menu

                if event.key == pygame.K_KP5: # press
                    press_menubutton(load["menu"]["menu_index"],load["menu"]["index"])
                elif event.key == pygame.K_KP0: # quit main menu
                    if load["menu"]["index"] == 1:
                        press_menubutton(3,1)

                elif event.key == pygame.K_KP2: # down
                    load["menu"]["menu_index"] += 1
                elif event.key == pygame.K_KP8: # up
                    load["menu"]["menu_index"] += -1
    
    # set buttons
    if load["menu"]["index"] == 0:
        load["menu"]["buttons"] = []

    elif load["menu"]["index"] == 1:
        load["menu"]["buttons"] = ["Play","Settings","Level Editor","Quit"]

    elif load["menu"]["index"] == 3:
        load["menu"]["buttons"] = ["Back","New Level"]
        for map in jsons["save_main"]["maps"]:
            load["menu"]["buttons"].append(f'Edit "{map["name"]}"')
    
    elif load["menu"]["index"] == 4:
        load["menu"]["buttons"] = ["Back","Story Mode","Bonus Levels","Custom Levels"]

    elif load["menu"]["index"] == 5:
        load["menu"]["buttons"] = ["Back"]
        for i,map in enumerate(jsons["save_main"]["maps"]):
            if i in jsons["save_main"]["completed"][2]:
                load["menu"]["buttons"].append(f'[X] {map["name"]}')
            else:
                load["menu"]["buttons"].append(f'[ ] {map["name"]}')
    
    elif load["menu"]["index"] == 6:
        load["menu"]["buttons"] = ["Back"]
        for i,map in enumerate(jsons["story_maps"]):
            if i in jsons["save_main"]["completed"][0]:
                load["menu"]["buttons"].append(f'[X] {map["name"]}')
            else:
                load["menu"]["buttons"].append(f'[ ] {map["name"]}')

    elif load["menu"]["index"] == 7:
        load["menu"]["buttons"] = ["Back"]
        for i,map in enumerate(jsons["bonus_maps"]):
            if i in jsons["save_main"]["completed"][1]:
                load["menu"]["buttons"].append(f'[X] {map["name"]}')
            else:
                load["menu"]["buttons"].append(f'[ ] {map["name"]}')
    
    elif load["menu"]["index"] == 8:
        load["menu"]["buttons"] = ["Back","Reset Savefile"]
                

    # screen reset
    screen.fill((0,255,255))

    # menu render
    if jsons["props_menus"][load["menu"]["index"]]["button"]:

        # render bg
        for y in range(int(SCREEN_SIZE[0]/BLOCK_SIZE[0])):
            for x in range(int(SCREEN_SIZE[1]/BLOCK_SIZE[1])):
                screen.blit(
                    pygame.transform.scale(pygame.image.load(jsons["props_blocks"][2]["texture"]),BLOCK_SIZE),
                    [x*BLOCK_SIZE[0],y*BLOCK_SIZE[1]]
                )

        load["menu"]["menu_index"] = load["menu"]["menu_index"] % len(load["menu"]["buttons"])

        if OLD_BUTTON_SYSTEM:
            screen.blit(make_text(f"Button index: {load["menu"]["menu_index"]}"),(0,40))
            screen.blit(make_text(f"Button: {load["menu"]["buttons"][load["menu"]["menu_index"]]}"),(0,60))
            screen.blit(make_text("This is a placeholder btw"),(0,90))
        else:
            # render buttons
            for i in range(len(load["menu"]["buttons"])):
                if i == load["menu"]["menu_index"]:
                    screen.blit(
                        make_text(f"> {load["menu"]["buttons"][i]}",30),
                        (40,40+i*30)
                    )
                else:
                    screen.blit(
                        make_text(f"  {load["menu"]["buttons"][i]}",30),
                        (40,40+i*30)
                    )
        
        # special menu render
        if load["menu"]["index"] == 3:
            screen.blit(make_text("I didnt code the level editor yet lol",color=(255,0,0)),(200,400))
        elif load["menu"]["index"] == 7:
            if load["menu"]["menu_index"] == 0:
                pass
            else:
                screen.blit(make_text(f"{jsons["bonus_maps"][load["menu"]["menu_index"]-1]["context"]}",size=15),(40,400))


    # map render    
    elif load["menu"]["index"] == 0:

        # check elements
        check_elements()

        # render map
        for z in range(len(load["map"]["textures"])):
            for y in range(len(load["map"]["textures"][z])):
                for x in range(len(load["map"]["textures"][z][y])):
                    screen.blit(
                        load_texture(jsons["props_blocks"][load["map"]["textures"][z][y][x]]["texture"]),
                        [
                            (-1 * load["player"]["position"][0] + x)*BLOCK_SIZE[0] + (350-BLOCK_SIZE[0]/2),
                            (-1 * load["player"]["position"][1] + y)*BLOCK_SIZE[1] + (350-BLOCK_SIZE[1]/2)
                        ]
                    )
                    
        # render billboards
        for z in range(len(load["map"]["billboards"])):
            for i in range(len(load["map"]["billboards"][z])):
                screen.blit(
                    load_texture(load["map"]["billboards"][z][i]["texture"]),
                    [
                        (-1 * load["player"]["position"][0] + load["map"]["billboards"][z][i]["position"][0]) * BLOCK_SIZE[0] + (350-BLOCK_SIZE[0]/2) ,
                        (-1 * load["player"]["position"][1] + load["map"]["billboards"][z][i]["position"][1]) * BLOCK_SIZE[1] + (350-BLOCK_SIZE[1]/2)
                    ]
                )

        # render keys
        screen.blit(load_texture("assets/textures/ui/keys_bg.png"),(535,535))
        render_keys()
    

    elif load["menu"]["index"] == 2: # pre ingame
        screen.fill((50,50,50))
        screen.blit(make_text(f"-{load["premap"]["name"]}-",50,(255,255,255)),(50,50))
        screen.blit(make_text(f"Press any key to start",20,(255,255,255)),(50,500))
        
        # render keys
        render_keys()


    # render player
    if load["menu"]["index"] == 0:
        screen.blit(
            load_texture(f"assets/textures/player/{load["player"]["texture"]}.png"),
            (350-BLOCK_SIZE[0]/2, 350-BLOCK_SIZE[1]/2)
        )
    elif load["menu"]["index"] == 2:
        screen.blit(
            load_texture(f"assets/textures/player/idle.png"),
            (350-BLOCK_SIZE[0]/2, 350-BLOCK_SIZE[1]/2)
        )

    # fps and more
    screen.blit(make_text(f"FPS: {round(clock.get_fps()*100)/100}",15,(80,80,80)),(0,0))

    # flip
    pygame.display.flip()

    # framecount
    load["framecount"] += 1

print("closing...")

# change files
for i in range(len(list(jsons_files.keys()))):

    with jsons_files[list(jsons_files.keys())[i]] as thefile:
        # jsons_files[list(jsons_files.keys())[i]] = thefile
        # dont uncomment the comment over this comment its for readibility its not code
        thefile.seek(0)
        if json.load(thefile) != jsons[list(jsons.keys())[i]]:
            print("diffrent file!!!")
            if CHANGE_FILES:
                if thefile.writable:
                    thefile.seek(0)   # idk maybe you can remove one of those seeks
                    thefile.truncate(0)
                    thefile.seek(0)
                    json.dump(jsons[list(jsons.keys())[i]],thefile)
                else:
                    print("FILE NOT WRITEABLE")
        
# close files
for i in range(len(list(jsons_files.keys()))):
    jsons_files[list(jsons_files.keys())[i]].close()

# bye
pygame.quit()
print("bye")