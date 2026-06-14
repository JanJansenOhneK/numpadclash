
import json

SCREEN_SIZE = (700,700)
BLOCK_SIZE = (SCREEN_SIZE[0]/10,SCREEN_SIZE[1]/10)

GAME_NAME = "Numpad Clash | PRE 1.0"

import pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(f"{GAME_NAME} (Loading...)")
pygame.display.set_icon(pygame.image.load("assets/textures/player/t_idle.png"))
clock = pygame.time.Clock()

running = True

jsons_files = {
    "props_blocks":open("assets/blockproperties.json","r"),
    "props_menus":open("assets/menus.json"),
    "save_main":open("saves/save0.json","r+")
}

jsons = {}
for i in range(len(list(jsons_files.keys()))):
    jsons[list(jsons_files.keys())[i]] = json.loads(list(jsons_files.values())[i].read())

load = {
    "map":{
        "textures":[
            [[1],[1],[1],[1],[1],[1]],
            [[1],[3],[3],[3],[3],[1]],
            [[1],[3],[1],[1],[1],[1]],
            [[1],[3],[1],[1],[3],[1]],
            [[1],[3],[3],[3],[1],[1]],
            [[1],[1],[1],[1],[1],[1]]
        ],
        "hitboxes":[
            [False,False,False,False,False,False],
            [False,True,True,True,True,False],
            [False,True,False,False,False,False],
            [False,True,False,False,True,False],
            [False,True,True,True,False,False],
            [False,False,False,False,False,False]
        ]
    },
    "menu":{
        "index":1,
        "menu_index":0
    },
    "player":{
        "position":[0,0]
    }
}

textures = {
    "plr_idle":"assets/textures/player/t_idle.png"
}
for i in range(len(list(textures.keys()))):
    textures[list(textures.keys())[i]] = pygame.transform.scale(
        pygame.image.load(list(textures.values())[i]),
        (BLOCK_SIZE[0],BLOCK_SIZE[1]) # placeholder !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    )

def check_collision(pos:tuple[int]) -> bool:
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

def make_text(text:str,size:int=20,color:tuple[int,int,int]=(255,255,255)) -> pygame.Surface:
    return pygame.font.SysFont("Arial",size).render(text,True,color)

def press_menubutton(index:int) -> None:
    global load, running
    if index == 0:
        load["menu"]["index"] = 0
    elif index == 1:
        pass
    elif index == 2:
        pass
    elif index == 3:
        running = False

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
                    load["menu"]["index"] = 1

                elif event.key == pygame.K_KP6: # right
                    plr_move((1,0))
                elif event.key == pygame.K_KP4: # left
                    plr_move((-1,0))
                elif event.key == pygame.K_KP2: # down
                    plr_move((0,1))
                elif event.key == pygame.K_KP8: # up
                    plr_move((0,-1))
            
            elif load["menu"]["index"] == 1:

                if event.key == pygame.K_KP5: # press
                    press_menubutton(load["menu"]["menu_index"])
                elif event.key == pygame.K_KP0: # quit
                    press_menubutton(3)

                elif event.key == pygame.K_KP2: # down
                    load["menu"]["menu_index"] += 1
                elif event.key == pygame.K_KP8: # up
                    load["menu"]["menu_index"] += -1
                

    # screen reset
    screen.fill((0,0,0))

    if load["menu"]["index"] == 1: # main menu
        load["menu"]["menu_index"] = load["menu"]["menu_index"] % 3

        screen.blit(make_text(f"Button index: {load["menu"]["menu_index"]}"),(0,40))
        screen.blit(make_text("0-Play 1-Settings 2-LevelEditor 3-Quit"),(0,60))
        screen.blit(make_text("This is a placeholder btw"),(0,90))
            
    elif load["menu"]["index"] == 0:

        # render bg
        

        # render map
        for y in range(len(load["map"]["textures"])):
            for x in range(len(load["map"]["textures"][y])):
                for z in range(len(load["map"]["textures"][y][x])):
                    block_texture = jsons["props_blocks"][load["map"]["textures"][y][x][z]]["texture"]
                    block_texture = pygame.image.load(block_texture)
                    block_texture = pygame.transform.scale(block_texture,(BLOCK_SIZE[0],BLOCK_SIZE[1]))
                    block_pos = [
                        (-1 * load["player"]["position"][0] + x)*BLOCK_SIZE[0] + (350-BLOCK_SIZE[0]/2),
                        (-1 * load["player"]["position"][1] + y)*BLOCK_SIZE[1] + (350-BLOCK_SIZE[1]/2)
                    ]
                    screen.blit(block_texture,block_pos)
                    

        # render player
        screen.blit(
            textures["plr_idle"],
            (350-BLOCK_SIZE[0]/2, 350-BLOCK_SIZE[1]/2)
        )

    # fps and more
    screen.blit(make_text(f"FPS: {round(clock.get_fps()*100)/100}",15),(0,0))

    # flip
    pygame.display.flip()




# close files
for i in range(len(list(jsons_files.keys()))):
    jsons_files[list(jsons_files.keys())[i]].close()

pygame.quit()