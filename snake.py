#!/usr/bin/env python

# import statements
import pygame
import sys
import time
import random

from pygame.locals import *

# frames per second
FPS = 5

# initializes pygame here
pygame.init()

# frames per second
fpsClock = pygame.time.Clock()

# defines the variables for the screen size
# You will use these variables later to create the pixel size of the game window you will be
# playing your game in later
#this is the width (left to right)
SCREEN_WIDTH = 640

#this is the height (up to down)
SCREEN_HEIGHT = 480

# previously you were using DISPLAYSURF to make the screen and its dimension
# in this game, we will use the variable name, 'screen'
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# pygame.surface is used for various display related and screen related functions that you will be using throughout
# the code
# the DISPLAYSURF.get_size() will automatically retrieve the size of the screen to make sure that the objects we
# will place on the screen are able to be used in the same width and height
surface = pygame.Surface(DISPLAYSURF.get_size())

# this is used solely for pixel formatting. it is not neccessarily visible to us therefore we are not going to spend
# very much time on it
surface = surface.convert()

# this will fill in the background of the display with a specific color
# it is using the rgb formatting here, (255, 255, 255), which is also the color white
surface.fill((255, 255, 255))

# the clock is used to control and keep track of how often the games display/screen refreeshes itself
clock = pygame.time.Clock()

# this will control how many often your computer will read-in a specific key on your keyboard when it is held down
pygame.key.set_repeat(1, 40)

# this defines the gridsize
# the gridsize is used for several calculations with the screen later on
GRIDSIZE = 10

# MAYBE PUT IN AN EXAMPLE OF A GRID HERE FOR THE STUDENTS TO BETTER UNDERSTAND A GRID AND WHAT IT DOES OR LOOKS LIKE

# this is a calculation used to define how the screen is split up
# in this particular case, by dividing the screen into 10 parts we can reference the screen in more reasonable spots
# do you remember the value of SCREENWIDTH? Look above if you do not
# that is a very large number, imagine if that number was what we used to place our snake and snake food, then it would
# all be way too small for us to actually see and play. Therefore by dividing the screen by 10 we are able to make the
# screen much easier to play with
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE

# we are doing the same thing we did with the width here on the height as well
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

# these coordinates are used to tell the snake which direction to go
# we will use them later to change directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# here is some more screen formatting which we will not discuss too much at this time
DISPLAYSURF.blit(surface, (0, 0))

# this is our first function, it should look familiar to the activity which you did in the past with functions
# it is used to draw a box
# a box is the same as the small squares that will be appearing on the screen
# this function has 3 parammeters that will be passed in from the calling of the function later in the code
# surf is used for the surface size in pixels
# color is the color of the box which will be passed in
# pos is used to tell the current position or location that the box is going to be placed
def draw_box(surf, color, pos):

    # this variable will be using the parameter pos to get the x and y coordinates that the rectangle will be made on
    # gridsize simply is telling the rectangle what size it will be in pixels
    # look above if you do not remember how large GRIDSIZE is
    # remember that the function follows the same basic format of pygame.Rect((x, y), (length, width))
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))

    # this line creates a rectangle
    # surf is the parameter that was passed in to the function
    # color was also passed in to the function
    # r is the variable for the rectangle we made earlier
    pygame.draw.rect(surf, color, r)

