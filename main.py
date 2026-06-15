
import json

SCREEN_SIZE = (700,700)
BLOCK_SIZE = (SCREEN_SIZE[0]/10,SCREEN_SIZE[1]/10)
SCALE_FACTOR = (BLOCK_SIZE[0]/16, BLOCK_SIZE[1]/16)

OLD_BUTTON_SYSTEM = False

GAME_NAME = "Numpad Clash | PRE 1.1.2"
import pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(f"{GAME_NAME} (Loading...)")
pygame.display.set_icon(pygame.image.load("assets/textures/player/t_idle.png"))
clock = pygame.time.Clock()

running = True

jsons_files = {
    "props_blocks":open("assets/blockproperties.json","r"),
    "props_menus":open("assets/menus.json","r"),
    "story_maps":open("assets/maps.json","r"),
    "save_main":open("saves/save0.json","r+")
}

jsons = {}
for i in range(len(list(jsons_files.keys()))):
    jsons[list(jsons_files.keys())[i]] = json.loads(list(jsons_files.values())[i].read())

load = {
    "map":{
        "billboards":[],
        "textures":[],
        "hitboxes":[],
        "spawn":[0,0]
    },
    "menu":{
        "index":1,
        "menu_index":0,
        "buttons":[]
    },
    "player":{
        "position":[0,0]
    },
    "framecount":0
}

textures = {
    "plr_idle":"assets/textures/player/t_idle.png"
}
for i in range(len(list(textures.keys()))):
    textures[list(textures.keys())[i]] = pygame.transform.scale_by(
        pygame.image.load(list(textures.values())[i]),
        SCALE_FACTOR # change
    )

def check_collision(pos:tuple[int]) -> bool:
    if pos[0] < 0:
        return True
    elif pos[1] < 0:
        return True
    elif pos[0] > len(load["map"]["hitboxes"][0]) - 1:
        return True
    elif pos[1] > len(load["map"]["hitboxes"]) - 1:
        return True
    else:
        return load["map"]["hitboxes"][pos[1]][pos[0]]

def plr_move(pos:tuple[int]):
    if check_collision((
        load["player"]["position"][0] + pos[0],
        load["player"]["position"][1] + pos[1]
    )):
        pass
    else:
        load["player"]["position"][0] += pos[0]
        load["player"]["position"][1] += pos[1]

def load_map(map) -> None:
    load["map"] = map
    load["player"] = {
        "position":map["spawn"]
    }

def make_text(text:str,size:int=30,color:tuple[int,int,int]=(0,0,0)) -> pygame.Surface:
    return pygame.font.SysFont("Arial",size).render(text,True,color)

def change_menu(index:int) -> None:
    global load
    load["menu"]["index"] = index
    load["menu"]["menu_index"] = 0

