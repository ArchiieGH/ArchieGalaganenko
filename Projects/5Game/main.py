import pygame
import sys
from scene import Scene, BossScene
from level import Level

def font_draw():  # reduces repetition

    main_screen.fill("Black")
    main_screen.blit(game_name_surf, game_name_rect)

pygame.init()   # initialises pygame

screen_width = 1500
screen_height = 1000

main_screen = pygame.display.set_mode((screen_width, screen_height))  # creates a screen with size 1500, 1000
clock = pygame.time.Clock()  # clock which tracks time

# font variables initialisation
game_bold_font = pygame.font.Font('graphics/dogica.ttf', 50)
game_slim_font = pygame.font.Font('graphics/dogica.ttf', 30)
game_name_surf = game_bold_font.render('5Game', False, "White")
game_name_rect = game_name_surf.get_rect(center=(500, 200))
game_start_surf = game_slim_font.render('Press any key to start', False, 'White')
game_start_rect = game_start_surf.get_rect(center=(500, 500))
game_end_surf = game_slim_font.render('Press any key to end', False, 'White')
game_end_rect = game_start_surf.get_rect(center=(500, 500))
game_over_surf = game_bold_font.render('Game Over', False, 'Red')
game_over_rect = game_over_surf.get_rect(center=(500, 350))
game_won_surf = game_bold_font.render('You Win!', False, 'Red')
game_won_rect = game_won_surf.get_rect(center=(500, 350))

boss_level_graph = [  # pre-defined graph for the final boss level
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
game_state = 1
scene_index = 0

scene_list = []  # contains all 5 levels

for i in range(0, 4):  # creates 4 procedurally generated level beforehand
    level = Level()  # returns graph of the initiated level
    scene = Scene(main_screen, level)
    scene_list.append(scene)
boss_scene = BossScene(main_screen, boss_level_graph)  # creates instance of BossScene object
scene_list.append(boss_scene)

# game loop
while True:

    for event in pygame.event.get():  # handles specific game events
        if game_state in range(2, 4):  # game finished
            if event.type == pygame.KEYDOWN:
                sys.exit()
        if game_state == 1:  # start of the game / main screen
            if event.type == pygame.KEYDOWN:
                game_state = 0
        if event.type == pygame.QUIT:  # exits the window
            sys.exit()

    if game_state == 0:  # main game
        main_screen.fill("Black")
        scene_list[scene_index].update()
        if scene_list[scene_index].player.advance:  # moves on to the next level when player completes it
            scene_list[scene_index].player.advance = False
            scene_index += 1
        if scene_list[scene_index].player.dead:
            game_state = 2
        if scene_list[4].boss.dead:  # all 5 levels completed
            game_state = 3

    if game_state == 1:  # main menu
        font_draw()
        main_screen.blit(game_start_surf, game_start_rect)

    if game_state == 2:  # game over
        font_draw()
        main_screen.blit(game_over_surf, game_over_rect)
        main_screen.blit(game_end_surf, game_end_rect)

    if game_state == 3:  # game won
        font_draw()
        main_screen.blit(game_won_surf, game_won_rect)
        main_screen.blit(game_end_surf, game_end_rect)

    pygame.display.update()  # updates entire surface of the screen
    clock.tick(60)  # makes the game run at max 60 fps