# this is a class that will make and hold on to the snake object in the game
# it will pass in the existing object
# an object is the same as we saw in javascript
# more specifically, an object has its own properties and information that it keeps track of
class Snake(object):

    # this is a  function
    # this function __init__ will set up the first pieces of information that make the snake act the right way
    def __init__(self):

        # this is used to make the snake turn into its original form
        # by assigning the lose() function to self we are allowing lose() to be called later in the code
        # this line will make more sense once you make the lose function later
        self.lose()

        # the following line gives the snake a color property
        # the rgb code (0, 0, 0) is the color black
        self.color = (0, 0, 0)

    # this function is used to tell you where the start of the snake is
    # it is passing self into itself in order to use it as a reference
    # this function does not tell the snake where to go but it does allow the function to tell you
    # where the snake currently is at
    # we will use this later
    # as you can tell there is a good amount of preparation needed in order to successfully create a full game
    def get_head_position(self):

        # this will simply return the first position of the snake
        # think of each square that is added to the snake as a new position on the snake
        # the first one is the head of the snake, the front of the snake
        return self.positions[0]

    # now we will define that lose() function that was mentioned earlier
    # it will be used to reset itself back to the start
    def lose(self):

        # the initial form of a snake has only 1 dot so the length will be set to 1 when the lose() function is called
        self.length = 1

        # this will reset the position of the snake to be in the middle of the screen
        # think about how it is set up
        # by dividing the width by 2 we will have the middle of the screen's horizontal position
        # by dividing the height by 2 we will have the middle of the screen's vertical position
        # when we are in the middle of both of these then we will be in the center of the screen
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]

        # do you remember the UP, DOWN, LEFT, and RIGHT variables we made earlier?
        # now we are going to use them
        # this random.choice() function will automatically pick a random option from
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # this is a new function that will choose which direction the snake will go in
    def point(self, pt):

        # this if statement asks the question...
        # is the length bigger than 1
        # and is the direction the same as the direction already being headed in?
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:

            # if the answer to the last question is true then have a blank return statement
            # a blank return will allow the code to just keep going without changing anything
            return

        # this is an else statement in case we are not going in the same direction
        # as the one that the user is trying to go into next
        # in that case, allow the user to change directions
        else:
            self.direction = pt

    # this function is used to keep the snake moving forward
    def move(self):

        # this variable will keep track of the current position we are at
        cur = self.positions[0]

        # these 2 variables are used to check the current direction you are going in
        # the x and y coordinates of that direction
        x = self.direction
        y = self.direction

        # this variable is used to calculate the new direction that the snake is going in
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)

        # if the snake is bigger than 1 square and the front of the snake touches any other part of the snake then it
        # will call the lose() function from earlier
        # it will shorten the length of the snake and also reset the position to the middle of the screen
        # go look at the lose() function made earlier and you will see it all there
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()

        # COME BACK LATER
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # this function will make a new box for each position that the snake has been in or is going in
    def draw(self, surf):
        for p in self.positions:
            draw_box(surf, self.color, p)

# this class will define the red dot (the apple)
# it is going to pass in the object in order to be used inside the function
class Apple(object):

    # this __init__ funciton is used to define the start of the apple
    def __init__(self):

        # the apple will have a position property to  be used
        self.position = (0, 0)

        # the apple also has a color property we are using
        # (255, 0, 0) is used to represent the color red
        self.color = (255, 0, 0)

        #this randomize function will be used for getting the apple to go on to a random part of the screen
        self.randomize()

    # this is where the randomize function is being defined
    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    # this function is the one we used for creating a new box
    def draw(self, surf):
        draw_box(surf, self.color, self.position)

# this function is used to check whether the snake has eaten an apple
def check_eat(snake, apple):

    # if the snake's head and apple are in the same place then the snake will get longer
    if snake.get_head_position() == apple.position:

        #this will increase the snake's length
        snake.length += 1

        # puts the apple back at a random place
        apple.randomize()


if __name__ == '__main__':

    # this will create a variable for the snake which will be updated constantly
    snake = Snake()

    # this will create a variable for the apple to be updated constantly
    apple = Apple()

    # this while loop will allow the controls to be constantly checked
    # and update the game screen as all the functions are being called
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.point(UP)
                elif event.key == K_DOWN:
                    snake.point(DOWN)
                elif event.key == K_LEFT:
                    snake.point(LEFT)
                elif event.key == K_RIGHT:
                    snake.point(RIGHT)

        # all the functions are now being called and some familiar lines from earlier activities
        # and projects are also here
        # see how much you can recognize and trace back through the code to find the sources
        surface.fill((255, 255, 255))
        snake.move()
        check_eat(snake, apple)
        snake.draw(surface)
        apple.draw(surface)
        font = pygame.font.Font(None, 36)
        text = font.render(str(snake.length), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = 20
        surface.blit(text, textpos)
        DISPLAYSURF.blit(surface, (0, 0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + snake.length / 3)
