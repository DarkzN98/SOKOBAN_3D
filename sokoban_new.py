# IMPORT PYGAME AND OPENGL

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT PYGAME MENU
import pygameMenu
from pygameMenu.locals import *

# IMPORT CLASSES
import Classes.Map as Map

def main():

    # INIT PYGAME

    pygame.init()
    display = (800, 600)
    clock = pygame.time.Clock()

    # INIT PYGAME DISPLAY AND OPENGL

    surface = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    # glTranslatef(0.0, 0.0, -5)
    # glRotatef(45, 1, 0, 0)
    glTranslate(1,0,-5)
    glRotatef(45,1,0,0)
    glOrtho(0,800,0,800,0,1000)
    glEnable(GL_DEPTH_TEST)

    # INIT PYGAME MENU
    pygame.font.init()
    font = pygame.font.Font("Fonts/Roboto-Regular.ttf",32)
    main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Main menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )

    # RENDER POSITION
    rotate_x = 0
    rotate_y = 0
    translate_x = 0
    translate_y = 0
    z_position = 0

    # MOUSE INPUTS
    mouse_rotate = False
    mouse_move = False

    # Set Game Mode
    # Mode 0 : Story
    # Mode 1 : Random
    game_mode = 1

    # CREATE CLASSES
    builder = Map.Map_Builder()
    builder.set_mode(game_mode)
    hasil_build = builder.build_map()
    # print(hasil_build)

    # MAIN GAME LOOP
    pygame.key.set_repeat(16,100)

    while True:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_rotate = True
                elif event.button == 3:
                    mouse_move = True
            elif event.type == MOUSEBUTTONUP:
                mouse_rotate = False
                mouse_move = False
            elif event.type == MOUSEMOTION:
                i, j = event.rel
                if mouse_move:
                    translate_x += i
                    translate_y -= j
                elif mouse_rotate:
                    rotate_x += i
                    rotate_y += j
            elif event.type == KEYDOWN:
                # print(event)
                if event.key == 114:
                    hasil_build = builder.build_map()
                    # hasil_build.print_map()
                elif event.key == 119:
                    hasil_build.player_move("up")
                elif event.key == 97:
                    hasil_build.player_move("left")
                elif event.key == 115:
                    hasil_build.player_move("down")
                elif event.key == 100:
                    hasil_build.player_move("right")
                elif event.key == 273:
                    z_position -= 50
                elif event.key == 274:
                    z_position += 50
                elif event.key == 276:
                    translate_x -= 50
                elif event.key == 275:
                    translate_x += 50
                elif event.key == 113:
                    rotate_x -= 50
                elif event.key == 101:
                    rotate_x += 50

                # print("OBJECTIVE COORDINATE : ({0},{1})".format(hasil_build.objectives.x, hasil_build.objectives.y))
                # print("Player Steps : {}".format(hasil_build.player.steps))
                # CHECK GOAL
                if hasil_build.tiles[hasil_build.goals.y][hasil_build.goals.x] == 3:
                    builder.current_level += 1
                    hasil_build = builder.build_map()
                    # hasil_build.print_map()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glPushMatrix()
        draw_map(hasil_build)

        # TRANSLATE OBJECT IF MOUSE MOVED
        glTranslatef(translate_x, translate_y, -z_position)
        glRotatef(rotate_y/20.,1,0,0)
        glRotatef(rotate_x/20.,0,1,0)
        # glPopMatrix()
        
        # RESET ROTATE
        rotate_x = 0
        rotate_y = 0
        translate_x = 0
        translate_y = 0
        z_position = 0

        pygame.display.flip()

def draw_map(map):

    # Set Box Size
    box_size = 200 

    # Find Center Point Of The Map
    center_x = len(map.tiles) / 2 
    center_y = len(map.tiles[0])/ 2 
    # print("Center X: {}\nCenter Y: {}".format(center_x,center_y))

    # Draw Plane
    for i in range(len(map.tiles)):
        for j in range(len(map.tiles[0])):
            draw_cube((j-center_x)*box_size,-box_size,(i-center_y)*-box_size,box_size,4)
            draw_plane((j-center_x)*box_size,-box_size,(i-center_y)*-box_size,box_size,0)

    # Draw Walls, Player, Objectives, and Goals
    # 1 : Walls
    # 2 : Player
    # 3 : Objectives
    # 4 : Goals

    for i in range(len(map.tiles)):
        for j in range(len(map.tiles[0])):
            if map.tiles[i][j] != 0 and map.tiles[i][j] != 4:
                draw_cube((j-center_x)*box_size,0,(i-center_y)*-box_size,box_size,map.tiles[i][j])
                draw_plane((j-center_x)*box_size,0,(i-center_y)*-box_size,box_size,map.tiles[i][j])
            elif map.tiles[i][j] == 4:
                draw_plane((j-center_x)*box_size,0,(i-center_y)*-box_size,box_size,map.tiles[i][j])

# Cube Drawer
def draw_cube( centerPosX, centerPosY, centerPosZ, edgeLength, mode):
    halfSideLength = edgeLength * 0.5
    vertices = (
        # front face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # back face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom left
        
        # left face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # right face
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # top face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # top face
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength  # bottom left
    )
    
    # OLD RENDER (POLYGONS)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    # NEW RENDER (GL_QUADS)
    glBegin(GL_QUADS)
    if mode == 0:
        glColor3f(0,0,1)
    elif mode == 1:
        glColor3f(0,1,0)
    elif mode == 2:
        glColor3f(1,0,0)
    elif mode == 3:
        glColor3f(1,0,1)
    elif mode == 4:
        glColor3f(0.5,0.5,0.5)

    # FOR EVERY VERTICES
    for x in range(24):
        glVertex3f(vertices[x*3],vertices[x*3 + 1],vertices[x * 3 + 2])
    glColor3f(0,0,0)
    glEnd()

def draw_plane( centerPosX, centerPosY, centerPosZ, edgeLength, mode):
    halfSideLength = edgeLength * 0.5
    vertices = (
        # front face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # back face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom left
        
        # left face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # right face
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # top face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength, # bottom left
        
        # top face
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength, # top left
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength, # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength  # bottom left
    )
    
    # OLD RENDER (POLYGONS)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLineWidth(2)
    if mode == 1:
        glColor3f(0,0,0)
    elif mode == 0:
        glColor3f(1,1,1)
    elif mode == 4:
        glLineWidth(5)
        glColor3f(0,1,1)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3,GL_FLOAT,0,vertices)
    glDrawArrays(GL_QUADS,0,24)
    glDisableClientState(GL_VERTEX_ARRAY)
    
# CALL MAIN
main()
