import pygame
import neat
import time
import random
import os


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

# Loading all the sprites
bird_sprites = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(
                    os.path.join("imgs", "bird2.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

pipe_sprite = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))

background_sprite = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))

base_sprite = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))


class Bird:
    images = bird_sprites
    max_rotation = 25
    rotation_velocity = 20
    animation_time = 5      # Time for which each bird is displayed.

    def __init__(self, x, y):
        '''Initializing the attributes'''
        self.x = x                   # x-position
        self.y = y                   # y-position
        self.tilt = 0                # the tilt of the bird(rotation)
        self.tick_count = 0          # current tick of the bird
        self.velocity = 0            # velocity of the bird
        self.height = self.y         # The height of the bird
        self.img_count = 0           # The current image id which is being shown for the bird
        self.image = self.images[0]  # The current image of the bird

    def jump(self):

        self.velocity = -10.5
        self.tick_count = 0  # Resetting the tick_count to zero everytime the jump method is called
        self.height = self.y

    def move(self):
        # Tick count works like time
        self.tick_count += 1

        # We call the move() function on every frame, and it updates the position of the bird, giving it a parabolic trajectory
        # The following equation gives the parabolic physics
        displacement = (self.velocity)*(self.tick_count) + \
            1.5*((self.tick_count)**2)

        # The terminal velocoty for the bird
        if displacement >= 16:
            displacement = 16

        # Fine tuning to make it look better
        if displacement < 0:
            displacement -= 2

        self.y += displacement

        # if we are moving upward or if we are above the jump height position
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:               # rotate the bird directly to maxrotation
                self.tilt = self.max_rotation
        # if the bird is falling down then the bird must slowly approach to a 90-degree rotation(nose-dive)
        else:
            if self.tilt > -90:
                self.tilt -= self.rotation_velocity

    def draw(self, win):
        # This variable keeps a track of the no. of times the bird was drawn to the window
        self.img_count += 1

        # Bird animation
        if self.img_count < self.animation_time:
            self.image = self.images[0]
        elif self.img_count < self.animation_time*2:
            self.image = self.images[1]
        elif self.img_count < self.animation_time*3:
            self.image = self.images[2]
        elif self.img_count < self.animation_time*4:
            self.image = self.images[1]
        elif self.img_count == self.animation_time*4 + 1:
            self.image = self.images[0]
            self.img_count = 0

        # Nose dive
        if self.tilt <= -80:
            self.image = self.images[1]
            # setting the image count to 10 so that it looks natural after the nose dive is done
            self.img_count = self.animation_time*2

        # Logic to rotate the image
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe:
    GAP = 200
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0            # Tracking where the top of pipe will be drawn
        self.bottom = 0         # Tracking where the bottom of pipe will be drawn
        self.pipe_top = pygame.transform.flip(pipe_sprite, False, True)
        self.pipe_bottom = pipe_sprite

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.velocity

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    velocity = 5
    width = base_sprite.get_width()
    image = base_sprite

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))


def draw_window(win, bird):
    win.blit(background_sprite, (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(win, bird)

    pygame.quit()
    quit()


main()