def press_menubutton(index:int,menu:int) -> None:
    global load, running
    if menu == 1:
        if index == 0:
            change_menu(3)
        elif index == 1:
            pass
        elif index == 2:
            change_menu(2)
        elif index == 3:
            running = False
    elif menu == 2:
        if index == 0:
            change_menu(1)
    elif menu == 3:
        if index == 0:
            change_menu(1)
        elif index == 1:
            change_menu(5)
        elif index == 2:
            change_menu(4)
    elif menu == 4:
        if index == 0:
            change_menu(3)
        else:
            load_map(jsons["save_main"]["maps"][index-1]["map"])
            change_menu(0)

    elif menu == 5:
        if index == 0:
            change_menu(3)
        else:
            load_map(jsons["story_maps"][index-1]["map"])
            change_menu(0)

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
            if load["menu"]["index"] == 0:
                if event.key == pygame.K_KP0: # quit to main menu
                    change_menu(1)

                elif event.key == pygame.K_KP6: # right
                    plr_move((1,0))
                elif event.key == pygame.K_KP4: # left
                    plr_move((-1,0))
                elif event.key == pygame.K_KP2: # down
                    plr_move((0,1))
                elif event.key == pygame.K_KP8: # up
                    plr_move((0,-1))
            
            elif jsons["props_menus"][load["menu"]["index"]]["button"]:

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

    elif load["menu"]["index"] == 2:
        load["menu"]["buttons"] = ["Back","New Level"]
        for map in jsons["save_main"]["maps"]:
            load["menu"]["buttons"].append(f'Edit "{map["name"]}"')
    
    elif load["menu"]["index"] == 3:
        load["menu"]["buttons"] = ["Back","Story Mode","Custom Levels"]

    elif load["menu"]["index"] == 4:
        load["menu"]["buttons"] = ["Back"]
        for map in jsons["save_main"]["maps"]:
            load["menu"]["buttons"].append(f'Play "{map["name"]}"')
    
    elif load["menu"]["index"] == 5:
        load["menu"]["buttons"] = ["Back"]
        for map in jsons["story_maps"]:
            load["menu"]["buttons"].append(f'Play "{map["name"]}"')
                

    # screen reset
    screen.fill((0,0,0))

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

            for i in range(len(load["menu"]["buttons"])):
                if i == load["menu"]["menu_index"]:
                    screen.blit(
                        make_text(f"--> {load["menu"]["buttons"][i]}",30),
                        (40,40+i*40)
                    )
                else:
                    screen.blit(
                        make_text(f"      {load["menu"]["buttons"][i]}",30),
                        (40,40+i*40)
                    )
        
        # special menu render
        if load["menu"]["index"] == 2:
            screen.blit(make_text("I didnt code the level editor yet lol",color=(255,0,0)),(200,400))

    

    # map render    
    elif load["menu"]["index"] == 0:
        # render bg

        # render map
        for z in range(len(load["map"]["textures"])):
            for y in range(len(load["map"]["textures"][z])):
                for x in range(len(load["map"]["textures"][z][y])):
                    block_texture = jsons["props_blocks"][load["map"]["textures"][z][y][x]]["texture"]
                    block_texture = pygame.image.load(block_texture)
                    block_texture = pygame.transform.scale(block_texture,BLOCK_SIZE)
                    block_pos = [
                        (-1 * load["player"]["position"][0] + x)*BLOCK_SIZE[0] + (350-BLOCK_SIZE[0]/2),
                        (-1 * load["player"]["position"][1] + y)*BLOCK_SIZE[1] + (350-BLOCK_SIZE[1]/2)
                    ]
                    screen.blit(block_texture,block_pos)
                    
        # render billboards
        for z in range(len(load["map"]["billboards"])):
            for i in range(len(load["map"]["billboards"][z])):

                billboard_texture = load["map"]["billboards"][z][i]["texture"]
                billboard_texture = pygame.image.load(billboard_texture)
                billboard_texture = pygame.transform.scale_by(billboard_texture,SCALE_FACTOR)
                
                billboard_pos = [
                    (-1 * load["player"]["position"][0] + load["map"]["billboards"][z][i]["position"][0]) * BLOCK_SIZE[0] + (350-BLOCK_SIZE[0]/2) ,
                    (-1 * load["player"]["position"][1] + load["map"]["billboards"][z][i]["position"][1]) * BLOCK_SIZE[1] + (350-BLOCK_SIZE[1]/2)
                ]
                screen.blit(billboard_texture,billboard_pos)

        # render player
        screen.blit(
            textures["plr_idle"],
            (350-BLOCK_SIZE[0]/2, 350-BLOCK_SIZE[1]/2)
        )

    # fps and more
    screen.blit(make_text(f"FPS: {round(clock.get_fps()*100)/100}",15,(80,80,80)),(0,0))

    # flip
    pygame.display.flip()

    # framecount
    load["framecount"] += 1




# close files
for i in range(len(list(jsons_files.keys()))):
    jsons_files[list(jsons_files.keys())[i]].close()

pygame.quit()