import pygame as pg

pg.init()

# Creating Canvas
canvas = pg.display.set_mode((460, 505))

# Title
pg.display.set_caption("Pacman")
exitStatus = False

# ----CONSTANTS----

# Map stuff
mapLayout = pg.image.load("images/pacman_map.png")
mapPosition = (0, 0)
human_error_length = 5

# Drawing the inital map rects
walls = [pg.Rect(319, 262, 13, 58), pg.Rect(319, 118, 13, 104), pg.Rect(126, 262, 13, 58), pg.Rect(126, 118, 13, 104)]

# Entities
pacman_right_original = pg.image.load("images/pacman_right.png")
pacman_right = pg.transform.scale(pacman_right_original, (28, 28))
pacman_left = pg.transform.flip(pacman_right, True, False)
pacman_up = pg.transform.rotate(pacman_right, -270.00)
pacman_down = pg.transform.rotate(pacman_right, -90.00)

playerStartingPosition = (215, 276)
Player_X_Pos = 215
Player_Y_Pos = 276
CurrentPacman = pacman_left
pacman_length = 31 

x_change = 0
y_change = 0

# Map Fruit
fruit_img = pg.image.load("images/fruit.png")
black_img = pg.image.load("images/black_pixel.png")
fruit_final_img = pg.transform.scale(fruit_img, (10, 10))
black_image_final = pg.transform.scale(black_img, (10, 10))
fruits = [(270, 285), (250, 285)]
fruits_bools = [True, True]

# Clock
clock = pg.time.Clock()

# FUNCTIONS

# draw_initial_walls()
# ----------------------
# draws pygame Rect objects for every wall in the map
# 
# returns: None
def draw_initial_walls(walls):
    for wall in walls:
        pg.draw.rect(canvas, (255, 0, 0), wall)
    return None

# check_entities()
#--------------------
# Checks for collisions between the player and fruit on the map
# Also redraws the fruit
#
# returns None
def check_entities(x_pos, y_pos, fruits, f_bools):
    # Checking if colliding with fruit
    index = 0
    for fruit in fruits:
        if x_pos == fruit[0]:
            f_bools[index] = False 
        index += 1

    # Drawing the fruit
    fruit_index = 0
    for _ in range(len(f_bools)):
        if f_bools[fruit_index] == True:
            # draw the fruit
            canvas.blit(fruit_final_img, fruits[fruit_index])
        fruit_index += 1
    return None

# check_wall_coliisions
# ------------------------
# Cheks colliions with the player against map walls and adjusts the new position
# of the character if the player runs into the wall
# 
# returns: new_x, new_y
def check_wall_collisions(Player_X_Pos, Player_Y_Pos, x_change, y_change, walls):
    # Moving right
    if x_change > 0:
        for wall in walls:
            # Passing above wall
            collidePAbove = wall.collidepoint((Player_X_Pos + pacman_length, Player_Y_Pos + pacman_length - human_error_length))
            # Passing below wall
            collidePBelow = wall.collidepoint((Player_X_Pos + pacman_length, Player_Y_Pos))
            if collidePAbove or collidePBelow:
                x_change = 0
    
    # Moving left
    if x_change < 0:
        for wall in walls:
            collide = wall.collidepoint((Player_X_Pos - 4, Player_Y_Pos))
            if collide:
                x_change = 0

    return (x_change, y_change)

while not exitStatus:

    # Setting backround
    canvas.blit(mapLayout, mapPosition)

    draw_initial_walls(walls)

    # Player Draw
    canvas.blit(CurrentPacman, (Player_X_Pos, Player_Y_Pos))

    # Game Events
    events = pg.event.get()
    for event in events:

        # Exiting game
        if event.type == pg.QUIT:
            exitStatus = True

        # Movement
        keys = pg.key.get_pressed()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                x_change = 1
                y_change = 0
                CurrentPacman = pacman_right
            if event.key == pg.K_LEFT:
                x_change = -1
                y_change = 0
                CurrentPacman = pacman_left
            if event.key == pg.K_UP:
                x_change = 0
                y_change = -1
                CurrentPacman = pacman_up
            if event.key == pg.K_DOWN:
                x_change = 0
                y_change = 1
                CurrentPacman = pacman_down

    # Checking wall collisions
    (new_x_change, new_y_change) = check_wall_collisions(Player_X_Pos, Player_Y_Pos, x_change, y_change, walls)

    # Updating the movement
    Player_X_Pos += new_x_change
    Player_Y_Pos += new_y_change

    # Checking Ghost and Fruit
    check_entities(Player_X_Pos, Player_Y_Pos, fruits, fruits_bools)

    pg.display.update()

    clock.tick(150)





